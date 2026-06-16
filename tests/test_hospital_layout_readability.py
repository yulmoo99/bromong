from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def test_hospital_mode_uses_branching_department_corridors_not_only_single_spines():
    src = APP_PATH.read_text(encoding="utf-8")

    assert "markHospitalDepartmentCorridorNetwork" in src
    assert "branchRows" in src
    assert "ring" in src
    assert "department_cluster" in src
    assert "hospital_program:department_cluster" in src


def test_draw_labels_once_per_connected_module_component():
    src = APP_PATH.read_text(encoding="utf-8")

    assert "drawModuleComponentLabels" in src
    assert "visitedLabels" in src
    assert "ctx.fillText(label, centroid" in src
    assert "ctx.fillText(label, c * cell + cell / 2, r * cell + cell / 2)" not in src
