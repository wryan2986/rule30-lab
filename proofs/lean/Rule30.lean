/-!
# Stable Boolean lemmas for Rule 30

This file formalizes the local Rule 30 update and the one-cell
left-permutive reconstruction used by the computational experiments.
-/

namespace Rule30

/-- The Rule 30 local update: `left XOR (center OR right)`. -/
def localUpdate (left center right : Bool) : Bool :=
  left.xor (center || right)

/-! The eight entries of the Rule 30 truth table, ordered from `111` to `000`. -/

theorem localUpdate_111 : localUpdate true true true = false := rfl

theorem localUpdate_110 : localUpdate true true false = false := rfl

theorem localUpdate_101 : localUpdate true false true = false := rfl

theorem localUpdate_100 : localUpdate true false false = true := rfl

theorem localUpdate_011 : localUpdate false true true = true := rfl

theorem localUpdate_010 : localUpdate false true false = true := rfl

theorem localUpdate_001 : localUpdate false false true = true := rfl

theorem localUpdate_000 : localUpdate false false false = false := rfl

/-- Recover the cell to the left from the center, its next value, and the right cell. -/
def sidewaysStep (center next right : Bool) : Bool :=
  next.xor (center || right)

/-- The left-permutive inversion identity in the form used for reconstruction. -/
theorem leftPermutiveInversion (left center right : Bool) :
    left = sidewaysStep center (localUpdate left center right) right := by
  cases left <;> cases center <;> cases right <;> rfl

/-- A sideways step recovers the original left cell from a genuine local update. -/
theorem sidewaysStep_recovers_left (left center right : Bool) :
    sidewaysStep center (localUpdate left center right) right = left := by
  cases left <;> cases center <;> cases right <;> rfl

/-- With the center and right inputs fixed, Rule 30 is injective in its left input. -/
theorem localUpdate_left_injective (center right : Bool) :
    Function.Injective (fun left => localUpdate left center right) := by
  intro first second hEqual
  cases first <;> cases second <;> cases center <;> cases right <;>
    simp_all [localUpdate]

/-- Reapplying Rule 30 after a sideways step recovers the supplied next value. -/
theorem localUpdate_sidewaysStep (center next right : Bool) :
    localUpdate (sidewaysStep center next right) center right = next := by
  cases center <;> cases next <;> cases right <;> rfl

/-- If the center and its next value are both `true`, the left cell is `false`. -/
theorem true_center_true_next_forces_left_false (left right : Bool)
    (hNext : localUpdate left true right = true) : left = false := by
  cases left <;> cases right
  · rfl
  · rfl
  · cases hNext
  · cases hNext

/-!
## Columns and bounded sideways reconstruction

A `Column` records one fixed spatial coordinate over all natural-numbered
times.  The definitions below are total functions, while
`reconstructionPair_bounded_correct` states correctness on a finite
triangular region: reconstructing to depth `depth` at time `time` uses no
boundary value after `time + depth`.
-/

/-- A time column of Boolean cell values. -/
abbrev Column := Nat → Bool

/-- A Rule 30 spacetime diagram, indexed by integer position and natural time. -/
abbrev Spacetime := Int → Nat → Bool

/--
A finite-reconstruction-friendly strip indexed from right to left:
index `0` is the supplied right column, index `1` is the center column,
and increasing indices move leftward.
-/
abbrev LeftwardStrip := Nat → Nat → Bool

/-- The pointwise Rule 30 evolution equation for a spacetime diagram. -/
def EvolvesByRule30 (x : Spacetime) : Prop :=
  ∀ position time,
    x position (time + 1) =
      localUpdate
        (x (position - 1) time)
        (x position time)
        (x (position + 1) time)

/-- Rule 30 evolution in right-to-left strip coordinates. -/
def EvolvesLeftwardByRule30 (x : LeftwardStrip) : Prop :=
  ∀ offset time,
    x (offset + 1) (time + 1) =
      localUpdate
        (x (offset + 2) time)
        (x (offset + 1) time)
        (x offset time)

/-- Reconstruct the column immediately to the left of `current`. -/
def sidewaysColumn (current right : Column) : Column := fun time =>
  sidewaysStep (current time) (current (time + 1)) (right time)

