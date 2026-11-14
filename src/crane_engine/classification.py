"""Duty classification of the crane structure and the hoist mechanism.

The duty can be given in one of three ways (decision D-016):

1. Direct: the client states the class (A-group, M-group or FEM group).
2. Operating pattern: cycles per hour, hours per day, days per year, design life
   and a load spectrum.
3. Schedule of lifts: a list of lift types, each with its load and number per day.

From the operating pattern or schedule of lifts the engine works out:

- the total number of working cycles C, which gives the class of utilisation U0–U9
- the load spectrum factor kQ = sum (Ci/C) x (Qi/Qmax)^3, which gives Q1–Q4
- the crane group A1–A8 from U and Q
- for the hoist, the total running time (T0–T9) and the spectrum factor km (L1–L4),
  which give the mechanism group M1–M8 and the FEM 9.511 group

Tables follow ISO 4301-1 / FEM 1.001. The EN 13001-1 stress history classes (S) used
for fatigue are worked out per detail in M3 (decision D-017).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from crane_engine.units import Q_, Quantity

# --- Class limits (upper limit of each class, inclusive) -------------------------------

#: Class of utilisation U0..U8 upper limits on total working cycles C. Above the last
#: limit is U9. ISO 4301-1 / FEM 1.001 Table T.2.1.2.2.
U_CLASS_LIMITS = (16_000, 32_000, 63_000, 125_000, 250_000, 500_000, 1_000_000,
                  2_000_000, 4_000_000)

#: Load spectrum class upper limits on kQ (cranes, Q1..Q4) and km (mechanisms, L1..L4).
#: ISO 4301-1 / FEM 1.001 Tables T.2.1.2.3 and T.2.1.3.3.
SPECTRUM_CLASS_LIMITS = (0.125, 0.25, 0.5, 1.0)

#: Mechanism class of utilisation T0..T8 upper limits on total running time in hours.
#: Above the last limit is T9. ISO 4301-1 / FEM 1.001 Table T.2.1.3.2.
T_CLASS_LIMITS = (200, 400, 800, 1_600, 3_200, 6_300, 12_500, 25_000, 50_000)

#: Group number by spectrum class (rows 1..4) and utilisation class (columns 0..9).
#: The same table gives crane groups A (from Q and U) and mechanism groups M (from L
#: and T). ISO 4301-1 / FEM 1.001 Tables T.2.1.2.4 and T.2.1.3.4.
GROUP_TABLE = {
    1: (1, 1, 1, 2, 3, 4, 5, 6, 7, 8),
    2: (1, 1, 2, 3, 4, 5, 6, 7, 8, 8),
    3: (1, 2, 3, 4, 5, 6, 7, 8, 8, 8),
    4: (2, 3, 4, 5, 6, 7, 8, 8, 8, 8),
}

#: FEM 9.511 hoist mechanism groups, used by hoist makers such as Podem.
FEM_GROUP_BY_M = {1: "1Dm", 2: "1Cm", 3: "1Bm", 4: "1Am", 5: "2m", 6: "3m", 7: "4m",
                  8: "5m"}
M_BY_FEM_GROUP = {fem: m for m, fem in FEM_GROUP_BY_M.items()}

#: Load spectrum described in words (ISO 4301-1 / FEM 1.001), with the nominal factor
#: at the top of each class. Used when no load distribution is known.
SPECTRUM_BY_NAME = {"light": 0.125, "moderate": 0.25, "heavy": 0.5, "very heavy": 1.0}


# --- Small look-up helpers ----------------------------------------------------------

def _class_index(value: float, limits: tuple) -> int:
    """Index of the first class whose upper limit is not exceeded."""
    for index, limit in enumerate(limits):
        if value <= limit:
            return index
    return len(limits)


def utilisation_class(total_cycles: float) -> int:
    """U class number (0–9) from total working cycles."""
    return _class_index(total_cycles, U_CLASS_LIMITS)


def spectrum_class(factor: float) -> int:
    """Q or L class number (1–4) from a spectrum factor kQ or km."""
    if not 0 < factor <= 1:
        raise ValueError(f"Spectrum factor must be in (0, 1], got {factor}")
    return _class_index(factor, SPECTRUM_CLASS_LIMITS) + 1


def running_time_class(hours: float) -> int:
    """T class number (0–9) from total running time in hours."""
    return _class_index(hours, T_CLASS_LIMITS)


def group(spectrum: int, utilisation: int) -> int:
    """A or M group number (1–8) from the spectrum and utilisation classes."""
    return GROUP_TABLE[spectrum][utilisation]


# --- Inputs --------------------------------------------------------------------------

@dataclass
class LiftType:
    """One line of a schedule of lifts."""

    description: str
    load: Quantity          # net hoist load, e.g. Q_(10, "t")
    lifts_per_day: float
    hoist_height: Quantity | None = None   # hook travel per lift; needed for the hoist


@dataclass
class ScheduleOfLifts:
    rated_capacity: Quantity
    lift_types: list[LiftType]
    working_days_per_year: float
    design_life_years: float
    hoist_speed: Quantity | None = None
    #: Mass that always hangs on the ropes (hook block, fixed attachments). Added to
    #: every load for the hoist spectrum only (assumption, decision D-018).
    fixed_attachment_mass: Quantity = field(default_factory=lambda: Q_(0, "t"))


@dataclass
class OperatingPattern:
    cycles_per_hour: float
    hours_per_day: float
    working_days_per_year: float
    design_life_years: float
    #: Load spectrum: a factor kQ in (0, 1] or one of "light", "moderate", "heavy",
    #: "very heavy".
    load_spectrum: float | str
    #: Hoist running hours per day; if omitted, no hoist group is worked out.
    hoist_hours_per_day: float | None = None
    #: Hoist spectrum factor km; defaults to the crane load spectrum.
    hoist_spectrum: float | str | None = None


# --- Result --------------------------------------------------------------------------

@dataclass
class DutyClassification:
    source: str                      # "direct", "operating pattern" or "schedule of lifts"
    a_group: int
    u_class: int | None = None
    q_class: int | None = None
    total_cycles: float | None = None
    k_q: float | None = None
    m_group: int | None = None
    t_class: int | None = None
    l_class: int | None = None
    hoist_running_hours: float | None = None
    k_m: float | None = None
    notes: list[str] = field(default_factory=list)

    @property
    def fem_group(self) -> str | None:
        return FEM_GROUP_BY_M[self.m_group] if self.m_group else None

    def summary(self) -> str:
        parts = [f"A{self.a_group}"]
        if self.u_class is not None:
            parts.append(f"(U{self.u_class}, Q{self.q_class})")
        if self.m_group:
            parts.append(f"hoist M{self.m_group} / FEM {self.fem_group}")
            if self.t_class is not None:
                parts.append(f"(T{self.t_class}, L{self.l_class})")
        return " ".join(parts)


# --- Classification routes -------------------------------------------------------------

def _spectrum_factor(spectrum: float | str) -> float:
    if isinstance(spectrum, str):
        try:
            return SPECTRUM_BY_NAME[spectrum.lower()]
        except KeyError:
            raise ValueError(f"Unknown load spectrum '{spectrum}'") from None
    return float(spectrum)


def classify_direct(a_group: int, m_group: int | None = None,
                    fem_group: str | None = None) -> DutyClassification:
    """Record a class stated by the client."""
    if not 1 <= a_group <= 8:
        raise ValueError(f"A-group must be 1–8, got {a_group}")
    if fem_group is not None:
        m_from_fem = M_BY_FEM_GROUP[fem_group]
        if m_group is not None and m_group != m_from_fem:
            raise ValueError(f"M{m_group} does not match FEM {fem_group} (M{m_from_fem})")
        m_group = m_from_fem
    result = DutyClassification(source="direct", a_group=a_group, m_group=m_group)
    result.notes.append("Class stated by client; U and Q classes not known. Fatigue "
                        "checks will need an assumed load history.")
    return result


def classify_from_pattern(pattern: OperatingPattern) -> DutyClassification:
    """Classify from cycles per hour, hours per day, days per year and design life."""
    days = pattern.working_days_per_year * pattern.design_life_years
    total_cycles = pattern.cycles_per_hour * pattern.hours_per_day * days
    k_q = _spectrum_factor(pattern.load_spectrum)
    u, q = utilisation_class(total_cycles), spectrum_class(k_q)
    result = DutyClassification(source="operating pattern", a_group=group(q, u),
                                u_class=u, q_class=q, total_cycles=total_cycles, k_q=k_q)
    if pattern.hoist_hours_per_day is not None:
        hours = pattern.hoist_hours_per_day * days
        k_m = _spectrum_factor(pattern.hoist_spectrum if pattern.hoist_spectrum is not None
                               else pattern.load_spectrum)
        _set_hoist(result, hours, k_m)
    return result


def classify_from_schedule(schedule: ScheduleOfLifts) -> DutyClassification:
    """Classify from a schedule of lifts."""
    if not schedule.lift_types:
        raise ValueError("Schedule of lifts is empty")
    days = schedule.working_days_per_year * schedule.design_life_years
    rated = schedule.rated_capacity.to("t").magnitude
    for lift in schedule.lift_types:
        if lift.load.to("t").magnitude > rated:
            raise ValueError(f"'{lift.description}' exceeds the rated capacity")

    # Structure: kQ = sum (Ci / C) x (Qi / Qmax)^3, using net loads.
    lifts_per_day = sum(lift.lifts_per_day for lift in schedule.lift_types)
    total_cycles = lifts_per_day * days
    k_q = sum((lift.lifts_per_day / lifts_per_day) * (lift.load.to("t").magnitude / rated) ** 3
              for lift in schedule.lift_types)
    u, q = utilisation_class(total_cycles), spectrum_class(k_q)
    result = DutyClassification(source="schedule of lifts", a_group=group(q, u),
                                u_class=u, q_class=q, total_cycles=total_cycles, k_q=k_q)

    # Hoist: running time = up and down the hoist height for every lift (D-018).
    if schedule.hoist_speed is None or any(lift.hoist_height is None
                                           for lift in schedule.lift_types):
        result.notes.append("Hoist group not worked out: hoist speed or hoist heights "
                            "missing.")
        return result
    dead = schedule.fixed_attachment_mass.to("t").magnitude
    hours_per_day = []
    for lift in schedule.lift_types:
        time_per_lift = (2 * lift.hoist_height / schedule.hoist_speed).to("h").magnitude
        hours_per_day.append(time_per_lift * lift.lifts_per_day)
    daily_hours = sum(hours_per_day)
    k_m = sum((h / daily_hours) * ((lift.load.to("t").magnitude + dead) / (rated + dead)) ** 3
              for h, lift in zip(hours_per_day, schedule.lift_types, strict=True))
    _set_hoist(result, daily_hours * days, k_m)
    return result


def _set_hoist(result: DutyClassification, hours: float, k_m: float) -> None:
    t, ell = running_time_class(hours), spectrum_class(k_m)
    result.hoist_running_hours = hours
    result.k_m = k_m
    result.t_class = t
    result.l_class = ell
    result.m_group = group(ell, t)
