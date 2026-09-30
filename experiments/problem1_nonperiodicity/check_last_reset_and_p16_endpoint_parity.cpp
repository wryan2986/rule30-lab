#include <bits/stdc++.h>
using namespace std;

struct Ent{uint8_t mask,fin;};
static Ent tab[65536][2];

static void init_tab(){
    for(int key=0;key<65536;key++){
        int b=key&255,c=key>>8;
        for(int init=0;init<2;init++){
            int a=init,m=0;
            for(int i=0;i<8;i++){
                if(a)m|=1<<i;
                int bi=(b>>i)&1,ci=(c>>i)&1;
                a=ci^(bi|a);
            }
            tab[key][init]={(uint8_t)m,(uint8_t)a};
        }
    }
}

static uint32_t slow_child(uint32_t b,uint32_t c,int n){
    vector<uint32_t> sol;
    for(int init=0;init<2;init++){
        int a=init; uint32_t out=0;
        for(int s=0;s<n;s++){
            if(a) out|=1u<<s;
            a=((c>>s)&1)^(((b>>s)&1)|a);
        }
        if(a==init) sol.push_back(out);
    }
    if(sol.size()!=1) throw runtime_error("nonunique slow child");
    return sol[0];
}

static uint32_t last_reset_child(uint32_t b,uint32_t c,int n){
    if(!b) throw runtime_error("zero low plane");
    int r=31-__builtin_clz(b);
    int a=1^__builtin_parity(c>>r);
    uint32_t out=0;
    int init=a;
    for(int s=0;s<n;s++){
        if(a) out|=1u<<s;
        a=((c>>s)&1)^(((b>>s)&1)|a);
    }
    if(a!=init) throw runtime_error("last-reset seed is not recurrent");
    return out;
}

static uint16_t child16(uint16_t b,uint16_t c){
    int r=31-__builtin_clz((uint32_t)b);
    int a=1^__builtin_parity((uint32_t)c>>r);
    uint16_t low=0; Ent e;
    e=tab[(b&255)|((c&255)<<8)][a];
    low=e.mask; a=e.fin;
    e=tab[((b>>8)&255)|(((c>>8)&255)<<8)][a];
    low|=uint16_t(e.mask)<<8;
    return low;
}

static uint16_t integrate8(uint8_t w){
    int cur=0; uint16_t x=0;
    for(int i=0;i<16;i++){
        if(cur) x|=uint16_t(1u<<i);
        cur^=(w>>(i&7))&1;
    }
    if(cur) throw runtime_error("integration failed");
    return x;
}

static pair<uint16_t,uint64_t> first_return16(uint16_t x){
    uint16_t a=x,b=0;
    for(uint64_t d=0;;d++){
        if(a==0) return {b,d};
        uint16_t z=child16(a,b);
        b=a; a=z;
    }
}

static uint8_t rot8(uint8_t x,int k){
    return uint8_t((x>>k)|(x<<(8-k)));
}

static uint8_t canon_subset(uint8_t mask){
    uint8_t best=mask;
    for(int k=1;k<8;k++) best=min(best,rot8(mask,k));
    return best;
}

static int orbit_feature8(uint8_t w,uint8_t pat){
    int v=0;
    for(int sh=0;sh<8;sh++){
        uint8_t rp=rot8(pat,sh);
        v^=((w&rp)==rp);
    }
    return v;
}

static int orbit_featureN(const string&s,const vector<int>&pat){
    int n=s.size(),v=0;
    for(int i=0;i<n;i++){
        int p=1;
        for(int d:pat) p&=(s[(i+d)%n]-'0');
        v^=p;
    }
    return v;
}

