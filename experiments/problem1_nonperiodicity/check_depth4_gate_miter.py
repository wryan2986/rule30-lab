#!/usr/bin/env python3
"""Exact depth-four blind-output gate miter on its 32,768 vertex lift."""
from __future__ import annotations

import hashlib, importlib.util, json, os, platform, resource, subprocess, sys, tempfile, time
import base64, struct
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results/problem1/20261002_depth4_gate_miter.json"
ANALYZER = ROOT / "experiments/problem1_nonperiodicity/analyze_blind_visit_rank.py"
REFERENCE = ROOT / "src/python/rule30_research_reference.py"
ADMISSION = ROOT / "proofs/informal/problem1_depth4_gate_miter_admission.md"
CRITERION = ROOT / "proofs/informal/problem1_blind_output_gate_criterion.md"
WALL_CAP, MEMORY_CAP, OUTPUT_CAP = 60.0, 256 * 1024 * 1024, 256 * 1024
START = time.monotonic()
NSTATE, NSHEET, NVERT = 4096, 8, 32768

def sha(b): return hashlib.sha256(b).hexdigest()
def parity(x): return x.bit_count() & 1
def bit(x, i): return (x >> i) & 1

def caps():
    if time.monotonic() - START > WALL_CAP: raise TimeoutError("60-second cap")
    rss = int(next(x.split()[1] for x in Path('/proc/self/status').read_text().splitlines() if x.startswith('VmRSS:'))) * 1024
    if rss > MEMORY_CAP: raise MemoryError("256-MiB resident cap")

def peak_rss():
    return int(next(x.split()[1] for x in Path('/proc/self/status').read_text().splitlines() if x.startswith('VmHWM:'))) * 1024

