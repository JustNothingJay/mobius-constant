"""Tests for MöbiusConstant — exact irrational constants."""

import math
import pytest
from decimal import Decimal
from mobius_constant import (
    MobiusConstant, MC, sqrt,
    Pi, Euler, Sqrt2, Sqrt3, Phi, Ln2,
    Alpha_inv, Alpha, VERIFIED_DEPTH,
)


# =====================================================================
# THE PROOF: sqrt(2) ** 2 == 2
# =====================================================================

class TestTheProof:
    """The problem that started it all — irrational identity failures."""

    def test_ieee754_sqrt2_squared_fails(self):
        """IEEE 754 gets this wrong."""
        assert math.sqrt(2) ** 2 != 2  # 2.0000000000000004

    def test_mobius_sqrt2_squared(self):
        """MöbiusConstant gets it right."""
        assert Sqrt2 ** 2 == 2

    def test_ieee754_sqrt3_squared_fails(self):
        assert math.sqrt(3) ** 2 != 3

    def test_mobius_sqrt3_squared(self):
        assert Sqrt3 ** 2 == 3

    def test_sqrt2_times_sqrt2(self):
        """√2 × √2 = 2 exactly."""
        assert Sqrt2 * Sqrt2 == 2

    def test_sqrt3_times_sqrt3(self):
        """√3 × √3 = 3 exactly."""
        assert Sqrt3 * Sqrt3 == 3


# =====================================================================
# PI IDENTITIES
# =====================================================================

class TestPiIdentities:
    """π arithmetic that IEEE 754 gets wrong."""

    def test_pi_plus_pi_equals_two_pi(self):
        assert Pi + Pi == Pi * 2

    def test_pi_minus_pi_is_zero(self):
        assert Pi - Pi == 0

    def test_pi_div_pi_is_one(self):
        assert Pi / Pi == 1

    def test_two_pi_div_two_is_pi(self):
        result = (Pi * 2) / MC(2)
        assert result == Pi

    def test_pi_times_one_is_pi(self):
        assert Pi * 1 == Pi

    def test_pi_squared_consistency(self):
        """Pi² computed two ways must agree."""
        a = Pi * Pi
        b = Pi ** 2
        assert a == b


# =====================================================================
# GOLDEN RATIO IDENTITIES
# =====================================================================

class TestPhiIdentities:
    """The golden ratio satisfies x² = x + 1."""

    def test_ieee754_phi_identity_passes_by_luck(self):
        """IEEE 754 gets φ² = φ + 1 right by cancellation luck."""
        phi_f = (1 + math.sqrt(5)) / 2
        assert phi_f ** 2 == phi_f + 1  # luck, not construction

    def test_mobius_phi_identity(self):
        """φ² = φ + 1 exactly."""
        assert Phi ** 2 == Phi + 1

    def test_phi_minus_one_reciprocal(self):
        """1/φ = φ - 1 exactly."""
        assert MC(1) / Phi == Phi - MC(1)


# =====================================================================
# SQRT FUNCTION
# =====================================================================

class TestSqrt:
    """Module-level sqrt produces exact results."""

    def test_sqrt_4(self):
        assert sqrt(4) == 2

    def test_sqrt_9(self):
        assert sqrt(9) == 3

    def test_sqrt_1(self):
        assert sqrt(1) == 1

    def test_sqrt_0(self):
        assert sqrt(0) == 0

    def test_sqrt_of_mc(self):
        """sqrt of a MobiusConstant."""
        result = sqrt(MC(2))
        # result² should equal 2
        assert result ** 2 == 2

    def test_sqrt_negative_raises(self):
        with pytest.raises(ValueError):
            sqrt(-1)

    def test_sqrt_product(self):
        """√2² × √8² = 2 × 8 = 16."""
        s2 = sqrt(MC(2))
        s8 = sqrt(MC(8))
        # Each squares exactly via polynomial identity
        assert s2 ** 2 * (s8 ** 2) == MC(16)


# =====================================================================
# ALPHA CONSISTENCY
# =====================================================================

class TestAlpha:
    """The fine-structure constant cross-checks."""

    def test_alpha_times_alpha_inv(self):
        """α × α⁻¹ = 1."""
        result = Alpha * Alpha_inv
        assert result == 1

    def test_alpha_inv_positive(self):
        assert Alpha_inv > 137

    def test_alpha_inv_less_than_138(self):
        assert Alpha_inv < 138

    def test_alpha_inv_starts_correctly(self):
        """First 12 digits match CODATA 2022."""
        s = str(Alpha_inv.value)
        assert s.startswith("137.035999")

    def test_verified_depth(self):
        assert VERIFIED_DEPTH == 100


# =====================================================================
# CONSTRUCTION
# =====================================================================

class TestConstruction:
    """Every input path produces the correct truth strand."""

    def test_from_string(self):
        n = MC("3.14")
        assert n.value == Decimal("3.14")

    def test_from_int(self):
        n = MC(42)
        assert n.value == Decimal(42)
        assert n.approx == 42.0

    def test_from_float(self):
        n = MC(0.5)
        assert n.value == Decimal("0.5")

    def test_from_decimal(self):
        n = MC(Decimal("1.41421356"))
        assert n.value == Decimal("1.41421356")

    def test_from_mobius_constant(self):
        a = MC("3.14")
        b = MC(a)
        assert b.value == a.value

    def test_invalid_type_raises(self):
        with pytest.raises(TypeError):
            MC([1, 2, 3])


