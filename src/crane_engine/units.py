"""Shared unit registry.

Every physical quantity in the engine carries its units, so kN cannot be mixed
with t, or mm with m, by mistake. All modules must import ``ureg``/``Q_`` from
here (one registry per program is a pint requirement).
"""

import pint

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity
Quantity = pint.Quantity  # type used in annotations

# Standard gravity, used to convert mass (t) to weight force (kN).
G = Q_(9.80665, "m/s**2")


def weight(mass: pint.Quantity) -> pint.Quantity:
    """Weight force of a mass under standard gravity, in kN."""
    return (mass * G).to("kN")
