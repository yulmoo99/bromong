from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def test_compact_ward_layout_uses_shape_aware_placement_helpers():
    source = APP_PATH.read_text(encoding="utf-8")

    assert "function canPlaceModule" in source
    assert "function findPlacement" in source
    assert "function fillModuleStrict" in source
    assert "preferNear" in source


def test_compact_ward_layout_builds_connected_longest_path_corridor_network():
    source = APP_PATH.read_text(encoding="utf-8")

    assert "function buildAdaptiveCorridorNetwork" in source
    assert "function bfsFrom" in source
    assert "function reconstructPath" in source
    assert "function farthestReachable" in source
    assert "diameter-like main path" in source
    assert "branch path" in source


def test_compact_ward_layout_places_rooms_around_corridor_network():
    source = APP_PATH.read_text(encoding="utf-8")

    assert "function canPlaceSuiteFromCorridor" in source
    assert "function placeSuiteFromCorridor" in source
    assert "for (const dir of ['up', 'down', 'left', 'right'])" in source
    assert "unifiedSuitePreset" in source
    assert "front_service_modular" in source
    assert "moduleShapeSignature" in source
    assert "moduleCodes.negative_pressure_patient_room" in source
    assert "moduleCodes.anteroom" in source
    assert "fillModuleStrict" in source
