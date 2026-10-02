#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

P16_LEAVES=[
"0000010101000101","0011101111101011","0101101101111011","0001010011100101",
"0101010110111111","0000100100100101","0000001001011001","0010111001100111",
"0001010010001111","0000011101010011","0010101110101101","0101111111011111",
"0000110110000111","0001001111001111","0001111001111111","0010111100111111",
]

def parse_lsb(s:str)->int:
    return sum((1<<i) for i,ch in enumerate(s) if ch=="1")

def parity(x:int)->int:
    return x.bit_count()&1

def broad_child(b:int,c:int,n:int)->int:
    if b==0: raise ValueError("nonzero low plane required")
    mask=(1<<n)-1
    r=b.bit_length()-1
    a0=1^parity(c>>r)
    D=(c^b)&mask
    M=(~b)&mask
    k=1
    while k<n:
        lo=(1<<k)-1
        od,om=D,M
        D=(od^(om&((od<<k)&mask)))&mask
        M=((om&lo)|(om&((om<<k)&mask)&(~lo&mask)))&mask
        k<<=1
    Y=D^(M&(mask if a0 else 0))
    return ((Y<<1)|a0)&mask

def portal_lift(w:int,p:int)->int:
    cur=0;x=0
    for s in range(2*p):
        x|=cur<<s
        cur^=(w>>(s%p))&1
    if cur: raise AssertionError("portal integration failed")
    return x

def quotient_seq(w:int,p:int,r:int)->list[int]:
    n=2*p
    x=portal_lift(w,p)
    J=(1<<n)-1
    low,high=x,J
    dyn=[]
    for _ in range(r):
        ch=broad_child(low,high,n)
        dyn.append(ch)
        high,low=low,ch
    seq=[]
    for s in range(p):
        q=(x>>s)&1
        st=0
        for j,z in enumerate(dyn):
            X=(z>>s)&1
            Y=X^((z>>(s+p))&1)
            if q: X^=Y
            st|=X<<(2*j)
            st|=Y<<(2*j+1)
        seq.append(st)
    return seq

def blind_state(st:int,r:int)->bool:
    H,K,L,M=1,0,0,1
    for j in range(r):
        X=(st>>(2*j))&1
        Y=(st>>(2*j+1))&1
        Yn=K^M^Y^(L&Y)^(M&X)^(M&Y)
        if Yn: return False
        H,K,L,M=L,M,X,Y
    return True

def k_profile(word:str,max_r:int)->list[int]:
    w=parse_lsb(word);p=len(word)
    return [
        sum(blind_state(st,r) for st in quotient_seq(w,p,r))
        for r in range(1,max_r+1)
    ]

def certified_p32_leaves()->list[str]:
    leaves=set()
    files=[
        ROOT/"results/problem1/20261002_period32_portal11_complete.json",
        ROOT/"results/problem1/20261002_twisted_half_period_and_p32_descendants.json",
        ROOT/"results/problem1/20261002_period32_complete_portal_root_census.json",
    ]
    for path in files:
        j=json.loads(path.read_text())
        for e in j.get("edges",[]):
            if e["parity"]=="odd": leaves.add(e["returned_canonical"])
        for e in j.get("descendant_certificates",[]):
            if e["parity"]=="odd": leaves.add(e["returned_canonical"])
        for e in j.get("portal_roots",[]):
            if e["parity"]=="odd": leaves.add(e["canonical_target"])
    return sorted(leaves)

def summarize(words:list[str],max_r:int)->dict:
    profs=[k_profile(w,max_r) for w in words]
    max_k=[max(p[r] for p in profs) for r in range(max_r)]
    first_rank_zero=next((r+1 for r,k in enumerate(max_k) if k<=1),None)
    first_blind_free=next((r+1 for r,k in enumerate(max_k) if k==0),None)
    return {
        "count":len(words),
        "max_k_by_r":max_k,
        "first_depth_all_odd_label_unique":first_rank_zero,
        "first_depth_all_blind_free":first_blind_free,
    }

def main():
    p16=summarize(P16_LEAVES,10)
    p32_words=certified_p32_leaves()
    p32=summarize(p32_words,12)

    # Exact complete ambient p16 comparison.
    ambient=[]
    seen=set()
    p=16;mask=(1<<p)-1
    for w in range(1<<p):
        if parity(w)==0: continue
        rots=[]
        for k in range(p):
            z=((w>>k)|((w<<(p-k))&mask))&mask if k else w
            rots.append(z)
        c=min(rots)
        if c not in seen:
            seen.add(c)
            ambient.append("".join("1" if (c>>i)&1 else "0" for i in range(p)))
    amb=summarize(ambient,10)

    out={
        "p16_terminating_leaves":p16,
        "p16_all_odd_necklaces":amb,
        "certified_p32_terminating_leaves":p32,
    }
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
