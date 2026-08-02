#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>
using u64=std::uint64_t;
constexpr int FRONTIER_MAX=28,CAMPAIGN_MAX=27,MAX_RADIUS=7,SOURCE_MAX=22,CAP=64,INITIAL_BUDGET=3;

u64 f(char g,u64 s){u64 t=s^((s<<1)|(s<<2));if(g=='t')return t;if(g=='u')return t^1;if(g=='p')return t^1^((s&1)==0?2:0);throw std::runtime_error("generator");}
std::vector<u64> next(const std::vector<u64>&v){std::vector<u64>o;o.reserve(v.size()*3);for(u64 s:v)for(char g:std::string("tup"))o.push_back(f(g,s));std::sort(o.begin(),o.end());o.erase(std::unique(o.begin(),o.end()),o.end());return o;}
bool has(const std::vector<u64>&v,u64 x){return std::binary_search(v.begin(),v.end(),x);}
unsigned fiber(const std::vector<std::vector<u64>>&l,int k,u64 q){unsigned m=0;for(int d=0;d<4;++d)if(has(l[k+1],4*q+unsigned(d)))m|=1u<<d;return m;}
u64 masks(const std::vector<std::vector<u64>>&l,int k,u64 x,int L){u64 z=0;for(int j=0;j<L;++j){x>>=2;z|=u64(fiber(l,k-1-j,x))<<(4*j);}return z;}
bool dominant(u64 a,u64 b,int L){for(int j=0;j<L;++j)if(((a>>(4*j))&15)&~((b>>(4*j))&15))return false;return true;}
bool sync(u64 a,u64 b,int L){for(int j=0;j<L;++j){unsigned x=(a>>(4*j))&15,y=(b>>(4*j))&15;if(y!=15&&y!=x)return false;}return true;}
std::string schedule(u64 s){std::string w;for(int i=0;i<CAP;++i){u64 r=s&15;char b;if(r==7)b='u';else if(r==11)b='t';else return w;s=f(b,f('p',(s-3)>>2));w.push_back(b);}throw std::runtime_error("schedule cap");}
bool admissible(const std::string&w){return w.find("uu")==std::string::npos&&w.find("ttttt")==std::string::npos&&w.find("ututtu")==std::string::npos;}
struct Occ{int k,L,best=999;u64 x,residue,cur,shadow=0;};
struct Node{int k;u64 q,p;bool operator<(const Node&o)const{return std::tie(k,q,p)<std::tie(o.k,o.q,o.p);}};
struct State{Node n;int budget;bool operator<(const State&o)const{return std::tie(n,budget)<std::tie(o.n,o.budget);}};
std::vector<Occ> select(const std::vector<std::vector<u64>>&l){std::vector<Occ>all;for(int k=2;k<=CAMPAIGN_MAX;++k){std::vector<Occ>os;int maxL=0;std::vector<std::unordered_map<u64,std::vector<int>>>idx(20);for(u64 x:l[k]){if((x&3)!=3)continue;auto w=schedule(x);for(int cut=0;cut<=(int)w.size();++cut){if(w.compare(cut,6,"ututut")||!admissible(w.substr(0,cut)+"utututu"))continue;int L=cut+1;u64 mm=(u64{1}<<(2*L))-1;int i=os.size();os.push_back({k,L,999,x,x&mm,masks(l,k,x,L),0});idx[L][x&mm].push_back(i);maxL=std::max(maxL,L);}}for(u64 y:l[k-1]){u64 state=y,seq=0;int dc=0;for(int j=0;j<maxL;++j){state>>=2;unsigned m=fiber(l,k-2-j,state);seq|=u64(m)<<(4*j);dc+=m!=15;int L=j+1;u64 r=y&((u64{1}<<(2*L))-1);auto it=idx[L].find(r);if(it==idx[L].end())continue;for(int i:it->second){auto&o=os[i];if(dc>o.best||!dominant(o.cur,seq,L)||!sync(o.cur,seq,L))continue;if(dc<o.best||y<o.shadow){o.best=dc;o.shadow=y;}}}}for(auto&o:os){if(o.best==999)throw std::runtime_error("shadow failure");all.push_back(o);}}return all;}
int local_cost(const std::vector<std::vector<u64>>&l,const Node&n){unsigned cm=fiber(l,n.k,n.q),sm=fiber(l,n.k-1,n.p);if(sm!=15&&sm!=cm)throw std::runtime_error("non-sync");return sm!=15;}
bool legal_child(const std::vector<std::vector<u64>>&l,const Node&n,int d,Node&c){c={n.k+1,4*n.q+unsigned(d),4*n.p+unsigned(d)};if(c.k+1>FRONTIER_MAX||!has(l[c.k],c.q)||!has(l[c.k-1],c.p))return false;unsigned cm=fiber(l,c.k,c.q),sm=fiber(l,c.k-1,c.p);return sm==15||sm==cm;}
bool alive(const std::vector<std::vector<u64>>&l,const State&s){return s.budget>=0&&local_cost(l,s.n)<=s.budget;}
bool transition(const std::vector<std::vector<u64>>&l,const State&s,int d,State&t){if(!alive(l,s))return false;Node c;if(!legal_child(l,s.n,d,c))return false;t={c,s.budget-local_cost(l,s.n)};return alive(l,t);}

