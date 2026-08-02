#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <limits>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>
using u64=std::uint64_t;constexpr int KMAX=28,CAP=64;
u64 fg(char g,u64 s){u64 t=s^((s<<1)|(s<<2));if(g=='t')return t;if(g=='u')return t^1;if(g=='p')return t^1^((s&1)==0?2:0);throw std::runtime_error("g");}
std::vector<u64> nxt(const std::vector<u64>&v){std::vector<u64>o;o.reserve(v.size()*3);for(u64 s:v){o.push_back(fg('t',s));o.push_back(fg('u',s));o.push_back(fg('p',s));}std::sort(o.begin(),o.end());o.erase(std::unique(o.begin(),o.end()),o.end());return o;}
bool has(const std::vector<u64>&v,u64 x){return std::binary_search(v.begin(),v.end(),x);}unsigned fib(const std::vector<std::vector<u64>>&l,int k,u64 q){unsigned m=0;for(int d=0;d<4;++d)if(has(l[k+1],4*q+unsigned(d)))m|=1u<<d;return m;}
u64 seq(const std::vector<std::vector<u64>>&l,int k,u64 x,int L){u64 z=0;for(int j=0;j<L;++j){x>>=2;z|=u64(fib(l,k-1-j,x))<<(4*j);}return z;}bool dom(u64 a,u64 b,int L){for(int j=0;j<L;++j)if(((a>>(4*j))&15)&~((b>>(4*j))&15))return false;return true;}int defects(u64 b,int L){int n=0;for(int j=0;j<L;++j)n+=((b>>(4*j))&15)!=15;return n;}
std::string sch(u64 s){std::string w;for(int i=0;i<CAP;++i){u64 r=s&15;char b;if(r==7)b='u';else if(r==11)b='t';else return w;s=fg(b,fg('p',(s-3)>>2));w.push_back(b);}throw std::runtime_error("cap");}bool adm(const std::string&w){return w.find("uu")==std::string::npos&&w.find("ttttt")==std::string::npos&&w.find("ututtu")==std::string::npos;}
struct Q{int k,L;u64 x,cm;long long mass=0;};using Key=std::tuple<int,int,u64,u64>;
void eval(const std::vector<std::vector<u64>>&l,int k,std::vector<Q*>&req){if(req.empty())return;int maxL=0;std::vector<std::unordered_map<u64,std::vector<int>>>idx(24);for(int i=0;i<(int)req.size();++i){Q*q=req[i];u64 mm=(u64{1}<<(2*q->L))-1;idx[q->L][q->x&mm].push_back(i);maxL=std::max(maxL,q->L);}for(u64 y:l[k-1]){u64 st=y,ss=0;int dc=0;for(int j=0;j<maxL;++j){st>>=2;unsigned m=fib(l,k-2-j,st);ss|=u64(m)<<(4*j);dc+=m!=15;int L=j+1;u64 rr=y&((u64{1}<<(2*L))-1);auto it=idx[L].find(rr);if(it==idx[L].end())continue;for(int i:it->second){Q*q=req[i];if(dom(q->cm,ss,L))q->mass+=(dc&1)?-1:1;}}}}
int main(){std::vector<std::vector<u64>>l(KMAX+1);l[1]={1};u64 outputs=1;for(int k=2;k<=KMAX;++k){l[k]=nxt(l[k-1]);outputs+=l[k].size();}std::map<Key,Q> nodes;u64 occurrences=0;for(int k=2;k<=KMAX;++k)for(u64 x:l[k]){if((x&3)!=3)continue;auto w=sch(x);for(int c=0;c<=(int)w.size();++c){if(w.compare(c,6,"ututut")||!adm(w.substr(0,c)+"utututu"))continue;++occurrences;int L=c+1;u64 cm=seq(l,k,x,L);for(int j=0;j<L;++j){int kk=k-j,LL=L-j;u64 xx=x>>(2*j),cc=cm>>(4*j);nodes.try_emplace({kk,LL,xx,cc},Q{kk,LL,xx,cc,0});}}}
std::vector<std::vector<Q*>>byk(KMAX+1);for(auto&[key,q]:nodes){(void)key;byk[q.k].push_back(&q);}for(int k=2;k<=KMAX;++k)eval(l,k,byk[k]);using ExactKey=std::tuple<int,unsigned,long long>;
using SignKey=std::tuple<int,unsigned,int>;
std::map<ExactKey,std::set<long long>> exact_transitions;
std::map<SignKey,std::set<long long>> sign_transitions;
u64 zero_nodes=0,negative_nodes=0,ancestor_transitions=0;
long long minimum_absolute_mass=std::numeric_limits<long long>::max();
for(auto&[key,q]:nodes){
    zero_nodes+=q.mass==0;
    negative_nodes+=q.mass<0;
    minimum_absolute_mass=std::min(minimum_absolute_mass,std::llabs(q.mass));
    if(q.L<2)continue;
    ++ancestor_transitions;
    Key pk={q.k-1,q.L-1,q.x>>2,q.cm>>4};
    auto it=nodes.find(pk);if(it==nodes.end())throw std::runtime_error("missing parent");
    auto& p=it->second;
    const unsigned local=unsigned(q.cm&15);
    exact_transitions[{q.k,local,p.mass}].insert(q.mass);
    const int parent_sign=(p.mass>0)-(p.mass<0);
    const SignKey sign_key{q.k,local,parent_sign};
    sign_transitions[sign_key].insert(q.mass);
}
int scalar_collision_classes=0,scalar_mixed_sign_classes=0;
for(const auto&[key,values]:exact_transitions){
    (void)key;if(values.size()<2)continue;++scalar_collision_classes;
    std::set<int> signs;for(long long v:values)signs.insert((v>0)-(v<0));
    scalar_mixed_sign_classes+=signs.size()>1;
}
int sign_collision_classes=0,sign_mixed_classes=0;
for(const auto&[key,values]:sign_transitions){
    (void)key;
    if(values.size()<2)continue;
    ++sign_collision_classes;
    std::set<int> signs;
    for(long long value:values)signs.insert((value>0)-(value<0));
    sign_mixed_classes+=signs.size()>1;
}
auto get_node=[&](int k,u64 x,int L)->const Q&{
    const u64 cm=seq(l,k,x,L);
    auto it=nodes.find({k,L,x,cm});
    if(it==nodes.end())throw std::runtime_error("explicit node absent");
    return it->second;
};
const auto& magnitude_a=get_node(17,0x190b9fdfbULL,2);
const auto& magnitude_b=get_node(17,0x1bcd3a7b3ULL,2);
const auto& magnitude_parent_a=get_node(16,0x642e7f7eULL,1);
const auto& magnitude_parent_b=get_node(16,0x6f34e9ecULL,1);
const auto& sign_a=get_node(18,0x642e4d2f1ULL,3);
const auto& sign_b=get_node(18,0x6473d46abULL,5);
const auto& sign_parent_a=get_node(17,0x190b934bcULL,2);
const auto& sign_parent_b=get_node(17,0x191cf51aaULL,4);
std::cout<<"maximum_complexity="<<KMAX<<'\n';
std::cout<<"phase_u_outputs="<<outputs<<'\n';
std::cout<<"gap_222_cylinders="<<occurrences<<'\n';
std::cout<<"gap_ancestor_cylinders="<<nodes.size()<<'\n';
std::cout<<"gap_ancestor_transitions="<<ancestor_transitions<<'\n';
std::cout<<"signed_zero_ancestor_cylinders="<<zero_nodes<<'\n';
std::cout<<"negative_ancestor_cylinders="<<negative_nodes<<'\n';
std::cout<<"minimum_absolute_ancestor_mass="<<minimum_absolute_mass<<'\n';
std::cout<<"scalar_collision_classes="<<scalar_collision_classes<<'\n';
std::cout<<"scalar_mixed_sign_classes="<<scalar_mixed_sign_classes<<'\n';
std::cout<<"sign_collision_classes="<<sign_collision_classes<<'\n';
std::cout<<"sign_mixed_classes="<<sign_mixed_classes<<'\n';
std::cout<<"magnitude_parent_a_mass="<<magnitude_parent_a.mass<<'\n';
std::cout<<"magnitude_parent_b_mass="<<magnitude_parent_b.mass<<'\n';
std::cout<<"magnitude_child_a_mass="<<magnitude_a.mass<<'\n';
std::cout<<"magnitude_child_b_mass="<<magnitude_b.mass<<'\n';
std::cout<<"sign_parent_a_mass="<<sign_parent_a.mass<<'\n';
std::cout<<"sign_parent_b_mass="<<sign_parent_b.mass<<'\n';
std::cout<<"sign_child_a_mass="<<sign_a.mass<<'\n';
std::cout<<"sign_child_b_mass="<<sign_b.mass<<'\n';
std::cout.flush();
if(outputs!=40122287||occurrences!=5162||nodes.size()!=7363||zero_nodes!=0
   ||scalar_collision_classes!=28||scalar_mixed_sign_classes!=0
   ||sign_collision_classes!=43||sign_mixed_classes!=20
   ||magnitude_parent_a.mass!=1650||magnitude_parent_b.mass!=1650
   ||magnitude_a.mass!=104||magnitude_b.mass!=605
   ||sign_parent_a.mass!=606||sign_parent_b.mass!=15
   ||sign_a.mass!=-83||sign_b.mass!=2){
    throw std::runtime_error("signed-slice census totals changed");
}
}
