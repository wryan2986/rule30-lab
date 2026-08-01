#!/usr/bin/env python3
"""Classify full-fiber and minimally defective dominant shadow paths."""
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter, defaultdict
from itertools import product
from typing import Any

PHASES=("p","u")
GAPS=(2,3,4,5)
FORBIDDEN=("uu","ttttt","ututtu")
ALLOWED_MASKS=(0b0000,0b0011,0b1011,0b1100,0b1111)
DEFAULT_MAXIMUM_COMPLEXITY=16
ABSOLUTE_MAXIMUM_COMPLEXITY=20
DEFAULT_SCHEDULE_CAP=64

class ShadowDefectLimitError(RuntimeError): pass

def forward_generator(name:str,state:int)->int:
    stepped=state^((state<<1)|(state<<2))
    if name=="t": return stepped
    if name=="u": return stepped^1
    if name=="p": return stepped^1^(2 if state&1==0 else 0)
    raise ValueError(name)

def frontier_children(state:int)->tuple[int,...]:
    return tuple(sorted({forward_generator(g,state) for g in "tup"}))

def phase_start(phase:str)->int:
    if phase=="p": return 3
    if phase=="u": return 1
    raise ValueError(phase)

def expected_bits(phase:str,complexity:int)->int:
    return 2*complexity if phase=="p" else 2*complexity-1

def build_levels(phase:str,maximum_complexity:int)->list[set[int]]:
    levels=[set(),{phase_start(phase)}]
    for _ in range(2,maximum_complexity+1):
        levels.append({c for s in levels[-1] for c in frontier_children(s)})
    return levels

def forced_zero_schedule(state:int,cap:int=DEFAULT_SCHEDULE_CAP)->str:
    word=[]
    for _ in range(cap):
        residue=state&15
        if residue==7: branch="u"
        elif residue==11: branch="t"
        else: return "".join(word)
        state=forward_generator(branch,forward_generator("p",(state-3)>>2))
        word.append(branch)
    raise ShadowDefectLimitError("forced schedule reached safety cap")

def admissible(word:str)->bool:
    return not any(factor in word for factor in FORBIDDEN)

def return_extension(gaps:tuple[int,...],include_final_u:bool)->str:
    word="u"
    for index,gap in enumerate(gaps):
        word+="t"*(gap-1)
        if index<len(gaps)-1 or include_final_u: word+="u"
    return word

def three_return_patterns()->tuple[tuple[tuple[int,...],str,str],...]:
    rows=[]
    for gaps in product(GAPS,repeat=3):
        target=return_extension(gaps,False)
        complete=return_extension(gaps,True)
        if admissible(complete): rows.append((gaps,target,complete))
    return tuple(rows)

def fiber_mask(levels:list[set[int]],complexity:int,quotient:int)->int:
    mask=sum(1<<digit for digit in range(4) if 4*quotient+digit in levels[complexity+1])
    if mask not in ALLOWED_MASKS: raise AssertionError("fiber escaped alphabet")
    return mask

def mask_sequence(levels:list[set[int]],complexity:int,state:int,depth:int)->tuple[int,...]:
    masks=[]
    for step in range(depth):
        quotient=state>>2
        level=complexity-1-step
        if level<1: raise ValueError("depth exceeds complexity")
        masks.append(fiber_mask(levels,level,quotient))
        state=quotient
    return tuple(masks)

def dominates(current:tuple[int,...],shadow:tuple[int,...])->bool:
    return len(current)==len(shadow) and all(not(a&~b) for a,b in zip(current,shadow))

def defect_count(shadow:tuple[int,...])->int:
    return sum(mask!=0b1111 for mask in shadow)

