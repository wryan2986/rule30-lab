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

/-- Reapplying Rule 30 after a sideways step recovers the supplied next value. -/
theorem localUpdate_sidewaysStep (center next right : Bool) :
    localUpdate (sidewaysStep center next right) center right = next := by
  cases center <;> cases next <;> cases right <;> rfl

/-- If the center and its next value are both `true`, the left cell is `false`. -/
theorem true_center_true_next_forces_left_false (left right : Bool)
    (hNext : localUpdate left true right = true) : left = false := by
  cases left <;> cases right <;> simp [localUpdate] at hNext ⊢

end Rule30
