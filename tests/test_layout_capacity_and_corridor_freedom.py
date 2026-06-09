from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_layout_places_additional_patient_suites_beyond_minimum_target_when_space_allows():
    text = source()

    assert "function estimateSuiteCapacity" in text
    assert "const desiredSuites = Math.max(targetBeds" in text
    assert "placed >= desiredSuites" in text
    assert "targetBeds" in text


def test_empty_candidate_area_is_consumed_by_more_patient_suites_not_only_reported():
    text = source()

    assert "function placeAdditionalSuitesInOpenPockets" in text
    assert "placeAdditionalSuitesInOpenPockets(corridorCells, desiredSuites" in text
    assert "possible_area" not in text.lower()


def test_remaining_feasible_pockets_are_filled_with_connected_program_rooms():
    text = source()
    compact_window = text[text.index("function placeCompactWardModules"):text.index("function compareLayoutOptions")]

    assert "function fillProgrammedPockets" in text
    assert "function bestProgramInfillRect" in text
    assert "function connectRoomRectToCorridor" in text
    assert "fillProgrammedPockets(corridorCells)" in compact_window
    assert "fillRemainingEdgeCells(corridorCells)" in compact_window
    assert "fillResidualServiceComponents(corridorCells)" in compact_window
    assert "connectResidualComponentToCorridor" in text
    assert "PROGRAM_RESERVE_CODE" in text
    assert "moduleCodes.support_reserve" not in text


def test_programmed_infill_is_included_in_corridor_access_validation():
    text = source()
    access_window = text[text.index("function moduleCellsReachableFromCorridor"):text.index("function removeDisconnectedModuleCells")]

    assert "PROGRAM_RESERVE_CODE" in access_window
    assert "reachable.has" in access_window


def test_corridor_network_supports_loops_branches_and_figure_eight_patterns():
    text = source()

    assert "function buildAdaptiveCorridorNetwork(strategyIndex = 0)" in text
    assert "addFigureEightLoops" in text
    assert "addCorridorBranches" in text
    assert "corridorStrategy" in text
    assert "figure_eight" in text
    assert "branching_loop" in text


def test_corridor_network_is_not_only_single_perimeter_rectangle():
    text = source()
    corridor_window = text[text.index("function addPerimeterLoop"):text.index("function rectTouchesExistingValue")]

    assert "perimeter_loop" in corridor_window
    assert "central connector" in corridor_window.lower()
    assert "branch" in corridor_window.lower()
    assert corridor_window.count("markCorridorWide") >= 8
