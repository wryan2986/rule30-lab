#include <bits/stdc++.h>
using namespace std;
struct Ent{uint8_t mask,fin;}; static Ent tab[65536][2];

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

static int child(uint32_t b,uint32_t c,uint32_t&out){
    int cnt=0; uint32_t ans=0;
    for(int init=0;init<2;init++){
        int a=init; uint32_t low=0;
        for(int ch=0;ch<4;ch++){
            auto e=tab[((b>>(8*ch))&255)|(((c>>(8*ch))&255)<<8)][a];
            low|=uint32_t(e.mask)<<(8*ch);
            a=e.fin;
        }
        if(a==init){cnt++;ans=low;}
    }
    out=ans; return cnt;
}

static pair<uint32_t,uint32_t> portal(const string&s){
    uint16_t c=0;
    for(int i=0;i<16;i++) if(s[i]=='1') c|=1u<<i;
    uint32_t a=0; int cur=0;
    for(int i=0;i<32;i++){
        if(cur) a|=1u<<i;
        cur=((c>>(i&15))&1)^cur;
    }
    if(cur) throw runtime_error("portal integration failed");
    return {a,0};
}

static inline uint32_t ror(uint32_t x,int k){return (x>>k)|(x<<(32-k));}
static inline int symbol(pair<uint32_t,uint32_t> st,int p){
    p&=31;
    return ((st.first>>p)&1)+2*((st.second>>p)&1);
}

static bool backphase(pair<uint32_t,uint32_t> st,int s){
    int g=0;
    for(int k=1;k<=32;k++){
        int v=symbol(st,s-k);
        if(v==1||v==3) return g==(v==1);
        if(v==2) g^=1;
    }
    return false;
}

static uint32_t candidates(pair<uint32_t,uint32_t> st){
    uint32_t a=st.first,b=st.second;
    uint32_t m2=(~a)&b,m1=a&(~b);
    return m2&ror(m2,1)&ror(m2,2)&ror(m1,3);
}

static string word(pair<uint32_t,uint32_t> st,int phase){
    string z;
    for(int i=0;i<32;i++) z.push_back('0'+symbol(st,phase+i));
    return z;
}
static string bits(uint32_t x){
    string z;
    for(int i=0;i<32;i++) z.push_back('0'+((x>>i)&1));
    return z;
}
static string rotmin(string s){
    string best=s;
    for(int k=1;k<32;k++){
        string t=s.substr(k)+s.substr(0,k);
        best=min(best,t);
    }
    return best;
}
static int minper(const string&s){
    for(int d:{1,2,4,8,16,32}){
        bool ok=true;
        for(int i=0;i<32;i++) if(s[i]!=s[i%d]){ok=false;break;}
        if(ok) return d;
    }
    return 32;
}

struct Cand{uint64_t d;int s;};

static int failure(const array<pair<uint32_t,uint32_t>,96>&ring,
                   uint64_t d,int phase,int H){
    auto get=[&](uint64_t q){return ring[q%96];};
    int n=0,type=1;
    while(n<=H){
        auto W=get(d+n);
        int d0=symbol(W,phase+n),d1=symbol(W,phase+n+1);
        int d2=symbol(W,phase+n+2),d3=symbol(W,phase+n+3);
        auto S1=get(d+n+1),S2=get(d+n+2);
        int h=(S1.first>>((phase+n)&31))&1;
        int k=(S2.first>>((phase+n)&31))&1;

        if(d0!=(type?2:3)||(d1!=1&&d1!=2)) return n;
        if(type==0){
            type=(d1==2)^((h==0)&&(k==0));
            n+=2; continue;
        }
        if(d1==1){type=1;n+=2;continue;}
        if(h==1){type=0;n+=2;continue;}
        if(!(d2==2&&d3==1)) return n;

        auto S5=get(d+n+5),S6=get(d+n+6);
        int h4=(S5.first>>((phase+n+4)&31))&1;
        int k4=(S6.first>>((phase+n+4)&31))&1;
        if(h4) return n+4;
        type=1^k4;
        n+=6;
    }
    return -1;
}

int main(){
    init_tab();

    const vector<string> leaves={
      "0000010101000101","0011101111101011","0101101101111011",
      "0001010011100101","0101010110111111","0000100100100101",
      "0000001001011001","0010111001100111","0001010010001111",
      "0000011101010011","0010101110101101","0101111111011111",
      "0000110110000111","0001001111001111","0001111001111111",
      "0010111100111111"
    };

    struct Target{int p;uint64_t d;int phase;int fail;string expected;};
    const vector<Target> ts={
      {0,20274660,7,44,"22212110133330210332200210123202"},
      {1,24780812,13,50,"22211331222013202222130300102223"},
      {3,54261234,5,52,"22211211321100012231222211000103"},
      {5,24689363,18,52,"22211221332003333211223311223203"}
    };

    for(auto T:ts){
        array<pair<uint32_t,uint32_t>,96> ring{};
        auto cur=portal(leaves[T.p]);
        deque<Cand> q;
        bool found=false;

        for(uint64_t d=0;d<=T.d+80;d++){
            ring[d%96]=cur;

            if(d<=T.d){
                uint32_t cm=candidates(cur);
                while(cm){
                    int s=__builtin_ctz(cm);
                    cm&=cm-1;
                    if(backphase(cur,s)) q.push_back({d,s});
                }
            }

            while(!q.empty()&&d>=q.front().d+72){
                auto c=q.front(); q.pop_front();
                if(c.d==T.d&&c.s==T.phase){
                    int f=failure(ring,c.d,c.s,64);
                    string w=word(ring[c.d%96],c.s);
                    if(f!=T.fail||w!=T.expected) return 2;
                    cout<<"source portal="<<T.p
                        <<" depth="<<T.d
                        <<" phase="<<T.phase
                        <<" failure="<<f
                        <<" word="<<w<<"\n";
                    found=true;
                }
            }

            if(d==T.d+80) break;

            uint32_t a;
            int n=child(cur.first,cur.second,a);
            if(n!=1) return 3;
            cur={a,cur.first};
        }
        if(!found) return 4;
    }

    int p=13;
    auto cur=portal(leaves[p]);
    uint64_t d=0;
    for(;;d++){
        if(cur.first==0){
            string c=bits(cur.second),canon=rotmin(c);
            uint32_t dummy;
            int cnt=child(cur.first,cur.second,dummy);

            cout<<"zero portal=13 depth="<<d
                <<" target="<<c
                <<" canonical="<<canon
                <<" parity="<<(__builtin_popcount(cur.second)&1)
                <<" weight="<<__builtin_popcount(cur.second)
                <<" period="<<minper(c)
                <<" p32_children="<<cnt<<"\n";

            if(d!=65154360ULL) return 5;
            if(canon!="00000001001101101001100111100001") return 6;
            if((__builtin_popcount(cur.second)&1)!=1) return 7;
            if(minper(c)!=32) return 8;
            if(cnt!=0) return 9;
            break;
        }

        uint32_t a;
        int n=child(cur.first,cur.second,a);
        if(n!=1) return 10;
        cur={a,cur.first};
    }

    return 0;
}