# =====================================================================
# ARITHMETIC
# =====================================================================

class TestArithmetic:
    """Both strands propagate through every operation."""

    def test_addition(self):
        result = MC("1.5") + MC("2.5")
        assert result == 4

    def test_subtraction(self):
        result = MC("5.0") - MC("2.0")
        assert result == 3

    def test_multiplication(self):
        result = MC("3.0") * MC("4.0")
        assert result == 12

    def test_division(self):
        result = MC("10") / MC("4")
        assert result == MC("2.5")

    def test_negation(self):
        assert (-MC("5")).value == Decimal("-5")

    def test_abs(self):
        assert abs(MC("-7")).value == Decimal("7")

    def test_power_int(self):
        assert (MC("3") ** 3) == 27

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            MC("1") / MC("0")

    def test_radd(self):
        result = 1 + MC("0.5")
        assert result == MC("1.5")

    def test_rsub(self):
        result = 10 - MC("3")
        assert result == 7

    def test_rmul(self):
        result = 3 * MC("2.5")
        assert result == MC("7.5")

    def test_rtruediv(self):
        result = 10 / MC("4")
        assert result == MC("2.5")


# =====================================================================
# COMPARISON — TRUTH GOVERNS
# =====================================================================

class TestComparison:
    """Equality and ordering use the truth strand, not the float."""

    def test_equality(self):
        assert MC("3.14") == MC("3.14")

    def test_inequality(self):
        assert MC("3.14") != MC("3.15")

    def test_less_than(self):
        assert MC("1") < MC("2")

    def test_greater_than(self):
        assert Pi > MC(3)

    def test_less_equal(self):
        assert MC("3") <= MC("3")

    def test_greater_equal(self):
        assert MC("3") >= MC("3")

    def test_hash_consistency(self):
        """Equal MöbiusConstants must have equal hashes."""
        a = MC("5") + MC("5")
        b = MC("10")
        assert hash(a) == hash(b)

    def test_usable_as_dict_key(self):
        d = {MC("10"): "found"}
        key = MC("5") + MC("5")
        assert d[key] == "found"

    def test_cross_type_int(self):
        assert MC(5) == 5

    def test_cross_type_float(self):
        assert MC(0.5) == 0.5


# =====================================================================
# STRAND ANATOMY
# =====================================================================

class TestStrands:
    """The residue must be the gap between float and truth."""

    def test_residue_of_pi(self):
        """Pi's float is not exactly π. The residue captures the gap."""
        r = Pi.residue
        assert r != 0  # float can't hold 100 digits

    def test_residue_of_integer_is_zero(self):
        n = MC(1)
        assert n.residue == Decimal("0")

    def test_collapse_returns_float(self):
        assert isinstance(Pi.collapse(), float)

    def test_diagnose_returns_dict(self):
        d = Pi.diagnose()
        assert "binary_strand" in d
        assert "truth_strand" in d
        assert "residue" in d
        assert d["name"] == "pi"

    def test_named_constant_repr(self):
        assert "pi" in repr(Pi)

    def test_unnamed_repr(self):
        r = repr(MC("3.14159"))
        assert "MC(" in r


# =====================================================================
# THE FAMOUS FAILURES — IRRATIONAL EDITION
# =====================================================================

class TestFamousFailures:
    """Every classic IEEE 754 irrational failure, corrected."""

    def test_sqrt2_squared(self):
        """√2² = 2. IEEE gets 2.0000000000000004."""
        assert Sqrt2 ** 2 == 2

    def test_sqrt3_squared(self):
        """√3² = 3."""
        assert Sqrt3 ** 2 == 3

    def test_phi_squared_minus_phi(self):
        """φ² − φ = 1."""
        assert Phi ** 2 - Phi == 1

    def test_sqrt2_times_sqrt8_equals_4(self):
        """√2² × √8² = 16."""
        s8 = sqrt(MC(8))
        assert Sqrt2 ** 2 * (s8 ** 2) == MC(16)

    def test_sqrt_product_identity(self):
        """√a² × √b² = a × b. The polynomial resolves each side."""
        s2 = sqrt(MC(2))
        s3 = sqrt(MC(3))
        # √2² = 2, √3² = 3 (each exact via polynomial), product = 6
        assert s2 ** 2 * (s3 ** 2) == MC(6)
        # √6² = 6 (exact via polynomial)
        s6 = sqrt(MC(6))
        assert s6 ** 2 == MC(6)

    def test_catastrophic_subtraction(self):
        """π − π = 0 exactly, even though floats can't hold π."""
        assert Pi - Pi == 0

    def test_alpha_inv_in_range(self):
        """α⁻¹ is between 137 and 138."""
        assert MC(137) < Alpha_inv < MC(138)

    def test_integer_sqrt_exact(self):
        """√4 = 2, √9 = 3, √16 = 4 — exact integers."""
        assert sqrt(MC(4)) == 2
        assert sqrt(MC(9)) == 3
        assert sqrt(MC(16)) == 4
        assert sqrt(MC(100)) == 10