/-- One column reconstructed from a genuine Rule 30 diagram is exact. -/
theorem sidewaysColumn_of_evolution (x : Spacetime) (hRule : EvolvesByRule30 x)
    (position : Int) (time : Nat) :
    sidewaysColumn (x position) (x (position + 1)) time =
      x (position - 1) time := by
  change
    sidewaysStep
        (x position time)
        (x position (time + 1))
        (x (position + 1) time) =
      x (position - 1) time
  rw [hRule position time]
  exact sidewaysStep_recovers_left _ _ _

/--
The reconstruction state `(right, current)` after a given number of
leftward steps.  Keeping both adjacent columns makes each recursive step
structural and mirrors the finite sideways algorithm.
-/
def reconstructionPair (center right : Column) : Nat → Column × Column
  | 0 => (right, center)
  | depth + 1 =>
      let previous := reconstructionPair center right depth
      (previous.2, sidewaysColumn previous.2 previous.1)

/-- The reconstructed column at the requested leftward depth. -/
def reconstructLeft (center right : Column) (depth : Nat) : Column :=
  (reconstructionPair center right depth).2

/--
Bounded triangular-region correctness for sideways reconstruction.

If the supplied center and right boundary columns agree with a genuine
right-to-left Rule 30 strip through `horizon`, then the reconstructed
adjacent pair at `(depth, time)` is exact whenever
`time + depth ≤ horizon`.
-/
theorem reconstructionPair_bounded_correct
    (x : LeftwardStrip)
    (hRule : EvolvesLeftwardByRule30 x)
    (center right : Column)
    (horizon : Nat)
    (hCenter : ∀ time, time ≤ horizon → center time = x 1 time)
    (hRight : ∀ time, time ≤ horizon → right time = x 0 time) :
    ∀ depth time,
      time + depth ≤ horizon →
        (reconstructionPair center right depth).2 time =
            x (depth + 1) time ∧
          (reconstructionPair center right depth).1 time =
            x depth time := by
  intro depth
  induction depth with
  | zero =>
      intro time hBound
      constructor
      · exact hCenter time hBound
      · exact hRight time hBound
  | succ depth ih =>
      intro time hBound
      have hEarlier : time + depth ≤ horizon :=
        Nat.le_trans (Nat.add_le_add_left (Nat.le_succ depth) time) hBound
      have hNextTime : (time + 1) + depth ≤ horizon := by
        have hIndices : (time + 1) + depth = time + (depth + 1) := by
          rw [Nat.add_assoc, Nat.add_comm 1 depth]
        exact
          Eq.mp
            (congrArg (fun index => index ≤ horizon) hIndices).symm
            hBound
      have hAtTime := ih time hEarlier
      have hAtNextTime := ih (time + 1) hNextTime
      constructor
      · change
          sidewaysColumn
              (reconstructionPair center right depth).2
              (reconstructionPair center right depth).1 time =
            x ((depth + 1) + 1) time
        change
          sidewaysStep
              ((reconstructionPair center right depth).2 time)
              ((reconstructionPair center right depth).2 (time + 1))
              ((reconstructionPair center right depth).1 time) =
            x (depth + 2) time
        rw [hAtTime.1, hAtNextTime.1, hAtTime.2]
        rw [hRule depth time]
        exact sidewaysStep_recovers_left _ _ _
      · change
          (reconstructionPair center right depth).2 time =
            x (depth + 1) time
        exact hAtTime.1

/-- The current-column projection of bounded triangular correctness. -/
theorem reconstructLeft_bounded_correct
    (x : LeftwardStrip)
    (hRule : EvolvesLeftwardByRule30 x)
    (center right : Column)
    (horizon depth time : Nat)
    (hCenter : ∀ time, time ≤ horizon → center time = x 1 time)
    (hRight : ∀ time, time ≤ horizon → right time = x 0 time)
    (hBound : time + depth ≤ horizon) :
    reconstructLeft center right depth time =
      x (depth + 1) time := by
  exact
    (reconstructionPair_bounded_correct
      x hRule center right horizon hCenter hRight depth time hBound).1

/-!
## Consecutive true values and finite tails
-/

