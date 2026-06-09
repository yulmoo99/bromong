from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_suite_placement_reserves_cells_that_can_widen_long_main_corridor():
    text = source()
    assert "function cellWouldBlockMainCorridorWidening" in text
    assert "function suiteBlocksMainCorridorWidening" in text
    window = text[text.index("function canPlaceSuiteFromCorridor"):text.index("function placeSuiteFromCorridor")]
    assert "!suiteBlocksMainCorridorWidening(rects)" in window


def test_narrow_width_policy_does_not_confuse_door_ticks_with_real_two_cell_width():
    text = source()
    assert "function hasParallelCorridorWidthMate" in text
    width_window = text[text.index("function longestNarrowCorridorRun"):text.index("function corridorWidthPolicyReport")]
    assert "hasParallelCorridorWidthMate" in width_window
    assert "corridorHasPerpendicularMate" not in width_window


def test_auto_layout_runs_width_repair_after_suite_placement_too():
    text = source()
    window = text[text.index("function placeCompactWardModules"):text.index("function compareLayoutOptions")]
    assert window.count("repairLongNarrowCorridorRuns(corridorCells)") >= 1
