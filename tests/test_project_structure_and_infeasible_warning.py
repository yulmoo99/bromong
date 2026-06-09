from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"
WRAPPER_PATH = ROOT / "prototype" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_project_sources_are_organized_under_src_ref_data():
    assert (ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py").is_file()
    assert (ROOT / "src" / "scripts").is_dir()
    assert (ROOT / "ref" / "docs").is_dir()
    assert (ROOT / "ref" / "research_sources").is_dir()
    assert (ROOT / "data" / "modules_ward_v01.json").is_file()
    assert WRAPPER_PATH.is_file(), "legacy Streamlit command should remain as a wrapper"


def test_infeasible_ward_generation_shows_user_warning_and_skips_invalid_options():
    text = source()
    assert "function layoutFeasibilityReport" in text
    assert "function showInfeasibleLayoutWarning" in text
    assert "ward-infeasible-warning" in text
    assert "cannot place ward modules" in text.lower()
    generate_window = text[text.index("function generateLayoutOptions"):text.index("function selectLayoutOption")]
    assert "layoutFeasibilityReport(targetBeds)" in generate_window
    assert "showInfeasibleLayoutWarning" in generate_window
    assert "return;" in generate_window


def test_nurse_station_policy_is_documented_as_centralized_not_leftover_infill():
    text = source()
    assert "Nurse stations generally work best near the ward centroid" in text
    assert "placeNurseStationCentral" in text
    assert "corridorCentralityScore" in text
