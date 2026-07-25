#include <algorithm>
#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using u128 = unsigned __int128;

namespace {
constexpr int MAX_DEPTH = 16;
constexpr int MAX_RESIDUAL = 20;
constexpr std::array<unsigned,4> CHILD_MASK{0b1011,0b1100,0b1110,0b0011};

struct U128Hash { size_t operator()(u128 x) const noexcept { uint64_t lo=(uint64_t)x, hi=(uint64_t)(x>>64); uint64_t z=lo^(hi+0x9e3779b97f4a7c15ULL+(lo<<6)+(lo>>2)); z^=z>>30; z*=0xbf58476d1ce4e5b9ULL; z^=z>>27; z*=0x94d049bb133111ebULL; z^=z>>31; return (size_t)z; } };
std::string hex128(u128 x){ if(!x)return "0x0"; std::string s; while(x){ unsigned d=(unsigned)(x&15); s.push_back("0123456789abcdef"[d]); x>>=4;} std::reverse(s.begin(),s.end()); return "0x"+s; }
int bit_length(u128 x){int n=0;while(x){++n;x>>=1;}return n;}
u128 forward(char name,u128 s){u128 t=s^((s<<1)|(s<<2)); if(name=='t')return t; if(name=='u')return t^1; if(name=='p')return t^1^((s&1)==0?2:0); throw std::runtime_error("name");}
std::vector<u128> children(u128 s){std::array<u128,3>a{forward('t',s),forward('u',s),forward('p',s)}; std::sort(a.begin(),a.end()); return std::vector<u128>(a.begin(),std::unique(a.begin(),a.end()));}
u128 phase_start(char p){return p=='p'?3:1;} int expected_bits(char p,int k){return p=='p'?2*k:2*k-1;}
std::optional<u128> inverse_t(u128 out){if(out==0)return u128{0};int w=bit_length(out)-2;if(w<=0)return std::nullopt;u128 s=0;for(int i=0;i<w;++i){unsigned lo=0;if(i>=1)lo|=(unsigned)((s>>(i-1))&1);if(i>=2)lo|=(unsigned)((s>>(i-2))&1);unsigned b=(unsigned)((out>>i)&1)^lo;s|=(u128)b<<i;}if(forward('t',s)!=out)return std::nullopt;return s;}
std::optional<u128> inverse_g(char n,u128 out){if(n=='t')return inverse_t(out);std::optional<u128>s;if(n=='u')s=inverse_t(out^1);else {unsigned low=(unsigned)(out&1)^1; s=inverse_t(out^1^(low==0?2:0));} if(!s||forward(n,*s)!=out)return std::nullopt;return s;}
std::optional<u128> candidate(u128 q,int d){char g=d==0?'t':d==1?'u':'p';auto r=inverse_g(g,q);if(!r)return std::nullopt;return 4*(*r)+(unsigned)d;}

struct Key {char p; int k; u128 x; bool operator==(Key const&o)const{return p==o.p&&k==o.k&&x==o.x;}};
struct KeyHash {size_t operator()(Key const&a)const noexcept{return U128Hash{}(a.x)^((size_t)a.k<<1)^a.p;}};
std::unordered_map<Key,bool,KeyHash> memo;
std::map<std::pair<char,int>,std::vector<u128>> levels;
std::map<std::pair<char,int>,std::unordered_set<u128,U128Hash>> level_sets;
void build_levels(char p,int maxk){std::vector<u128> cur{phase_start(p)};levels[{p,1}]=cur;level_sets[{p,1}]={cur.begin(),cur.end()};for(int k=2;k<=maxk;++k){std::vector<u128> nxt; nxt.reserve(cur.size()*3);for(u128 x:cur){auto cs=children(x);nxt.insert(nxt.end(),cs.begin(),cs.end());}std::sort(nxt.begin(),nxt.end());nxt.erase(std::unique(nxt.begin(),nxt.end()),nxt.end());levels[{p,k}]=nxt;level_sets[{p,k}]={nxt.begin(),nxt.end()};cur.swap(nxt);}}
bool member(char p,int k,u128 x){if(k<1||bit_length(x)!=expected_bits(p,k))return false;if(k<=MAX_RESIDUAL){auto it=level_sets.find({p,k});return it!=level_sets.end()&&it->second.count(x);}Key key{p,k,x};auto it=memo.find(key);if(it!=memo.end())return it->second;u128 q=x>>2;int e=(int)(x&3);bool ok=false;for(int d=0;d<4&&!ok;++d){if(((CHILD_MASK[d]>>e)&1)==0)continue;auto par=candidate(q,d);if(par&&member(p,k-1,*par))ok=true;}memo.emplace(key,ok);return ok;}

uint64_t mask64(int w){return w==64?~0ULL:((uint64_t{1}<<w)-1);} // widths <=32 here
uint64_t inv_t_mod(uint64_t out,int w){uint64_t mask=w?mask64(w):0;out&=mask;uint64_t s=0;for(int i=0;i<w;++i){unsigned lo=0;if(i>=1)lo|=(s>>(i-1))&1;if(i>=2)lo|=(s>>(i-2))&1;unsigned b=((out>>i)&1)^lo;s|=(uint64_t)b<<i;}return s;}
uint64_t inv_g_mod(char n,uint64_t out,int w){uint64_t mask=w?mask64(w):0;out&=mask;if(n=='t')return inv_t_mod(out,w);if(n=='u')return inv_t_mod(out^1,w);unsigned low=(out&1)^1;return inv_t_mod(out^1^(low==0?2:0),w);}
uint64_t fringe(uint64_t s){uint64_t row=1+2*s;uint64_t odd=row^((row>>1)|(row>>2));return (odd<<1)^(odd|(odd>>1));}
std::string actual_driver(int L){uint64_t s=0;std::string out;for(int i=0;i<L;++i){out.push_back((s&3)==0?'u':'t');s=fringe(s);}return out;}
uint64_t survivor_word(std::string word){uint64_t s=0;int w=0;for(auto it=word.rbegin();it!=word.rend();++it){w+=2;int iw=w-2;s=inv_g_mod(*it,s,iw);s=inv_g_mod('p',s,iw);s=((s<<2)|3)&mask64(w);}return s;}

struct FilterResult {std::vector<u128> states; std::vector<size_t> funnel;};
FilterResult cylinder_filter(char p,int L,int k,uint64_t X){memo.clear();if(k<=L){std::vector<u128> s;if(member(p,k,X))s.push_back(X);return {s,{s.size()}};}int r=k-L;if(r<1||r>MAX_RESIDUAL)throw std::runtime_error("residual outside campaign");std::vector<u128> cur=levels.at({p,r});std::vector<size_t> funnel{cur.size()};for(int idx=L-1;idx>=0;--idx){int e=(X>>(2*idx))&3;int c=r+(L-1-idx);std::vector<u128> nxt;nxt.reserve(cur.size());for(u128 q:cur){u128 y=(q<<2)|(unsigned)e;if(member(p,c+1,y))nxt.push_back(y);}cur.swap(nxt);funnel.push_back(cur.size());if(cur.empty())break;}return {cur,funnel};}

int kappa(char p,int L,uint64_t X,int lower,int upper,FilterResult* final=nullptr){for(int k=lower;k<=upper;++k){auto row=cylinder_filter(p,L,k,X);if(!row.states.empty()){if(final)*final=std::move(row);return k;}}return -1;}
std::string funnel_string(std::vector<size_t> const&v){std::ostringstream o;for(size_t i=0;i<v.size();++i){if(i)o<<',';o<<v[i];}return o.str();}

uint64_t small_exhaustive(){uint64_t checks=0;for(char p:{'p','u'}){for(int k=1;k<=10;++k){auto const& full=levels.at({p,k});for(int L=1;L<=std::min(5,k+1);++L){uint64_t mod=uint64_t{1}<<(2*L);std::map<uint64_t,size_t> direct;for(u128 x:full)direct[(uint64_t)x&(mod-1)]++;for(uint64_t X=0;X<mod;++X){auto f=cylinder_filter(p,L,k,X);size_t want=direct[X];if(f.states.size()!=want){std::cerr<<"mismatch "<<p<<" k"<<k<<" L"<<L<<" X"<<X<<" got"<<f.states.size()<<" want"<<want<<"\n";throw std::runtime_error("small mismatch");}++checks;}}}}return checks;}
}

