# Crane Design Tool – Project Plan

Status: **draft for owner approval** (13 November 2026)

## 1. Purpose

A web tool, used by sales and engineering, that takes a crane specification, selects a
BS EN 15011 compliant crane from catalogue, standard and custom parts, and produces a
design pack.

## 2. Scope

| Item | Scope |
|---|---|
| Design standard | BS EN 15011, using BS EN 13001-1, -2, -3-1, -3-3 and BS EN 13135 (see D-001) |
| Capacity | Up to 150t, including twin-hoist cranes of 2 × 75t |
| Span | Up to 90m |
| Crane types | Overhead travelling cranes first. Goliath and semi-goliath later (see question 1) |
| Hoists and end carriages | Podem catalogue parts up to Podem's limits. Custom parts beyond those limits |
| Structure | Always custom: girders, end beams/ties, and legs for goliaths |
| Standard parts | An in-house library that grows over time. A custom part that has been designed and approved can be promoted to a standard part |

### What the range means for the engineering

- **Up to 90m span:** box girders, and likely shipping in sections with bolted splices.
  Other checks that matter at this size:
  - skew forces and long-travel synchronisation (EN 13001-2 / EN 15011)
  - horizontal deflection and camber
  - natural frequency
  - wheel load distribution, using bogies/equalisers where needed
- **Twin hoists (2 × 75t):** load sharing between the hoists, and tandem/synchronised
  control. Load combinations and wheel loads must cover each hoist working alone and
  both working together.
- **Beyond Podem limits:** a custom crab/open winch brings rope, drum and hook design into
  scope (EN 13001-3-2, -3-5). These are not in the README's standards list yet, so
  they need adding when we get there.

## 3. How it will be used

| Mode | Who | Inputs | Outputs |
|---|---|---|---|
| **Quick selection** | Sales | Short spec: SWL, span, lift, duty, building limits, environment. Sensible defaults for the rest | Ranked options, budget price (from user-entered rates), GA sketch, wheel loads, quotation datasheet |
| **Full design** | Engineering | Full spec. Can override any default | Full design pack, with check and approve steps |

Both modes work on one project record. When a quote is won, engineering picks up the
sales selection; nothing is re-entered. Only engineering can issue a design pack.

## 4. Platform decision (plain English)

**Web app (proposed, D-006).**

- Sales and engineering share one catalogue, one set of rates and one project history.
- Nothing to install, and updates reach everyone at once.
- Revision control and approvals are much easier with everything in one place.

The calculation engine is kept as a separate Python package. If a desktop version is
ever needed, the engineering code does not change.

## 5. Selection logic

1. Classify duty (EN 13001-1): U and Q classes, then the crane and mechanism classes.
2. Choose candidate crane arrangements: single or double girder, one or two hoists.
3. **Hoist:** use a Podem hoist if one meets SWL, class, lift, speed and headroom.
   Otherwise flag "custom crab".
4. **End carriages:** use Podem if wheel load, wheelbase and drive rating are within
   their limits. Otherwise flag "custom end carriage/bogie".
5. **Girders:** size custom box or rolled-section girders for strength, fatigue,
   deflection and stability (EN 13001-3-1).
6. **Wheels and rails:** check to EN 13001-3-3.
7. **Rank** the options that pass by price, weight, headroom, wheel loads and margin.
   Show why each rejected option failed.

## 6. Design pack (built from the owner's templates)

The owner's templates and sample documents set the structure and styling.

| Document | Contents |
|---|---|
| Calculation report | Clause references and utilisations |
| Control philosophy | Including twin-hoist synchronisation and long-travel skew control |
| Designer's risk assessment | CDM 2015 / ISO 12100 hazard log |
| Drawings | GA first. Manufacturing drawing approach depends on question 5 |
| O&M manual | Per EN 12644 |
| Compliance file | Test procedures (1.25 static / 1.1 dynamic), Declaration of Conformity draft |

## 7. Milestones

Each task is a small pull request with a plain-English summary. Every calculation is
checked against a hand calculation the owner approves.

| # | Milestone | Result |
|---|---|---|
| M0 | Project set-up: structure, CLAUDE.md, DECISIONS.md, tests, GitHub Actions | Foundations (README first task) |
| M1 | Units, materials, duty classification (EN 13001-1) | Classes from duty inputs |
| M2 | Loads and load combinations (EN 13001-2): dynamic factors, combinations A/B/C, skew | Load cases for a crane |
| M3 | Girder checks (EN 13001-3-1): rolled section, then box girder (static, fatigue, stability, deflection) | Girder design check |
| M4 | Wheel loads and wheel/rail checks (EN 13001-3-3) | End carriage loading |
| M5 | Podem catalogue import and selection rules | Catalogue-based options |
| M6 | Sales quick-selection screen and budget pricing | First usable tool for sales |
| M7 | Calculation report and GA output from templates | First design pack documents |
| M8 | Twin hoist (2 × 75t), long spans and splices, custom end carriages/bogies | Full capacity and span range |
| M9 | Custom crab (adds EN 13001-3-2, -3-5), control philosophy, DRA, O&M | Complete design pack |
| M10 | Goliath and semi-goliath | Extended crane types |

**Validation:** the owner's past projects become test cases. The tool must reproduce
their checked results within an agreed tolerance.

## 8. Open engineering questions

1. **90m span:** is this for goliaths (README says "later") or overhead travelling cranes
   in a hall? Should M1–M7 stay overhead-travelling only?
2. **2 × 75t:** two hoists on one crab, or two separate crabs? Will they lift one load in
   tandem (needing synchronisation and load sharing), independently, or both?
3. **Deflection limit:** what is your company standard for vertical and horizontal
   deflection (e.g. span/750, span/1000)?
4. **Podem data:** which Podem datasheets or selection tables do you have (PDF/Excel)?
   And do we have permission to put that data into the tool?
5. **Drawings:** which CAD system produces your manufacturing drawings? Should the tool
   produce the GA and a parameter sheet that drives your CAD models, or full fabrication
   drawings itself?
6. **Templates:** please share your templates and sample documents. They can go in a
   `templates/` folder if the repository stays private.
