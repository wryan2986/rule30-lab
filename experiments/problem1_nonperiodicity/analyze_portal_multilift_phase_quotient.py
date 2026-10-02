#!/usr/bin/env python3
"""
Exact multilift half-period quotient checks for Rule-30 Problem 1.

The normalized r-layer stack has 2r bits.  Its transition is driven directly
by the old odd leaf bit w_s, not by the antiperiodic prefix bit q_s.

Use --max-r 8 to reproduce the exact even-length/odd-weight sector counts
recorded in results/problem1/20261002_portal_multilift_phase_quotient.json.
"""
from __future__ import annotations
import argparse
from itertools import product
from collections import defaultdict, deque

def phi_q(state: tuple[int,...], q: int) -> tuple[int,...]:
    # Base paired layers: all-one high plane J=(1,0), antiperiodic x=(q,1).
    pairs=[(1,0),(q,1)] + [tuple(state[i:i+2]) for i in range(0,len(state),2)]
    out=[]
    for j in range(2,len(pairs)):
        H,K=pairs[j-2]
        L,M=pairs[j-1]
        X,Y=pairs[j]
        out.extend((
            H ^ (L | X),
            K ^ M ^ Y ^ (L & Y) ^ (M & X) ^ (M & Y),
        ))
    return tuple(out)

def half_swap(state: tuple[int,...]) -> tuple[int,...]:
    out=[]
    for i in range(0,len(state),2):
        X,Y=state[i],state[i+1]
        out.extend((X ^ Y,Y))
    return tuple(out)

def transition(state: tuple[int,...], w: int) -> tuple[int,...]:
    z=phi_q(state,0)
    return half_swap(z) if w else z

def scc_ids(adj,radj):
    n=len(adj)
    seen=[False]*n
    order=[]
    for start in range(n):
        if seen[start]:
            continue
        stack=[(start,0)]
        seen[start]=True
        while stack:
            v,i=stack[-1]
            if i < len(adj[v]):
                u=adj[v][i]
                stack[-1]=(v,i+1)
                if not seen[u]:
                    seen[u]=True
                    stack.append((u,0))
            else:
                order.append(v)
                stack.pop()
    comp=[-1]*n
    cid=0
    for start in reversed(order):
        if comp[start] != -1:
            continue
        comp[start]=cid
        stack=[start]
        while stack:
            v=stack.pop()
            for u in radj[v]:
                if comp[u] == -1:
                    comp[u]=cid
                    stack.append(u)
        cid += 1
    return comp

def exact_even_odd_sector(r: int) -> list[tuple[int,...]]:
    """
    States lying on a closed driver walk of even length and odd Hamming weight.

    Product graph tracks (driver-weight parity, length parity).  State s is
    admissible iff (s,0,0) and (s,1,0) are in the same SCC.
    """
    states=list(product((0,1),repeat=2*r))
    index={s:i for i,s in enumerate(states)}
    n=len(states)*4
    adj=[[] for _ in range(n)]
    radj=[[] for _ in range(n)]
    def node(i,a,l):
        return i*4+a*2+l
    nexts=[(index[transition(s,0)],index[transition(s,1)]) for s in states]
    for i in range(len(states)):
        for a in (0,1):
            for l in (0,1):
                v=node(i,a,l)
                for b in (0,1):
                    u=node(nexts[i][b],a^b,l^1)
                    adj[v].append(u)
                    radj[u].append(v)
    comp=scc_ids(adj,radj)
    return [
        s for i,s in enumerate(states)
        if comp[node(i,0,0)] == comp[node(i,1,0)]
    ]

def cyclic_path(word: str, r: int, candidates=None):
    states = candidates if candidates is not None else product((0,1),repeat=2*r)
    solutions=[]
    bits=[int(c) for c in word]
    for s0 in states:
        s=s0
        path=[]
        for b in bits:
            path.append(s)
            s=transition(s,b)
        if s == s0:
            solutions.append(path)
    if len(solutions) != 1:
        raise AssertionError((word,r,len(solutions)))
    return solutions[0]

def canonical_path(path):
    return min(tuple(path[k:]+path[:k]) for k in range(len(path)))

