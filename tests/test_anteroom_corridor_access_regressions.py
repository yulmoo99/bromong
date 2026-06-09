from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_suite_placement_requires_anteroom_corridor_access_not_room_only():
    text = source()
    suite_window = text[text.index("function canPlaceSuiteFromCorridor"):text.index("function placeSuiteFromCorridor")]
    assert "anteroomCorridorContactCount" in text
    assert "suiteDoorPolicyOk" in text
    assert "suiteDoorPolicyOk(r, c, dir, rects)" in suite_window
    assert "anteroomCorridorContactCount(rects.ante) >= 2" in text


def test_patient_room_door_policy_is_anteroom_only_or_both_not_room_only():
    text = source()
    assert "roomCorridorContactCount" in text
    assert "roomContacts === 0 || roomContacts >= 2" in text
    assert "rec.room === 1" in text


def test_rule_report_validates_anteroom_door_connections_after_generation():
    text = source()
    assert "function suiteDoorAccessReport" in text
    rule_window = text[text.index("function checkWardRules"):text.index("function clearGrid")]
    assert "suiteDoorAccessReport()" in rule_window
    assert "Anteroom corridor contacts" in text
