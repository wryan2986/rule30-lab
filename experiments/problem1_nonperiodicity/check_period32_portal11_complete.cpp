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
static uint32_t integrate(uint32_t w,int init){int cur=init;uint32_t x=0;for(int i=0;i<32;i++){if(cur)x|=1u<<i;cur^=(w>>i)&1u;}if(cur!=init)throw runtime_error("odd source");return x;}
static string bits(uint32_t x){string s;for(int i=0;i<32;i++)s.push_back('0'+((x>>i)&1u));return s;}
static string rotmin(string s){string z=s;for(int k=1;k<32;k++){string t=s.substr(k)+s.substr(0,k);z=min(z,t);}return z;}
static int min_period(const string&s){for(int d:{1,2,4,8,16,32}){bool ok=true;for(int i=0;i<32;i++)if(s[i]!=s[i%d]){ok=false;break;}if(ok)return d;}return 32;}

struct Cert{const char*path;const char*source;int choice;uint64_t depth;const char*target;int parity;int weight;};
static const vector<Cert> certs={
    {"0","01001000110110001101110010100100",0,3122858413ULL,"00001000000011011001100001010110",1,11},
    {"1","01001000110110001101110010100100",1,1990824624ULL,"10111111110111001110011100010100",0,20},
    {"10","10111111110111001110011100010100",0,1022338055ULL,"10100000111011001111101000001001",1,15},
    {"11","10111111110111001110011100010100",1,1337460335ULL,"00010010101110001011000100000000",0,10},
    {"110","00010010101110001011000100000000",0,539640101ULL,"10100111011011000110100010111000",0,16},
    {"111","00010010101110001011000100000000",1,6765909665ULL,"11101110001011000111101100000111",0,18},
    {"1100","10100111011011000110100010111000",0,2369294537ULL,"10100010110010000100001101101110",0,14},
    {"1101","10100111011011000110100010111000",1,255992085ULL,"11011110000110011101110100001101",0,18},
    {"11010","11011110000110011101110100001101",0,917411703ULL,"01111100101101111111111001111010",1,23},
    {"11011","11011110000110011101110100001101",1,6298685676ULL,"01101101010000101101001111001110",1,17},
    {"11000","10100010110010000100001101101110",0,620392484ULL,"00011011111011101010111110100000",0,18},
    {"11001","10100010110010000100001101101110",1,1147356616ULL,"00000010110000010101010111010000",1,11},
    {"110000","00011011111011101010111110100000",0,201439386ULL,"00000001001110000001110110001100",1,11},
    {"110001","00011011111011101010111110100000",1,454421730ULL,"00000000110100010011010101000011",1,11},
    {"1110","11101110001011000111101100000111",0,1429186925ULL,"00100110111100111100011110010111",1,19},
    {"1111","11101110001011000111101100000111",1,10313972740ULL,"11110011000001000001111101000100",0,14},
    {"11110","11110011000001000001111101000100",0,3872621716ULL,"01011100111110001010000101110010",0,16},
    {"11111","11110011000001000001111101000100",1,2951840447ULL,"11111111100010100011000101101011",1,19},
    {"111100","01011100111110001010000101110010",0,5364443153ULL,"00111000000001110000101111000101",1,13},
    {"111101","01011100111110001010000101110010",1,785466342ULL,"10101001011011000100111101011110",0,18},
    {"1111010","10101001011011000100111101011110",0,4406394223ULL,"11001001100101110011100011100001",0,16},
    {"1111011","10101001011011000100111101011110",1,317183221ULL,"11111001001000000110101111111001",0,18},
    {"11110100","11001001100101110011100011100001",0,677140366ULL,"01000010011000011011001110001100",1,13},
    {"11110101","11001001100101110011100011100001",1,4702237002ULL,"10101001110110000100110000110101",1,15},
    {"11110110","11111001001000000110101111111001",0,116187861ULL,"00011010111110111100111111001101",1,21},
    {"11110111","11111001001000000110101111111001",1,2168338618ULL,"10110111110111111010000111011101",0,22},
    {"111101110","10110111110111111010000111011101",0,9483082542ULL,"10001000101000100101011110000101",1,13},
    {"111101111","10110111110111111010000111011101",1,1166528144ULL,"11011011000100011110010110001010",0,16},
    {"1111011110","11011011000100011110010110001010",0,12479646968ULL,"01110100000101011100001010101101",1,15},
    {"1111011111","11011011000100011110010110001010",1,839208297ULL,"10101111010000100100100100010101",0,14},
    {"11110111110","10101111010000100100100100010101",0,4698029932ULL,"10010100111100000010110011100100",0,14},
    {"11110111111","10101111010000100100100100010101",1,80005764ULL,"01010111100111101010111011111001",1,21},
    {"111101111100","10010100111100000010110011100100",0,4773510433ULL,"01001011001100000000111100001000",1,11},
    {"111101111101","10010100111100000010110011100100",1,10268483482ULL,"01101011111101001101000010010101",1,17}
};

