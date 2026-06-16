from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def test_3d_viewer_ui_and_scripts_removed_from_planner():
    src = APP_PATH.read_text(encoding="utf-8")

    assert "View Selected Layout in 3D" not in src
    assert "threeDPanel" not in src
    assert "threeDCanvas" not in src
    assert "threeDStatus" not in src
    assert "renderSelectedLayout3D" not in src
    assert "GLTFLoader" not in src
    assert "three.js" not in src


def test_canvas_remains_as_2d_plan_review_stage():
    src = APP_PATH.read_text(encoding="utf-8")

    assert "Planning Canvas" in src
    assert "Generate / Regenerate Layout Options" in src
    assert "canvas id=\"grid\"" in src
