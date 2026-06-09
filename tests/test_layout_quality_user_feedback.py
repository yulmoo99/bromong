from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_support_reserve_is_not_used_as_blanket_leftover_infill():
    text = source()

    assert "function placeMinimalSupportRooms" in text
    assert "function fillNeutralSupportInfill" not in text
    assert "neutralizeRemainingCells" not in text
    assert "fillNeutralSupportInfill();" not in text


def test_all_strategy_options_share_same_patient_suite_module_shape():
    text = source()

    assert "const unifiedSuitePreset" in text
    assert "suitePresets = [" not in text
    assert "presetStrategies" not in text
    assert "placeOrderedWardSuites(corridorCells, targetBeds, strategyIndex, unifiedSuitePreset)" in text


def test_layout_options_differ_by_corridor_and_anchor_strategy_not_room_shape():
    text = source()

    assert "const corridorStrategy =" in text
    assert "buildAdaptiveCorridorNetwork(strategyIndex)" in text
    assert "preferredDirsByStrategy" in text
    assert "strategyLayoutHash" in text
    assert "moduleShapeSignature" in text


def test_compact_layout_does_not_force_spacing_between_ward_modules():
    text = source()

    assert "minSpacing" not in text
    assert "i % 2" not in text[text.index("function orderedCorridorAnchors"):text.index("function placeOrderedWardSuites")]
    assert "allowAdjacentSuites" in text


def test_duplicate_layout_buttons_are_merged_into_single_generate_action():
    text = source()

    assert text.count('onclick="generateLayoutOptions()"') == 1
    assert "Generate / Regenerate Layout Options" in text
    assert "Place Compact Ward Modules" not in text