int main(){build_levels('p',MAX_RESIDUAL);build_levels('u',MAX_RESIDUAL);const uint64_t small_checks=small_exhaustive();
std::map<int,std::pair<int,int>> expected{{1,{1,2}},{2,{3,2}},{3,{7,2}},{4,{8,7}},{5,{8,12}},{6,{12,14}},{7,{13,14}},{8,{17,14}},{9,{17,18}},{10,{17,19}},{11,{21,26}},{12,{28,27}},{13,{30,30}},{14,{33,30}},{15,{34,30}},{16,{36,30}}};
int prevp=1,prevu=1;uint64_t checksum=1469598103934665603ULL;for(int L=1;L<=MAX_DEPTH;++L){uint64_t X=survivor_word(actual_driver(L));FilterResult fp,fu;int kp=kappa('p',L,X,1,expected[L].first,&fp);int ku=kappa('u',L,X,1,expected[L].second,&fu);if(kp!=expected[L].first||ku!=expected[L].second)throw std::runtime_error("kappa mismatch");std::cout<<"actual depth="<<L<<" residue=0x"<<std::hex<<X<<std::dec<<" kappa_p="<<kp<<" p_minimizers="<<fp.states.size()<<" p_funnel="<<funnel_string(fp.funnel)<<" kappa_u="<<ku<<" u_minimizers="<<fu.states.size()<<" u_funnel="<<funnel_string(fu.funnel)<<"\n";checksum^=X+((uint64_t)kp<<40)+((uint64_t)ku<<48);checksum*=1099511628211ULL;prevp=kp;prevu=ku;}
for(auto [word,label]:std::vector<std::pair<std::string,std::string>>{{"tutututttutu","w12"},{"tutututttututu","w14"},{"tutututttutututu","w16"}}){int L=word.size();uint64_t X=survivor_word(word);auto f=cylinder_filter('u',L,25,X);if(f.states.size()!=1)throw std::runtime_error("counter unique");std::cout<<"counter "<<label<<" depth="<<L<<" residue=0x"<<std::hex<<X<<std::dec<<" minimizers="<<f.states.size()<<" state="<<hex128(f.states.front())<<" funnel="<<funnel_string(f.funnel)<<"\n";}
std::cout<<"small_exhaustive_cylinder_checks="<<small_checks<<"\n";std::cout<<"max_depth="<<MAX_DEPTH<<"\n";std::cout<<"max_residual="<<MAX_RESIDUAL<<"\n";std::cout<<"p_residual_states="<<levels[{ 'p',MAX_RESIDUAL}].size()<<"\n";std::cout<<"u_residual_states="<<levels[{ 'u',MAX_RESIDUAL}].size()<<"\n";std::cout<<"checksum=0x"<<std::hex<<checksum<<std::dec<<"\n";
}
