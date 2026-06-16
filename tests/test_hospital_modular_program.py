import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "modules_ward_v01.json"
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def load_db():
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def test_grid_is_1_8m_and_base_hospital_module_is_2_by_4_cells():
    db = load_db()
    assert db["grid_assumption"]["default_cell_size_m"] == 1.8
    assert db["grid_assumption"]["cell_area_m2"] == 3.24
    base = db["hospital_module_basis"]
    assert base["base_module_m"] == [3.6, 7.2]
    assert base["base_module_cells"] == [2, 4]
    assert round(base["base_module_area_m2"], 1) == 25.9
    assert base["corridor_width_cells"] == 1


def test_hospital_program_checklist_contains_requested_functions_and_module_counts():
    db = load_db()
    programs = {p["id"]: p for p in db["hospital_program_modules"]}
    expected = {
        "exam_room": 1,
        "specimen_collection": 1,
        "emergency_care": 1.5,
        "observation_4bed": 2,
        "ct_suite": 2,
        "xray_room": 1,
        "diagnostic_lab": 2,
        "pathology_lab": 2,
        "treatment_room": 1,
        "infusion_6bed": 2,
        "dialysis_4bed": 2,
        "dialysis_8bed": 3,
        "operating_room": 2,
        "surgery_support": 2,
        "delivery_room": 1,
        "newborn_treatment": 1,
        "clinical_research_lab": 1,
        "data_analysis_room": 1,
        "meeting_room": 1,
        "administration": 1,
    }
    assert set(expected).issubset(programs)
    for program_id, module_count in expected.items():
        assert programs[program_id]["module_count"] == module_count
        assert programs[program_id]["base_module_cells"] == [2, 4]


def test_streamlit_ui_exposes_hospital_checklist_and_auto_layout_mode():
    src = APP_PATH.read_text(encoding="utf-8")
    assert "hospitalProgramPanel" in src
    assert "input type=\"checkbox\"" in src
    assert "getSelectedHospitalPrograms" in src
    assert "generateHospitalLayoutOptions" in src
    assert "Hospital Modular Program" in src
    assert "3.6m × 7.2m" in src
    assert "1.8m grid" in src


def test_hospital_auto_layout_uses_one_cell_corridor_and_selected_program_rectangles():
    src = APP_PATH.read_text(encoding="utf-8")
    assert "const CELL_SIZE_M = 1.8" in src
    assert "const HOSPITAL_BASE_MODULE_CELLS = {w:2, h:4}" in src
    assert "const HOSPITAL_CORRIDOR_WIDTH_CELLS = 1" in src
    assert "placeSelectedHospitalPrograms" in src
    assert "hospital_program:" in src
    assert "panel.innerHTML = HOSPITAL_PROGRAMS.map" in src
    assert "getSelectedHospitalPrograms" in src
