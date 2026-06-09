from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_suite_door_band_is_connected_to_main_corridor_network_before_placement():
    text = source()
    assert "function connectDoorBandToCorridorNetwork" in text
    place_window = text[text.index("function placeSuiteFromCorridor"):text.index("function orderedCorridorAnchors")]
    assert "connectDoorBandToCorridorNetwork(r, c, dir, rects, corridorCells)" in place_window
    assert "suiteFootprintBlockedCells(rects)" in text
    assert "if (blocked.has(keyOf(rr, nc))) continue" in text


def test_corridor_network_report_rejects_disconnected_corridor_components():
    text = source()
    assert "function corridorNetworkReport" in text
    assert "connectedComponentsOf(moduleCodes.controlled_corridor)" in text
    assert "disconnected corridor components" in text
    rule_window = text[text.index("function checkWardRules"):text.index("function clearGrid")]
    assert "corridorNetworkReport()" in rule_window


def test_support_and_room_access_use_orthogonal_not_diagonal_corridor_contact():
    text = source()
    window = text[text.index("function rectTouchesCorridor"):text.index("const unifiedSuitePreset")]
    assert "neighbors4(r, c)" in window
    assert "r0 - 1" not in window
    assert "c0 - 1" not in window


def test_access_report_is_not_a_stub_that_always_returns_true():
    text = source()
    assert "function moduleCellsReachableFromCorridor() { return true;" not in text
    assert "function corridorAccessReport()" in text
    assert "corridorReachableSet" in text
    assert "must be reached from corridor without passing through another room" in text