/--
In a genuine spacetime diagram, two consecutive `true` values in one
column force the adjacent-left value at the earlier time to be `false`.
-/
theorem consecutive_true_values_force_adjacent_left_false
    (x : Spacetime)
    (hRule : EvolvesByRule30 x)
    (position : Int)
    (time : Nat)
    (hCurrent : x position time = true)
    (hNext : x position (time + 1) = true) :
    x (position - 1) time = false := by
  have hLocal :
      localUpdate
          (x (position - 1) time)
          (x position time)
          (x (position + 1) time) = true :=
    (hRule position time).symm.trans hNext
  rw [hCurrent] at hLocal
  apply true_center_true_next_forces_left_false
  exact hLocal

/--
Finite-tail form: if a column is `true` on the closed interval from
`start` through `start + length`, then its adjacent-left column is `false`
on the half-open interval from `start` through `start + length`.
-/
theorem true_closed_interval_forces_left_false_on_halfOpen_interval
    (x : Spacetime)
    (hRule : EvolvesByRule30 x)
    (position : Int)
    (start length : Nat)
    (hTrue : ∀ time, start ≤ time → time ≤ start + length →
      x position time = true) :
    ∀ time, start ≤ time → time < start + length →
      x (position - 1) time = false := by
  intro time hStart hEnd
  apply consecutive_true_values_force_adjacent_left_false x hRule position time
  · exact hTrue time hStart (Nat.le_of_lt hEnd)
  · exact hTrue (time + 1) (Nat.le_trans hStart (Nat.le_succ time)) hEnd

/--
Infinite-tail form of the same local implication: an all-`true` column tail
forces the adjacent-left column to be `false` from the same starting time.
This theorem does not itself contradict such a tail; that requires a separate
width-two nonperiodicity theorem.
-/
theorem true_tail_forces_adjacent_left_false_tail
    (x : Spacetime)
    (hRule : EvolvesByRule30 x)
    (position : Int)
    (start : Nat)
    (hTrue : ∀ time, start ≤ time → x position time = true) :
    ∀ time, start ≤ time → x (position - 1) time = false := by
  intro time hStart
  apply consecutive_true_values_force_adjacent_left_false x hRule position time
  · exact hTrue time hStart
  · exact hTrue (time + 1) (Nat.le_trans hStart (Nat.le_succ time))

/-!
## A false column tail and its right neighbor

When the cell to the left is `false`, a `true` center remains `true` at the
next step regardless of its right neighbor.  The separate published width-two
theorem and the classical eventual-constancy deduction are not imported here.
-/

/-- With a `false` left input, a `true` center remains `true`. -/
theorem false_left_true_center_stays_true_locally (right : Bool) :
    localUpdate false true right = true := by
  cases right <;> rfl

/--
If one column is `false` from `start` onward and its right neighbor is `true`
at a later time, that right neighbor stays `true` at every subsequent offset.
-/
theorem false_left_tail_true_right_persists
    (x : Spacetime)
    (hRule : EvolvesByRule30 x)
    (leftPosition rightPosition : Int)
    (hAdjacent : rightPosition - 1 = leftPosition)
    (start time : Nat)
    (hFalse : ∀ later, start ≤ later → x leftPosition later = false)
    (hStart : start ≤ time)
    (hTrue : x rightPosition time = true) :
    ∀ offset, x rightPosition (time + offset) = true := by
  intro offset
  induction offset with
  | zero =>
      exact hTrue
  | succ offset ih =>
      have hStartOffset : start ≤ time + offset :=
        Nat.le_trans hStart (Nat.le_add_right time offset)
      have hLeft : x leftPosition (time + offset) = false :=
        hFalse (time + offset) hStartOffset
      calc
        x rightPosition (time + Nat.succ offset) =
            x rightPosition ((time + offset) + 1) := by
              rw [Nat.add_succ]
        _ = localUpdate
              (x (rightPosition - 1) (time + offset))
              (x rightPosition (time + offset))
              (x (rightPosition + 1) (time + offset)) :=
            hRule rightPosition (time + offset)
        _ = true := by
              rw [hAdjacent, hLeft, ih]
              exact
                false_left_true_center_stays_true_locally
                  (x (rightPosition + 1) (time + offset))

end Rule30