struct LKey{std::array<int,4>child;bool operator<(const LKey&o)const{return child<o.child;}};
class CappedLanguage{const std::vector<std::vector<u64>>&l;std::vector<std::map<LKey,int>>canon;std::map<std::tuple<int,int,u64,u64,int>,int>memo;public:explicit CappedLanguage(const std::vector<std::vector<u64>>&x):l(x),canon(MAX_RADIUS+1){}int id(int r,const State&s){if(!alive(l,s))return -1;auto key=std::make_tuple(r,s.n.k,s.n.q,s.n.p,s.budget);auto it=memo.find(key);if(it!=memo.end())return it->second;LKey z{{-1,-1,-1,-1}};if(r)for(int d=0;d<4;++d){State t;if(transition(l,s,d,t))z.child[d]=id(r-1,t);}auto&mp=canon[r];auto jt=mp.find(z);int v;if(jt==mp.end()){v=mp.size();mp.emplace(z,v);}else v=jt->second;memo[key]=v;return v;}int alphabet(int r)const{return canon[r].size();}};

int main(){std::vector<std::vector<u64>>l(FRONTIER_MAX+1);l[1]={1};u64 outputs=1;for(int k=2;k<=FRONTIER_MAX;++k){l[k]=next(l[k-1]);outputs+=l[k].size();}
auto os=select(l);std::map<int,u64>hist;std::set<Node>all,source;for(const auto&o:os){++hist[o.best];for(int j=1;j<=o.L;++j){Node n{o.k-j,o.x>>(2*j),o.shadow>>(2*j)};all.insert(n);if(n.k<=SOURCE_MAX)source.insert(n);}}
std::set<State>source_states;for(const auto&n:source)source_states.insert({n,INITIAL_BUDGET});CappedLanguage r(l);std::vector<std::map<State,int>>ids(MAX_RADIUS+1);for(int d=0;d<=MAX_RADIUS;++d)for(const auto&s:source_states)ids[d][s]=r.id(d,s);
std::cout<<"outputs="<<outputs<<"\nocc="<<os.size()<<"\ndef0="<<hist[0]<<"\ndef3="<<hist[3]<<"\nall="<<all.size()<<"\nsource="<<source.size()<<"\n";
for(int d=0;d<=MAX_RADIUS;++d){std::map<std::pair<int,int>,std::vector<State>>level;std::map<int,std::vector<State>>un;for(const auto&s:source_states){level[{s.n.k,ids[d][s]}].push_back(s);un[ids[d][s]].push_back(s);}int ls=-1,us=-1;if(d<MAX_RADIUS){ls=us=0;for(const auto&[k,v]:level){(void)k;std::set<int>z;for(const auto&s:v)z.insert(ids[d+1][s]);ls+=z.size()>1;}for(const auto&[k,v]:un){(void)k;std::set<int>z;for(const auto&s:v)z.insert(ids[d+1][s]);us+=z.size()>1;}}std::cout<<"r"<<d<<"_alphabet="<<r.alphabet(d)<<" r"<<d<<"_level="<<level.size()<<" r"<<d<<"_un="<<un.size();if(d<MAX_RADIUS)std::cout<<" r"<<d<<"_lsplit="<<ls<<" r"<<d<<"_usplit="<<us;std::cout<<"\n";}
std::set<State>deep;for(const auto&n:source)if(n.k<=18)deep.insert({n,INITIAL_BUDGET});bool changed=true;while(changed){changed=false;std::vector<State>v(deep.begin(),deep.end());for(const auto&s:v){if(s.n.k>=22)continue;for(int d=0;d<4;++d){State t;if(transition(l,s,d,t)&&deep.insert(t).second)changed=true;}}}
for(int rr=0;rr<=MAX_RADIUS;++rr){std::set<int>cl;for(const auto&s:deep)cl.insert(r.id(rr,s));std::cout<<"deep_r"<<rr<<"="<<cl.size()<<"\n";}
for(int R=1;R<=6;++R){std::map<int,std::vector<State>>classes;for(const auto&s:deep)classes[r.id(R,s)].push_back(s);int split=0;for(const auto&[id,v]:classes){(void)id;std::set<int>z;for(const auto&s:v)z.insert(r.id(R+1,s));split+=z.size()>1;}std::map<std::pair<int,int>,std::set<int>>tr;for(const auto&s:deep)if(s.n.k<22){int c=r.id(R,s);for(int d=0;d<4;++d){State t;int x=-1;if(transition(l,s,d,t))x=r.id(R,t);tr[{c,d}].insert(x);}}int nondet=0;for(const auto&[k,v]:tr){(void)k;nondet+=v.size()>1;}std::cout<<"R"<<R<<"_classes="<<classes.size()<<" R"<<R<<"_split="<<split<<" R"<<R<<"_nondet="<<nondet<<"\n";}
constexpr int R=4;std::set<int>seen;for(int k=1;k<=22;++k){std::set<int>z;int count=0;for(const auto&s:deep)if(s.n.k==k){z.insert(r.id(R,s));++count;}int fresh=0;for(int x:z)fresh+=!seen.count(x);std::cout<<"k"<<k<<"_states="<<count<<" k"<<k<<"_classes="<<z.size()<<" k"<<k<<"_new="<<fresh<<"\n";seen.insert(z.begin(),z.end());}

struct AKeyLocal {int budget; unsigned cm,sm; u64 residue; bool operator<(const AKeyLocal&o)const{return std::tie(budget,cm,sm,residue)<std::tie(o.budget,o.cm,o.sm,o.residue);} bool operator==(const AKeyLocal&o)const{return budget==o.budget&&cm==o.cm&&sm==o.sm&&residue==o.residue;}};
auto affine_stats=[&](int bits){u64 modmask=(u64{1}<<bits)-1;std::map<AKeyLocal,int> cid;int nextid=0;auto feature=[&](const State&s){unsigned cm=fiber(l,s.n.k,s.n.q),sm=fiber(l,s.n.k-1,s.n.p);u64 h=s.n.q-4*s.n.p;return AKeyLocal{s.budget,cm,sm,h&modmask};};for(const auto&s:deep){auto key=feature(s);if(!cid.count(key))cid[key]=nextid++;}std::map<std::pair<int,int>,std::set<AKeyLocal>> targets;std::map<std::pair<int,int>,bool> dead;for(const auto&s:deep)if(s.n.k<22){int c=cid[feature(s)];for(int d=0;d<4;++d){State t;if(transition(l,s,d,t))targets[{c,d}].insert(feature(t));else dead[{c,d}]=true;}}int nondet=0;for(const auto&[key,v]:targets)if(v.size()+(dead[key]?1:0)>1)++nondet;return std::pair<int,int>{static_cast<int>(cid.size()),nondet};};
for(int bits=2;bits<=24;bits+=2){auto [classes,nondet]=affine_stats(bits);std::cout<<"affine_bits_"<<bits<<"_classes="<<classes<<" affine_bits_"<<bits<<"_nondet="<<nondet<<"\n";}
for(int bits: {14,16,18}){u64 mm=(u64{1}<<bits)-1;auto feat=[&](const State&s){return AKeyLocal{s.budget,fiber(l,s.n.k,s.n.q),fiber(l,s.n.k-1,s.n.p),(s.n.q-4*s.n.p)&mm};};struct Seen{bool dead;AKeyLocal target;State state;};std::map<std::pair<AKeyLocal,int>,Seen> seen;bool printed=false;for(const auto&s:deep)if(s.n.k<22&&!printed){for(int d=0;d<4&&!printed;++d){State t;bool ok=transition(l,s,d,t);AKeyLocal target=ok?feat(t):AKeyLocal{-1,0,0,0};auto key=std::make_pair(feat(s),d);auto it=seen.find(key);if(it==seen.end()){seen[key]={!ok,target,s};continue;}if(it->second.dead!=!ok||(!ok?false:!(it->second.target==target))){const State&a=it->second.state;std::cout<<"witness_bits="<<bits<<" digit="<<d<<" a_k="<<a.n.k<<" a_q=0x"<<std::hex<<a.n.q<<" a_p=0x"<<a.n.p<<std::dec<<" a_budget="<<a.budget<<" b_k="<<s.n.k<<" b_q=0x"<<std::hex<<s.n.q<<" b_p=0x"<<s.n.p<<std::dec<<" b_budget="<<s.budget<<" a_h="<<(a.n.q-4*a.n.p)<<" b_h="<<(s.n.q-4*s.n.p)<<" a_ok="<<(!it->second.dead)<<" b_ok="<<ok<<"\n";printed=true;}}}}
std::set<int> deep5,deep6;for(const auto&s:deep){deep5.insert(r.id(5,s));deep6.insert(r.id(6,s));}auto [a18c,a18n]=affine_stats(18);auto [a20c,a20n]=affine_stats(20);if(outputs!=40122287||os.size()!=2989||hist[0]!=2986||hist[3]!=3||all.size()!=4320||source.size()!=744||deep.size()!=3077||deep5.size()!=899||deep6.size()!=899||a18n!=11||a20c!=3074||a20n!=0)throw std::runtime_error("totals changed");
std::cout<<"deep_states="<<deep.size()<<"\n";
}
