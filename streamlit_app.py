"""Streamlit Cloud entrypoint for the Graduation Hospital Planner.

This lightweight wrapper keeps the development source layout under `src/` while
providing the root-level `streamlit_app.py` file that Streamlit Community Cloud
and the in-app Deploy flow discover most reliably.
"""

from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
APP = SRC / "graduation_hospital_planner" / "grid_drag_canvas_app.py"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

runpy.run_path(str(APP), run_name="__main__")
