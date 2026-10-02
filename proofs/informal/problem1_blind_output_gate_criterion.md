# Problem 1: an exact criterion for affine hidden-label transport

Status: LEMMA WITH PROOF — INDEPENDENTLY CHECKED.
This is an equivalence criterion, not a proof that all extension maps
are affine. Problem 1 remains **OPEN**.

## 1. Domain and definitions

Fix even p>=2 and r>=1. Let R be a realizable aligned depth-r normalized
cyclic portal orbit whose earlier raw parent tracks and last raw parent
track are nonzero. Its nonempty complete odd-label fiber C_R is the
affine cube fixing every nonblind driver label and imposing odd parity
on the free labels at the blind phases B_R. Write its dimension as

    m=u_r=max(|B_R|-1,0).

If there are no blind phases, nonemptiness means the forced labels are
already odd and C_R is a singleton. The same holds with one blind phase.
No least-period condition is imposed on R or the labels.

The nonzero-parent theorem guarantees a unique added cyclic layer
V_s(w)=(X_s(w),Y_s(w)) for every w in C_R. Use the last two fixed upper
histories (H_s,K_s), (L_s,M_s). Define its outgoing difference gate

    d_s(w)=K_s+M_s+M_s X_s(w)+(1+L_s+M_s)Y_s(w)
          =Y_(s+1)(w).

The extension E(w) consists of R and this full aligned new pair history.
All arithmetic is over GF(2).

**Gate condition H_gate for this fiber.** For every s in B_R there are
constants alpha_s,beta_s in GF(2) such that

    d_s(w)=alpha_s+beta_s w_s for every w in C_R.     (1)

Thus an outgoing gate at a phase where its upper driver label is hidden
may depend on that label itself, but not on other label coordinates once
that label is fixed. This is a scalar test at specified phases, not a
statement that the whole new Y history is constant.

## 2. All-depth equivalence

**Theorem.** On the stated domain, E is affine on C_R if and only if
H_gate holds. This applies at every r>=1.

### Sufficiency

Choose one fixed odd base driver w0 in C_R. For a given phase the exact
next-layer update is

    V_(s+1)=T_(w_s)(V_s),
    T_w(V)=A_s(w)V+c_s(w),

with the upper pairs fixed as in the monodromy theorem. Its only
driver-dependent change is in the first output coordinate:

    T_(w_s)(V)=T_(w0_s)(V)+(w_s+w0_s)D_s(V)e_X,
    e_X=(1,0)^T.                                  (2)

At a nonblind upper phase w_s=w0_s. At a blind phase, put
delta_s=w_s+w0_s and use (1) in the actual cyclic extension. Since
delta_s^2=delta_s,

    delta_s d_s(w)
      =delta_s[alpha_s+beta_s(w0_s+delta_s)]
      =[alpha_s+beta_s w0_s+beta_s]delta_s.         (3)

Thus every actual extension satisfies a linear recurrence whose matrices
are those of the FIXED odd base driver w0 and whose added forcing is an
affine function of w. One-period composition has the form

    V_p=A V_0+c+Q(w+w0),                           (4)

where Q is a fixed linear map on the driver coordinates. The base driver
is odd and the raw parent is nonzero. The monodromy theorem gives A^2=0,
so I+A is invertible, with inverse I+A. Cyclicity therefore determines

    V_0=(I+A)[c+Q(w+w0)].                          (5)

This is affine in w, and propagating the fixed linear recurrence makes
every V_s affine. Since R is constant, E is affine. This argument uses
the base odd return; it does not replace the driver by possibly even
all-zero free labels and assume an inverse for that different return.

### Necessity

Suppose E is affine on C_R. Then X_s,Y_s,d_s, and

    F_s=H_s+L_s+(1+L_s)X_s

are affine functions of the cube coordinates. The update

    X_(s+1)=F_s+w_s d_s

shows that w_s d_s is also affine.

If m=0, the fiber is a singleton, so (1) holds by taking beta_s=0.
If m>=1, every blind label w_s varies on C_R. In any affine coordinate
system t in GF(2)^m write

    w_s=a+l(t), d_s=b+d(t),

where l is a nonzero linear form and d is a linear form. A product of
these affine forms can be affine only if d is in the span of l. Indeed,
if d were not in that span, choose u with l(u)=0,d(u)=1 and v with
l(v)=1. The second finite difference of the product in directions u,v is

    l(u)d(v)+l(v)d(u)=1,

contradicting affineness. Hence d=0 or d=l. In either case d_s is an
affine function of w_s alone, proving (1). This also covers m=1, when
the span condition is automatic. The theorem follows.

## 3. Stronger special cases and exact rank

**Blind-gate invariance H_B.** If beta_s=0 for every blind phase, the
new gate values are fixed on C_R. H_B therefore implies affine extension,
and its new blind set is the fixed set

    B_new={s in B_R : alpha_s=0}.

Full newest-Y invariance H_Y implies H_B. The reverse implication is not
asserted: Y can vary at phases following nonblind upper transitions.

More generally, if E is affine, all of its nonempty fibers have the same
dimension m-rank(E). For a realized full extension orbit, its preimage
is exactly the complete odd-label cube determined by that orbit's blind
phases: it projects to R, and uniqueness of the added layer identifies
every realizing driver with this extension. Its dimension is u_(r+1).
Consequently u_(r+1) is constant over C_R and

    rank(E)=u_r-u_(r+1),                           (6)

even if the deeper blind SET varies between outputs. This does not prove
that such variation occurs in Rule 30; it distinguishes what the general
criterion permits from the stronger H_B conclusion.

## 4. Use as an adversarial test

H_gate can be refuted on one complete upper fiber by two drivers with
the same w_s but different outgoing d_s at one upper blind phase. On
the present nonzero-parent domain, that refutes H_ext itself by the
equivalence theorem. A full four-word output parallelogram remains a
direct independent certificate of non-affineness.

At dimensions zero and one, every map is affine. Such fibers cannot
refute H_gate or H_ext, although they can refute the stronger H_B/H_Y.
This explains why higher-depth extension tests with only lines cannot
establish general affine transport.

The general all-fiber gate condition is a falsifiable research target.
Neither the equivalence nor any finite gate test provides transport
through a zero return or a charge on the same original finite support.

## 5. Independent review

A separately pinned Luna reviewer accepted the equivalence on its stated
complete odd-fiber, nonzero-parent domain. The review explicitly checked
dimension zero, dimension one, the second-difference necessity at larger
dimension, the fixed odd base in the sufficiency argument, and complete
output fibers in the rank calculation. The parent re-derived these cases
and the cyclic fixed-point equation before accepting the proof.

The review verifies the criterion and its consequences, not the general
H_gate conjecture. The p30,r6 counterexample in
`problem1_hidden_label_reset_counterexample.md` shows that H_Y is stronger
than required; its exact two-dimensional extension satisfies H_B/H_gate.
