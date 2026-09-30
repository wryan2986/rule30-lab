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
    out=ans;
    return cnt;
}

static pair<uint32_t,uint32_t> portal(const string&s){
    uint16_t c=0;
    for(int i=0;i<16;i++) if(s[i]=='1') c|=1u<<i;

    uint32_t a=0;
    int cur=0;
    for(int i=0;i<32;i++){
        if(cur) a|=1u<<i;
        cur=((c>>(i&15))&1)^cur;
    }

    if(cur) throw runtime_error("portal integration failed");
    return {a,0};
}

static string bits(uint32_t x){
    string z;
    for(int i=0;i<32;i++) z.push_back('0'+((x>>i)&1));
    return z;
}

static string rotmin(string s){
    string b=s;
    for(int k=1;k<32;k++){
        string t=s.substr(k)+s.substr(0,k);
        b=min(b,t);
    }
    return b;
}

static int min_period(const string&s){
    for(int d:{1,2,4,8,16,32}){
        bool ok=true;
        for(int i=0;i<32;i++) if(s[i]!=s[i%d]){ok=false;break;}
        if(ok) return d;
    }
    return 32;
}

int main(int argc,char**argv){
    if(argc!=3){
        cerr<<"usage: "<<argv[0]<<" PORTAL_INDEX CAP\n";
        return 2;
    }

    init_tab();

    int p=atoi(argv[1]);
    uint64_t cap=strtoull(argv[2],nullptr,10);

    const vector<string> leaves={
      "0000010101000101","0011101111101011","0101101101111011",
      "0001010011100101","0101010110111111","0000100100100101",
      "0000001001011001","0010111001100111","0001010010001111",
      "0000011101010011","0010101110101101","0101111111011111",
      "0000110110000111","0001001111001111","0001111001111111",
      "0010111100111111"
    };

    if(p<0||p>=16) return 3;

    auto cur=portal(leaves[p]);

    for(uint64_t d=0;d<=cap;d++){
        if(cur.first==0){
            string s=bits(cur.second);
            string canon=rotmin(s);
            int parity=__builtin_popcount(cur.second)&1;
            int weight=__builtin_popcount(cur.second);
            int period=min_period(s);

            uint32_t dummy;
            int cnt=child(cur.first,cur.second,dummy);

            cout<<"portal="<<p
                <<" zero_depth="<<d
                <<" high="<<s
                <<" canonical="<<canon
                <<" parity="<<parity
                <<" weight="<<weight
                <<" period="<<period
                <<" period32_children="<<cnt
                <<"\n";

            if(p==5){
                if(d!=105696243ULL) return 4;
                if(canon!="00000000001001100000010001101101") return 5;
                if(parity!=1||weight!=9||period!=32||cnt!=0) return 6;
            }
            if(p==13){
                if(d!=65154360ULL) return 7;
                if(canon!="00000001001101101001100111100001") return 8;
                if(parity!=1||weight!=13||period!=32||cnt!=0) return 9;
            }

            return 0;
        }

        if(d==cap) break;

        uint32_t a;
        int n=child(cur.first,cur.second,a);
        if(n!=1){
            cout<<"portal="<<p
                <<" event_depth="<<(d+1)
                <<" count="<<n
                <<"\n";
            return 10;
        }

        cur={a,cur.first};
    }

    cout<<"portal="<<p<<" no_zero_through="<<cap<<"\n";
    return 0;
}