def canonical_word(word: str) -> str:
    return min(word[k:]+word[:k] for k in range(len(word)))

def encode(state):
    return sum(bit<<i for i,bit in enumerate(state))

FIVE_STATES={
    "A":(0,0,1,0),
    "B":(0,1,0,0),
    "C":(0,1,0,1),
    "D":(1,1,0,0),
    "E":(1,1,1,1),
}

OBSERVER_COLLISIONS={
    4:("1001110011100101","1001110111101101"),
    5:("111000011100100101","111010011101100101"),
    6:("00111000011101101101","00111010011100101101"),
    7:("010011100101111010100101","010011101101111000100101"),
    8:("01011011110000111000100101","01011011110100111010100101"),
}

def verify_five_state():
    inv={v:k for k,v in FIVE_STATES.items()}
    expected={
        "A":{0:"E",1:"C"},
        "B":{0:"D",1:"B"},
        "C":{0:"D",1:"B"},
        "D":{0:"A",1:"A"},
        "E":{0:"A",1:"A"},
    }
    for name,s in FIVE_STATES.items():
        for b in (0,1):
            assert inv[transition(s,b)] == expected[name][b]

    sync={
        "100":"A",
        "101":"A",
        "110":"D",
        "111":"B",
    }
    for word,target in sync.items():
        images=set()
        for s in FIVE_STATES.values():
            t=s
            for c in word:
                t=transition(t,int(c))
            images.add(t)
        assert images == {FIVE_STATES[target]}

    # Coboundary: D xor E = 1 xor g(s) xor g(s+).
    g={"A":0,"B":0,"C":1,"D":0,"E":1}
    for name,s in FIVE_STATES.items():
        h=s[1]^s[3]
        for b in (0,1):
            nxt=inv[transition(s,b)]
            assert h == (1 ^ g[name] ^ g[nxt])

def verify_portal_5_6_collision():
    leaves={
        5:"0000100100100101",
        6:"0000001001011001",
    }
    expected_labels={
        5:"1001001010000100",
        6:"1011001000000100",
    }
    expected_sig=[4,26,51,4,26,51,4,26,51,4,31,36,31,36,26,51]
    signatures={}
    for idx,word in leaves.items():
        path=cyclic_path(word,3)
        rotations=[
            (tuple(path[k:]+path[:k]),k)
            for k in range(len(path))
        ]
        can,k=min(rotations)
        labels=word[k:]+word[:k]
        code=[encode(s) for s in can]
        assert code == expected_sig
        assert labels == expected_labels[idx]
        signatures[idx]=tuple(can)
    assert signatures[5] == signatures[6]

    blind=(1,1,0,0,1,1)
    assert transition(blind,0) == transition(blind,1)

def verify_observer_collisions():
    for r,(a,b) in OBSERVER_COLLISIONS.items():
        assert len(a)%2 == 0 and len(b)==len(a)
        assert sum(map(int,a))%2 == 1
        assert sum(map(int,b))%2 == 1
        assert canonical_word(a) != canonical_word(b)
        pa=canonical_path(cyclic_path(a,r))
        pb=canonical_path(cyclic_path(b,r))
        assert pa == pb

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--max-r",type=int,default=6)
    args=ap.parse_args()

    verify_five_state()
    verify_portal_5_6_collision()
    verify_observer_collisions()

    sizes={}
    for r in range(1,args.max_r+1):
        sec=exact_even_odd_sector(r)
        sizes[r]=len(sec)
        print(f"r={r} exact_even_length_odd_weight_sector={len(sec)}")

    expected={1:3,2:5,3:14,4:30,5:75,6:195,7:443,8:1168}
    for r,n in sizes.items():
        assert n == expected[r]

    r3=exact_even_odd_sector(3)
    blind=[s for s in r3 if transition(s,0)==transition(s,1)]
    assert sorted(blind)==[
        (1,1,0,0,0,1),
        (1,1,0,0,1,1),
    ]
    print("r3_blind_states",blind)
    print("portal5_portal6_common_r3_signature",
          [4,26,51,4,26,51,4,26,51,4,31,36,31,36,26,51])
    print("observer_collisions_verified",len(OBSERVER_COLLISIONS))

if __name__=="__main__":
    main()
