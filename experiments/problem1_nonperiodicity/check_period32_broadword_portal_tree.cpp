#include <bits/stdc++.h>
using namespace std;

static inline uint32_t broad_child(uint32_t b,uint32_t c){
    unsigned r=31u-__builtin_clz(b);
    unsigned a0=1u^__builtin_parity(c>>r);

    uint32_t D=c^b, M=~b;

    #define STEP(K) do { \
        constexpr uint32_t LO=(uint32_t)((1ULL<<(K))-1ULL); \
        uint32_t od=D, om=M; \
        D=od^(om&(od<<(K))); \
        M=(om&LO)|(om&(om<<(K))&~LO); \
    } while(0)

    STEP(1); STEP(2); STEP(4); STEP(8); STEP(16);
    #undef STEP

    uint32_t Y=D^(M&(a0?0xffffffffu:0u));
    return (Y<<1)|a0;
}

static uint32_t scalar_child(uint32_t b,uint32_t c){
    unsigned r=31u-__builtin_clz(b);
    int a0=1^__builtin_parity(c>>r);
    int a=a0;
    uint32_t out=0;
    for(int s=0;s<32;s++){
        if(a) out|=1u<<s;
        a=((c>>s)&1)^(((b>>s)&1)|a);
    }
    if(a!=a0) throw runtime_error("nonrecurrent scalar seed");
    return out;
}

static uint32_t parse_bits(const string&s){
    uint32_t x=0;
    for(int i=0;i<32;i++) if(s[i]=='1') x|=1u<<i;
    return x;
}

static string bits(uint32_t x){
    string s;
    for(int i=0;i<32;i++) s.push_back('0'+((x>>i)&1));
    return s;
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

static pair<uint32_t,uint32_t> portal(const string&s){
    uint16_t c=0;
    for(int i=0;i<16;i++) if(s[i]=='1') c|=1u<<i;

    uint32_t a=0;
    int cur=0;
    for(int i=0;i<32;i++){
        if(cur) a|=1u<<i;
        cur^=(c>>(i&15))&1;
    }
    if(cur) throw runtime_error("portal integration failed");
    return {a,0};
}

static uint32_t integrate(uint32_t w,int init){
    int cur=init;
    uint32_t x=0;
    for(int i=0;i<32;i++){
        if(cur) x|=1u<<i;
        cur^=(w>>i)&1;
    }
    if(cur!=init) throw runtime_error("target has odd parity");
    return x;
}

struct Hit{
    uint64_t depth;
    uint32_t high;
};

static Hit scan(uint32_t a,uint32_t b,uint64_t cap){
    for(uint64_t d=0;d<=cap;d++){
        if(a==0) return {d,b};
        if(d==cap) break;
        uint32_t z=broad_child(a,b);
        b=a;
        a=z;
    }
    throw runtime_error("certificate cap reached before zero return");
}

struct Cert{
    string name;
    bool from_portal;
    int portal_index;
    string target;
    int integration_choice;
    uint64_t depth;
    string high;
    string canonical;
    int parity;
};

int main(int argc,char**argv){
    mt19937_64 rng(0x30a57aULL);
    for(int i=0;i<1000000;i++){
        uint32_t b=(uint32_t)rng();
        if(!b) b=1;
        uint32_t c=(uint32_t)rng();
        if(broad_child(b,c)!=scalar_child(b,c)){
            cerr<<"broadword mismatch at sample "<<i<<"\n";
            return 2;
        }
    }
    cout<<"broadword_random_period32_pairs=1000000 mismatches=0\n";

    const vector<string> leaves={
      "0000010101000101","0011101111101011","0101101101111011",
      "0001010011100101","0101010110111111","0000100100100101",
      "0000001001011001","0010111001100111","0001010010001111",
      "0000011101010011","0010101110101101","0101111111011111",
      "0000110110000111","0001001111001111","0001111001111111",
      "0010111100111111"
    };

    const vector<Cert> certs={
      {"portal0-root",true,0,"",0,1420791101ULL,
       "10110001110101101101011111010011",
       "00011101011011010111110100111011",0},

      {"portal2-root",true,2,"",0,1555560444ULL,
       "11100010010101100101111000010001",
       "00001000111100010010101100101111",1},

      {"portal6-root",true,6,"",0,1255920142ULL,
       "01101110011001100111101000110101",
       "00011010101101110011001100111101",0},

      {"portal7-root",true,7,"",0,1324488168ULL,
       "01000100010100100010010011101000",
       "00001000100010100100010010011101",1},

      {"p0-c0",false,0,
       "10110001110101101101011111010011",0,687106285ULL,
       "11100010011011011100111010001001",
       "00010011011011100111010001001111",1},

      {"p0-c1",false,0,
       "10110001110101101101011111010011",1,1919529090ULL,
       "11111001000111001010011010101000",
       "00011100101001101010100011111001",0},

      {"p0-c1-c0",false,0,
       "11111001000111001010011010101000",0,1649036947ULL,
       "11010010100011010000111100100010",
       "00001111001000101101001010001101",0},

      {"p6-c1",false,0,
       "01101110011001100111101000110101",1,580240392ULL,
       "11010110100000110011100101010000",
       "00000110011100101010000110101101",0},

      {"p6-c1-c0",false,0,
       "11010110100000110011100101010000",0,991084817ULL,
       "01011001111010100101010111101001",
       "00101010111101001010110011110101",0},

      {"p6-c1-c0-c0",false,0,
       "01011001111010100101010111101001",0,610754117ULL,
       "10000101000111010100101111011110",
       "00001010001110101001011110111101",1},

      {"p6-c1-c0-c1",false,0,
       "01011001111010100101010111101001",1,958678924ULL,
       "00111100100111110101110101111100",
       "00001111001001111101011101011111",0},

      {"p6-c1-c0-c1-c0",false,0,
       "00111100100111110101110101111100",0,575834567ULL,
       "11001101110010000110010001101000",
       "00001100100011010001100110111001",0}
    };

    if(argc<2 || string(argv[1])=="--list"){
        for(auto &c:certs) cout<<c.name<<"\n";
        return 0;
    }

    vector<int> todo;
    string arg=argv[1];
    if(arg=="--all"){
        for(int i=0;i<(int)certs.size();i++) todo.push_back(i);
    }else{
        for(int i=0;i<(int)certs.size();i++)
            if(certs[i].name==arg) todo.push_back(i);
        if(todo.empty()){
            cerr<<"unknown certificate "<<arg<<"\n";
            return 3;
        }
    }

    for(int ix:todo){
        const auto &c=certs[ix];
        uint32_t a,b=0;

        if(c.from_portal){
            auto st=portal(leaves[c.portal_index]);
            a=st.first;
            b=st.second;
        }else{
            uint32_t w=parse_bits(c.target);
            if(__builtin_popcount(w)&1){
                cerr<<"branch target is odd in "<<c.name<<"\n";
                return 4;
            }
            a=integrate(w,c.integration_choice);
        }

        auto h=scan(a,b,c.depth);

        string raw=bits(h.high);
        string can=rotmin(raw);
        int par=__builtin_popcount(h.high)&1;
        int per=min_period(raw);

        cout<<c.name
            <<" depth="<<h.depth
            <<" high="<<raw
            <<" canonical="<<can
            <<" parity="<<par
            <<" period="<<per<<"\n";

        if(h.depth!=c.depth || raw!=c.high || can!=c.canonical ||
           par!=c.parity || per!=32)
            return 5;
    }

    return 0;
}
