#!/usr/bin/env python3
from __future__ import annotations

def parity(x:int)->int:return x.bit_count()&1

def child(b:int,c:int,n:int)->int:
    if b==0: raise ValueError("nonzero low plane required")
    r=b.bit_length()-1
    a0=1^parity(c>>r)
    a=a0;out=0
    for s in range(n):
        out|=a<<s
        a=((c>>s)&1)^(((b>>s)&1)|a)
    assert a==a0
    return out

def portal_lift(w:int,p:int)->int:
    cur=0;x=0
    for s in range(2*p):
        x|=cur<<s
        cur^=(w>>(s%p))&1
    assert cur==0
    return x

def half_pairs(z:int,p:int):
    return [((z>>s)&1,(z>>(s+p))&1) for s in range(p)]

def verify_twisted_child(b:int,c:int,p:int):
    n=2*p
    a=child(b,c,n)
    A=half_pairs(a,p);B=half_pairs(b,p);C=half_pairs(c,p)
    for s in range(p):
        nxt=A[s+1] if s+1<p else (A[0][1],A[0][0])
        rhs=(C[s][0]^(B[s][0]|A[s][0]),
             C[s][1]^(B[s][1]|A[s][1]))
        assert nxt==rhs

def main():
    checks=0
    for p in range(1,5):
        n=2*p
        for b in range(1,1<<n):
            for c in range(1<<n):
                verify_twisted_child(b,c,p)
                checks+=1
    print("twisted_child_exhaustive_checks",checks)

    portal_checks=0
    for p in range(1,11):
        n=2*p;J=(1<<n)-1
        for w in range(1<<p):
            if parity(w)==0: continue
            x=portal_lift(w,p)
            u=child(x,J,n)
            X=half_pairs(x,p);U=half_pairs(u,p)
            q=[a for a,b in X]
            assert all(b==(1-a) for a,b in X)
            assert all(pair!=(1,1) for pair in U)
            first=[a for a,b in U]
            diff=[a^b for a,b in U]
            for s in range(p):
                if s+1<p:
                    un=first[s+1];dn=diff[s+1]
                else:
                    un=first[0]^diff[0]
                    dn=diff[0]
                assert un==(1^(q[s]|first[s]))
                assert dn==(1^first[s]^(q[s]&diff[s]))
            portal_checks+=1
    print("portal_odd_words_checked",portal_checks)
    print("third_lift_pair_11_occurrences",0)
    print("q0_transition","(U,D)->(1^U,1^U)")
    print("q1_transition","(U,D)->(0,1^U^D)")
    print("composition_01","constant (0,1)")
    print("composition_10","constant (1,1)")

if __name__=="__main__":
    main()