def phase_campaign(phase:str,maximum_complexity:int,schedule_cap:int)->dict[str,Any]:
    levels=build_levels(phase,maximum_complexity)
    patterns=three_return_patterns()
    totals=Counter(outputs=sum(len(levels[k]) for k in range(1,maximum_complexity+1)))
    totals["eligible_outputs"]=sum(
        1 for k in range(1,maximum_complexity+1) for state in levels[k] if state&3==3
    )
    defect_hist=Counter()
    chosen_sequences=Counter()
    incomplete=[]
    examples=[]
    distinct=set()
    minimum=None
    maximum=None
    for complexity in range(2,maximum_complexity+1):
        occurrences=[]
        needed_depths=set()
        for current in sorted(levels[complexity]):
            if current.bit_length()!=expected_bits(phase,complexity):
                raise AssertionError("bit-length law failed")
            if current&3!=3: continue
            schedule=forced_zero_schedule(current,schedule_cap)
            for cut in range(len(schedule)+1):
                base=schedule[:cut]
                matches=[
                    gaps for gaps,target,complete in patterns
                    if schedule[cut:].startswith(target) and admissible(base+complete)
                ]
                if matches:
                    occurrences.append((current,cut,cut+1,matches))
                    needed_depths.add(cut+1)
        if not occurrences: continue
        indexes={}
        for depth in sorted(needed_depths):
            modulus=4**depth
            by_residue=defaultdict(dict)
            for shadow in sorted(levels[complexity-1]):
                residue=shadow%modulus
                sequence=mask_sequence(levels,complexity-1,shadow,depth)
                by_residue[residue].setdefault(sequence,shadow)
            indexes[depth]=by_residue
            saturated_sequence=(0b1111,)*depth
            covered=sum(saturated_sequence in sequences for sequences in by_residue.values())
            if covered<modulus:
                incomplete.append({
                    "complexity":complexity,
                    "depth":depth,
                    "covered_residues":covered,
                    "all_residues":modulus,
                })
        for current,cut,depth,matches in occurrences:
            residue=current%(4**depth)
            current_sequence=mask_sequence(levels,complexity,current,depth)
            candidates=[]
            for shadow_sequence,shadow in indexes[depth].get(residue,{}).items():
                if dominates(current_sequence,shadow_sequence):
                    candidates.append((defect_count(shadow_sequence),shadow_sequence,shadow))
            weight=len(matches)
            totals["occurrences"]+=weight
            if cut: totals["positive_cut_occurrences"]+=weight
            totals["maximum_cut"]=max(totals["maximum_cut"],cut)
            totals["maximum_depth"]=max(totals["maximum_depth"],depth)
            distinct.add((complexity,depth,residue))
            if not candidates:
                totals["dominant_failures"]+=weight
                continue
            defects,shadow_sequence,shadow=min(candidates)
            totals["dominant_occurrences"]+=weight
            if defects==0: totals["saturated_occurrences"]+=weight
            else: totals["saturated_failures"]+=weight
            defect_hist[defects]+=weight
            chosen_sequences[shadow_sequence]+=weight
            row={
                "complexity":complexity,
                "state_hex":hex(current),
                "cut":cut,
                "depth":depth,
                "residue_hex":hex(residue),
                "gaps":[list(g) for g in matches],
                "minimum_defects":defects,
                "current_masks":[f"0b{x:04b}" for x in current_sequence],
                "shadow_masks":[f"0b{x:04b}" for x in shadow_sequence],
                "shadow_hex":hex(shadow),
            }
            if minimum is None or defects<minimum["minimum_defects"]: minimum=row
            if maximum is None or defects>maximum["minimum_defects"]: maximum=row
            if defects and len(examples)<8: examples.append(row)
    totals["distinct_occurrence_cylinders"]=len(distinct)
    return {
        "phase":phase,
        "totals":dict(totals),
        "minimum_defect_histogram":{str(k):v for k,v in sorted(defect_hist.items())},
        "chosen_shadow_mask_sequences":{
            "/".join(f"{m:04b}" for m in seq):count
            for seq,count in sorted(chosen_sequences.items())
        },
        "incomplete_saturated_residue_pairs":incomplete,
        "minimum_example":minimum,
        "maximum_example":maximum,
        "defect_examples":examples,
    }

def run_campaign(maximum_complexity:int=DEFAULT_MAXIMUM_COMPLEXITY,schedule_cap:int=DEFAULT_SCHEDULE_CAP)->dict[str,Any]:
    if not 2<=maximum_complexity<=ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise ShadowDefectLimitError("maximum complexity outside controlled range")
    phases={p:phase_campaign(p,maximum_complexity,schedule_cap) for p in PHASES}
    fields=("outputs","eligible_outputs","occurrences","positive_cut_occurrences",
            "dominant_occurrences","dominant_failures","saturated_occurrences",
            "saturated_failures","distinct_occurrence_cylinders")
    combined={f:sum(phases[p]["totals"].get(f,0) for p in PHASES) for f in fields}
    combined["maximum_cut"]=max(phases[p]["totals"].get("maximum_cut",0) for p in PHASES)
    combined["maximum_depth"]=max(phases[p]["totals"].get("maximum_depth",0) for p in PHASES)
    combined["maximum_minimum_defects"]=max(
        phases[p]["maximum_example"]["minimum_defects"] if phases[p]["maximum_example"] else 0
        for p in PHASES
    )
    payload={
        "status":"finite-saturated-shadow-no-go-and-defect-classification",
        "maximum_complexity":maximum_complexity,
        "schedule_cap":schedule_cap,
        "admissible_three_return_patterns":len(three_return_patterns()),
        "theorem":{
            "saturated_shadow":"A depth-L shadow is saturated when every quotient ancestor along the common cylinder has fiber 1111; such a path is automatically dominant.",
            "defect_measure":"The defect count is the number of non-1111 shadow masks in a dominant path.",
        },
        "phases":phases,
        "combined":combined,
        "scientific_boundary":(
            "Saturated-shadow sufficiency is exact, while existence and minimum-defect "
            "counts are finite through the configured complexity. The complexity-25 "
            "campaign supplies exact counterexamples to universal saturated-shadow "
            "existence but not an all-depth bound on dominant-shadow defects."
        ),
    }
    encoded=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
    payload["certificate_sha256"]=hashlib.sha256(encoded).hexdigest()
    return payload

def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--maximum-complexity",type=int,default=DEFAULT_MAXIMUM_COMPLEXITY)
    parser.add_argument("--schedule-cap",type=int,default=DEFAULT_SCHEDULE_CAP)
    args=parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_complexity,args.schedule_cap),indent=2,sort_keys=True))
if __name__=="__main__": main()
