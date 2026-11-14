"""Calculation and selection engine for BS EN 15011 bridge and gantry cranes.

Engineering code only: no web or database code lives here, so it can be tested
on its own and reused by the web app, reports or a desktop tool.
"""

from crane_engine.units import Q_, ureg

__all__ = ["Q_", "ureg"]
__version__ = "0.1.0"
