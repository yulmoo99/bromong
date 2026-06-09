from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_compact_sites_have_linear_corridor_strategies_available():
    text = source()
    assert "function usableAreaStats" in text
    assert "function shouldUseCompactLinearCorridor" in text
    assert "addLinearWardCorridor" in text
    assert "single_loaded_linear" in text
    assert "double_loaded_linear" in text


def test_adaptive_corridor_does_not_force_loop_for_small_area():
    text = source()
    window = text[text.index("function buildAdaptiveCorridorNetwork"):text.index("function rectTouchesCorridor")]
    assert "shouldUseCompactLinearCorridor" in window
    assert "if (compact)" in window
    assert "addLinearWardCorridor" in window
    assert "figure_eight" in window
    assert "s.area < 760 && strategyIndex !== 1" in text


def test_nurse_station_prefers_central_corridor_intersection_or_centroid():
    text = source()
    assert "function corridorCentralityScore" in text
    assert "function placeNurseStationCentral" in text
    support_window = text[text.index("function placeMinimalSupportRooms"):text.index("function fillRemainingEdgeCells")]
    assert "placeNurseStationCentral" in support_window
    assert "moduleCodes.nurse_station" in text
    assert "centerR" in text and "centerC" in text


def test_option_panel_explains_when_compact_sites_use_linear_not_loop_strategy():
    text = source()
    assert "function corridorStrategyName" in text
    assert "function strategyLabelForIndex" in text
    panel_window = text[text.index("function renderOptionPanel"):text.index("function generateLayoutOptions")]
    assert "strategyLabelForIndex(idx, opt.corridorStrategy)" in panel_window
    assert "corridorStrategy:" in panel_window
    assert "1자 양측복도" in text
    assert "1자 단측복도" in text


def test_generated_options_store_the_actual_corridor_strategy_used_for_selection():
    text = source()
    generate_window = text[text.index("function generateLayoutOptions"):text.index("function selectLayoutOption")]
    assert "const corridorStrategy = corridorStrategyName(strategy)" in generate_window
    assert "corridorStrategy" in generate_window


def test_nurse_station_is_reserved_before_patient_suite_greedy_fill():
    text = source()
    compact_window = text[text.index("function placeCompactWardModules"):text.index("function compareLayoutOptions")]
    assert compact_window.index("placeNurseStationCentral()") < compact_window.index("placeOrderedWardSuites")
    assert "placeRemainingSupportRooms" in compact_window
