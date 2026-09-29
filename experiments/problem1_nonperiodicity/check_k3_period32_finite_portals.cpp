#include <bits/stdc++.h>
using namespace std;

struct Ent { uint8_t mask, fin; };
static Ent tab[65536][2];

static void init_tab(){
    for(int key=0; key<65536; ++key){
        int b=key&255, c=(key>>8)&255;
        for(int init=0; init<2; ++init){
            int a=init, mask=0;
            for(int i=0;i<8;i++){
                if(a) mask|=1<<i;
                int bi=(b>>i)&1, ci=(c>>i)&1;
                a=ci^(bi|a);
            }
            tab[key][init]={(uint8_t)mask,(uint8_t)a};
        }
    }
}

static int child(uint32_t b,uint32_t c,uint32_t& out){
    int count=0; uint32_t ans=0;
    for(int init=0; init<2; ++init){
        int a=init; uint32_t low=0;
        for(int ch=0; ch<4; ++ch){
            int bb=(b>>(8*ch))&255, cc=(c>>(8*ch))&255;
            auto e=tab[bb|(cc<<8)][a];
            low|=uint32_t(e.mask)<<(8*ch);
            a=e.fin;
        }
        if(a==init){ count++; ans=low; }
    }
    out=ans;
    return count;
}

static pair<uint32_t,uint32_t> portal(const string& s){
    uint16_t c16=0;
    for(int i=0;i<16;i++) if(s[i]=='1') c16|=1u<<i;

    uint32_t a=0; int cur=0;
    for(int i=0;i<32;i++){
        if(cur) a|=1u<<i;
        cur=((c16>>(i&15))&1)^cur;
    }
    if(cur) throw runtime_error("portal integration failed");
    return {a,0};
}

static inline int symbol(pair<uint32_t,uint32_t> st,int phase){
    phase&=31;
    return ((st.first>>phase)&1)+2*((st.second>>phase)&1);
}

static bool backward_phase(pair<uint32_t,uint32_t> st,int s){
    int gamma=0;
    for(int k=1;k<=32;k++){
        int v=symbol(st,s-k);
        if(v==1||v==3) return gamma==(v==1);
        if(v==2) gamma^=1;
    }
    return false;
}

static bool exit_candidate(pair<uint32_t,uint32_t> st,int s){
    return symbol(st,s)==2
        && symbol(st,s+1)==2
        && symbol(st,s+2)==2
        && symbol(st,s+3)==1
        && backward_phase(st,s);
}

static int failure(const vector<pair<uint32_t,uint32_t>>& st,
                   int d,int phase,int H){
    int n=0, type=1; // 1 one-bit, 0 cyclic

    while(n<=H){
        auto W=st[d+n];
        int d0=symbol(W,phase+n);
        int d1=symbol(W,phase+n+1);
        int d2=symbol(W,phase+n+2);
        int d3=symbol(W,phase+n+3);

        int h=(st[d+n+1].first>>((phase+n)&31))&1;
        int k=(st[d+n+2].first>>((phase+n)&31))&1;

        if(d0!=(type?2:3) || (d1!=1&&d1!=2))
            return n;

        if(type==0){
            type=(d1==2)^((h==0)&&(k==0));
            n+=2;
            continue;
        }

        if(d1==1){
            type=1;
            n+=2;
            continue;
        }

        if(h==1){
            type=0;
            n+=2;
            continue;
        }

        if(!(d2==2&&d3==1))
            return n;

        int h4=(st[d+n+5].first>>((phase+n+4)&31))&1;
        int k4=(st[d+n+6].first>>((phase+n+4)&31))&1;

        if(h4)
            return n+4;

        type=1^k4;
        n+=6;
    }

    return -1;
}

int main(int argc,char** argv){
    init_tab();

    const vector<string> leaves={
      "0000010101000101","0011101111101011","0101101101111011",
      "0001010011100101","0101010110111111","0000100100100101",
      "0000001001011001","0010111001100111","0001010010001111",
      "0000011101010011","0010101110101101","0101111111011111",
      "0000110110000111","0001001111001111","0001111001111111",
      "0010111100111111"
    };

    if(argc>1 && string(argv[1])=="--billion-first"){
        auto cur=portal(leaves[0]);
        const uint64_t CAP=1000000000ULL;

        for(uint64_t d=0; d<=CAP; ++d){
            if(cur.first==0){
                cout<<"zero_depth="<<d<<"\n";
                return 0;
            }

            if(d==CAP) break;

            uint32_t a;
            int n=child(cur.first,cur.second,a);
            if(n!=1){
                cout<<"nonunique_depth="<<(d+1)<<" count="<<n<<"\n";
                return 0;
            }
            cur={a,cur.first};
        }

        cout<<"no_zero_through="<<CAP<<"\n";
        return 0;
    }

    constexpr int D=10000000, H=64;
    uint64_t exits=0, survivors=0;
    int min_depth=INT_MAX, max_failure=-1;
    map<int,uint64_t> hist;

    for(int p=0;p<16;p++){
        vector<pair<uint32_t,uint32_t>> st(D+H+8);
        st[0]=portal(leaves[p]);

        for(int d=0; d<D+H+7; ++d){
            if(st[d].first==0){
                cerr<<"unexpected zero portal="<<p<<" depth="<<d<<"\n";
                return 2;
            }

            uint32_t a;
            int n=child(st[d].first,st[d].second,a);
            if(n!=1){
                cerr<<"unexpected fork portal="<<p
                    <<" depth="<<(d+1)<<" count="<<n<<"\n";
                return 3;
            }
            st[d+1]={a,st[d].first};
        }

        for(int d=0; d<=D; ++d){
            for(int s=0;s<32;s++){
                if(!exit_candidate(st[d],s))
                    continue;

                exits++;
                min_depth=min(min_depth,d);

                int f=failure(st,d,s,H);
                if(f<0)
                    survivors++;
                else{
                    hist[f]++;
                    max_failure=max(max_failure,f);
                }
            }
        }
    }

    cout<<"portal_necklaces=16\n";
    cout<<"connector_depth="<<D
        <<" exit_occurrences="<<exits
        <<" survivors="<<survivors
        <<" min_exit_depth="<<min_depth
        <<" max_failure_offset="<<max_failure<<"\n";

    cout<<"failure_hist";
    for(auto [k,v]:hist) cout<<" "<<k<<":"<<v;
    cout<<"\n";

    if(exits!=10001374ULL ||
       survivors!=0 ||
       min_depth!=7 ||
       max_failure!=42)
        return 1;

    return 0;
}
