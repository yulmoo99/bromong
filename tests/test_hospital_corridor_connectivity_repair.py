from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def test_hospital_program_layout_repairs_corridor_components_into_one_network():
    src = APP_PATH.read_text(encoding="utf-8")

    assert "function ensureAllCorridorsConnected" in src
    assert "connectedComponentsOf(moduleCodes.controlled_corridor)" in src
    assert "grid[rr][cc] === 1 || grid[rr][cc] === moduleCodes.controlled_corridor" in src
    assert "markCorridor(rr, cc, corridorCells || [])" in src
    assert "ensureAllCorridorsConnected(corridorCells);" in src


def test_corridor_repair_runs_after_program_modules_are_placed_before_edge_fill():
    src = APP_PATH.read_text(encoding="utf-8")
    fragment = """const placedPrograms = placeSelectedHospitalPrograms(programRequests, corridorCells, strategy);
    ensureAllCorridorsConnected(corridorCells);
    fillRemainingEdgeCells(corridorCells);"""

    assert fragment in src