static bool verify(const Cert&c){
    uint32_t w=parse_bits(c.source);
    if(__builtin_popcount(w)&1) throw runtime_error("source must be even");
    uint32_t a=integrate(w,c.choice),b=0;
    for(uint64_t d=0;d<=c.depth;d++){
        if(a==0){
            string raw=bits(b);
            cout<<"path="<<c.path<<" depth="<<d
                <<" parity="<<(__builtin_popcount(b)&1)
                <<" weight="<<__builtin_popcount(b)
                <<" period="<<min_period(raw)
                <<" raw="<<raw<<" canonical="<<rotmin(raw)<<"\n";
            return d==c.depth && raw==c.target &&
                   ((__builtin_popcount(b)&1)==c.parity) &&
                   __builtin_popcount(b)==c.weight && min_period(raw)==32;
        }
        if(d==c.depth)break;
        uint32_t z=broad_child(a,b); b=a; a=z;
    }
    cerr<<"no return at certificate depth for path "<<c.path<<"\n";
    return false;
}

static int resume_scan(uint64_t start,uint32_t a,uint32_t b,uint64_t cap){
    for(uint64_t d=start;d<=cap;d++){
        if(a==0){
            string raw=bits(b);
            cout<<"hit depth="<<d<<" parity="<<(__builtin_popcount(b)&1)
                <<" weight="<<__builtin_popcount(b)
                <<" period="<<min_period(raw)
                <<" raw="<<raw<<" canonical="<<rotmin(raw)<<"\n";
            return 0;
        }
        if(d==cap){
            cout<<"nohit depth="<<d<<" a="<<hex<<setfill('0')<<setw(8)<<a
                <<" b="<<setw(8)<<b<<dec<<"\n";
            return 1;
        }
        uint32_t z=broad_child(a,b); b=a; a=z;
    }
    return 2;
}

int main(int argc,char**argv){
    if(argc<2 || string(argv[1])=="--list"){
        for(auto&c:certs) cout<<c.path<<" depth="<<c.depth<<"\n";
        return 0;
    }
    string arg=argv[1];
    if(arg=="--resume"){
        if(argc!=6){cerr<<"--resume START A_HEX B_HEX CAP\n";return 3;}
        uint64_t start=strtoull(argv[2],nullptr,10);
        uint32_t a=strtoul(argv[3],nullptr,16),b=strtoul(argv[4],nullptr,16);
        uint64_t cap=strtoull(argv[5],nullptr,10);
        return resume_scan(start,a,b,cap);
    }
    if(arg=="--all"){
        atomic<int> next{0},fail{0};
        unsigned nt=min<unsigned>(certs.size(),max(1u,thread::hardware_concurrency()));
        vector<thread> workers;
        for(unsigned k=0;k<nt;k++)workers.emplace_back([&]{
            for(;;){int i=next.fetch_add(1);if(i>=(int)certs.size())break;if(!verify(certs[i]))fail++;}
        });
        for(auto&t:workers)t.join();
        return fail?4:0;
    }
    for(auto&c:certs) if(arg==c.path) return verify(c)?0:5;
    cerr<<"unknown path\n"; return 6;
}
