from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_main_corridor_width_policy_is_explicit():
    text = source()
    assert "MAIN_CORRIDOR_MIN_WIDTH_CELLS = 1" in text
    assert "HOSPITAL_CORRIDOR_WIDTH_CELLS = 1" in text
    assert "SHORT_CONNECTOR_MAX_CELLS" in text
    assert "function repairLongNarrowCorridorRuns" in text
    assert "function corridorWidthPolicyReport" in text


def test_adaptive_corridor_repairs_long_one_cell_runs_before_room_placement():
    text = source()
    window = text[text.index("function buildAdaptiveCorridorNetwork"):text.index("function rectTouchesCorridor")]
    assert "repairLongNarrowCorridorRuns(corridorCells)" in window
    assert "return corridorCells" in window


def test_rule_report_mentions_main_corridor_width_policy():
    text = source()
    window = text[text.index("function checkWardRules"):text.index("function clearGrid")]
    assert "corridorWidthPolicyReport" in window
    assert "Corridor width OK: 1-cell / 1.8m" in text
