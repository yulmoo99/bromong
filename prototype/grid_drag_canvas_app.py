"""Compatibility wrapper for the reorganized Streamlit app.

Preferred command:
  streamlit run src/graduation_hospital_planner/grid_drag_canvas_app.py

This wrapper keeps the older prototype/grid_drag_canvas_app.py command working.
"""
from pathlib import Path
import runpy

APP_PATH = Path(__file__).resolve().parents[1] / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"
runpy.run_path(str(APP_PATH), run_name="__main__")
