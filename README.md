# mobius-constant

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19157585.svg)](https://doi.org/10.5281/zenodo.19157585)

**Exact irrational constants — `sqrt(2)**2 == 2`, by construction.**

```python
>>> from mobius_constant import Sqrt2, Pi, Phi
>>> Sqrt2 ** 2 == 2
True
>>> Pi + Pi == Pi * 2
True
>>> Phi ** 2 == Phi + 1
True
```

IEEE 754 gets all three wrong. MöbiusConstant gets them right.

## The Problem

```python
import math
math.sqrt(2) ** 2 == 2        # False  →  2.0000000000000004
math.sqrt(3) ** 2 == 3        # False
phi = (1 + math.sqrt(5)) / 2
phi ** 2 == phi + 1            # False  →  violates defining identity
```

Forty-one years of IEEE 754 and irrational constants still can't satisfy their own identities.

## The Fix

Every constant is stored as two strands:

| Strand | Role | Example (√2) |
|--------|------|-------------|
| **Binary** | `float64` — hardware-fast | `1.4142135623730951` |
| **Truth** | Verified digit string — 100 digits, no loss | `1.41421356237309504880168872420969807856...` |

The float gives you speed. The digits give you truth. Comparison uses truth.

The digits are **pre-verified, not computed on demand**:
- **π** and **α** cross-check via the SECS equation: α⁻¹ + S·α = 4π³ + π² + π
- **√2**, **√3**, **φ** are verified by their minimal polynomials
- **e** is verified by Taylor series convergence
- Round-trip π → α → π recovers all 100 digits exactly

## Install

```
pip install mobius-constant
```

Pure Python. One dependency: `mpmath` (for non-integer exponentiation only).

## Constants

| Constant | Symbol | Value | Identity |
|----------|--------|-------|----------|
| `Pi` | π | 3.14159265... | Cross-checked via α |
| `Euler` | e | 2.71828182... | Taylor convergence |
| `Sqrt2` | √2 | 1.41421356... | x² − 2 = 0 |
| `Sqrt3` | √3 | 1.73205080... | x² − 3 = 0 |
| `Phi` | φ | 1.61803398... | x² − x − 1 = 0 |
| `Ln2` | ln 2 | 0.69314718... | — |
| `Alpha_inv` | α⁻¹ | 137.035999... | SECS equation |
| `Alpha` | α | 0.00729735... | 1/α⁻¹ |

## Compute Your Own

```python
from mobius_constant import MC, sqrt

# Any square root, exact to 100 digits
s5 = sqrt(MC(5))
assert s5 ** 2 == 5

# Arithmetic propagates both strands
x = MC("1.41421356237309504880168872420969807856967187537694")
y = x * x  # truth strand: exact multiplication of all digits
```

## The α ↔ π Relationship

The fine-structure constant α and π are not circularly defined. Both are independently real:

- **π** — computable by Chudnovsky, Machin, BBP, dozens of algorithms
- **α** — measurable from electron g-2, cesium recoil, rubidium recoil

The equation α⁻¹ + S·α = 4π³ + π² + π is the **auditor**, not the definition. It validates that the digits of both constants are correct. If the round-trip fails at digit N, either your π or your α is wrong — the equation tells you where.

## See Also

- [mobius-number](https://github.com/JustNothingJay/mobius-number) — Complementary residue arithmetic for rationals (`0.1 + 0.2 == 0.3`)
- [mobius-integer](https://github.com/JustNothingJay/mobius-integer) — Möbius function and Dirichlet series in Rust

## License

MIT — Jay Carpenter, 2026
