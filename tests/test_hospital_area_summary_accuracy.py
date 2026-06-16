import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"
DB_PATH = ROOT / "data" / "modules_ward_v01.json"

STALE_GRID_PHRASES = (
    "1.5m 그리드",
    "1.5m 계획 그리드",
    "1.5m grid",
    "1.5m x 1.5m",
    "1.5m × 1.5m",
    "1칸 = 1.5m",
    "1 grid cell = 1.5m",
    "3x3 cells at 1.5m",
    "2 cells at 1.5m",
)


def app_source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_area_summary_uses_actual_placement_feasibility_not_shelf_estimate():
    src = app_source()

    assert "findMinimumHospitalPlacementFootprint" in src
    assert "canPlaceHospitalBlocksInRect" in src
    assert "hospitalRequiredFootprint(getSelectedHospitalProgramRequests())" not in src
    assert "배치 가능 최소 영역" in src
    assert "복도 포함 최소 필요 면적" not in src


def test_no_stale_1_5m_grid_wording_in_tracked_text_files():
    tracked = subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True, encoding="utf-8"
    ).splitlines()
    offenders = []
    for rel in tracked:
        path = ROOT / rel
        if rel == "tests/test_hospital_area_summary_accuracy.py":
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".glb", ".pdf"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        found = [phrase for phrase in STALE_GRID_PHRASES if phrase in text]
        if found:
            offenders.append((rel, found))
    assert offenders == []


def test_hospital_db_grid_notes_match_1_8m_cell_area():
    db = json.loads(DB_PATH.read_text(encoding="utf-8"))
    assert db["grid_assumption"]["default_cell_size_m"] == 1.8
    assert db["grid_assumption"]["cell_area_m2"] == 3.24
    assert "1.8m" in db["grid_assumption"]["note"]

    db_text = DB_PATH.read_text(encoding="utf-8")
    assert "3x3 cells at 1.5m" not in db_text
    assert "2 cells at 1.5m" not in db_text
