# Decisions Log

Key project and engineering decisions, with date and who decided.

| ID | Date | Decision | Decided by | Notes |
|---|---|---|---|---|
| D-001 | 2026-11-13 | Design standard is BS EN 15011 (bridge and gantry cranes) with its supporting standards | Owner | "EN 15001" in the first brief was a slip |
| D-002 | 2026-11-13 | Capacity range up to 150t, including twin hoists of 2 × 75t | Owner | |
| D-003 | 2026-11-13 | Span range up to 90m | Owner | Crane type for long spans to be confirmed (PLAN.md Q1) |
| D-004 | 2026-11-13 | Tool is used by sales (quick selection, budget price) and engineering (full design pack) | Owner | |
| D-005 | 2026-11-13 | Hoists and end carriages: Podem catalogue parts up to Podem limits, custom beyond. Structure always custom. In-house standard parts library built up over time | Owner | |
| D-006 | 2026-11-13 | Delivered as a web app; calculation engine kept as a separate Python package | Proposed by Claude, pending owner confirmation | Owner was not 100% sure; see PLAN.md section 4 |
| D-007 | 2026-11-13 | Design pack documents built from the owner's existing templates and sample documents | Owner | Templates to be supplied |
| D-008 | 2026-11-14 | Original README brief withdrawn and deleted; plan rewritten without it | Owner | |
| D-009 | 2026-11-14 | Long spans (up to 90m) apply to both overhead travelling and gantry cranes | Owner | |
| D-010 | 2026-11-14 | 2 × 75t cranes lift one load in tandem (synchronised hoisting, combined limiter) | Owner | Arrangement confirmed in D-015 |
| D-011 | 2026-11-14 | Deflection limit span/750 as company standard; tighter limit set per project where extra accuracy is required | Owner | Horizontal uses the same default until told otherwise (Claude assumption) |
| D-012 | 2026-11-14 | Podem datasheets and sample prices may be used in the tool | Owner (Podem permission obtained) | Data to be supplied before M5 |
| D-013 | 2026-11-14 | Drawings output as AutoCAD-compatible DXF; app hosted in the cloud | Owner | Cloud provider chosen at M11 |
| D-014 | 2026-11-14 | Generic document templates used until company templates are supplied | Owner | |
| D-015 | 2026-11-14 | Tandem cranes use two separate crabs, each running on both girders of a double-girder bridge | Owner | |
| D-016 | 2026-11-14 | Duty can be given three ways: class stated by client, operating pattern, or schedule of lifts | Owner | |
| D-017 | 2026-11-14 | Crane and mechanism groups (A, M, FEM 9.511) from ISO 4301-1 / FEM 1.001 tables; EN 13001-1 stress history (S) classes worked out per detail in the fatigue checks (M3) | Proposed by Claude, pending owner check | Tables in docs/worked-examples/M1-duty-classification.md |
| D-018 | 2026-11-14 | kQ for the structure uses net loads. Hoist km adds any fixed attachment mass (hook block) to every load. Hoist running time per lift = up and down the hoist height | Proposed by Claude, pending owner check | |
