#include <bits/stdc++.h>
using namespace std;
using U8 = uint8_t;
static inline int lo(int x){ return x & 1; }
static inline int hi(int x){ return (x >> 1) & 1; }

bool backward_exit_phase(const array<U8,16>& w){
    int gamma=0;
    for(int k=1;k<=16;k++){
        int s=w[16-k];
        if(s==1 || s==3) return gamma==(s==1);
        if(s==2) gamma^=1;
    }
    return false;
}

vector<vector<U8>> recurrent_solutions(
    const array<U8,16>& base, int P, int m,
    const vector<vector<U8>>& tr)
{
    vector<vector<U8>> out;
    for(int init=0;init<2;init++){
        vector<U8> u(P); u[0]=init; int cur=init;
        for(int s=0;s<P;s++){
            int bs=base[s&15], nxt;
            if(m==1) nxt=hi(bs)^(lo(bs)|cur);
            else if(m==2) nxt=lo(bs)^(tr[0][s]|cur);
            else nxt=tr[m-3][s]^(tr[m-2][s]|cur);
            if(s<P-1) u[s+1]=nxt;
            cur=nxt;
        }
        if(cur==init) out.push_back(move(u));
    }
    return out;
}

vector<U8> doubled_solution(
    const array<U8,16>& base, int P, int m,
    const vector<vector<U8>>& tr, int init)
{
    int Q=2*P;
    vector<U8> u(Q); u[0]=init; int cur=init;
    for(int s=0;s<Q;s++){
        int bs=base[s&15], nxt;
        if(m==1) nxt=hi(bs)^(lo(bs)|cur);
        else if(m==2) nxt=lo(bs)^(tr[0][s%P]|cur);
        else nxt=tr[m-3][s%P]^(tr[m-2][s%P]|cur);
        if(s<Q-1) u[s+1]=nxt;
        cur=nxt;
    }
    if(cur!=init) throw runtime_error("2P lift failed to close");
    return u;
}

struct Branch { int P=16; vector<vector<U8>> tr; };

array<U8,4> driver_prefix(const Branch& B, int n){
    array<U8,4> d{};
    for(int s=0;s<4;s++)
        d[s]=2*B.tr[n-2][(s+n)%B.P]+B.tr[n-1][(s+n)%B.P];
    return d;
}

pair<int,int> shadow_pair(const Branch& B, int n){
    return {B.tr[n][n%B.P],B.tr[n+1][n%B.P]};
}

bool source_prefix_ok(const array<U8,4>& d, int type){
    return d[0]==(type?2:3) && (d[1]==1 || d[1]==2);
}

int simulate_sources(const array<U8,16>& base,const Branch& B,int H){
    int n=0,type=1;
    while(n<=H){
        array<U8,4> d{};
        if(n==0) for(int i=0;i<4;i++) d[i]=base[i];
        else d=driver_prefix(B,n);
        auto pr=shadow_pair(B,n);
        if(!source_prefix_ok(d,type)) return n;

        if(type==0){
            type=(d[1]==2)^((pr.first==0)&&(pr.second==0));
            n+=2;
            continue;
        }

        if(d[1]==1){ type=1; n+=2; continue; }
        if(pr.first==1){ type=0; n+=2; continue; }

        if(!(d[2]==2 && d[3]==1)) return n;
        auto at4=shadow_pair(B,n+4);
        if(at4.first!=0) return n+4;
        type=1^at4.second;
        n+=6;
    }
    return -1;
}

struct FixedResult { int status; int offset; int first_nonunique; };

FixedResult fixed_period_pass(const array<U8,16>& base,int H){
    vector<vector<U8>> tr;

    auto ensure=[&](int M)->int{
        while((int)tr.size()<M){
            auto ss=recurrent_solutions(base,16,(int)tr.size()+1,tr);
            if(ss.size()!=1) return (int)tr.size()+1;
            tr.push_back(ss[0]);
        }
        return 0;
    };

    auto d4=[&](int n){
        array<U8,4> d{};
        for(int s=0;s<4;s++)
            d[s]=2*tr[n-2][(s+n)&15]+tr[n-1][(s+n)&15];
        return d;
    };

    auto pair16=[&](int n){
        return pair<int,int>(tr[n][n&15],tr[n+1][n&15]);
    };

    int n=0,type=1;
    while(n<=H){
        int m=ensure(n+8);
        if(m) return {2,n,m};

        array<U8,4> d{};
        if(n==0) for(int i=0;i<4;i++) d[i]=base[i];
        else d=d4(n);

        auto pr=pair16(n);
        if(!source_prefix_ok(d,type)) return {0,n,0};

        if(type==0){
            type=(d[1]==2)^((pr.first==0)&&(pr.second==0));
            n+=2;
            continue;
        }

        if(d[1]==1){ type=1; n+=2; continue; }
        if(pr.first==1){ type=0; n+=2; continue; }

        if(!(d[2]==2 && d[3]==1)) return {0,n,0};
        auto at4=pair16(n+4);
        if(at4.first) return {0,n+4,0};
        type=1^at4.second;
        n+=6;
    }

    return {1,n,0};
}

