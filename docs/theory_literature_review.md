# Rule 30 prize problems: theory and literature review

Review date: 2026-07-21

This note records what the cited sources actually establish. It distinguishes source facts, deductions made in this project, unresolved interpretation issues, and checks still recommended. It uses $0$ for white, $1$ for black, and time $t=0$ for the single-cell initial row.

## Definitions used in this review

Let $F$ be the Rule 30 cellular automaton on bi-infinite binary configurations, with

\[
F(x)_j=x_{j-1}\mathbin{\oplus}(x_j\lor x_{j+1}).
\]

Let $x^*$ be the single-cell configuration

\[
x^*_0=1,\qquad x^*_j=0\quad(j\ne0),
\]

and define the scalar center sequence by

\[
c_t=F^t(x^*)_0\qquad(t\in\mathbb N).
\]

A sequence $a_t$ is *eventually periodic* when there are $p\ge1$ and $T\ge0$ such that $a_{t+p}=a_t$ for every $t\ge T$. For an interval $I\subset\mathbb Z$, the trace is

\[
\operatorname{Tr}_{I}(x)[t]=F^t(x)|_I.
\]

These scalar and trace definitions avoid an ambiguity in the Wolfram Language notation discussed below.

## Primary sources

1. The [official Wolfram Rule 30 Prizes site](https://www.rule30prize.org/) states the three headline questions and the prize guidelines. It says that the problems concern the center-cell sequence generated from one nonzero cell.
2. Stephen Wolfram's [2019 prize announcement](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/) supplies the natural-language discussion, Wolfram Language predicates, and the proposed computational model for Problem 3.
3. The official [`CellularAutomaton` documentation](https://reference.wolfram.com/language/ref/CellularAutomaton.html) fixes the semantics of the Wolfram Language expression used in the announcement: a time specification $t$ returns all steps $0,\ldots,t$, while a nested singleton selects one spatial cell without retaining that spatial dimension.
4. Erica Jen, [“Global Properties of Cellular Automata,” *Journal of Statistical Physics* 43 (1986), 219–242](https://doi.org/10.1007/BF01010579), is the paper cited by Wolfram for the two-column result. The publisher page exposes the abstract and bibliographic record but not public full text.
5. Erica Jen, [“Aperiodicity in One-Dimensional Cellular Automata,” *Physica D* 45 (1990), 3–18](https://doi.org/10.1016/0167-2789(90)90169-P), contains the applicable result as Proposition 3. A public Los Alamos manuscript is available through the [U.S. Department of Energy OSTI repository](https://www.osti.gov/servlets/purl/7230855).
6. Johan Kopra, [“Rapid Left Expansivity, a Commonality between Wolfram's Rule 30 and Powers of $p/q$,” *Theoretical Computer Science* 946 (2023), 113668](https://doi.org/10.1016/j.tcs.2022.12.018), gives a modern definition-and-proof route and recovers Jen's result as Corollary 3.7. The author manuscript is openly available from the [University of Turku repository](https://urn.fi/URN:NBN:fi-fe2023031832340).

## Verified source facts

### The three prize questions

The official site and announcement agree on the intended initial condition and on these mathematical targets.

#### Problem 1: eventual nonperiodicity

The natural-language question asks whether the center column ever becomes periodic, including after an arbitrarily long transient. With the scalar convention above, the conjectured affirmative answer is

\[
\neg\exists p\ge1\;\exists T\ge0\;\forall t\ge T:\quad c_{t+p}=c_t.
\]

Thus the prize question is about *eventual* periodicity, not merely periodicity beginning at $t=0$.

#### Problem 2: limiting single-bit frequency

The natural-language question asks whether black and white occur equally often on average. A precise scalar form is

\[
\lim_{N\to\infty}\frac1N\sum_{t=0}^{N-1}c_t=\frac12.
\]

Equivalently, with $D(N)=\sum_{t=0}^{N-1}(2c_t-1)$, the required conclusion is $D(N)=o(N)$. This is only a one-bit frequency claim; it is weaker than normality, independence, or any general assertion of randomness.

#### Problem 3: published prose and displayed predicate

The official headline is: “Does computing the nth cell of the center column require at least $O(n)$ computational effort?” The explanatory prose asks whether it can be computed in “less than $O(n)$” effort. The announcement then suggests, for definiteness, a Turing machine whose initial tape contains the digits of $n$, whose output is the one center bit, and whose effort can be counted in machine steps. It also mentions other universal models, but does not fix one as binding.

The displayed formal predicate can be transcribed as follows. Let a finite machine description $m$ define

\[
M_m(n)=(v_m(n),t_m(n)),
\]

where $v_m(n)$ is its output and $t_m(n)$ its effort. The announcement writes

\[
\neg\exists m:\left[
  \bigl(\forall n,\ v_m(n)=c_n\bigr)
  \land
  \limsup_{n\to\infty}\frac{t_m(n)}n<\infty
\right].
\tag{P3-published}
\]

For nonnegative finite runtimes, the second conjunct is exactly $t_m(n)=O(n)$. Therefore the literal predicate says that **no finite exact machine has an $O(n)$ runtime bound**. It does not merely say that no exact machine is sublinear.

### A notation defect in the announcement's formal section

The announcement defines

```wolfram
c[t_] := CellularAutomaton[30, {{1}, 0}, {t, {{0}}}]
```

which, under the official function documentation, is the center prefix through time $t$, not the scalar $c_t$. Problem 3 explicitly uses `Last[c[n]]`, consistent with that fact. The displayed Problem 1 predicate nevertheless compares `c[t+p]` with `c[t]`; taken literally, those are prefixes of different lengths. The accompanying prose is unambiguous, so this appears to be a notation error or an unstated overload. Problem 2's `Total[c[t]]/t` also includes $t+1$ samples while dividing by $t$, but this off-by-one does not change the stated limit. Repository work should use the scalar definition $c_t=F^t(x^*)_0$.

### Jen's two-column result

Jen's 1990 public manuscript defines finite initial conditions as compactly supported configurations on an infinite lattice. Its Proposition 3 states, in modern terminology, that for a propagating elementary rule permutive in the relevant outer argument, at most one temporal column can be eventually periodic. The paper explicitly lists Rule 30 among the rules satisfying the proposition and captions its Rule 30 figure by saying that at most one temporal sequence can be periodic.

The same manuscript cites Jen's 1986 “Global Properties” paper for the lemma/result underlying Proposition 3. This explains the apparent bibliographic discrepancy: Wolfram attributes the result to 1986, while Kopra cites Proposition 3 of the 1990 paper.

Kopra's 2023 paper supplies the cleanest modern statement. In its notation:

- a configuration belongs to $\mathcal L_0(\Sigma)$ when it is nonzero and eventually zero to the left, so it has a leftmost nonzero symbol;
- an elementary cellular automaton is left spreading exactly when its local rule maps $001$ to $1$;
- Corollary 3.7 says that if a binary ECA is left permutive and left spreading and $x\in\mathcal L_0(\Sigma_2)$, then every adjacent width-two trace $\operatorname{Tr}_{[i,i+1]}(x)$ is not eventually periodic.

This modern result is slightly broader in its initial-condition hypothesis than compact support: it permits an arbitrary right tail.

## Derived inferences

The statements in this section are deductions made from the sourced results, not quotations from those sources.

### Problem 3's three plausible formulations differ

Fix a concrete machine model and let “exact” mean that the same finite, total machine outputs $c_n$ correctly for every $n$.

| Label | Mathematical statement | Meaning |
|---|---|---|
| P3-sublinear | No exact machine has $t(n)=o(n)$. | Excludes genuinely sublinear algorithms. |
| P3-linear-lower-bound | Every exact machine has $t(n)=\Omega(n)$. | Requires a positive eventual linear lower bound for each exact machine. |
| P3-published | No exact machine has $t(n)=O(n)$. | Literal consequence of the displayed `limsup` predicate. It excludes even $\Theta(n)$ algorithms. |

P3-published implies P3-sublinear, and P3-linear-lower-bound also implies P3-sublinear. P3-published and P3-linear-lower-bound do not imply each other without an additional regularity assumption on runtimes. For example, a runtime that alternates between very small and superlinear values can be neither $O(n)$ nor $\Omega(n)$. Consequently, the three claims must remain separate in experiments, proofs, and documentation.

The prose about a machine running “much less than $n$” steps and the example target $O(\log n)$ are evidence that P3-sublinear is the intended shortcut question. The displayed formula, however, unambiguously encodes P3-published. Only the Prize Committee can supply a binding contest interpretation.

### The width-two theorem's hypotheses hold for Rule 30 and the one-cell seed

The hypothesis check is direct:

| Hypothesis | Check |
|---|---|
| Binary, radius-one, bi-infinite CA | This is the standard Rule 30 system used in the prize statement. |
| Left permutive | For fixed $b,c$, the map $a\mapsto a\oplus(b\lor c)$ swaps $0$ and $1$, hence is bijective. |
| Quiescent zero background | $f(0,0,0)=0$. |
| Left spreading | $f(0,0,1)=1$, which is Kopra's criterion for an ECA. |
| Allowed initial configuration | The single-cell seed is nonzero, zero sufficiently far to the left, and in fact compactly supported; hence it satisfies both Kopra's $\mathcal L_0$ hypothesis and Jen's finite-initial-condition hypothesis. |
| Relevant trace | The adjacent pair $[-1,0]$ is one of the intervals covered by Corollary 3.7. |

Thus Kopra's Corollary 3.7 applies to $x^*$: the trace $\operatorname{Tr}_{[-1,0]}(x^*)$ is not eventually periodic.

### Rigorous partial consequence: the center cannot be eventually all one

Assume for contradiction that there is a $T$ such that $c_t=1$ for every $t\ge T$. For every $t\ge T$, the Rule 30 equation at the center gives

\[
1=c_{t+1}
 =F^t(x^*)_{-1}\oplus\bigl(c_t\lor F^t(x^*)_1\bigr)
 =F^t(x^*)_{-1}\oplus1.
\]

Therefore $F^t(x^*)_{-1}=0$ for every $t\ge T$. The adjacent trace at $[-1,0]$ is consequently the constant pair $(0,1)$ from time $T$ onward, so it is eventually period one. This contradicts Kopra's Corollary 3.7 (equivalently, Jen's at-most-one-periodic-column result).

**Status:** rigorous partial theorem, conditional only on the cited published width-two theorem and the stated Rule 30 convention.

**Scope:** this rules out an eventually constant-one center. It does **not** rule out an eventually constant-zero center, an eventual cycle of period greater than one, or eventual periodicity in general. It therefore does not solve Problem 1.

## Unresolved interpretation issues

1. **Problem 3 asymptotic class.** The prose suggests P3-sublinear, the heading uses upper-bound notation where lower-bound notation is expected, and the displayed predicate is P3-published. These are not equivalent.
2. **Machine model.** The announcement proposes a Turing machine “for definiteness” but also permits other universal systems. Linear versus sublinear time is not invariant under arbitrary simulation overhead, so a proof must fix a model.
3. **Input representation.** The prose proposes the digits of $n$, apparently binary or another fixed radix. With binary input, an $\Omega(n)$ bound is exponential in the input length $\Theta(\log n)$. Unary input would define a materially different problem.
4. **Cost measure.** Machine steps, total cellular-automaton cell updates, word-RAM operations, bit operations, circuit size/depth, and measured CPU time are not interchangeable at the $n$ threshold.
5. **Uniformity and advice.** Requiring one finite machine suggests a uniform algorithm and rules out storing the infinite answer sequence, but preprocessing, advice, nonuniform circuits, and oracle access are not expressly specified.
6. **Exactness and randomness.** The statement requires the correct bit for every $n$, but it does not expressly say whether randomized zero-error machines are in scope. Bounded-error prediction is plainly insufficient for an exact prize solution.
7. **Runtime pathologies.** `limsup` permits irregular runtimes and makes P3-published different from an $\Omega(n)$ lower bound. Halting and the treatment of $t(n)=\infty$ also need explicit conventions.
8. **Indexing.** The source alternates between prefix-valued `c[t]` and scalar uses. All project claims should state whether $c_0$ is included and whether “the $n$th bit” means time $n$ or the one-indexed $n$th list element.
9. **Original theorem citation.** The exact result is publicly checkable in Jen's 1990 manuscript and Kopra's 2023 reproof. A page-level comparison with the paywalled 1986 journal article remains desirable for definitive historical attribution, but is not needed for the deduction above.

## Recommended theorem and specification checks

1. Adopt three separately named Problem 3 specifications—P3-sublinear, P3-linear-lower-bound, and P3-published—and never transfer a result between them without proof.
2. For computational work, publish a canonical baseline model: a deterministic multitape Turing machine; canonical binary input with no leading zeroes; one output bit; a single finite uniform machine; no advice or oracle; total correctness; and elapsed transition count including input access. Translate RAM, circuit, and cellular-automaton results to this model with explicit overhead.
3. Before presenting any Problem 3 result as prize-relevant, request a written interpretation from the Prize Committee, especially on whether the intended target is “no $o(n)$” or the displayed “no $O(n)$.” This is an external adjudication issue, not something experiments can resolve.
4. Formalize in Lean the local Rule 30 identity, left-permutive inversion, the eventually-one implication for the left neighbor, and the final contradiction *assuming* the width-two theorem as a named hypothesis. Formalizing Kopra's entire dynamical theorem can be a later, separate project.
5. Independently restate and check Kopra's definitions of $\mathcal L_0$, trace orientation, left spreading, and eventual periodicity against the repository's coordinate conventions. Add a small executable example confirming that `[-1,0]` is the intended adjacent trace.
6. Obtain the complete 1986 Jen paper through a lawful library route and record the exact theorem/lemma pages. Compare it with Proposition 3 in the 1990 manuscript; treat this as bibliographic verification rather than a mathematical blocker.
7. Do not generalize the eventually-all-one argument to other periods without a new lemma. In particular, the equation for an all-zero center tail yields equality of the left and right neighbors, not their periodicity.

## Bottom line

The authoritative prize materials support precise formulations of Problems 1 and 2 but contain a substantive asymptotic-notation mismatch for Problem 3. The literal displayed Problem 3 predicate excludes every exact $O(n)$ algorithm; the surrounding prose most naturally asks whether any exact $o(n)$ shortcut exists. These must be tracked separately.

The width-two literature result is applicable to the single-cell Rule 30 evolution. It rigorously proves the useful but limited statement that the center column cannot become permanently $1$. It does not establish full center-column nonperiodicity.
