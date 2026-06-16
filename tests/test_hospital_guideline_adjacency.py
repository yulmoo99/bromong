import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "modules_ward_v01.json"
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def load_db():
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def test_guideline_sources_are_recorded_without_fake_adjacency_score():
    db = load_db()
    src = APP_PATH.read_text(encoding="utf-8")

    source_ids = {s["id"] for s in db["sources"]}
    assert "USER_PDF_MEDICAL_FACILITY_GUIDELINE_2018" in source_ids
    assert "KR_MEDICAL_SERVICE_ACT_FACILITY_RULES" in source_ids
    assert "hospital_program_adjacency_rules" not in db
    assert "guideline adjacency" not in src
    assert "인접 기준" not in src


def test_hospital_program_modules_carry_real_planning_sources_and_cell_size_note():
    db = load_db()
    programs = {p["id"]: p for p in db["hospital_program_modules"]}

    assert db["grid_assumption"]["default_cell_size_m"] == 1.8
    assert db["grid_assumption"]["cell_area_m2"] == 3.24
    assert "1.8m × 1.8m" in db["grid_assumption"]["note"]
    assert "USER_PDF_MEDICAL_FACILITY_GUIDELINE_2018" in programs["operating_room"]["design_basis"]
    assert "KR_MEDICAL_SERVICE_ACT_FACILITY_RULES" in programs["operating_room"]["legal_basis"]
    assert "USER_PDF_MEDICAL_FACILITY_GUIDELINE_2018" in programs["dialysis_4bed"]["design_basis"]
