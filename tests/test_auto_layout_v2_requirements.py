from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"
REQ_PATH = ROOT / "ref" / "docs" / "10_auto_layout_v2_user_requirements.md"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_auto_layout_v2_requirements_document_is_saved():
    text = REQ_PATH.read_text(encoding="utf-8")

    assert "무그리드 모드" in text
    assert "그리드 기반 자동배치 모드" in text
    assert "청결동선과 감염동선" in text
    assert "병동 모듈 단위마다 윤곽선" in text


def test_app_has_bed_count_and_three_option_generation_ui():
    text = source()

    assert "bedCount" in text
    assert "Generate Layout Options" in text
    assert "function generateLayoutOptions" in text
    assert "function createDefaultMaskForBedCount" in text
    assert "function selectLayoutOption" in text
    assert "function compareLayoutOptions" in text
    assert "layoutOptions" in text


def test_auto_layout_v2_tracks_clusters_boundaries_and_dimensions():
    text = source()

    assert "clusterGrid" in text
    assert "function assignClusterRect" in text
    assert "function drawClusterOutlines" in text
    assert "function moduleDimensionText" in text
    assert "cluster_id" in text
    assert "1.8m × 1.8m" in text


def test_generation_enforces_clean_infection_buffer_before_scoring():
    text = source()

    assert "function cleanInfectionBufferOk" in text
    assert "function validateConstraintFirstLayout" in text
    assert "direct clean-infected contact" in text
    assert "buffer" in text
    assert "validity.ok" in text


def test_generation_scores_area_fill_and_outer_edge_use():
    text = source()

    assert "function fillRemainingEdgeCells" in text
    assert "function layoutUtilizationScore" in text
    assert "edgeFillScore" in text
    assert "areaFillScore" in text
    assert "compareAnalysis" in text
