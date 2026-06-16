import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "modules_ward_v01.json"
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def load_db():
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def test_streamlit_sidebar_defaults_open_rectangle_and_no_cell_size_slider():
    src = APP_PATH.read_text(encoding="utf-8")

    assert 'initial_sidebar_state="expanded"' in src
    assert 'st.sidebar.radio("Drawing tool", ["pencil", "rectangle"], horizontal=True, index=1)' in src
    assert 'Cell size px' not in src
    assert 'cell = 20' in src


def test_guideline_adjacency_scoring_was_removed_from_ui_and_layout_logic():
    src = APP_PATH.read_text(encoding="utf-8")
    db = load_db()

    assert "hospital_program_adjacency_rules" not in db
    assert "HOSPITAL_ADJACENCY_RULES" not in src
    assert "guideline adjacency" not in src
    assert "인접 기준" not in src
    assert "adjacencyScore" not in src
    assert "hospitalProgramAdjacencyScore" not in src


def test_hospital_program_checklist_has_quantities_and_operating_room_bundle():
    src = APP_PATH.read_text(encoding="utf-8")
    db = load_db()
    programs = {p["id"]: p for p in db["hospital_program_modules"]}

    assert "recovery_room" in programs
    assert "central_supply" in programs
    assert programs["operating_room"]["default_quantity"] == 0  # 기본은 체크 해제 상태
    assert programs["operating_room"]["quantity_step"] == 1
    assert "HOSPITAL_PROGRAM_BUNDLES" in src
    assert "operating_room: ['surgery_support', 'recovery_room', 'central_supply']" in src
    assert "program-qty" in src
    assert "getSelectedHospitalProgramRequests" in src
    assert "quantity" in src


def test_hospital_auto_layout_places_program_requests_by_quantity_not_singletons():
    src = APP_PATH.read_text(encoding="utf-8")

    assert "expandHospitalProgramRequests" in src
    assert "for (let i=0; i<request.quantity; i++)" in src
    assert "placedProgramInstances" in src
    assert "배치 모듈" in src
