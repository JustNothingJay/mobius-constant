"""
MöbiusConstant core implementation.

A constant that carries its own truth. Two strands — the binary
approximation and the verified digit string — coexist as one object.

The float gives you speed.
The digits give you truth.
Comparison uses truth.

The digits are not computed on demand. They are pre-verified values,
stored as strings, confirmed by independent methods. The α↔π
round-trip is the auditor, not the definition.

For algebraic constants (√2, √3, φ), the minimal polynomial provides
a structural proof that the digits are correct. For transcendentals
(π, e), independent algorithms cross-check the digits.
"""

from __future__ import annotations

from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from typing import Optional, Tuple, Union

# Set decimal precision high enough for 100-digit arithmetic
getcontext().prec = 120
getcontext().rounding = ROUND_HALF_EVEN


class MobiusConstant:
    """
    An irrational constant that carries its own truth.

    Internally:
      _approx : float      — the binary strand (fast, lossy)
      _value  : Decimal     — the truth strand (verified digits)
      _name   : str | None  — identity ("pi", "sqrt2", etc.)
      _poly   : tuple|None  — minimal polynomial coefficients (algebraic only)

    The float is the shadow. The Decimal is the substance.
    Comparison always uses the Decimal.
    """

    __slots__ = ('_approx', '_value', '_name', '_poly')

    def __init__(
        self,
        value: Union[str, float, int, Decimal, 'MobiusConstant'],
        *,
        name: Optional[str] = None,
        poly: Optional[Tuple[int, ...]] = None,
    ):
        if isinstance(value, MobiusConstant):
            self._approx = value._approx
            self._value = value._value
            self._name = value._name
            self._poly = value._poly
        elif isinstance(value, Decimal):
            self._value = value
            self._approx = float(value)
            self._name = name
            self._poly = poly
        elif isinstance(value, str):
            self._value = Decimal(value)
            self._approx = float(self._value)
            self._name = name
            self._poly = poly
        elif isinstance(value, int):
            self._value = Decimal(value)
            self._approx = float(value)
            self._name = name
            self._poly = poly
        elif isinstance(value, float):
            self._value = Decimal(str(value))
            self._approx = value
            self._name = name
            self._poly = poly
        else:
            raise TypeError(f"Cannot create MobiusConstant from {type(value)}")

    # ------------------------------------------------------------------
    # Strand access
    # ------------------------------------------------------------------

    @property
    def approx(self) -> float:
        """The binary strand — hardware-fast, carries rounding error."""
        return self._approx

    @property
    def value(self) -> Decimal:
        """The truth strand — verified digits."""
        return self._value

    @property
    def name(self) -> Optional[str]:
        """Identity label, if this is a named constant."""
        return self._name

    @property
    def poly(self) -> Optional[Tuple[int, ...]]:
        """Minimal polynomial (algebraic constants only)."""
        return self._poly

    @property
    def residue(self) -> Decimal:
        """The gap between the float shadow and the truth."""
        return self._value - Decimal(str(self._approx))

    # ------------------------------------------------------------------
    # Collapse
    # ------------------------------------------------------------------

    def collapse(self) -> float:
        """Return the best float representation of the truth strand."""
        return float(self._value)

    # ------------------------------------------------------------------
    # Arithmetic — both strands propagate
    # ------------------------------------------------------------------

    def __add__(self, other: Union[MobiusConstant, int, float, str]) -> MobiusConstant:
        other = _coerce(other)
        return MobiusConstant._from_parts(
            self._approx + other._approx,
            self._value + other._value,
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = _coerce(other)
        return MobiusConstant._from_parts(
            self._approx - other._approx,
            self._value - other._value,
        )

    def __rsub__(self, other):
        other = _coerce(other)
        return other.__sub__(self)

    def __mul__(self, other):
        other = _coerce(other)
        # Algebraic identity: if both operands are the same algebraic
        # constant, x*x = x² which the polynomial resolves exactly.
        if (self._poly and other._poly
                and self._name and self._name == other._name
                and len(self._poly) == 3):
            return _poly_square(self)
        return MobiusConstant._from_parts(
            self._approx * other._approx,
            self._value * other._value,
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = _coerce(other)
        if other._value == 0:
            raise ZeroDivisionError("MobiusConstant division by zero")
        # Algebraic identity: 1/x for degree-2 polynomial ax²+bx+c=0
        # gives 1/x = -(ax+b)/c
        if (other._poly and len(other._poly) == 3
                and self._value == Decimal(1)):
            return _poly_reciprocal(other)
        return MobiusConstant._from_parts(
            self._approx / other._approx,
            self._value / other._value,
        )

    def __rtruediv__(self, other):
        other = _coerce(other)
        return other.__truediv__(self)

    def __neg__(self):
        return MobiusConstant._from_parts(
            -self._approx,
            -self._value,
        )

    def __abs__(self):
        return MobiusConstant._from_parts(
            abs(self._approx),
            abs(self._value),
        )

    def __pow__(self, exp):
        if isinstance(exp, int):
            # Algebraic identity: x² resolved via minimal polynomial
            if exp == 2 and self._poly and len(self._poly) == 3:
                return _poly_square(self)
            return MobiusConstant._from_parts(
                self._approx ** exp,
                self._value ** exp,
            )
        if isinstance(exp, MobiusConstant):
            # Decimal doesn't support arbitrary Decimal exponents natively.
            # Use ln/exp via mpmath for the truth strand.
            return _pow_decimal(self, exp)
        return NotImplemented

    # ------------------------------------------------------------------
    # Square root — special case, returns verified result for known constants
    # ------------------------------------------------------------------

    def sqrt(self) -> MobiusConstant:
        """
        Exact square root using Newton's method on the truth strand.
        For integer inputs, this produces the algebraic constant (e.g. √2).
        """
        return _sqrt_decimal(self)

    # ------------------------------------------------------------------
    # Comparison — the truth strand governs, always
    # ------------------------------------------------------------------

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            other = _coerce(other)
        if not isinstance(other, MobiusConstant):
            return NotImplemented
        return self._value == other._value

    def __ne__(self, other):
        if isinstance(other, (int, float)):
            other = _coerce(other)
        if not isinstance(other, MobiusConstant):
            return NotImplemented
        return self._value != other._value

    def __lt__(self, other):
        other = _coerce(other)
        return self._value < other._value

    def __le__(self, other):
        other = _coerce(other)
        return self._value <= other._value

    def __gt__(self, other):
        other = _coerce(other)
        return self._value > other._value

    def __ge__(self, other):
        other = _coerce(other)
        return self._value >= other._value

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self):
        if self._name:
            return f"MC({self._name})"
        # Show enough digits to be useful, not all 100
        s = str(self._value)
        if len(s) > 22:
            s = s[:20] + "..."
        return f"MC('{s}')"

    def __str__(self):
        return str(self._value)

    def __float__(self):
        return float(self._value)

    def __int__(self):
        return int(self._value)

    def __hash__(self):
        return hash(self._value)

    # ------------------------------------------------------------------
    # Diagnostic
    # ------------------------------------------------------------------

    def diagnose(self) -> dict:
        """Return both strands, the residue, and identity info."""
        return {
            "binary_strand": self._approx,
            "truth_strand": str(self._value),
            "residue": str(self.residue),
            "name": self._name,
            "poly": self._poly,
            "collapsed": self.collapse(),
        }

    # ------------------------------------------------------------------
    # Internal factory
    # ------------------------------------------------------------------

    @classmethod
    def _from_parts(cls, approx: float, value: Decimal, name=None, poly=None):
        obj = cls.__new__(cls)
        obj._approx = approx
        obj._value = value
        obj._name = name
        obj._poly = poly
        return obj


# ======================================================================
# Module-level helpers
# ======================================================================

def _coerce(value) -> MobiusConstant:
    """Convert a raw value into a MobiusConstant."""
    if isinstance(value, MobiusConstant):
        return value
    return MobiusConstant(value)


def _poly_square(mc: MobiusConstant) -> MobiusConstant:
    """
    Compute x² using the minimal polynomial identity.

    For a degree-2 polynomial ax² + bx + c = 0:
      x² = -(bx + c) / a

    This is exact by construction — the polynomial IS the truth.
    √2² = 2, φ² = φ + 1, etc.
    """
    a, b, c = [Decimal(coef) for coef in mc._poly]
    # x² = -(b*x + c) / a
    result_value = -(b * mc._value + c) / a
    result_approx = -(float(b) * mc._approx + float(c)) / float(a)
    return MobiusConstant._from_parts(result_approx, result_value)


def _poly_reciprocal(mc: MobiusConstant) -> MobiusConstant:
    """
    Compute 1/x using the minimal polynomial identity.

    For a degree-2 polynomial ax² + bx + c = 0:
      ax² + bx + c = 0  →  x(ax + b) = -c  →  1/x = -(ax + b) / c

    This is exact by construction.
    1/φ = φ − 1, etc.
    """
    a, b, c = [Decimal(coef) for coef in mc._poly]
    # 1/x = -(a*x + b) / c
    result_value = -(a * mc._value + b) / c
    result_approx = -(float(a) * mc._approx + float(b)) / float(c)
    return MobiusConstant._from_parts(result_approx, result_value)


def _sqrt_decimal(mc: MobiusConstant) -> MobiusConstant:
    """
    Compute square root to full Decimal precision via Newton's method.
    Pure arithmetic on the truth strand — no floats consulted.
    """
    import math
    x = mc._value

    if x < 0:
        raise ValueError("Cannot take square root of negative MobiusConstant")
    if x == 0:
        return MobiusConstant(0)

    # Newton's method: x_{n+1} = (x_n + S/x_n) / 2
    # Start from float approximation
    guess = Decimal(str(math.sqrt(float(x))))
    two = Decimal(2)
    for _ in range(200):  # quadratic convergence
        new_guess = (guess + x / guess) / two
        if new_guess == guess:
            break
        guess = new_guess

    # If the input is an integer or exact rational, tag the result
    # with its minimal polynomial so that squaring is exact.
    # sqrt(n) has minimal polynomial x² - n = 0 → poly = (1, 0, -n)
    int_val = None
    if x == int(x):
        int_val = int(x)
        # Check if it's a perfect square first
        isqrt = int(Decimal(int_val).sqrt())
        if isqrt * isqrt == int_val:
            return MobiusConstant(isqrt)

    result = MobiusConstant._from_parts(
        math.sqrt(mc._approx),
        guess,
        poly=(1, 0, -int_val) if int_val is not None else None,
    )
    return result


def _pow_decimal(base: MobiusConstant, exp: MobiusConstant) -> MobiusConstant:
    """
    General exponentiation for non-integer exponents.
    Uses float for speed strand, mpmath for truth strand.
    """
    from mpmath import mp, mpf, power, nstr

    old_dps = mp.dps
    mp.dps = 120
    try:
        base_mp = mpf(str(base._value))
        exp_mp = mpf(str(exp._value))
        result_mp = power(base_mp, exp_mp)
        result_str = nstr(result_mp, 100)
    finally:
        mp.dps = old_dps

    return MobiusConstant._from_parts(
        base._approx ** exp._approx,
        Decimal(result_str),
    )


def sqrt(value) -> MobiusConstant:
    """Module-level sqrt: exact square root via the truth strand."""
    return _coerce(value).sqrt()
