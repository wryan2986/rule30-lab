from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_budget_language_affine_no_go.py"
)
SPEC = importlib.util.spec_from_file_location("budget_language", MODULE_PATH)
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


@pytest.fixture(scope="module")
def campaign():
    return M.run_campaign(16, 5)


def test_affine_separation_recursion():
    node = M.PairNode(7, 12345, 2345)
    for digit in range(4):
        lifted = M.PairNode(8, 4 * node.current + digit, 4 * node.shadow + digit)
        assert M.affine_separation(lifted) == 4 * M.affine_separation(node) - 3 * digit


def test_budget_profile_matches_bruteforce_language():
    levels = M.build_levels(18)
    rows, nodes = M.selected_certificates(levels, 14)
    assert rows and nodes
    state = M.BudgetState(min(nodes), 3)
    profile = M.budget_language_profile(levels, state, 3)
    words = M.feasible_words(levels, state, 3)

    def accepted(word):
        cursor = profile
        for digit in word:
            if cursor is None or cursor == ():
                return False
            cursor = cursor[digit]
        return cursor is not None

    from itertools import product

    for length in range(4):
        for word in product(range(4), repeat=length):
            assert accepted(word) == (word in words)


def test_campaign_has_no_dominant_failure(campaign):
    assert campaign["gap_222_occurrences"] == 10
    assert campaign["dominant_failures"] == 0


def test_controlled_budget_partition_stabilizes(campaign):
    rows = campaign["partitions"]
    assert [row["classes"] for row in rows] == [1, 7, 12, 12, 12, 12]
    assert rows[2]["classes_split_next"] == 0


def test_small_affine_modulus_is_nondeterministic(campaign):
    rows = {row["bits"]: row for row in campaign["affine_quotients"]}
    assert rows[4]["nondeterministic_class_digits"] == 2


def test_larger_controlled_modulus_only_separates_states(campaign):
    rows = {row["bits"]: row for row in campaign["affine_quotients"]}
    assert rows[6]["nondeterministic_class_digits"] == 0
    assert rows[6]["classes"] == campaign["closure_states"]


def test_limits_are_enforced():
    with pytest.raises(M.BudgetLanguageLimitError):
        M.run_campaign(19, 5)
    with pytest.raises(M.BudgetLanguageLimitError):
        M.run_campaign(16, 6)
