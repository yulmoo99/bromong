from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def test_app_includes_shape_ratio_rule_checker_hooks():
    source = APP_PATH.read_text(encoding="utf-8")

    assert "function connectedComponentsOf(value)" in source
    assert "function checkModuleShapePolicies()" in source
    assert "aspect_ratio_preferred_max" in source
    assert "Shape / aspect ratio checks" in source
