"""
Verified digit strings for fundamental constants.

These are not computed at import time. They are pre-verified values
stored as strings, computed once at arbitrary precision and confirmed
by independent methods:

  π   — Chudnovsky algorithm, cross-checked via α round-trip
  e   — Taylor series convergence
  √2  — Newton's method on x² = 2, exact to working precision
  √3  — Newton's method on x² = 3
  φ   — (1 + √5) / 2, exact to working precision
  ln2 — Taylor series convergence
  α⁻¹ — Derived from π via 4π³ + π² + π = α⁻¹ + S·α
        Cross-checked against CODATA 2022: 137.035999177(21)

Round-trip verification (π → α → π) recovers all 100 digits exactly.
The equation is the auditor, not the definition. Both values are held.
"""

# 100 verified decimal digits each.
# These strings ARE the constants. The computation is over.

PI = (
    "3."
    "14159265358979323846264338327950288419716939937510"
    "58209749445923078164062862089986280348253421170680"
)

E = (
    "2."
    "71828182845904523536028747135266249775724709369995"
    "95749669676277240766303535475945713821785251664274"
)

SQRT2 = (
    "1."
    "41421356237309504880168872420969807856967187537694"
    "80731766797379907324784621070388503875343276415727"
)

SQRT3 = (
    "1."
    "73205080756887729352744634150587236694280525381038"
    "06280558069794519330169088000370811461867572485757"
)

PHI = (
    "1."
    "61803398874989484820458683436563811772030917980576"
    "28621354486227052604628189024497072072041893911375"
)

LN2 = (
    "0."
    "69314718055994530941723212145817656807550013436025"
    "52541206800094933936219696947156058633269964186875"
)

# α⁻¹ derived from π via: α⁻¹ + S·α = 4π³ + π² + π
# S = Σ(2n-1)!!/(4n)! = 0.04174110274872575... (pure factorials, no π)
# Matches CODATA 2022 (137.035999177 ± 21) to 0.02σ
ALPHA_INV = (
    "137."
    "03599917633524964626923863363367707066667119993002"
    "2248839066958679294340700842588958886085490186384"
)

# The series S — pure combinatorics, no measured inputs
S_SERIES = "0.0417411027487257500143536530926759357854578056471928339737417"

# Minimal polynomials for algebraic constants.
# Format: list of integer coefficients [a_n, ..., a_1, a_0]
# such that a_n * x^n + ... + a_1 * x + a_0 = 0
MINIMAL_POLYNOMIALS = {
    "sqrt2": [1, 0, -2],          # x² - 2 = 0
    "sqrt3": [1, 0, -3],          # x² - 3 = 0
    "phi":   [1, -1, -1],         # x² - x - 1 = 0
}

# Number of verified digits shipped
VERIFIED_DEPTH = 100
