#include <algorithm>
#include <array>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <optional>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
using u64=std::uint64_t;
constexpr int MAXK=25;
constexpr std::array<unsigned,4> CHILD{0b1011,0b1100,0b1110,0b0011};

u64 forward(char g,u64 s){u64 t=s^((s<<1)|(s<<2));if(g=='t')return t;if(g=='u')return t^1;if(g=='p')return t^1^((s&1)==0?2:0);throw std::runtime_error("g");}
std::vector<u64> next_level(const std::vector<u64>& cur){std::vector<u64> out;out.reserve(cur.size()*3);for(u64 s:cur){out.push_back(forward('t',s));out.push_back(forward('u',s));out.push_back(forward('p',s));}std::sort(out.begin(),out.end());out.erase(std::unique(out.begin(),out.end()),out.end());return out;}
bool contains(const std::vector<u64>& v,u64 x){return std::binary_search(v.begin(),v.end(),x);}
int bitlen(u64 x){return x?64-__builtin_clzll(x):0;}
std::optional<u64> inv_t(u64 out){if(out==0)return u64{0};int w=bitlen(out)-2;if(w<=0)return std::nullopt;u64 s=0;for(int i=0;i<w;++i){unsigned lo=0;if(i>=1)lo|=(s>>(i-1))&1;if(i>=2)lo|=(s>>(i-2))&1;unsigned b=((out>>i)&1)^lo;s|=u64(b)<<i;}if(forward('t',s)!=out)return std::nullopt;return s;}
std::optional<u64> inv_g(char g,u64 out){std::optional<u64>s;if(g=='t')s=inv_t(out);else if(g=='u')s=inv_t(out^1);else if(g=='p'){unsigned low=(out&1)^1;s=inv_t(out^1^(low==0?2:0));}else throw std::runtime_error("g");if(!s||forward(g,*s)!=out)return std::nullopt;return s;}
std::optional<u64> candidate(u64 q,int d){char g=d==0?'t':d==1?'u':'p';auto r=inv_g(g,q);if(!r)return std::nullopt;return 4*(*r)+unsigned(d);}
unsigned fiber_from_pred(unsigned p){unsigned f=0;for(int d=0;d<4;++d)if((p>>d)&1)f|=CHILD[d];return f;}
unsigned pred_mask(const std::vector<u64>& level,u64 q){unsigned p=0;for(int d=0;d<4;++d){auto x=candidate(q,d);if(x&&contains(level,*x))p|=1u<<d;}if((p&4)&&!(p&8))throw std::runtime_error("mate");return p;}
unsigned signature(const std::vector<u64>& level,u64 q){unsigned p=pred_mask(level,q),f=fiber_from_pred(p);return (p<<4)|f;}
std::string bits(unsigned x){std::string s;for(int i=3;i>=0;--i)s.push_back((x>>i&1)?'1':'0');return s;}

struct PhaseSummary{u64 outputs=0,edge_occurrences=0;std::set<unsigned> signatures;std::set<u64> edges;};
PhaseSummary campaign(char phase){std::vector<u64> cur{phase=='p'?3ULL:1ULL};PhaseSummary z;for(int k=1;k<=MAXK;++k){z.outputs+=cur.size();std::vector<unsigned> csig;csig.reserve(cur.size());for(u64 q:cur){unsigned s=signature(cur,q);csig.push_back(s);z.signatures.insert(s);}if(k==MAXK)break;auto next=next_level(cur);std::vector<unsigned> nsig;nsig.reserve(next.size());for(u64 q:next){unsigned s=signature(next,q);nsig.push_back(s);z.signatures.insert(s);}for(size_t i=0;i<cur.size();++i){u64 q=cur[i];for(int d=0;d<4;++d){u64 child=4*q+d;auto it=std::lower_bound(next.begin(),next.end(),child);if(it==next.end()||*it!=child)continue;size_t j=it-next.begin();u64 code=(u64(csig[i])<<24)|(u64(d)<<20)|u64(nsig[j]);z.edges.insert(code);++z.edge_occurrences;}}cur.swap(next);}return z;}

std::vector<std::vector<u64>> small_levels(){std::vector<std::vector<u64>> l(8);l[1]={3};for(int k=2;k<=7;++k)l[k]=next_level(l[k-1]);return l;}
std::pair<unsigned,unsigned> visible(const std::vector<std::vector<u64>>&l,int kq,u64 q,int kp,u64 p){return {fiber_from_pred(pred_mask(l[kq],q)),fiber_from_pred(pred_mask(l[kp],p))};}
void verify_counterexamples(){auto l=small_levels();auto unsafe=visible(l,4,222,3,50);auto safe=visible(l,6,3202,5,802);auto ulow=visible(l,3,222>>2,2,50>>2);auto slow=visible(l,5,3202>>2,4,802>>2);if(unsafe!=std::pair<unsigned,unsigned>{11,15}||safe!=unsafe||ulow!=std::pair<unsigned,unsigned>{15,12}||slow!=std::pair<unsigned,unsigned>{15,15})throw std::runtime_error("counterexample");
unsigned src=signature(l[1],3),a=signature(l[2],12),b=signature(l[6],3204),c=signature(l[7],14332);if(src!=0x83||a!=0x2c||b!=0xef||c!=0x00)throw std::runtime_error("nondeterminism");}
}
int main(){verify_counterexamples();auto p=campaign('p'),u=campaign('u');std::cout<<"maximum_complexity="<<MAXK<<"\n";std::cout<<"phase_p_outputs="<<p.outputs<<"\nphase_u_outputs="<<u.outputs<<"\n";std::cout<<"total_outputs="<<p.outputs+u.outputs<<"\n";std::cout<<"phase_p_signatures="<<p.signatures.size()<<"\nphase_u_signatures="<<u.signatures.size()<<"\n";std::cout<<"phase_p_edges="<<p.edges.size()<<"\nphase_u_edges="<<u.edges.size()<<"\n";std::cout<<"phase_p_edge_occurrences="<<p.edge_occurrences<<"\nphase_u_edge_occurrences="<<u.edge_occurrences<<"\n";std::cout<<"unsafe_visible=1011/1111 digit=2 lower=1111/1100\n";std::cout<<"safe_visible=1011/1111 digit=2 lower=1111/1111\n";std::cout<<"universal_signatures=12\n";if(p.signatures.size()!=12||u.signatures.size()!=12||p.edges.size()!=194||u.edges.size()!=194)throw std::runtime_error("totals");}
