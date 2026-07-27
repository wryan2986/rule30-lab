#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter
from typing import Any

PHASES=("p","u")
CHILD_MASK={0:0b1011,1:0b1100,2:0b1110,3:0b0011}
ALLOWED_FIBERS=(0b0000,0b0011,0b1011,0b1100,0b1111)
DEFAULT_MAXIMUM_COMPLEXITY=16
ABSOLUTE_MAXIMUM_COMPLEXITY=20

class CampaignLimitError(RuntimeError): pass

def forward_generator(name:str,state:int)->int:
    stepped=state^((state<<1)|(state<<2))
    if name=='t': return stepped
    if name=='u': return stepped^1
    if name=='p': return stepped^1^(2 if state&1==0 else 0)
    raise ValueError(name)

def frontier_children(state:int)->tuple[int,...]:
    return tuple(sorted({forward_generator(g,state) for g in 'tup'}))

def phase_start(phase:str)->int:
    if phase=='p': return 3
    if phase=='u': return 1
    raise ValueError(phase)

def build_levels(phase:str,maximum_complexity:int)->list[set[int]]:
    levels=[set(),{phase_start(phase)}]
    for _ in range(2,maximum_complexity+1):
        levels.append({c for s in levels[-1] for c in frontier_children(s)})
    return levels

def inverse_t(output:int)->int|None:
    if output<0: raise ValueError
    if output==0:return 0
    width=output.bit_length()-2
    if width<=0:return None
    state=0
    for position in range(width):
        lower=0
        if position>=1: lower|=(state>>(position-1))&1
        if position>=2: lower|=(state>>(position-2))&1
        state|=((((output>>position)&1)^lower)<<position)
    return state if forward_generator('t',state)==output else None

def inverse_generator(name:str,output:int)->int|None:
    if name=='t': state=inverse_t(output)
    elif name=='u': state=inverse_t(output^1)
    elif name=='p':
        recovered_low=(output&1)^1
        state=inverse_t(output^1^(2 if recovered_low==0 else 0))
    else: raise ValueError(name)
    return state if state is not None and forward_generator(name,state)==output else None

def candidate_parent(quotient:int,parent_digit:int)->int|None:
    generator='t' if parent_digit==0 else 'u' if parent_digit==1 else 'p'
    residual=inverse_generator(generator,quotient)
    return None if residual is None else 4*residual+parent_digit

def predecessor_mask(levels:list[set[int]],complexity:int,quotient:int)->int:
    current=levels[complexity]
    mask=0
    for digit in range(4):
        parent=candidate_parent(quotient,digit)
        if parent is not None and parent in current: mask|=1<<digit
    if mask&0b0100 and not mask&0b1000:
        raise AssertionError('digit-2 predecessor lacked digit-3 mate')
    return mask

def fiber_from_predecessor(mask:int)->int:
    result=0
    for digit in range(4):
        if mask>>digit&1: result|=CHILD_MASK[digit]
    if result not in ALLOWED_FIBERS: raise AssertionError('bad fiber')
    return result

def fiber_mask(levels:list[set[int]],complexity:int,quotient:int)->int:
    nxt=levels[complexity+1]
    actual=sum(1<<d for d in range(4) if 4*quotient+d in nxt)
    pred=predecessor_mask(levels,complexity,quotient)
    expected=fiber_from_predecessor(pred)
    if actual!=expected: raise AssertionError('lift formula mismatch')
    return actual

def signature(levels:list[set[int]],complexity:int,state:int)->tuple[int,int]:
    pred=predecessor_mask(levels,complexity,state)
    return pred,fiber_from_predecessor(pred)

def universal_signature_table()->list[tuple[int,int]]:
    rows=[]
    for pred in range(16):
        if pred&0b0100 and not pred&0b1000: continue
        rows.append((pred,fiber_from_predecessor(pred)))
    if len(rows)!=12: raise AssertionError
    return rows

def closure_counterexample()->dict[str,Any]:
    levels=build_levels('p',7)
    def row(kq,q,kp,p):
        current=(fiber_mask(levels,kq,q),fiber_mask(levels,kp,p))
        digit=q&3
        if p&3!=digit: raise AssertionError
        lower=(fiber_mask(levels,kq-1,q>>2),fiber_mask(levels,kp-1,p>>2))
        return {'current_level':kq,'current':q,'shadow_level':kp,'shadow':p,
                'current_hex':hex(q),'shadow_hex':hex(p),'shared_digit':digit,
                'visible_pair':[f'0b{current[0]:04b}',f'0b{current[1]:04b}'],
                'lower_pair':[f'0b{lower[0]:04b}',f'0b{lower[1]:04b}'],
                'lower_is_dominant':not(lower[0]&~lower[1])}
    unsafe=row(4,222,3,50)
    safe=row(6,3202,5,802)
    if unsafe['visible_pair']!=safe['visible_pair'] or unsafe['shared_digit']!=safe['shared_digit']:
        raise AssertionError
    if unsafe['lower_is_dominant'] or not safe['lower_is_dominant']: raise AssertionError
    return {'unsafe':unsafe,'safe':safe,
            'consequence':'fiber-mask pair plus shared digit does not determine the next lower pair'}

