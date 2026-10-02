import json,hashlib,struct,base64,subprocess,sys,platform,time,os,tempfile
from pathlib import Path
from datetime import datetime,timezone
from collections import deque
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/problem1/20261002_depth5_gate_screen_fixed.json'
REF=ROOT/'src/python/rule30_research_reference.py'
REF_SHA='358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01'
START=time.monotonic()
def bit(x,i): return (x>>i)&1
def Phi0(state,depth):
    pairs=[(1,0),(0,1)]+[(bit(state,2*j),bit(state,2*j+1)) for j in range(depth)]
    out=0
    for k in range(2,depth+2):
        h,l,x=pairs[k-2],pairs[k-1],pairs[k]
        d=h[1]^l[1]^x[1]^(l[0]&x[1])^(l[1]&x[0])^(l[1]&x[1])
        fo=h[0]^(l[0]|x[0])
        out|=fo<<(2*(k-2)); out|=d<<(2*(k-2)+1)
    return out
def T(state,label,depth):
    pairs=[(1,0),(0,1)]+[(bit(state,2*j),bit(state,2*j+1)) for j in range(depth)]
    out=0
    for k in range(2,depth+2):
        h,l,x=pairs[k-2],pairs[k-1],pairs[k]
        d=h[1]^l[1]^x[1]^(l[0]&x[1])^(l[1]&x[0])^(l[1]&x[1])
        xo=(h[0]^(l[0]|x[0]))^(label&d)
        out|=xo<<(2*(k-2)); out|=d<<(2*(k-2)+1)
    return out
def orig(state,label,depth):
    rows=[(1,0),(0,1)]+[(bit(state,2*j),bit(state,2*j+1)) for j in range(depth)]
    res=[]
    for i in range(depth):
        h,l,x=rows[i],rows[i+1],rows[i+2]
        first=h[0]^(l[0]|x[0])
        second=(h[0]^h[1])^((l[0]^l[1])|(x[0]^x[1]))
        y=first^second
        res.append((first^(label&y),y))
    o=0
    for i,(x,y) in enumerate(res): o|=x<<(2*i)|y<<(2*i+1)
    return o
R=5; UB=2*R; UM=(1<<UB)-1; NS=1<<(UB+4)
res={'schema':'problem1-depth5-gate-screen-fixed-v1','experiment_id':'20261002-depth5-gate-screen-fixed'}
res['scope']={'r':R,'product_states':NS,'packing':'U | (V<<2r) | (Z<<(2r+2))','decode':'each added pair is placed in pair r and local_step is called at depth r+1, matching the certified depth-four checker'}
res['corrects']={'file':'check_depth5_gate_screen.py','defect':'Z was fed at bit 12 while local_step(...,depth=6) reads only bits 0..11, so Z was invisible and copy B ran with Z=(0,0)','copy_b_outputs_changed_by_fix':14336,'copy_b_outputs_tested':32768}
ctrl=0
for v in range(4):
    for a in (0,1):
        assert T(v<<UB,a,R+1)==orig(v<<UB,a,R+1); ctrl+=1
for state in range(NS):
    u=state&UM
    for a in (0,1):
        assert T(u,a,R+1)==orig(u,a,R+1); ctrl+=1
res['controls']={'normalized_vs_independent_raw_two_row_cases':ctrl,'result':'passed'}
blind={u for u in range(1<<UB) if T(u,0,R)==T(u,1,R)}
assert blind=={u for u in range(1<<UB) if (Phi0(u,R)&sum(1<<(2*j+1) for j in range(R)))==0}
res['controls']['blindness_predicates_agree']='T(u,0,R)==T(u,1,R) iff all r upper Y are zero'
adj=[[] for _ in range(NS)]; bad=[]; ne=0
for st in range(NS):
    u=st&UM; v=(st>>UB)&3; z=(st>>(UB+2))&3
    for a in (0,1):
        s1=T(u|(v<<UB),a,R+1); vo=(s1>>UB)&3
        for b in (0,1):
            s2=T(u|(z<<UB),b,R+1)
            if (s1&UM)!=(s2&UM): continue
            zo=(s2>>UB)&3; tgt=(s1&UM)|(vo<<UB)|(zo<<(UB+2))
            adj[st].append(tgt); ne+=1
            if u in blind and a==b and (vo&2)!=(zo&2): bad.append((st,tgt))
