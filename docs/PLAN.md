# Crane Design Tool – Project Plan

Status: **draft for approval** (14 November 2026)

## 1. Purpose

A web app, used by sales and engineering, that takes a crane specification, selects a
BS EN 15011 compliant crane from catalogue, standard and custom parts, and produces a
design pack.

## 2. Scope

| Item | Scope |
|---|---|
| Design standard | BS EN 15011 (bridge and gantry cranes) |
| Capacity | Up to 150t, including twin-hoist cranes of 2 × 75t |
| Span | Up to 90m |
| Crane types | Overhead travelling (single/double girder) and gantry/semi-gantry (goliath) |
| Hoists and end carriages | Podem catalogue parts up to Podem's limits. Custom parts beyond those limits |
| Structure | Always custom: girders, end beams, and gantry legs and sill beams |
| Standard parts | An in-house library that grows over time. A custom part that has been designed and approved can be promoted to a standard part |

### Supporting standards

| Area | Standards |
|---|---|
| Classification, loads, steel structures | EN 13001-1, -2, -3-1 |
| Wire ropes, drums, hooks, wheels and rails | EN 13001-3-2, -3-5, -3-3 |
| Hoists, limiters, equipment, controls | EN 14492-2, EN 12077-2, EN 13135, EN 13557 |
| Electrical equipment, control system safety | EN 60204-32, EN ISO 13849-1 |
| Information for use, access | EN 12644-1/-2, EN 13586 |
| Risk assessment and legal basis | ISO 12100, CDM 2015, Supply of Machinery (Safety) Regulations 2008 / EU Machinery Regulation 2023/1230 (applies from January 2027) |
| Outdoor and special environments | Wind to EN 13001-2, corrosion protection to ISO 12944, ATEX where needed |

### What the range means for the engineering

- **Up to 90m span:** box girders, probably shipped in sections with bolted splices.
  Other checks that matter at this size:
  - skew forces, and synchronising the long-travel drives
  - horizontal deflection and camber
  - natural frequency
  - wheel load distribution, using bogies/equalisers where needed
  - on gantries, a fixed leg and a hinged leg, plus wind and storm-tie-down checks
- **Twin hoists (2 × 75t):** load sharing between the hoists, and tandem/synchronised
  control. Load cases must cover each hoist working alone and both working together.
- **Beyond Podem limits:** a custom crab/open winch brings rope, drum, hook, gearbox,
  brake and motor design into scope. That includes an emergency drum brake where the
  application needs one.

## 3. How it will be used

| Mode | Who | Inputs | Outputs |
|---|---|---|---|
| **Quick selection** | Sales | Short spec: SWL, span, lift, duty, building limits, environment. Sensible defaults for the rest | Ranked options, budget price (from rates you maintain), GA sketch, wheel loads, quotation datasheet |
| **Full design** | Engineering | Full spec. Any default can be overridden | Full design pack, with check and approve steps |

Both modes work on one project record. When a quote is won, engineering picks up the
sales selection; nothing is re-entered. Only engineering can issue a design pack.

## 4. Platform: web app (D-006)

- Sales and engineering share one catalogue, one set of rates and one project history.
- Nothing to install, and updates reach everyone at once.
- Revision control, approvals and the audit trail are much easier with everything in
  one place.

The calculation engine is a separate Python package, so a desktop or offline version can
be added later without touching the engineering code.

| Layer | Technology |
|---|---|
| Interface | React + TypeScript |
| Server | Python (FastAPI) |
| Units | `pint` (every quantity carries its units) |
| Database | PostgreSQL |
| Documents | Word templates via `docxtpl`, then PDF |
| Drawings | DXF/PDF via `ezdxf`, and optionally 3D STEP |

## 5. Selection logic

1. Classify duty (EN 13001-1): U and Q classes, then the crane and mechanism classes.
2. Choose candidate arrangements: single girder, double girder or gantry; one or two
   hoists.
3. **Hoist:** use a Podem hoist if one meets SWL, class, lift, speed and headroom.
   Otherwise design a custom crab.
4. **End carriages:** use Podem if wheel load, wheelbase and drive rating are within
   their limits. Otherwise design custom end carriages/bogies.
5. **Structure:** size the girders, end beams and legs for strength, fatigue, deflection
   and stability (EN 13001-3-1).
6. **Wheels and rails:** check to EN 13001-3-3. Report the runway reactions.
7. **Rank** the options that pass by price, weight, headroom, wheel loads and margin.
   Show why each rejected option failed.

## 6. Design pack (built from your templates)

| Document | Contents |
|---|---|
| Calculation report | Inputs, formulas, clause references and utilisation for every check |
| Control philosophy | Operating modes, limits and overload protection, safety functions with required PL, twin-hoist synchronisation, anti-skew control |
| Designer's risk assessment | CDM 2015 / ISO 12100 hazard log |
| Drawings | GA, girder and end-carriage fabrication, electrical schematic, bill of materials |
| O&M manual | EN 12644; inspection and maintenance schedule; design working period monitoring; spares |
| Compliance file | Test procedures (1.25 × SWL static, 1.1 × SWL dynamic), Declaration of Conformity draft, technical file index |

Every document is generated from one design record. Changing the spec regenerates the
whole pack consistently, under revision control. All outputs are a design aid and are
issued only after check and approval by a competent engineer.

## 7. Milestones

| # | Milestone | Result |
|---|---|---|
| M0 | Project set-up: structure, automated tests, CI | Foundations |
| M1 | Spec input and data model; duty classification (EN 13001-1) | Specs saved, classes derived |
| M2 | Loads and load combinations (EN 13001-2): dynamic factors, combinations A/B/C, skew | Load cases for a crane |
| M3 | Girder checks (EN 13001-3-1): rolled section, then box girder (static, fatigue, stability, deflection) | Girder design check |
| M4 | Wheel loads and wheel/rail checks (EN 13001-3-3) | End carriage loading |
| M5 | Podem catalogue import and selection rules | Catalogue-based options |
| M6 | Sales quick-selection screen and budget pricing | First usable tool for sales |
| M7 | Calculation report and GA output from your templates | First design pack documents |
| M8 | Twin hoist (2 × 75t), long spans and splices, custom end carriages/bogies | Full capacity and span range |
| M9 | Custom crab, control philosophy, DRA, O&M, compliance file | Complete design pack |
| M10 | Gantry/semi-gantry cranes, outdoor wind | All crane types |
| M11 | Users and roles, check/approve/issue workflow, audit trail | Production ready |

**Validation:** your past projects become test cases. The tool must reproduce their
checked results within an agreed tolerance.

## 8. Open questions

1. **90m span:** is this mostly gantries, or overhead travelling cranes in a hall too?
   That decides whether gantries move earlier than M10.
2. **2 × 75t:** two hoists on one crab, or two separate crabs? Will they lift one load in
   tandem, independently, or both?
3. **Deflection limit:** what is your company standard for vertical and horizontal
   deflection (e.g. span/750, span/1000)?
4. **Podem data:** which Podem datasheets or selection tables do you have (PDF/Excel)?
   And do we have permission to put that data into the tool?
5. **Drawings:** which CAD system produces your manufacturing drawings? Should the tool
   produce full fabrication drawings, or a GA plus a parameter sheet that drives your
   CAD models?
6. **Templates:** please share your templates and sample documents. A `templates/`
   folder works if the repository is private.
7. **Hosting:** should the web app run on your own servers or in the cloud (e.g. Azure,
   if you use Microsoft 365)?
