import pint
import pytest

from crane_engine import Q_
from crane_engine.units import weight


def test_weight_of_150t_load():
    # Hand check: 150 000kg x 9.80665m/s2 = 1471.0kN
    assert weight(Q_(150, "t")).magnitude == pytest.approx(1470.9975)


def test_units_cannot_be_mixed():
    with pytest.raises(pint.DimensionalityError):
        Q_(10, "kN") + Q_(5, "m")
