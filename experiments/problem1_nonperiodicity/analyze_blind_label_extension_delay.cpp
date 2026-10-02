#include <bits/stdc++.h>
using namespace std;

static inline int parity64(uint64_t x){ return __builtin_parityll(x); }

static inline uint64_t broad_child(uint64_t b,uint64_t c,int n){
    if(!b) throw runtime_error("nonzero low plane required");
    uint64_t mask=(n==64?~0ULL:((1ULL<<n)-1ULL));
    int r=63-__builtin_clzll(b);
    int a0=1^parity64(c>>r);
    uint64_t D=(c^b)&mask, M=(~b)&mask;
    for(int k=1;k<n;k<<=1){
        uint64_t lo=(1ULL<<k)-1ULL, od=D, om=M;
        D=(od^(om&((od<<k)&mask)))&mask;
        M=((om&lo)|(om&((om<<k)&mask)&(~lo&mask)))&mask;
    }
    uint64_t Y=D^(M&(a0?mask:0ULL));
    return ((Y<<1)|a0)&mask;
}

static uint64_t portal_lift(uint32_t w,int p){
    int cur=0; uint64_t x=0;
    for(int s=0;s<2*p;s++){
        x|=(uint64_t)cur<<s;
        cur^=(w>>(s%p))&1u;
    }
    if(cur) throw runtime_error("portal integration did not close");
    return x;
}

static uint64_t stack_transition(uint64_t state,int r,int driver){
    int H=1,K=0,L=0,M=1;
    uint64_t out=0;
    for(int j=0;j<r;j++){
        int X=(state>>(2*j))&1u;
        int Y=(state>>(2*j+1))&1u;
        int Xn=H^(L|X);
        int Yn=K^M^Y^(L&Y)^(M&X)^(M&Y);
        if(driver) Xn^=Yn;
        out|=(uint64_t)Xn<<(2*j);
        out|=(uint64_t)Yn<<(2*j+1);
        H=L; K=M; L=X; M=Y;
    }
    return out;
}

static bool blind(uint64_t state,int r){
    return stack_transition(state,r,0)==stack_transition(state,r,1);
}

// Context bits are K,L,M = Y_(j-2), X_(j-1), Y_(j-1).
static optional<int> blind_context_step(int ctx,int pair_code){
    int K=(ctx>>2)&1, L=(ctx>>1)&1, M=ctx&1;
    int X=(pair_code>>1)&1, Y=pair_code&1;
    int q=K^M^Y^(L&Y)^(M&X)^(M&Y);
    if(q) return nullopt;
    return (M<<2)|(X<<1)|Y;
}

static void verify_blind_language(){
    // Exact transition table, pair_code 0=00,1=01,2=10,3=11.
    const vector<vector<pair<int,int>>> expected={
        {{0,0},{2,2}},
        {{2,6},{3,7}},
        {{0,0},{1,1},{2,2},{3,3}},
        {{1,5},{2,6}},
        {{1,1},{3,3}},
        {{0,4},{1,5}},
        {},
        {{0,4},{3,7}},
    };
    for(int s=0;s<8;s++){
        vector<pair<int,int>> got;
        for(int a=0;a<4;a++){
            auto z=blind_context_step(s,a);
            if(z) got.push_back({a,*z});
        }
        if(got!=expected[s]) throw runtime_error("blind DFA mismatch");
    }

    // b_r = number of r-layer raw blind prefixes from start context 001.
    array<unsigned long long,8> cur{}, nxt{};
    cur[1]=1;
    vector<unsigned long long> b={1};
    for(int r=1;r<=20;r++){
        nxt.fill(0);
        for(int s=0;s<8;s++) for(int a=0;a<4;a++){
            auto z=blind_context_step(s,a);
            if(z) nxt[*z]+=cur[s];
        }
        cur=nxt;
        unsigned long long total=0;
        for(auto v:cur) total+=v;
        b.push_back(total);
    }
    if(b[1]!=2 || b[2]!=2) throw runtime_error("blind initial counts");
    for(int r=3;r<(int)b.size();r++)
        if(b[r]!=b[r-1]+2*b[r-3]) throw runtime_error("blind recurrence");

    // (11)^r is blind for every tested r; the DFA proves this for all r
    // because 001 --11--> 111 and 111 --11--> 111.
    for(int r=1;r<=30;r++){
        uint64_t s=0;
        for(int j=0;j<r;j++) s|=3ULL<<(2*j);
        if(!blind(s,r)) throw runtime_error("all-11 blind tower failed");
    }
}

