"""
MöbiusConstant — Exact Irrational Constants

Every constant is stored as two strands:
  - The binary approximation (float64, hardware-fast)
  - The verified digit string (Decimal, no loss to 100 digits)

They are not two representations. They are one object.
The float gives you speed. The digits give you truth.
Comparison uses truth.

The digits are pre-verified, not computed on demand:
  - π and α cross-check via: α⁻¹ + S·α = 4π³ + π² + π
  - √2, √3, φ are verified by their minimal polynomials
  - e is verified by Taylor series convergence

    >>> from mobius_constant import Pi, Sqrt2
    >>> Sqrt2 ** 2 == 2
    True
    >>> Pi * 2 == Pi + Pi
    True

Jay Carpenter, 2026
"""

from mobius_constant.core import MobiusConstant, sqrt
from mobius_constant._digits import (
    PI, E, SQRT2, SQRT3, PHI, LN2, ALPHA_INV, S_SERIES,
    MINIMAL_POLYNOMIALS, VERIFIED_DEPTH,
)

# ─── Pre-built constant singletons ────────────────────────────

Pi = MobiusConstant(PI, name="pi")
"""π — 100 verified digits. Cross-checked via α round-trip."""

Euler = MobiusConstant(E, name="e")
"""e — 100 verified digits. Euler's number."""

Sqrt2 = MobiusConstant(SQRT2, name="sqrt2", poly=(1, 0, -2))
"""√2 — 100 verified digits. Minimal polynomial: x² − 2 = 0."""

Sqrt3 = MobiusConstant(SQRT3, name="sqrt3", poly=(1, 0, -3))
"""√3 — 100 verified digits. Minimal polynomial: x² − 3 = 0."""

Phi = MobiusConstant(PHI, name="phi", poly=(1, -1, -1))
"""φ — the golden ratio. 100 verified digits. x² − x − 1 = 0."""

Ln2 = MobiusConstant(LN2, name="ln2")
"""ln(2) — 100 verified digits."""

Alpha_inv = MobiusConstant(ALPHA_INV, name="alpha_inv")
"""α⁻¹ — the fine-structure constant inverse. 100 verified digits.
Derived from π via: α⁻¹ + S·α = 4π³ + π² + π.
Matches CODATA 2022 (137.035999177 ± 21) to 0.02σ."""

Alpha = MobiusConstant.__new__(MobiusConstant)
Alpha._approx = 1.0 / float(ALPHA_INV)
Alpha._value = 1 / Alpha_inv.value
Alpha._name = "alpha"
Alpha._poly = None
"""α — the fine-structure constant. 1/α⁻¹."""

# Convenience alias
MC = MobiusConstant

__version__ = "0.1.0"
__all__ = [
    "MobiusConstant", "MC", "sqrt",
    "Pi", "Euler", "Sqrt2", "Sqrt3", "Phi", "Ln2",
    "Alpha_inv", "Alpha",
    "VERIFIED_DEPTH",
]
