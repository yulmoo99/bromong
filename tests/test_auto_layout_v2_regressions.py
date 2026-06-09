from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_v2_generate_options_uses_shape_aware_adaptive_layout_not_fixed_template():
    text = source()

    assert "function buildAdaptiveCorridorNetwork" in text
    assert "function placeCompactWardModules" in text
    assert "buildAdaptiveCorridorNetwork(strategyIndex);" in text
    assert "function generateStableWardLayout" not in text
    assert "stable 2-bed cluster template" not in text


def test_each_adaptive_suite_gets_unique_cluster_id_incremented():
    text = source()

    assert "function newClusterId" in text
    assert "const cid = newClusterId();" in text
    assert "placeSuiteFromCorridor(r, c, dir, preset)" in text
    assert "cluster_${{String(nextClusterNo).padStart(2, '0')}}" not in text


def test_cluster_outline_tracks_only_ward_suite_cells_not_square_reserve_box():
    text = source()

    assert "function isWardSuiteClusterValue" in text
    assert "grid[r][c] !== 0" not in text[text.index("function assignClusterRect"):text.index("function drawClusterOutlines")]
    assert "isWardSuiteClusterValue(grid[r][c])" in text[text.index("function assignClusterRect"):text.index("function drawClusterOutlines")]


def test_shape_aware_suite_placement_allows_adjacent_patient_room_modules():
    text = source()

    suite_window = text[text.index("function canPlaceSuiteFromCorridor"):text.index("function placeSuiteFromCorridor")]
    assert "function rectTouchesExistingValue" in text
    assert "moduleCodes.negative_pressure_patient_room" in text
    assert "!rectTouchesExistingValue" not in suite_window


def test_no_grid_mode_is_explicitly_handled_before_layout_generation():
    text = source()

    assert "if (!gridHasUsableArea()) createDefaultMaskForBedCount(targetBeds);" in text
    assert "createDefaultMaskForBedCount" in text
    assert "Generate Layout Options" in text


def test_shape_aware_layout_keeps_buffer_and_minimal_support_rooms():
    text = source()

    assert "cleanInfectionBufferOk" in text
    assert "repairCleanInfectionContacts" in text
    assert "direct clean-infected contact" in text
    assert "placeMinimalSupportRooms" in text


def test_all_programmed_rooms_must_have_corridor_access_path():
    text = source()

    assert "function corridorAccessReport" in text
    assert "moduleCellsReachableFromCorridor" in text
    assert "All programmed rooms have an access path to the controlled corridor" in text
    assert "removeDisconnectedModuleCells" in text
    assert "checks.push(corridorAccessReport())" in text


def test_support_rooms_are_placed_adjacent_to_corridor_not_free_floating():
    text = source()

    assert "function placeSupportModuleNearCorridor" in text
    assert "rectTouchesCorridor" in text
    assert "placeSupportModuleNearCorridor(moduleCodes.nurse_station" in text
    assert "findPlacement(moduleCodes.nurse_station" not in text


def test_ward_suites_are_placed_from_ordered_aesthetic_corridor_anchors():
    text = source()

    assert "function orderedCorridorAnchors" in text
    assert "function placeOrderedWardSuites" in text
    assert "anchor.step" in text
    assert "anchor.preferredDirs" in text
    assert "placeOrderedWardSuites(corridorCells" in text


def test_leftover_area_is_not_blanket_filled_as_support_reserve():
    text = source()

    assert "support_reserve" in text
    assert "function placeMinimalSupportRooms" in text
    assert "moduleCodes.support_reserve" not in text
    assert "fillNeutralSupportInfill();" not in text


def test_front_service_suite_keeps_wc_beside_anteroom_and_room_behind():
    text = source()

    assert "front_service" in text
    assert "canPlaceFrontServiceSuiteFromCorridor" in text
    assert "placeFrontServiceSuiteFromCorridor" in text
    assert "WC beside anteroom" in text
    assert "room behind service band" in text


def test_generate_layout_options_keeps_three_named_distinct_strategy_cards():
    text = source()

    assert "function strategyLabelForIndex" in text
    assert "layoutOptions.length === 3" in text
    assert "distinctSignature" in text
    assert "Option ${" in text
    assert "corridorStrategy" in text


def test_layout_generation_buttons_are_merged_into_single_three_option_action():
    text = source()

    assert '<button onclick="generateLayoutOptions()">Generate / Regenerate Layout Options</button>' in text
    assert text.count('onclick="generateLayoutOptions()"') == 1
    assert '<button onclick="placeCompactWardModules()">Place Compact Ward Modules</button>' not in text