struct Sig {
    array<uint32_t,28> a{};
    bool operator<(Sig const& o) const {
        return lexicographical_compare(a.begin(),a.end(),o.a.begin(),o.a.end());
    }
    bool operator==(Sig const& o) const { return a==o.a; }
};

static Sig orbit_signature(uint32_t w,int p,int r){
    int n=2*p;
    uint64_t x=portal_lift(w,p);
    uint64_t J=(1ULL<<n)-1ULL;
    uint64_t low=x, high=J;
    array<uint64_t,10> dyn{};
    for(int j=0;j<r;j++){
        uint64_t ch=broad_child(low,high,n);
        dyn[j]=ch; high=low; low=ch;
    }

    array<uint32_t,28> seq{};
    for(int s=0;s<p;s++){
        int q=(x>>s)&1u;
        uint32_t st=0;
        for(int j=0;j<r;j++){
            int X=(dyn[j]>>s)&1u;
            int Y=X^((dyn[j]>>(s+p))&1u);
            if(q) X^=Y;
            st|=(uint32_t)X<<(2*j);
            st|=(uint32_t)Y<<(2*j+1);
        }
        seq[s]=st;
    }

    int best=0;
    for(int k=1;k<p;k++){
        for(int i=0;i<p;i++){
            uint32_t u=seq[(k+i)%p], v=seq[(best+i)%p];
            if(u<v){ best=k; break; }
            if(u>v) break;
        }
    }
    Sig z;
    for(int i=0;i<p;i++) z.a[i]=seq[(best+i)%p];
    return z;
}

static int necklace_n;
static int necklace_a[29];
static vector<uint32_t> necklace_words;

static void gen_necklaces(int t,int per){
    if(t>necklace_n){
        if(necklace_n%per==0){
            uint32_t w=0; int wt=0;
            for(int i=1;i<=necklace_n;i++) if(necklace_a[i]){
                w|=1u<<(i-1); wt++;
            }
            if(wt&1) necklace_words.push_back(w);
        }
        return;
    }
    necklace_a[t]=necklace_a[t-per];
    gen_necklaces(t+1,per);
    for(int j=necklace_a[t-per]+1;j<=1;j++){
        necklace_a[t]=j;
        gen_necklaces(t+1,t);
    }
}

struct CensusRow {
    int p;
    size_t necklaces;
    int first_injective_r;
    size_t collision_classes_at_previous;
};

static CensusRow census_period(int p,int max_r){
    necklace_n=p;
    necklace_words.clear();
    memset(necklace_a,0,sizeof(necklace_a));
    gen_necklaces(1,1);

    size_t previous_collisions=0;
    for(int r=1;r<=max_r;r++){
        vector<pair<Sig,uint32_t>> v;
        v.reserve(necklace_words.size());
        for(uint32_t w:necklace_words) v.push_back({orbit_signature(w,p,r),w});
        sort(v.begin(),v.end(),[](auto const&A,auto const&B){
            if(A.first==B.first) return A.second<B.second;
            return A.first<B.first;
        });
        size_t distinct=0, collisions=0;
        for(size_t i=0;i<v.size();){
            size_t j=i+1;
            while(j<v.size() && v[j].first==v[i].first) j++;
            distinct++;
            if(j-i>1) collisions++;
            i=j;
        }
        if(distinct==necklace_words.size())
            return {p,necklace_words.size(),r,previous_collisions};
        previous_collisions=collisions;
    }
    throw runtime_error("observer did not become injective within max_r");
}

int main(int argc,char**argv){
    int max_p=22, max_r=10;
    for(int i=1;i<argc;i++){
        string a=argv[i];
        if(a=="--max-period" && i+1<argc) max_p=stoi(argv[++i]);
        else if(a=="--max-r" && i+1<argc) max_r=stoi(argv[++i]);
        else throw runtime_error("usage: --max-period N --max-r R");
    }
    if(max_p>28 || max_p<2 || (max_p&1)) throw runtime_error("max-period must be even and <=28");
    if(max_r>10) throw runtime_error("this checker stores at most 10 dynamic layers");

    verify_blind_language();
    cout<<"blind_prefix_generating_function=(1+x)/(1-x-2*x^3)\n";
    cout<<"blind_recurrence=b_r=b_(r-1)+2*b_(r-3), b0=1,b1=2,b2=2\n";
    cout<<"raw_all_11_blind_tower=verified\n";

    for(int p=2;p<=max_p;p+=2){
        auto row=census_period(p,max_r);
        cout<<"p="<<row.p
            <<" odd_necklaces="<<row.necklaces
            <<" first_injective_r="<<row.first_injective_r
            <<" previous_collision_classes="<<row.collision_classes_at_previous
            <<"\n";
    }
}