int main(){
    constexpr int H=64,M=72;
    array<U8,16> w{};
    w[0]=2;w[1]=2;w[2]=2;w[3]=1;
    const uint32_t total=1u<<24;

    uint64_t phase_count=0,unique_fail=0,unique_survive=0;
    map<int,uint64_t> unique_fail_hist,first_nonunique_hist;
    vector<array<U8,16>> exceptions;

    for(uint32_t code=0;code<total;code++){
        uint32_t x=code;
        for(int i=4;i<16;i++){ w[i]=x&3; x>>=2; }

        bool period8=true;
        for(int i=0;i<8;i++)
            if(w[i]!=w[i+8]){ period8=false; break; }

        if(period8 || !backward_exit_phase(w)) continue;
        phase_count++;

        auto r=fixed_period_pass(w,H);
        if(r.status==0){
            unique_fail++;
            unique_fail_hist[r.offset]++;
        } else if(r.status==1){
            unique_survive++;
        } else {
            exceptions.push_back(w);
            first_nonunique_hist[r.first_nonunique]++;
        }
    }

    uint64_t dead=0,survive=0,total_branches=0,max_branches=0,max_period=16;
    map<int,uint64_t> exceptional_fail_hist;

    for(const auto& base:exceptions){
        vector<Branch> branches(1);

        for(int m=1;m<=M;m++){
            vector<Branch> next;

            for(const auto& B:branches){
                auto ss=recurrent_solutions(base,B.P,m,B.tr);

                if(ss.empty()){
                    int Q=2*B.P;
                    if(Q>4096) throw runtime_error("unexpected period growth");

                    for(int init=0;init<2;init++){
                        Branch C;
                        C.P=Q;
                        C.tr.reserve(m);

                        for(const auto& old:B.tr){
                            vector<U8> e(Q);
                            for(int i=0;i<Q;i++) e[i]=old[i%B.P];
                            C.tr.push_back(move(e));
                        }

                        C.tr.push_back(
                            doubled_solution(base,B.P,m,B.tr,init));
                        next.push_back(move(C));
                    }
                } else {
                    for(auto u:ss){
                        Branch C=B;
                        C.tr.push_back(move(u));
                        next.push_back(move(C));
                    }
                }
            }

            branches.swap(next);
            if(branches.empty()) break;
            if(branches.size()>20000)
                throw runtime_error("unexpected phase explosion");
        }

        max_branches=max<uint64_t>(max_branches,branches.size());
        total_branches+=branches.size();

        bool any=false;
        for(const auto& B:branches){
            max_period=max<uint64_t>(max_period,B.P);
            int f=simulate_sources(base,B,H);
            if(f<0) any=true;
            else exceptional_fail_hist[f]++;
        }

        if(any) survive++;
        else dead++;
    }

    cout<<"phase_compatible_exact_p16="<<phase_count<<"\n";
    cout<<"unique_fail="<<unique_fail
        <<" unique_survive="<<unique_survive
        <<" exceptional_words="<<exceptions.size()<<"\n";
    cout<<"exceptional_dead="<<dead
        <<" exceptional_survive="<<survive
        <<" terminal_branches="<<total_branches
        <<" max_branches_per_word="<<max_branches
        <<" max_period_seen="<<max_period<<"\n";

    cout<<"unique_fail_hist";
    for(auto [k,v]:unique_fail_hist) cout<<" "<<k<<":"<<v;
    cout<<"\nfirst_nonunique_hist";
    for(auto [k,v]:first_nonunique_hist) cout<<" "<<k<<":"<<v;
    cout<<"\nexceptional_fail_hist";
    for(auto [k,v]:exceptional_fail_hist) cout<<" "<<k<<":"<<v;
    cout<<"\n";

    if(phase_count!=8388480ULL ||
       unique_fail!=8386657ULL ||
       unique_survive!=0 ||
       exceptions.size()!=1823 ||
       dead!=1823 ||
       survive!=0 ||
       total_branches!=3647 ||
       max_branches!=3 ||
       max_period!=32){
        cerr<<"regression mismatch\n";
        return 1;
    }

    return 0;
}
