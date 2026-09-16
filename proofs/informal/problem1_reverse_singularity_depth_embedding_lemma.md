# Problem 1: reverse singularity depths are inherited lower-period termination widths

Status: exact structural lemma plus an empirical identification for the known p=2,4,8 terminating necklaces.

## Observation that removes a mystery

Runs 58--61 found reverse derivative singularities at depths

    9, 30, 401.

Run 53 independently found termination columns for the unique known terminating necklaces

    N_2 = 8,
    N_4 = 29,
    N_8 = 400.

Thus the singular depths are exactly

    N_2 + 1, N_4 + 1, N_8 + 1.

This is not a numerical coincidence. It follows from a simple embedding property of the reverse recurrence.

## Setup

The forward temporal-column reconstruction is

    q_(i+2) = S q_i xor (q_(i+1) OR q_i),
    q_0 = 0,
    q_1 = c.

A reverse predecessor x of a known pair (u,w) satisfies

    w = S x xor (u OR x).                 (R)

Let E map a cyclic p-word to the cyclic 2p-word obtained by repeating it twice. E commutes with shift, xor, and OR. Therefore it commutes with both the forward recurrence and equation (R).

## Embedding lemma

Suppose a length-p terminating trajectory from (0,c_p) reaches its first terminal pair (0,0) after termination column N_p. Suppose moreover that along the reverse path from the terminal pair back to (0,c_p), each predecessor is unique (up to whatever phase convention has already been fixed).

Embed every p-word by repetition into length 2p. Starting from the length-2p terminal pair, reverse propagation must reproduce the embedded length-p reverse trajectory for exactly the same N_p steps: at each step E(x) is a predecessor because E commutes with (R), and uniqueness forces it to be the predecessor on that branch.

Consequently the first equation immediately before the embedded legal initial pair is reached has

    u = 0,
    w = E(c_p),

and hence reduces to

    E(c_p) = S x xor x.                  (D_p)

Thus the inherited lower-scale reverse orbit necessarily ends in a derivative singularity at reverse depth N_p+1.

## Why doubling removes the lower-period obstruction

Every eligible doubling word c_p has odd XOR parity. Therefore at temporal length p the equation

    c_p = Sx xor x

has no cyclic solution: the image of S+I consists exactly of even-parity words.

But E(c_p)=c_p c_p has even total parity. Hence at temporal length 2p, (D_p) has exactly two solutions, differing by the constant-one kernel of S+I.

So the scale transition has a clean interpretation:

1. the length-2p reverse basin initially retraces the entire embedded length-p terminating trajectory;
2. exactly one step before the lower-period initial condition, the lower-period reverse orbit is blocked by odd parity;
3. repeating the odd word twice cancels that parity obstruction;
4. two complementary derivative lifts become available at length 2p;
5. only after choosing one of those lifts does genuinely new scale-2p reverse dynamics begin.

This explains both the dyadic divisibility mechanism and the previously unexplained singularity-depth values.

## Match to the computed scales

The known termination columns are

    N_2=8, N_4=29, N_8=400.

Therefore the embedding lemma predicts inherited derivative singularities at

    9, 30, 401,

exactly the depths found independently in runs 58--61.

The right-hand sides also match the lower-period terminating necklaces, modulo the phase/orientation conventions used by the reverse scripts:

- depth 9: the alternating period-2 word, i.e. c_2;
- depth 30: the reported block `1101`, a cyclic rotation of c_4=`0111`;
- depth 401: the reported block `11000010`; this is a cyclic rotation of the temporal reversal of c_8=`00001101` (the reversal difference is attributable to the shift/orientation convention and should be normalized in future scripts).

The important invariant statement is not the displayed representative but that the singular right-hand side is the embedded lower-scale initial word under a consistent convention.

## Consequence for the renormalization program

The long forced intervals between singularities no longer need to be regarded as unexplained 20- and 370-step computations. They are the already-known lower-period terminating trajectories, viewed backward and periodically embedded at the next temporal scale.

The remaining genuinely new object at each scale is therefore much smaller conceptually: the dynamics beginning at either solution of

    Sx xor x = E(c_p)

and ending, if successful, at a legal length-2p initial pair (0,c_(2p)).

This reframes the all-scale induction. It is enough to characterize this **post-lift connector segment** and prove that, from the two complementary derivative lifts, reverse propagation is rigid (modulo phase/complement symmetries) until it reaches one length-2p terminating necklace.

## What is proved and what is not

Proved here:

- repetition embedding commutes with the recurrence and reverse predecessor equation;
- a unique lower-period reverse path embeds unchanged at double period;
- its next predecessor equation is exactly the cyclic derivative equation with repeated odd right-hand side;
- that equation has exactly two complementary solutions at double period and none at the original odd-parity period;
- hence inherited singularity depth is exactly N_p+1 under the uniqueness hypothesis.

Not proved:

- uniqueness of the reverse path at every dyadic p;
- existence/uniqueness of c_(2p) after the derivative lift;
- an all-scale description of the post-lift connector segment.

Those are now the precise remaining renormalization questions.