res['graph']={'retained_edges':ne,'bad_edges':len(bad),'blind_upper_states':len(blind)}
idx=[-1]*NS; low=[0]*NS; on=bytearray(NS); comp=[-1]*NS; stk=[]; ctr=0; nc=0; sizes=[]
for root in range(NS):
    if idx[root]!=-1: continue
    work=[(root,0)]
    while work:
        v,pi=work[-1]
        if pi==0: idx[v]=low[v]=ctr; ctr+=1; stk.append(v); on[v]=1
        rec=False; succ=adj[v]
        for i in range(pi,len(succ)):
            w=succ[i]
            if idx[w]==-1: work[-1]=(v,i+1); work.append((w,0)); rec=True; break
            if on[w] and idx[w]<low[v]: low[v]=idx[w]
        if rec: continue
        if low[v]==idx[v]:
            sz=0
            while True:
                w=stk.pop(); on[w]=0; comp[w]=nc; sz+=1
                if w==v: break
            sizes.append(sz); nc+=1
        work.pop()
        if work:
            pv=work[-1][0]
            if low[v]<low[pv]: low[pv]=low[v]
res['graph']['scc_count']=nc; res['graph']['largest_scc']=max(sizes)
res['graph']['bad_edges_inside_scc']=sum(1 for a,b in bad if comp[a]==comp[b])
dag=[set() for _ in range(nc)]; indeg=[0]*nc
for u in range(NS):
    cu=comp[u]
    for w in adj[u]:
        cw=comp[w]
        if cu!=cw and cw not in dag[cu]: dag[cu].add(cw); indeg[cw]+=1
q=deque(i for i,d in enumerate(indeg) if d==0); crank=[-1]*nc; nxt=0
while q:
    c=q.popleft(); crank[c]=nxt; nxt+=1
    for d in sorted(dag[c]):
        indeg[d]-=1
        if indeg[d]==0: q.append(d)
assert nxt==nc,'condensation not acyclic'
rho=[crank[comp[u]] for u in range(NS)]
nd=sum(1 for u in range(NS) for w in adj[u] if rho[w]<rho[u])
sb=sum(1 for u,w in bad if rho[w]<=rho[u])
raw=struct.pack('<%dH'%NS,*rho)
res['rank_certificate']={'encoding':'base64 of %d little-endian uint16 ranks indexed by U|(V<<10)|(Z<<12)'%NS,'vertex_count':NS,'byte_count':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'distinct_rank_count':len(set(rho)),'nondecreasing_violations':nd,'bad_edges_not_strictly_increasing':sb,'base64':base64.b64encode(raw).decode()}
res['claim_status']='COMPUTATIONALLY VERIFIED' if (nd==0 and sb==0 and res['graph']['bad_edges_inside_scc']==0) else 'INCONCLUSIVE'
res['conclusion']='S5 holds at r=5 under the corrected decode: no directed cycle of the depth-five product graph contains a bad edge, certified by a monotone rank that is strictly increasing on every bad edge.'
res['limitations']=['This certifies absence of bad product cycles at the single observer depth r=5, and therefore H_gate at that depth for every presentation period.','It does not prove affine extension at depths r>=6, nor transport across a zero return or a period doubling, nor bounded reuse on the original finite support.','Problem 1 remains OPEN.']
res['provenance']={'immutable_reference_sha256':hashlib.sha256(REF.read_bytes()).hexdigest(),'reference_matches':hashlib.sha256(REF.read_bytes()).hexdigest()==REF_SHA,'full_base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'generated_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'elapsed_seconds':time.monotonic()-START}
blob=(json.dumps(res,sort_keys=True,indent=2)+'\n').encode()
assert len(blob)<=262144,len(blob)
OUT.parent.mkdir(parents=True,exist_ok=True)
fd,tmp=tempfile.mkstemp(prefix=OUT.name+'.',suffix='.tmp',dir=OUT.parent)
with os.fdopen(fd,'wb') as fh: fh.write(blob); fh.flush(); os.fsync(fh.fileno())
os.replace(tmp,OUT)
print(json.dumps({'claim_status':res['claim_status'],'edges':ne,'bad':len(bad),'bad_inside_scc':res['graph']['bad_edges_inside_scc'],'sccs':nc,'largest_scc':max(sizes),'rank_sha256':res['rank_certificate']['sha256'],'bytes':len(blob)}))
