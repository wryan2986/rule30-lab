# Astra automation handoff — 2026-09-20 run154

Problem 1 remains OPEN.

## New result

Run153 left terminal hidden slack

    g=g_(t+5) in {0,1,2,3}

with exact forced-birth original-cut jump

    s_(t+6)-s_(t+5)=g+2.

Run154 combines this with the exact global-front residence trace and the distinguished cyclic source at `q=t+2`.

For characteristic `j=t+6`, hidden slack `g` means its residence starts at `t+5-g`. Before the final eraser, the global-front theorem forces the diagonal cells

    r_g(t+5-g), r_(g-1)(t+6-g), ..., r_0(t+5)

to be zero.

If `g=3`, this requires both

    r_3(q)=0

and

    r_2(q+1)=0.

Write `a=r_3(q)`. The distinguished source has `r_1(q)=1,r_2(q)=0`, so Rule30 gives

    r_2(q+1)=1 XOR a=NOT a.

Thus the second required zero forces `a=1`, contradicting the first. Hence

    g_(t+5)<=2,
    s_(t+6)-s_(t+5)<=4.

The run153 scalar jump set `{2,3,4,5}` is reduced to `{2,3,4}` by genuine spacetime geometry.

Also, `g>=2` forces `a=1`, and then the next residence zero `r_1(q+2)=0` is automatically satisfied (independent of `b=r_4(q)`). So the immediate distinguished-motif calculation does not exclude `g=2`.

Full note: `proofs/informal/problem1_run154_distinguished_source_excludes_maximal_hidden_slack.md`.

## Next target

Try to exclude `g=2` using an additional cyclic/gate/global-shadow condition. The rigid source motif plus its first two forward cells are compatible with `g=2`, so do not merely extend that same local calculation. A useful theorem would force `g<=1` (jump <=3), or construct a full admissible witness with `g=2` and record that as the stopping fence for this hidden-slack route.
