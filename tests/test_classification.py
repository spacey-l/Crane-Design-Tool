"""Duty classification tests. Worked examples are hand-checked in
docs/worked-examples/M1-duty-classification.md."""

import pytest

from crane_engine import Q_
from crane_engine.classification import (
    LiftType,
    OperatingPattern,
    ScheduleOfLifts,
    classify_direct,
    classify_from_pattern,
    classify_from_schedule,
    group,
    running_time_class,
    spectrum_class,
    utilisation_class,
)


def example_schedule(attachment_t=0.0):
    h = Q_(6, "m")
    return ScheduleOfLifts(
        rated_capacity=Q_(20, "t"),
        lift_types=[
            LiftType("Full load", Q_(20, "t"), 5, h),
            LiftType("Half load", Q_(10, "t"), 20, h),
            LiftType("Quarter load", Q_(5, "t"), 25, h),
        ],
        working_days_per_year=240,
        design_life_years=20,
        hoist_speed=Q_(4, "m/min"),
        fixed_attachment_mass=Q_(attachment_t, "t"),
    )


# --- Worked example 1: schedule of lifts ---------------------------------------------

def test_schedule_structure():
    r = classify_from_schedule(example_schedule())
    assert r.total_cycles == pytest.approx(240_000)
    assert r.k_q == pytest.approx(0.1578125)
    assert (r.u_class, r.q_class, r.a_group) == (4, 2, 4)


def test_schedule_hoist():
    r = classify_from_schedule(example_schedule())
    assert r.hoist_running_hours == pytest.approx(12_000)
    assert r.k_m == pytest.approx(0.1578125)
    assert (r.t_class, r.l_class, r.m_group, r.fem_group) == (6, 2, 6, "3m")
    assert r.summary() == "A4 (U4, Q2) hoist M6 / FEM 3m (T6, L2)"


def test_schedule_hoist_with_hook_block():
    r = classify_from_schedule(example_schedule(attachment_t=1.0))
    assert r.k_m == pytest.approx(0.169150, abs=1e-6)
    assert r.k_q == pytest.approx(0.1578125)  # structure uses net loads only


def test_schedule_without_hoist_data_gives_note():
    s = example_schedule()
    s.hoist_speed = None
    r = classify_from_schedule(s)
    assert r.m_group is None and r.notes


def test_schedule_load_over_capacity_rejected():
    s = example_schedule()
    s.lift_types.append(LiftType("Overload", Q_(25, "t"), 1))
    with pytest.raises(ValueError):
        classify_from_schedule(s)


# --- Worked example 2: operating pattern (sits on class boundaries) --------------------

def test_pattern():
    r = classify_from_pattern(OperatingPattern(
        cycles_per_hour=10, hours_per_day=8, working_days_per_year=250,
        design_life_years=25, load_spectrum="moderate", hoist_hours_per_day=2))
    assert r.total_cycles == pytest.approx(500_000)
    assert (r.u_class, r.q_class, r.a_group) == (5, 2, 5)
    assert r.hoist_running_hours == pytest.approx(12_500)
    assert (r.t_class, r.l_class, r.m_group) == (6, 2, 6)


# --- Direct statement by client ----------------------------------------------------------

def test_direct_fem_group():
    r = classify_direct(a_group=5, fem_group="2m")
    assert r.m_group == 5 and r.u_class is None


def test_direct_mismatch_rejected():
    with pytest.raises(ValueError):
        classify_direct(a_group=5, m_group=4, fem_group="2m")


# --- Table look-ups ------------------------------------------------------------------------

@pytest.mark.parametrize("cycles, expected", [
    (16_000, 0), (16_001, 1), (250_000, 4), (250_001, 5), (4_000_000, 8), (4_000_001, 9)])
def test_u_class_limits(cycles, expected):
    assert utilisation_class(cycles) == expected


@pytest.mark.parametrize("factor, expected", [
    (0.05, 1), (0.125, 1), (0.126, 2), (0.5, 3), (1.0, 4)])
def test_spectrum_class_limits(factor, expected):
    assert spectrum_class(factor) == expected


def test_spectrum_out_of_range():
    with pytest.raises(ValueError):
        spectrum_class(1.2)


@pytest.mark.parametrize("hours, expected", [(200, 0), (201, 1), (50_000, 8), (50_001, 9)])
def test_t_class_limits(hours, expected):
    assert running_time_class(hours) == expected


@pytest.mark.parametrize("spectrum, utilisation, expected", [
    (1, 0, 1), (1, 9, 8), (2, 5, 5), (3, 1, 2), (4, 0, 2), (4, 6, 8)])
def test_group_table(spectrum, utilisation, expected):
    assert group(spectrum, utilisation) == expected
