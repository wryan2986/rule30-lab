#!/usr/bin/env python3
from __future__ import annotations

LEAVES = [
    "0000010101000101","0011101111101011","0101101101111011",
    "0001010011100101","0101010110111111","0000100100100101",
    "0000001001011001","0010111001100111","0001010010001111",
    "0000011101010011","0010101110101101","0101111111011111",
    "0000110110000111","0001001111001111","0001111001111111",
    "0010111100111111",
]
# 1 = odd/singleton root, 0 = even/branching root.
OUTCOME = [0,0,1,1,0,1,0,1,0,1,0,0,0,1,1,1]

def parity(x:int)->int:
    return x.bit_count() & 1

def parse_lsb(s:str)->int:
    x=0
    for i,ch in enumerate(s):
        if ch=="1":
            x |= 1 << i
    return x

def broad_child(b:int,c:int,n:int)->int:
    if b==0:
        raise ValueError("nonzero low plane required")
    mask=(1<<n)-1
    r=b.bit_length()-1
    a0=1 ^ parity(c>>r)
    D=(c^b)&mask
    M=(~b)&mask
    k=1
    while k<n:
        lo=(1<<k)-1
        od,om=D,M
        D=(od ^ (om & ((od<<k)&mask))) & mask
        M=((om&lo) | (om & ((om<<k)&mask) & (~lo&mask))) & mask
        k <<= 1
    Y=D ^ (M & (mask if a0 else 0))
    return ((Y<<1)|a0) & mask

def portal_lift(w:int,p:int)->int:
    cur=0
    x=0
    for s in range(2*p):
        x |= cur << s
        cur ^= (w>>(s%p)) & 1
    if cur:
        raise AssertionError("odd repeated derivative did not close at 2p")
    return x

def orbit_signature(w:int,p:int,r:int)->tuple[int,...]:
    n=2*p
    x=portal_lift(w,p)
    J=(1<<n)-1
    low,high=x,J
    dynamic=[]
    for _ in range(r):
        ch=broad_child(low,high,n)
        dynamic.append(ch)
        high,low=low,ch

    seq=[]
    for s in range(p):
        q=(x>>s)&1
        state=0
        for j,z in enumerate(dynamic):
            X=(z>>s)&1
            X2=(z>>(s+p))&1
            Y=X^X2
            if q:
                X ^= Y
            state |= X << (2*j)
            state |= Y << (2*j+1)
        seq.append(state)

    return min(tuple(seq[k:]+seq[:k]) for k in range(p))

def gf2_affine_state_visit_test(signatures:list[tuple[int,...]])->dict:
    states=sorted({s for sig in signatures for s in sig})
    # columns: constant, then parity of visit count to each observed state.
    rows=[]
    for sig in signatures:
        row=1
        for i,state in enumerate(states,1):
            if sum(v==state for v in sig)&1:
                row |= 1<<i
        rows.append(row)

    piv={}
    inconsistent=False
    for row,rhs in zip(rows,OUTCOME,strict=True):
        x=row
        y=rhs
        while x:
            p=x.bit_length()-1
            if p in piv:
                br,by=piv[p]
                x ^= br
                y ^= by
            else:
                piv[p]=(x,y)
                break
        if x==0 and y:
            inconsistent=True
            break
    return {
        "observed_states":len(states),
        "rank_before_inconsistency":len(piv),
        "affine_classifier_exists":not inconsistent,
    }

def main()->None:
    words=[parse_lsb(s) for s in LEAVES]
    summaries=[]
    sigs_r4=None
    for r in range(1,9):
        groups={}
        sigs=[]
        for portal,(w,out) in enumerate(zip(words,OUTCOME,strict=True)):
            sig=orbit_signature(w,16,r)
            sigs.append(sig)
            groups.setdefault(sig,[]).append((portal,out))
        mixed=[
            [(portal,"odd" if out else "even") for portal,out in group]
            for group in groups.values()
            if len({out for _,out in group})>1
        ]
        summaries.append((r,len(groups),mixed))
        if r==4:
            sigs_r4=sigs

    expected=[(1,15,1),(2,15,1),(3,15,1),(4,16,0),
              (5,16,0),(6,16,0),(7,16,0),(8,16,0)]
    got=[(r,n,len(mixed)) for r,n,mixed in summaries]
    if got != expected:
        raise AssertionError((got,expected))

    for r,n,mixed in summaries:
        print(f"r={r} distinct_unlabeled_orbits={n} mixed_parity_classes={len(mixed)}")
        for group in mixed:
            print("  mixed",group)

    if summaries[0][2] != [[(5,"odd"),(6,"even")]]:
        raise AssertionError("unexpected r=1 collision")
    if summaries[1][2] != [[(5,"odd"),(6,"even")]]:
        raise AssertionError("unexpected r=2 collision")
    if summaries[2][2] != [[(5,"odd"),(6,"even")]]:
        raise AssertionError("unexpected r=3 collision")

    affine=gf2_affine_state_visit_test(sigs_r4)
    print("r4_state_visit_affine_test",affine)
    if affine["affine_classifier_exists"]:
        raise AssertionError("unexpected affine state-visit classifier")

if __name__=="__main__":
    main()