static bool consistent_degree(const array<int,256>&f,int maxdeg){
    vector<uint8_t> pats;
    set<uint8_t> seen;
    for(int mask=1;mask<256;mask++){
        if(__builtin_popcount((unsigned)mask)>maxdeg) continue;
        uint8_t c=canon_subset((uint8_t)mask);
        if(seen.insert(c).second) pats.push_back(c);
    }

    int nv=1+(int)pats.size(); // explicit constant + orbit features
    vector<uint64_t> rows;

    for(int wi=0;wi<256;wi++) if(__builtin_popcount((unsigned)wi)&1){
        uint64_t row=1ULL;
        for(int j=0;j<(int)pats.size();j++)
            if(orbit_feature8((uint8_t)wi,pats[j]))
                row|=1ULL<<(j+1);
        if(f[wi]) row|=1ULL<<nv;
        rows.push_back(row);
    }

    int rank=0;
    for(int col=0;col<nv;col++){
        int pr=-1;
        for(int i=rank;i<(int)rows.size();i++)
            if((rows[i]>>col)&1){pr=i;break;}
        if(pr<0) continue;

        swap(rows[rank],rows[pr]);
        for(int i=0;i<(int)rows.size();i++)
            if(i!=rank && ((rows[i]>>col)&1))
                rows[i]^=rows[rank];
        rank++;
    }

    uint64_t coeffmask=(1ULL<<nv)-1;
    for(auto row:rows)
        if((row&coeffmask)==0 && ((row>>nv)&1))
            return false;
    return true;
}

int main(){
    init_tab();

    uint64_t checked=0;
    for(int n=1;n<=8;n++){
        uint32_t lim=1u<<n;
        for(uint32_t b=1;b<lim;b++)
            for(uint32_t c=0;c<lim;c++){
                if(slow_child(b,c,n)!=last_reset_child(b,c,n))
                    return 2;
                checked++;
            }
    }

    cout<<"last_reset_exhaustive_pairs="<<checked<<"\n";
    if(checked!=86870) return 3;

    array<int,256> f{};
    uint64_t oddret=0,evenret=0,maxdepth=0;

    for(int wi=0;wi<256;wi++){
        if((__builtin_popcount((unsigned)wi)&1)==0) continue;
        uint16_t x=integrate8((uint8_t)wi);
        auto [end,d]=first_return16(x);
        int p=__builtin_popcount((unsigned)end)&1;
        f[wi]=p;
        if(p) oddret++; else evenret++;
        maxdepth=max(maxdepth,d);
    }

    cout<<"p8_odd_inputs=128 odd_returns="<<oddret
        <<" even_returns="<<evenret
        <<" max_return_depth="<<maxdepth<<"\n";

    if(oddret!=56||evenret!=72||maxdepth!=214005) return 4;

    bool d6=consistent_degree(f,6);
    bool d7=consistent_degree(f,7);

    cout<<"cyclic_orbit_formula_degree_le_6="<<(d6?"yes":"no")<<"\n";
    cout<<"cyclic_orbit_formula_degree_le_7="<<(d7?"yes":"no")<<"\n";

    if(d6||!d7) return 5;

    const vector<uint8_t> epats={
        (1u<<0)|(1u<<2),
        (1u<<0)|(1u<<1)|(1u<<2),
        (1u<<0)|(1u<<1)|(1u<<6),
        (1u<<0)|(1u<<1)|(1u<<2)|(1u<<3),
        (1u<<0)|(1u<<1)|(1u<<2)|(1u<<6),
        (1u<<0)|(1u<<1)|(1u<<2)|(1u<<3)|(1u<<6),
        (1u<<0)|(1u<<1)|(1u<<2)|(1u<<3)|(1u<<4)|(1u<<5)|(1u<<6)
    };

    for(int wi=0;wi<256;wi++) if(__builtin_popcount((unsigned)wi)&1){
        int v=0;
        for(auto p:epats) v^=orbit_feature8((uint8_t)wi,p);
        if(v!=f[wi]) return 6;
    }

    cout<<"explicit_degree7_classifier=verified\n";

    vector<vector<int>> pats={
        {0,2},{0,1,2},{0,1,6},{0,1,2,3},
        {0,1,2,6},{0,1,2,3,6},{0,1,2,3,4,5,6}
    };

    vector<pair<int,string>> known={
        {5,"0000100100100101"},
        {13,"0001001111001111"}
    };

    for(auto &[portal,s]:known){
        int v=0;
        for(auto &p:pats) v^=orbit_featureN(s,p);
        cout<<"p16_parent="<<portal
            <<" scaled_degree7_prediction="<<v
            <<" actual_p32_return_parity=1\n";
        if(portal==5 && v!=1) return 7;
        if(portal==13 && v!=0) return 8;
    }

    cout<<"scaled_degree7_formula_fails_on_portal=13\n";
    return 0;
}