def signature_nondeterminism()->dict[str,Any]:
    levels=build_levels('p',8)
    examples=[]
    for k,parent in ((1,3),(5,801),(6,3583)):
        digit=0; child=4*parent+digit
        source=signature(levels,k,parent); target=signature(levels,k+1,child)
        examples.append({'level':k,'parent':parent,'parent_hex':hex(parent),'digit':digit,
                         'source_signature':[f'0b{source[0]:04b}',f'0b{source[1]:04b}'],
                         'child':child,'child_hex':hex(child),
                         'target_signature':[f'0b{target[0]:04b}',f'0b{target[1]:04b}']})
    if len({tuple(x['source_signature']) for x in examples})!=1: raise AssertionError
    if len({tuple(x['target_signature']) for x in examples})!=3: raise AssertionError
    return {'examples':examples,'consequence':'even the 12-symbol signature and digit define a nondeterministic transition relation'}

def phase_campaign(phase:str,maximum_complexity:int)->dict[str,Any]:
    levels=build_levels(phase,maximum_complexity)
    signature_maps=[{} for _ in range(maximum_complexity+1)]
    sig_counts=Counter(); edge_counts=Counter()
    for k in range(1,maximum_complexity):
        signature_maps[k]={state:signature(levels,k,state) for state in levels[k]}
        sig_counts.update(signature_maps[k].values())
    outputs=sum(len(levels[k]) for k in range(1,maximum_complexity+1))
    for k in range(1,maximum_complexity-1):
        next_map=signature_maps[k+1]
        for state,source in signature_maps[k].items():
            for digit in range(4):
                child=4*state+digit
                target=next_map.get(child)
                if target is not None: edge_counts[(source,digit,target)]+=1
    realized=set(sig_counts)
    if realized!=set(universal_signature_table()):
        raise AssertionError('campaign did not realize all universal signatures')
    return {'phase':phase,'outputs_checked':outputs,
            'signature_counts':{f'0b{p:04b}/0b{f:04b}':n for (p,f),n in sorted(sig_counts.items())},
            'distinct_signature_edges':len(edge_counts),
            'edge_occurrences':sum(edge_counts.values())}

def run_campaign(maximum_complexity:int=DEFAULT_MAXIMUM_COMPLEXITY)->dict[str,Any]:
    if not 8<=maximum_complexity<=ABSOLUTE_MAXIMUM_COMPLEXITY: raise CampaignLimitError
    rows={p:phase_campaign(p,maximum_complexity) for p in PHASES}
    payload={'status':'exact-mask-closure-obstruction-and-twelve-signature-refinement',
             'maximum_complexity':maximum_complexity,
             'theorem':{
                 'universal_signature_alphabet':'P(q) can use only masks with digit 2 implying digit 3; M(q) is the OR of the four fixed child masks, giving exactly twelve parent/fiber signatures.',
                 'mask_pair_no_go':'The visible dominant fiber-mask pair and shared digit do not determine whether dominance survives one quotient step.',
                 'signature_transition_boundary':'The twelve-symbol parent/fiber signature is exact local information but its digit transition remains nondeterministic.'},
             'universal_signatures':[[f'0b{p:04b}',f'0b{f:04b}'] for p,f in universal_signature_table()],
             'closure_counterexample':closure_counterexample(),
             'signature_nondeterminism':signature_nondeterminism(),
             'phases':rows,
             'scientific_boundary':'This result disproves closure of the six fiber-mask pairs and gives an exact twelve-symbol refinement. It does not prove closure of a richer transducer, the all-depth adjacent-shadow inclusion, phase-complexity divergence, exclusion of eventual period two, or Rule 30 center nonperiodicity.'}
    encoded=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
    payload['certificate_sha256']=hashlib.sha256(encoded).hexdigest()
    return payload

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--maximum-complexity',type=int,default=DEFAULT_MAXIMUM_COMPLEXITY)
    args=ap.parse_args();print(json.dumps(run_campaign(args.maximum_complexity),indent=2,sort_keys=True))
if __name__=='__main__':main()
