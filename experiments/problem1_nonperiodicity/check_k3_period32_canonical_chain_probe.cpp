#include <bits/stdc++.h>
using namespace std;

static inline int sym(uint64_t x,int i){
    return (x>>(2*(i&31)))&3;
}

uint64_t canonical(uint32_t q){
    uint64_t x=0;
    for(int i=0;i<16;i++){
        int b=(q>>i)&1;
        x |= uint64_t(b) << (2*i);
        x |= uint64_t(1-b) << (2*(i+16));
    }
    return x;
}

vector<uint64_t> period32_children(uint64_t X){
    uint8_t e[32],a[32];
    for(int i=0;i<32;i++) e[i]=sym(X,i);

    vector<uint64_t> out;
    for(int init=0;init<2;init++){
        a[0]=init;
        int cur=init;

        for(int s=0;s<32;s++){
            int b=e[s]&1;
            int c=(e[s]>>1)&1;
            int nxt=c^(b|cur);
            if(s<31) a[s+1]=nxt;
            cur=nxt;
        }

        if(cur==init){
            uint64_t y=0;
            for(int s=0;s<32;s++)
                y |= uint64_t(a[s]+2*(e[s]&1)) << (2*s);
            out.push_back(y);
        }
    }

    sort(out.begin(),out.end());
    out.erase(unique(out.begin(),out.end()),out.end());
    return out;
}

bool exit_phase(uint64_t x){
    if(!(sym(x,0)==2&&sym(x,1)==2&&sym(x,2)==2&&sym(x,3)==1))
        return false;

    int gamma=0;
    for(int k=1;k<=32;k++){
        int s=sym(x,32-k);
        if(s==1||s==3) return gamma==(s==1);
        if(s==2) gamma^=1;
    }

    return false;
}

int source_failure(const vector<uint64_t>& st,int d,int H){
    int n=0,type=1;

    while(n<=H){
        uint64_t W=st[d+n];
        int d0=sym(W,n);
        int d1=sym(W,n+1);
        int d2=sym(W,n+2);
        int d3=sym(W,n+3);

        int h=sym(st[d+n+1],n)&1;
        int k=sym(st[d+n+2],n)&1;

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

        int h4=sym(st[d+n+5],n+4)&1;
        int k4=sym(st[d+n+6],n+4)&1;

        if(h4)
            return n+4;

        type=1^k4;
        n+=6;
    }

    return -1;
}

int main(){
    constexpr int UNIQUE_DEPTH=1000;
    constexpr int EXIT_DEPTH=928;
    constexpr int H=64;

    vector<uint64_t> layer;
    layer.reserve(65536);

    for(uint32_t q=0;q<65536;q++)
        layer.push_back(canonical(q));

    for(int d=1;d<=UNIQUE_DEPTH;d++){
        vector<uint64_t> next;
        next.reserve(65536);

        for(uint64_t x:layer){
            auto ch=period32_children(x);

            if(ch.size()!=1){
                cerr<<"nonunique/doubling at depth "<<d<<"\n";
                return 2;
            }

            next.push_back(ch[0]);
        }

        auto sorted=next;
        sort(sorted.begin(),sorted.end());

        if(unique(sorted.begin(),sorted.end())!=sorted.end()){
            cerr<<"merger at depth "<<d<<"\n";
            return 3;
        }

        layer.swap(next);
    }

    uint64_t exits=0,survivors=0;
    int min_exit_depth=INT_MAX;
    int max_fail=-1;
    map<int,uint64_t> fail_hist;

    for(uint32_t q=0;q<65536;q++){
        vector<uint64_t> st(UNIQUE_DEPTH+1);
        st[0]=canonical(q);

        for(int d=0;d<UNIQUE_DEPTH;d++){
            auto ch=period32_children(st[d]);

            if(ch.size()!=1)
                return 4;

            st[d+1]=ch[0];
        }

        for(int d=0;d<=EXIT_DEPTH;d++){
            if(!exit_phase(st[d]))
                continue;

            exits++;
            min_exit_depth=min(min_exit_depth,d);

            int f=source_failure(st,d,H);

            if(f<0)
                survivors++;
            else {
                fail_hist[f]++;
                max_fail=max(max_fail,f);
            }
        }
    }

    cout<<"canonical_chains=65536\n";
    cout<<"unique_nonmerging_through_depth="<<UNIQUE_DEPTH<<"\n";
    cout<<"exit_scan_depth="<<EXIT_DEPTH
        <<" exit_nodes="<<exits
        <<" survivors="<<survivors
        <<" min_exit_depth="<<min_exit_depth
        <<" max_failure_offset="<<max_fail<<"\n";

    cout<<"failure_hist";
    for(auto [k,v]:fail_hist)
        cout<<" "<<k<<":"<<v;
    cout<<"\n";

    if(exits!=118359ULL ||
       survivors!=0 ||
       min_exit_depth!=7 ||
       max_fail!=34){
        cerr<<"regression mismatch\n";
        return 1;
    }

    return 0;
}
