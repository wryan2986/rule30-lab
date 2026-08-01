#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>
using u64=std::uint64_t;
constexpr int MAXK=25, CAP=64;
u64 f(char g,u64 s){u64 t=s^((s<<1)|(s<<2));if(g=='t')return t;if(g=='u')return t^1;if(g=='p')return t^1^((s&1)==0?2:0);throw std::runtime_error("g");}
std::vector<u64> next(const std::vector<u64>&c){std::vector<u64>o;o.reserve(c.size()*3);for(u64 s:c){o.push_back(f('t',s));o.push_back(f('u',s));o.push_back(f('p',s));}std::sort(o.begin(),o.end());o.erase(std::unique(o.begin(),o.end()),o.end());return o;}
std::vector<std::vector<u64>> levels(char p){std::vector<std::vector<u64>>l(MAXK+1);l[1]={p=='p'?3ULL:1ULL};for(int k=2;k<=MAXK;++k)l[k]=next(l[k-1]);return l;}
bool has(const std::vector<u64>&v,u64 x){return std::binary_search(v.begin(),v.end(),x);}
unsigned fiber(const std::vector<std::vector<u64>>&l,int k,u64 q){unsigned m=0;for(int d=0;d<4;++d)if(has(l[k+1],4*q+d))m|=1u<<d;return m;}
u64 maskseq(const std::vector<std::vector<u64>>&l,int n,u64 y,int L){u64 z=0;for(int s=0;s<L;++s){u64 q=y>>2;int k=n-1-s;unsigned m=fiber(l,k,q);z|=u64(m)<<(4*s);y=q;}return z;}
std::string sched(u64 s){std::string w;for(int i=0;i<CAP;++i){u64 r=s&15;char b;if(r==7)b='u';else if(r==11)b='t';else return w;s=f(b,f('p',(s-3)>>2));w.push_back(b);}throw std::runtime_error("cap");}
bool adm(const std::string&w){return w.find("uu")==std::string::npos&&w.find("ttttt")==std::string::npos&&w.find("ututtu")==std::string::npos;}
struct Pat{std::array<int,3>g;std::string t,c;};
std::vector<Pat> pats(){std::vector<Pat>z;for(int a=2;a<=5;++a)for(int b=2;b<=5;++b)for(int c=2;c<=5;++c){std::array<int,3>g{a,b,c};std::string t="u",co="u";for(int i=0;i<3;++i){t.append(g[i]-1,'t');co.append(g[i]-1,'t');if(i<2){t+='u';co+='u';}else co+='u';}if(adm(co))z.push_back({g,t,co});}return z;}
bool dominates(u64 cur,u64 sh,int L){for(int s=0;s<L;++s){unsigned a=(cur>>(4*s))&15,b=(sh>>(4*s))&15;if(a&~b)return false;}return true;}
int defects(u64 sh,int L){int n=0;for(int s=0;s<L;++s)if(((sh>>(4*s))&15)!=15)++n;return n;}
std::string seqstr(u64 z,int L){std::string s;for(int i=0;i<L;++i){if(i)s+=',';unsigned m=(z>>(4*i))&15;for(int b=3;b>=0;--b)s+=((m>>b)&1)?'1':'0';}return s;}
struct Row{u64 r,seq,y;bool operator<(const Row&o)const{return std::tie(r,seq,y)<std::tie(o.r,o.seq,o.y);}};
int main(){auto ps=pats();int globalmax=0;u64 total=0,fail=0;std::map<int,u64>hist;std::set<std::string> usedseqs;
 for(char phase:{'p','u'}){auto l=levels(phase);
  for(int k=2;k<=MAXK;++k){
   struct Occ{u64 x;int cut,L,w;std::vector<std::array<int,3>>gs;};std::vector<Occ>os;std::set<int>ds;
   for(u64 x:l[k]){if((x&3)!=3)continue;auto w=sched(x);for(int cut=0;cut<=(int)w.size();++cut){std::string base=w.substr(0,cut);std::vector<std::array<int,3>>gs;for(auto&p:ps)if(w.compare(cut,p.t.size(),p.t)==0&&adm(base+p.c))gs.push_back(p.g);if(!gs.empty()){os.push_back({x,cut,cut+1,(int)gs.size(),gs});ds.insert(cut+1);}}}
   if(os.empty())continue;
   std::map<int,std::vector<Row>> idx;
   for(int L:ds){u64 mask=(u64{1}<<(2*L))-1;auto&v=idx[L];v.reserve(l[k-1].size());for(u64 y:l[k-1])v.push_back({y&mask,maskseq(l,k-1,y,L),y});std::sort(v.begin(),v.end());}
   for(auto&o:os){u64 mask=(u64{1}<<(2*o.L))-1,r=o.x&mask,cs=maskseq(l,k,o.x,o.L);auto&v=idx[o.L];Row lo{r,0,0},hi{r,std::numeric_limits<u64>::max(),std::numeric_limits<u64>::max()};auto a=std::lower_bound(v.begin(),v.end(),lo),b=std::upper_bound(v.begin(),v.end(),hi);int best=999;u64 bestseq=0,besty=0;u64 lastseq=std::numeric_limits<u64>::max();for(auto it=a;it!=b;++it){if(it->seq==lastseq)continue;lastseq=it->seq;if(dominates(cs,it->seq,o.L)){int d=defects(it->seq,o.L);if(d<best){best=d;bestseq=it->seq;besty=it->y;}}}total+=o.w;if(best==999){fail+=o.w;std::cout<<"NO_DOM phase="<<phase<<" k="<<k<<" L="<<o.L<<" x=0x"<<std::hex<<o.x<<std::dec<<"\n";continue;}hist[best]+=o.w;globalmax=std::max(globalmax,best);usedseqs.insert(seqstr(bestseq,o.L));if(best>0){std::cout<<"RELAX phase="<<phase<<" k="<<k<<" cut="<<o.cut<<" L="<<o.L<<" weight="<<o.w<<" x=0x"<<std::hex<<o.x<<" residue=0x"<<r<<" shadow=0x"<<besty<<std::dec<<" defects="<<best<<" cur="<<seqstr(cs,o.L)<<" sh="<<seqstr(bestseq,o.L)<<" gaps=";for(auto g:o.gs)std::cout<<g[0]<<g[1]<<g[2]<<";";std::cout<<"\n";}}
  }
 }
 std::cout<<"total="<<total<<" fail="<<fail<<" max_min_defects="<<globalmax<<"\n";for(auto[k,v]:hist)std::cout<<"defect_hist_"<<k<<"="<<v<<"\n";std::cout<<"chosen_sequences="<<usedseqs.size()<<"\n"; for (const auto& q:usedseqs) std::cout<<"chosen="<<q<<"\n";
 if(total!=3395||fail!=0||globalmax!=3||hist[0]!=3393||hist[3]!=2||hist.size()!=2||usedseqs.size()!=9)throw std::runtime_error("totals");
}
