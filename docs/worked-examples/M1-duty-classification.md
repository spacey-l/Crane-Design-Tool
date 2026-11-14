# M1 – Duty classification: worked examples for hand check

Status: **awaiting engineer check**. Please verify the tables against your copies of
ISO 4301-1 / FEM 1.001 and EN 13001-1, and tick or correct each example.

## Method

| Step | Formula / table |
|---|---|
| Total working cycles | C = lifts per day × working days per year × design life |
| Class of utilisation | U0 ≤16 000, U1 ≤32 000, U2 ≤63 000, U3 ≤125 000, U4 ≤250 000, U5 ≤500 000, U6 ≤1 000 000, U7 ≤2 000 000, U8 ≤4 000 000, U9 above |
| Load spectrum factor (structure) | kQ = Σ (Ci/C)(Qi/Qmax)³, net loads |
| Load spectrum class | Q1 ≤0.125, Q2 ≤0.25, Q3 ≤0.5, Q4 ≤1.0 |
| Hoist running time | 2 × hoist height ÷ hoist speed per lift (up and down), × lifts |
| Running time class | T0 ≤200h, T1 ≤400h, T2 ≤800h, T3 ≤1600h, T4 ≤3200h, T5 ≤6300h, T6 ≤12 500h, T7 ≤25 000h, T8 ≤50 000h, T9 above |
| Hoist spectrum factor | km = Σ (ti/T)((Li + dead)/(Lmax + dead))³ |
| Groups A and M | ISO 4301-1 table below (same table for A from Q,U and M from L,T) |
| FEM 9.511 | M1 1Dm, M2 1Cm, M3 1Bm, M4 1Am, M5 2m, M6 3m, M7 4m, M8 5m |

| | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Q1/L1 | 1 | 1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| Q2/L2 | 1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 8 |
| Q3/L3 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 8 | 8 |
| Q4/L4 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 8 | 8 | 8 |

## Example 1 – Schedule of lifts

20t SWL, 240 days/year, 20 years (4800 days), hoist height 6m, hoist speed 4m/min.

| Lift | Load | Lifts/day |
|---|---|---|
| Full load | 20t | 5 |
| Half load | 10t | 20 |
| Quarter load | 5t | 25 |

- C = 50 × 4800 = **240 000 → U4**
- kQ = (5/50)(1)³ + (20/50)(0.5)³ + (25/50)(0.25)³ = 0.1 + 0.05 + 0.0078 = **0.1578 → Q2**
- **A4**
- Hoist: 2 × 6 ÷ 4 = 3min per lift; 50 × 3 = 150min = 2.5h/day; × 4800 = **12 000h → T6**
- km = kQ (all lifts take equal time) = 0.1578 → **L2**
- **M6 / FEM 3m**
- With a 1t hook block: km = 0.1 + 0.4(11/21)³ + 0.5(6/21)³ = **0.1692** (still L2)

☐ Checked by: ________ Date: ________

## Example 2 – Operating pattern (on class boundaries)

10 cycles/h, 8h/day, 250 days/year, 25 years, "moderate" spectrum, hoist 2h/day.

- C = 10 × 8 × 250 × 25 = **500 000 → U5** (limit is inclusive)
- Moderate → kQ = 0.25 → **Q2** → **A5**
- Hoist: 2 × 250 × 25 = **12 500h → T6** (inclusive), L2 → **M6 / FEM 3m**

☐ Checked by: ________ Date: ________

## Example 3 – Stated by client

A5 with hoist FEM 2m → recorded as **A5, M5**. U and Q are unknown, so the tool flags
that fatigue checks will need an assumed load history.

☐ Checked by: ________ Date: ________