def atomic_json(obj):
    raw = (json.dumps(obj, sort_keys=True, indent=2) + '\n').encode()
    if len(raw) > OUTPUT_CAP: raise ValueError("256-KiB result cap")
    fd, tmp = tempfile.mkstemp(prefix=OUT.name+'.', suffix='.tmp', dir=OUT.parent)
    try:
        with os.fdopen(fd, 'wb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, OUT)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def local_step(state, label, depth=5):
    """Polynomial quotient transition, independent of the raw two-row control."""
    pairs = [(1,0),(0,1)] + [(bit(state,2*j),bit(state,2*j+1)) for j in range(depth)]
    out = 0
    for j in range(2,depth+2):
        h,l,x = pairs[j-2:j+1]
        first = h[0] ^ l[0] ^ x[0] ^ (l[0] & x[0])
        d = h[1] ^ l[1] ^ x[1] ^ (l[0] & x[1]) ^ (l[1] & x[0]) ^ (l[1] & x[1])
        out |= (first ^ (label & d)) << (2*(j-2))
        out |= d << (2*(j-2)+1)
    return out

def original_step(state, label):
    """Separately written original two-row bit-array recurrence."""
    rows = [(1,0),(0,1)]
    rows.extend((bit(state,2*j),bit(state,2*j+1)) for j in range(5))
    result=[]
    for i in range(5):
        h,l,x=rows[i:i+3]
        first=h[0] ^ (l[0] | x[0])
        second=(h[0]^h[1]) ^ ((l[0]^l[1]) | (x[0]^x[1]))
        Y=first^second
        result.append((first ^ (label & Y),Y))
    value=0
    for i,(x,y) in enumerate(result): value |= x<<(2*i) | y<<(2*i+1)
    return value

def upper_blind(u):
    return local_step(u,0,4)==local_step(u,1,4)

def edge_data(state, a, b):
    sa=(state&255) | (((state>>8)&3)<<8)
    sb=(state&255) | (((state>>10)&3)<<8)
    aa,bb=local_step(sa,a),local_step(sb,b)
    if (aa & 255) != (bb & 255): return None
    return aa,bb,bit(aa,9),bit(bb,9)

def raw_scalar_child(low, high, n):
    # Direct seed search for x_(s+1)=high_s XOR (low_s OR x_s).
    sols=[]
    for seed in (0,1):
        x=seed; word=0
        for s in range(n):
            word |= x<<s
            x=bit(high,s) ^ (bit(low,s)|x)
        if x==seed: sols.append(word)
    if len(sols)!=1: raise ValueError(("cyclic child is not unique",low,high,sols))
    return sols[0]

def scalar_stack(word, p, depth):
    n=2*p; q=x=0
    for s in range(n): x |= q<<s; q ^= bit(word,s%p)
    if q: raise AssertionError("odd driver did not integrate on 2p")
    low,high=x,(1<<n)-1; layers=[]
    for _ in range(depth):
        child=raw_scalar_child(low,high,n); layers.append(child); high,low=low,child
    states=[]; q=0
    for s in range(p):
        st=0
        for j,z in enumerate(layers):
            X=bit(z,s); Y=X^bit(z,s+p)
            if q: X ^= Y
            st |= X<<(2*j) | Y<<(2*j+1)
        states.append(st); q ^= bit(word,s)
    if q!=1: raise AssertionError("normalized row carry mismatch")
    return states,layers

def load_analyzer():
    spec=importlib.util.spec_from_file_location('depth4_analyzer',ANALYZER)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def analyzer_word(word,p,r,an):
    # The existing analyzer's quotient_seq uses its packed broad-child path.
    return list(an.quotient_seq(word,p,r+1))

def nonzero_parent(states):
    return all(any((st>>(2*j))&3 for st in states) for j in range(4))

def tarjan_iterative(adj, rev):
    seen=bytearray(NVERT); order=[]
    for root in range(NVERT):
        if seen[root]: continue
        seen[root]=1; stack=[(root,0)]
        while stack:
            v,k=stack[-1]
            if k < len(adj[v]):
                w=adj[v][k][0]; stack[-1]=(v,k+1)
                if not seen[w]: seen[w]=1; stack.append((w,0))
            else: order.append(v); stack.pop()
    comp=[-1]*NVERT; sizes=[]; cid=0
    for root in reversed(order):
        if comp[root]>=0: continue
        comp[root]=cid; stack=[root]; size=0
        while stack:
            v=stack.pop(); size+=1
            for w in rev[v]:
                if comp[w]<0: comp[w]=cid; stack.append(w)
        sizes.append(size); cid+=1
    return comp,sizes

def bfs(adj, comp, cid, start, goal, accept_nonzero):
    # Return path vertices and labels; optionally force passage through a nonzero-parent vertex.
    initial=(start,bool((start&4095)&0xC0)); q=deque([initial]); prev={initial:None}; pedge={}
    final=None
    while q:
        v,hit=q.popleft()
        if v==goal and (hit or not accept_nonzero): final=(v,hit); break
        for w,label in adj[v]:
            if comp[w]!=cid: continue
            nh=hit or bool((w&4095)&0xC0)
            key=(w,nh)
            if key not in prev: prev[key]=(v,hit); pedge[key]=label; q.append(key)
    if final is None:return None
    labels=[]; vertices=[]; cur=final
    while cur is not None:
        vertices.append(cur[0]); pr=prev[cur]
        if pr is not None: labels.append(pedge[cur])
        cur=pr
    return list(reversed(vertices)),list(reversed(labels))

def main():
    caps(); source=Path(__file__).read_bytes(); analyzer_bytes=ANALYZER.read_bytes(); admission=ADMISSION.read_bytes(); criterion=CRITERION.read_bytes(); ref=REFERENCE.read_bytes()
    if sha(ref) != '358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01':
        raise AssertionError('immutable reference hash differs')
    analyzer=load_analyzer()
    # Exhaustive 4096 x 4 local-transition control.
    transition_control=0
    for state in range(NSTATE):
        state_a = (state & 255) | (((state >> 8) & 3) << 8)
        state_b = (state & 255) | (((state >> 10) & 3) << 8)
        for a in range(2):
            for b in range(2):
                if local_step(state_a,a)!=original_step(state_a,a) or local_step(state_b,b)!=original_step(state_b,b): raise AssertionError((state,a,b))
                transition_control+=1
    adj=[[] for _ in range(NVERT)]; rev=[[] for _ in range(NVERT)]; bad=[]; edge_count=0
    for sheet in range(8):
        for st in range(NSTATE):
            u=(sheet<<12)|st
            for a in range(2):
                for b in range(2):
                    dat=edge_data(st,a,b)
                    if dat is None: continue
                    aa,bb,ya,yb=dat; nh=sheet ^ a ^ (b<<1) ^ 4
                    nxt=(aa&255) | (((aa>>8)&3)<<8) | (((bb>>8)&3)<<10)
                    v=(nh<<12)|nxt
                    adj[u].append((v,(a,b))); rev[v].append(u); edge_count+=1
                    if (upper_blind(st&255) and a==b and ya!=yb): bad.append((u,v,(a,b),ya,yb))
            if st % 512==0: caps()
    comp,sizes=tarjan_iterative(adj,rev); caps()
    witness=None
    # Search order is integer source vertex, then lexicographic labels (a,b).
    nonzero_vertices={v for v in range(NVERT) if (v&4095)&0xC0}
    for u,v,lab,ya,yb in bad:
        if (u>>12)!=0: continue
        cid=comp[u]
        if comp[v]!=cid: continue
        goal=(u&~(7<<12)) | (( (u>>12)^3 )<<12) # sheet xor (1,1,0) = 3
        # Find v -> goal through a vertex whose last upper pair is nonzero.
        # Use layered BFS and explicit actual predecessor path.
        path=bfs(adj,comp,cid,v,goal,True)
        if path is None: continue
        vertices,labels=path
        # Fix the start's nonzero marker too, and assemble the bad edge plus return path.
        edges=[lab]+labels
        states=[u&4095]+[x&4095 for x in vertices[:-1]]
        labels_a=[x[0] for x in edges]; labels_b=[x[1] for x in edges]; p=len(edges)
        if p%2 or parity(sum(x<<i for i,x in enumerate(labels_a)))!=1 or parity(sum(x<<i for i,x in enumerate(labels_b)))!=1: continue
        witness=(u,v,lab,ya,yb,edges,states,p); break
    result={"schema":"problem1-depth4-gate-miter-v1","experiment_id":"20261002-depth4-gate-miter","status":"finite_graph_unverified","claim_status":"FINITE_EXPERIMENT","scope":{"r":4,"product_states":4096,"parity_sheets":8,"vertices":NVERT,"labels_per_vertex":4,"retained_edges":edge_count,"upper_output_equality_required":True,"target_sheet_xor":{"driver_a":1,"driver_b":1,"time":0},"fixed_boundary_pairs":[[1,0],[0,1]]},"caps":{"wall_seconds":60,"resident_bytes":268435456,"output_bytes":262144,"peak_resident_bytes":peak_rss()},"graph":{"scc_count":len(sizes),"largest_scc":max(sizes,default=0),"scc_size_histogram":{str(k):sizes.count(k) for k in sorted(set(sizes))},"vertex_order":"lifted vertex integer 0..32767, encoded (sheet<<12)|state; label-pair order lexicographic (a,b)"},"controls":{"local_polynomial_vs_original_two_row_all_4096_by_4":"passed","local_transition_label_pair_cases":transition_control,"existing_analyzer_and_independent_two_seed_scalar":"pending witness-dependent"},"witness":None,"limitations":["No exhaustive period enumeration.","A graph absence is only an unchecked finite graph result, not an all-period theorem.","No claim about transport through zero returns or the original finite-support prize instance."],"provenance":{"source_sha256":{},"full_base_commit":subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),"immutable_reference_sha256":sha(ref),"generated_utc":datetime.now(timezone.utc).isoformat(),"python":sys.version,"platform":platform.platform(),"cpu_model":next((ln.split(':',1)[1].strip() for ln in Path('/proc/cpuinfo').read_text().splitlines() if ln.lower().startswith('model name')),platform.processor()),"elapsed_seconds":time.monotonic()-START}}
    result['provenance']['source_sha256']={"checker":sha(source),"analyzer":sha(analyzer_bytes),"admission":sha(admission),"criterion":sha(criterion),"immutable_reference":sha(ref)}
    if witness:
        u,v,lab,ya,yb,edges,states,p=witness
        wa=sum(x[0]<<i for i,x in enumerate(edges)); wz=sum(x[1]<<i for i,x in enumerate(edges))
        # Canonical upper-blind phases are selected directly from common cycle states.
        blind=[i for i,st in enumerate(states) if upper_blind(st&255)]
        s=0; t=next((i for i in blind if i!=s),None)
        if t is None: raise AssertionError("no second upper-blind phase for square")
        words=[wa,wz,wa^(1<<s)^(1<<t),wz^(1<<s)^(1<<t)]
        if len(set(words)) != 4 or any(parity(word) != 1 for word in words):
            raise AssertionError('square must have four distinct odd members')
        replays=[]
        for wi,word in enumerate(words):
            ss,layers=scalar_stack(word,p,5)
            if ss!=analyzer_word(word,p,4,analyzer): raise AssertionError("analyzer/scalar canonical stack mismatch")
            if not nonzero_parent(ss): raise AssertionError("zero raw upper parent in replay")
            if any(original_step(ss[i],bit(word,i))!=ss[(i+1)%p] for i in range(p)):
                raise AssertionError("original two-row phase replay mismatch")
            if any(((ss[i]&255)!=states[i]&255) for i in range(p)):
                raise AssertionError("scalar replay does not reproduce common upper cycle")
            if wi==0 and any(((ss[i]>>8)&3)!=((states[i]>>8)&3) for i in range(p)):
                raise AssertionError("first canonical scalar replay misses product driver-A track")
            if wi==1 and any(((ss[i]>>8)&3)!=((states[i]>>10)&3) for i in range(p)):
                raise AssertionError("second canonical scalar replay misses product driver-B track")
            replays.append({"word_lsb_first":"".join(str(bit(word,i)) for i in range(p)),"word_integer":word,"all_upper_states_match_base":[x&255 for x in ss]==[x&255 for x in scalar_stack(wa,p,5)[0]],"all_upper_blind_phases":[i for i,x in enumerate(ss) if upper_blind(x&255)],"analyzer_match":True,"original_two_row_phase_replay":"passed","full_stack_sha256":sha(json.dumps(ss,separators=(',',':')).encode())})
        seqs=[scalar_stack(word,p,5)[0] for word in words]
        xor_words=[a ^ b ^ c ^ d for a,b,c,d in zip(*seqs)]
        square_nonzero=any(xor_words)
        if not square_nonzero: raise AssertionError("four-word full extension square is affine")
        result['status']='counterexample_found'; result['claim_status']='COUNTEREXAMPLE'; result['controls']['existing_analyzer_and_independent_two_seed_scalar']='passed for all four square words'
        result['witness']={"period":p,"bad_phase":s,"second_blind_phase":t,"bad_edge":{"source_state":u&4095,"destination_state":v&4095,"labels":list(lab),"new_Y_outputs":[ya,yb]},"drivers_and_square":replays,"parity_each_driver":"odd","cycle_length":"even","common_upper_orbit":True,"full_extension_square_xor_nonzero":True,"full_extension_xor_sha256":sha(json.dumps(xor_words,separators=(',',':')).encode()),"bad_edge_return_path_vertex_count":len(states),"graph_cycle_states_sha256":sha(json.dumps(states,separators=(',',':')).encode())}
    elif bad:
        result['controls']['existing_analyzer_and_independent_two_seed_scalar']='not applicable; no recovered counterexample'
        result['graph']['bad_edge_count']=len(bad)
        result['graph']['bad_edges_in_cyclic_scc']=sum(comp[u]==comp[v] for u,v,*_ in bad)
    else:
        result['graph']['bad_edge_count']=0
        result['controls']['existing_analyzer_and_independent_two_seed_scalar']='not applicable; no bad edge'
    if not witness:
        # Topologically rank the SCC condensation. Every original edge must be nondecreasing.
        dag=[set() for _ in sizes]; indeg=[0]*len(sizes)
        for u in range(NVERT):
            cu=comp[u]
            for v,_ in adj[u]:
                cv=comp[v]
                if cu!=cv and cv not in dag[cu]: dag[cu].add(cv); indeg[cv]+=1
        q=deque(i for i,d in enumerate(indeg) if d==0); ranks=[-1]*len(sizes); nxt_rank=0
        while q:
            c=q.popleft(); ranks[c]=nxt_rank; nxt_rank+=1
            for d in sorted(dag[c]):
                indeg[d]-=1
                if indeg[d]==0:q.append(d)
        if nxt_rank!=len(sizes): raise AssertionError("SCC condensation is not acyclic")
        rank_array=bytearray()
        for v in range(NVERT): rank_array.extend(struct.pack('<H',ranks[comp[v]]))
        if any(ranks[comp[v]]<ranks[comp[u]] for u in range(NVERT) for v,_ in adj[u]):
            raise AssertionError("topological rank decreases along edge")
        group_flags=[0]*nxt_rank
        for v in range(NVERT):
            st=v&4095; sheet=v>>12; rank=ranks[comp[v]]
            if sheet==0 and any((source==v and rank==ranks[comp[target]]) for source,target,*_ in bad): group_flags[rank]|=1
            if sheet==0 and ranks[comp[v]]==ranks[comp[(v&4095)|(3<<12)]]: group_flags[rank]|=2
            if st&0xC0: group_flags[rank]|=4
        result['scc_rank_certificate']={"encoding":"base64 of 32768 little-endian uint16 ranks, indexed by lifted vertex integer (sheet<<12)|state","vertex_count":NVERT,"integer_width_bits":16,"byte_count":len(rank_array),"sha256":sha(bytes(rank_array)),"base64":base64.b64encode(rank_array).decode(),"distinct_rank_count":nxt_rank,"edge_monotonicity":"checked on every retained directed edge","group_exclusion_checks":{"rank_groups_with_sheet0_internal_bad_edge":sum(bool(x&1) for x in group_flags),"rank_groups_with_same_state_sheet0_and_sheet3":sum(bool(x&2) for x in group_flags),"rank_groups_with_nonzero_last_upper_pair":sum(bool(x&4) for x in group_flags),"rank_groups_satisfying_all_three_cycle_necessities":sum(x==7 for x in group_flags),"exclusion_condition":"each rank group fails at least one necessary condition for a lifted counterexample cycle"}}
    result['provenance']['elapsed_seconds']=time.monotonic()-START; result['caps']['peak_resident_bytes']=peak_rss()
    result['implementation_diagnostics'] = [
        'Superseded control decoded the first added pair for both copies; final control decodes each copy separately and compares polynomial with raw two-row transitions.',
        'Unused witness draft checked pairwise output differences instead of the four-output XOR and tested parent nonzero per phase instead of per layer; both corrected. These were implementation bugs, not mathematical counterexamples.'
    ]
    result['result_hashes'] = {'canonical_payload_sha256_excluding_result_hashes': sha(json.dumps(result,sort_keys=True,separators=(',',':')).encode())}
    atomic_json(result)
    print(json.dumps({"status":result['status'],"vertices":NVERT,"edges":edge_count,"scc_count":len(sizes),"witness":bool(witness),"elapsed_seconds":result['provenance']['elapsed_seconds'],"output":str(OUT)}))

if __name__=='__main__': main()
