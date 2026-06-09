import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "modules_ward_v01.json"


def load_db():
    return json.loads(DB_PATH.read_text(encoding="utf-8"))


def test_each_module_has_area_and_shape_policy():
    db = load_db()
    assert "general_room_standards" in db
    modules = {m["id"]: m for m in db["modules"]}

    for module_id in [
        "negative_pressure_patient_room",
        "anteroom",
        "ensuite_toilet_shower",
        "controlled_corridor",
        "nurse_station",
        "clean_supply_alcove",
        "soiled_waste_holding",
    ]:
        module = modules[module_id]
        assert "planning_area_m2" in module
        assert "shape_policy" in module
        assert module["shape_policy"]["shape_type"] in {"rectangular", "linear"}


def test_clinical_room_aspect_ratio_policy_is_strict_enough():
    modules = {m["id"]: m for m in load_db()["modules"]}
    room = modules["negative_pressure_patient_room"]

    assert room["planning_area_m2"] == 20.25
    assert room["shape_policy"]["preferred_grid_sizes"][0] == [3, 3]
    assert room["shape_policy"]["aspect_ratio_preferred_max"] <= 1.5
    assert room["shape_policy"]["aspect_ratio_hard_max"] <= 1.8


def test_corridor_is_linear_and_exempt_from_aspect_ratio_check():
    modules = {m["id"]: m for m in load_db()["modules"]}
    corridor = modules["controlled_corridor"]

    assert corridor["shape_policy"]["shape_type"] == "linear"
    assert corridor["shape_policy"]["aspect_ratio_check"] is False
    assert corridor["shape_policy"]["min_width_cells"] == 2
