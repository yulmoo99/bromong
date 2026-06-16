import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def test_operating_room_bundle_uses_minimum_shared_support_not_one_to_one_clone():
    src = APP_PATH.read_text(encoding="utf-8")

    assert "HOSPITAL_PROGRAM_BUNDLE_MIN_QTY" in src
    assert "operating_room: {surgery_support: 1, recovery_room: 1, central_supply: 1}" in src
    assert "for (const bundledId of (HOSPITAL_PROGRAM_BUNDLES[box.value] || [])) addRequest(bundledId, quantity, true);" not in src
    assert "const bundledQuantity = Number((HOSPITAL_PROGRAM_BUNDLE_MIN_QTY[box.value] || {})[bundledId] || 1);" in src
    assert "addRequest(bundledId, bundledQuantity, true);" in src


def test_user_selected_support_quantity_can_exceed_automatic_or_minimum():
    src = APP_PATH.read_text(encoding="utf-8")

    # addRequest keeps the larger quantity, so if OR auto-adds one shared recovery module
    # but the user explicitly requests three, the explicit quantity wins.
    assert "prev.quantity = Math.max(prev.quantity, quantity)" in src
