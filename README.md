This repository is a new crane design tool that I own. I am a chartered mechanical
engineer, not a programmer. Write the code, explain decisions in plain English, and
ask me engineering questions; do not ask me programming questions.

Product: concept design and checking of overhead travelling cranes to BS EN 15011,
using BS EN 13001-1, -2, -3-1, -3-3 and BS EN 13135. Later: goliath cranes, reports,
GA and 3D views, budget pricing with user-entered rates.

Rules for the whole project (put them in CLAUDE.md):
- Python calculation engine, SI units handled by a units library; no magic numbers.
- Every calculation function cites its clause and has at least one worked example
  checked against a hand calculation I approve, not only against its own output.
- Every engineering decision gets an ID and a line in docs/DECISIONS.md with date
  and who decided.
- British English. No space between number and unit in text (10mm).
- Tests run automatically on every change (GitHub Actions); nothing is merged with
  a failing test.
- Work in small steps: one pull request per task, with a plain-English summary of
  what changed and how to check it.

First task: set up the project structure, CLAUDE.md, docs/DECISIONS.md, the test
set-up and the GitHub Actions workflow. Then propose a milestone plan for the
calculation engine and wait for my approval before starting it.
