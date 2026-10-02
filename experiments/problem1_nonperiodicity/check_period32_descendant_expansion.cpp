#include <bits/stdc++.h>
using namespace std;
static inline uint32_t broad_child(uint32_t b,uint32_t c){
    unsigned r=31u-__builtin_clz(b);
    unsigned a0=1u^__builtin_parity(c>>r);
    uint32_t D=c^b,M=~b;
#define STEP(K) do{constexpr uint32_t LO=(uint32_t)((1ULL<<(K))-1ULL);uint32_t od=D,om=M;D=od^(om&(od<<(K)));M=(om&LO)|(om&(om<<(K))&~LO);}while(0)
    STEP(1);STEP(2);STEP(4);STEP(8);STEP(16);
#undef STEP
    uint32_t Y=D^(M&(a0?0xffffffffu:0u));
    return (Y<<1)|a0;
}
static uint32_t parse_bits(const string&s){uint32_t x=0;for(int i=0;i<32;i++)if(s[i]=='1')x|=1u<<i;return x;}
static string bits(uint32_t x){string s;for(int i=0;i<32;i++)s.push_back('0'+((x>>i)&1u));return s;}
static string rotmin(string s){string z=s;for(int k=1;k<32;k++){string t=s.substr(k)+s.substr(0,k);z=min(z,t);}return z;}
static int min_period(const string&s){for(int d:{1,2,4,8,16,32}){bool ok=true;for(int i=0;i<32;i++)if(s[i]!=s[i%d]){ok=false;break;}if(ok)return d;}return 32;}
static uint32_t integrate(uint32_t w,int init){int cur=init;uint32_t x=0;for(int i=0;i<32;i++){if(cur)x|=1u<<i;cur^=(w>>i)&1u;}if(cur!=init)throw runtime_error("odd source");return x;}
struct Cert{const char*name;const char*source;int choice;uint64_t depth;const char*target;};
static const vector<Cert> certs={
    {"p1-c0","00101001100111010000001001000011",0,2385564355ULL,"01111000011111001100111011010110"},
    {"p4-c0","01111010100000101011100000010011",0,404356749ULL,"00001000110010101000100111000010"},
    {"p4-c1","01111010100000101011100000010011",1,203191865ULL,"10111001010001101101111000001010"},
    {"p4-c1-c1","10111001010001101101111000001010",1,207230746ULL,"00101110100100110010110101000000"},
    {"p8-c0","10101101000100001100101010001000",0,3311656131ULL,"10101010010111111000110010000010"},
    {"p8-c1","10101101000100001100101010001000",1,2912141700ULL,"11011100100001000100000110100100"},
    {"p8-c1-c0","11011100100001000100000110100100",0,1984702874ULL,"01011000100011011000110001101010"},
    {"p8-c1-c1","11011100100001000100000110100100",1,3320394584ULL,"11011110001000011000101101010000"},
    {"p8-c1-c0-c0","01011000100011011000110001101010",0,2119222437ULL,"01110010001110111001110110110111"},
    {"p8-c1-c0-c1","01011000100011011000110001101010",1,1888558713ULL,"10101110101010100011101110101100"},
    {"p8-c1-c1-c0","11011110001000011000101101010000",0,386045218ULL,"11011001001101111011100000110100"},
    {"p8-c1-c1-c1","11011110001000011000101101010000",1,100726797ULL,"00100010110011000110001000010110"},
    {"p10-c0","11110110001101110000100001000010",0,2214214662ULL,"01100000100010010011011000111110"},
    {"p10-c1","11110110001101110000100001000010",1,1558425976ULL,"01011101111101100011101100001110"},
    {"p10-c0-c0","01100000100010010011011000111110",0,39916667ULL,"00110101001010110111111101100110"},
    {"p10-c0-c1","01100000100010010011011000111110",1,318427669ULL,"00110101100000111011100000001011"},
    {"p10-c0-c1-c0","00110101100000111011100000001011",0,3940764551ULL,"11000101000111100001011111000010"},
    {"p10-c0-c1-c1","00110101100000111011100000001011",1,229417894ULL,"10010100101101011011111010001111"},
    {"p11-c0","01001000110110001101110010100100",0,3122858413ULL,"00001000000011011001100001010110"},
    {"p11-c1","01001000110110001101110010100100",1,1990824624ULL,"10111111110111001110011100010100"},
    {"p11-c1-c0","10111111110111001110011100010100",0,1022338055ULL,"10100000111011001111101000001001"},
    {"p11-c1-c1","10111111110111001110011100010100",1,1337460335ULL,"00010010101110001011000100000000"},
    {"p11-c1-c1-c0","00010010101110001011000100000000",0,539640101ULL,"10100111011011000110100010111000"},
    {"p11-c1-c1-c0-c1","10100111011011000110100010111000",1,255992085ULL,"11011110000110011101110100001101"},
    {"p12-c0","10100101000111011000011100010001",0,91485337ULL,"00001010111110111001101001101010"}
};
static bool verify(const Cert&c){
    uint32_t w=parse_bits(c.source);
    if(__builtin_popcount(w)&1) throw runtime_error("source not even");
    uint32_t a=integrate(w,c.choice),b=0;
    for(uint64_t d=0;d<=c.depth;d++){
        if(a==0){
            string raw=bits(b);
            cout<<c.name<<" depth="<<d<<" parity="<<(__builtin_popcount(b)&1)
                <<" weight="<<__builtin_popcount(b)<<" period="<<min_period(raw)
                <<" raw="<<raw<<" canonical="<<rotmin(raw)<<"\n";
            return d==c.depth && raw==c.target && min_period(raw)==32;
        }
        if(d==c.depth)break;
        uint32_t z=broad_child(a,b);b=a;a=z;
    }
    return false;
}
int main(int argc,char**argv){
    if(argc<2||string(argv[1])=="--list"){for(auto&c:certs)cout<<c.name<<"\n";return 0;}
    string a=argv[1];
    if(a=="--all"){
        atomic<int>fail{0},next{0};mutex mu;vector<thread>ts;
        unsigned nt=min<unsigned>(certs.size(),max(1u,thread::hardware_concurrency()));
        for(unsigned k=0;k<nt;k++)ts.emplace_back([&]{for(;;){int i=next.fetch_add(1);if(i>=(int)certs.size())break;bool ok=verify(certs[i]);if(!ok)fail++;}});
        for(auto&t:ts)t.join();return fail?2:0;
    }
    for(auto&c:certs)if(a==c.name)return verify(c)?0:3;
    return 4;
}
