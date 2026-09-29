#include <bits/stdc++.h>
using namespace std;
using U=uint8_t;

static const string WORD="22211221323333032110021130122112";

static int min_period(const array<U,32>& w){
    for(int d: {1,2,4,8,16,32}){
        bool ok=true;
        for(int i=0;i<32;i++) if(w[i]!=w[i%d]){ok=false;break;}
        if(ok) return d;
    }
    return 32;
}

static bool backward_phase(const array<U,32>& w){
    int gamma=0;
    for(int k=1;k<=32;k++){
        int x=w[32-k];
        if(x==1||x==3) return gamma==(x==1);
        if(x==2) gamma^=1;
    }
    return false;
}

static vector<array<U,32>> traces(const array<U,32>& b,int M){
    vector<array<U,32>> tr;
    for(int m=1;m<=M;m++){
        vector<array<U,32>> sol;
        for(int init=0;init<2;init++){
            array<U,32> u{}; u[0]=init; int cur=init;
            for(int s=0;s<32;s++){
                int bs=b[s], nxt;
                if(m==1) nxt=((bs>>1)&1)^((bs&1)|cur);
                else if(m==2) nxt=(bs&1)^(tr[0][s]|cur);
                else nxt=tr[m-3][s]^(tr[m-2][s]|cur);
                if(s<31) u[s+1]=nxt;
                cur=nxt;
            }
            if(cur==init) sol.push_back(u);
        }
        if(sol.size()!=1) throw runtime_error("nonunique lift");
        tr.push_back(sol[0]);
    }
    return tr;
}

static array<int,4> driver(const array<U,32>& b,
                           const vector<array<U,32>>& tr,int n){
    if(n==0) return {b[0],b[1],b[2],b[3]};
    array<int,4> d{};
    for(int s=0;s<4;s++)
        d[s]=2*tr[n-2][(s+n)&31]+tr[n-1][(s+n)&31];
    return d;
}

static pair<int,int> shadow_pair(const vector<array<U,32>>& tr,int n){
    return {tr[n][n&31],tr[n+1][n&31]};
}

static int source_failure(const array<U,32>& b,
                          const vector<array<U,32>>& tr){
    int n=0,type=1;
    while(n<=64){
        auto d=driver(b,tr,n);
        auto [h,k]=shadow_pair(tr,n);

        if(d[0]!=(type?2:3) || (d[1]!=1&&d[1]!=2))
            return n;

        if(type==0){
            type=(d[1]==2)^((h==0)&&(k==0));
            n+=2;
            continue;
        }

        if(d[1]==1){ type=1; n+=2; continue; }
        if(h==1){ type=0; n+=2; continue; }

        if(!(d[2]==2&&d[3]==1))
            return n;

        auto [h4,k4]=shadow_pair(tr,n+4);
        if(h4) return n+4;

        type=1^k4;
        n+=6;
    }
    return -1;
}

static inline uint32_t ror1(uint32_t x){
    return (x>>1)|(x<<31);
}

int main(){
    array<U,32> w{};
    uint32_t a=0,b=0;
    for(int i=0;i<32;i++){
        w[i]=WORD[i]-'0';
        if(w[i]&1) a|=1u<<i;
        if(w[i]&2) b|=1u<<i;
    }

    if(min_period(w)!=32) return 1;
    if(!(w[0]==2&&w[1]==2&&w[2]==2&&w[3]==1)) return 2;
    if(!backward_phase(w)) return 3;

    auto tr=traces(w,80);
    int fail=source_failure(w,tr);
    cout<<"source_failure_offset="<<fail<<"\n";
    if(fail!=44) return 4;

    const uint64_t CAP=1000000000ULL;
    for(uint64_t d=0;d<=CAP;d++){
        if((a|b)==0){
            cout<<"projection_zero_depth="<<d<<"\n";
            return 5;
        }

        bool p16=(((a^(a>>16))&0xffffu)==0)
              && (((b^(b>>16))&0xffffu)==0);
        if(p16){
            cout<<"projection_period_drop_depth="<<d<<"\n";
            return 6;
        }

        if(d==CAP) break;

        uint32_t c=ror1(a)^(b|a);
        a=b; b=c;
    }

    cout<<"no_period_drop_through="<<CAP<<"\n";
    return 0;
}
