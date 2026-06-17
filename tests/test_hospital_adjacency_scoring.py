from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def app_source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_hospital_adjacency_rules_encode_guideline_clusters():
    src = app_source()

    assert "const HOSPITAL_ADJACENCY_RULES" in src
    assert "USER_PDF_MEDICAL_FACILITY_GUIDELINE_2018" in src
    assert "operating_room" in src
    assert "recovery_room" in src
    assert "['operating_room','recovery_room',100" in src
    assert "['operating_room','surgery_support',100" in src
    assert "['operating_room','central_supply',70" in src
    assert "['emergency_care','observation_4bed',100" in src
    assert "['emergency_care','ct_suite',70" in src
    assert "['ct_suite','xray_room',100" in src
    assert "['specimen_collection','diagnostic_lab',70" in src
    assert "['delivery_room','newborn_treatment',100" in src


def test_hospital_layout_candidates_are_scored_by_adjacency_before_single_result():
    src = app_source()

    assert "const HOSPITAL_RELATED_GROUPS" in src
    assert "function buildHospitalProgramGroups" in src
    assert "function hospitalGroupRows" in src
    assert "function blockHasFacingRows" in src
    assert "function hospitalProgramCentroids" in src
    assert "function scoreHospitalAdjacency" in src
    assert "function chooseBestHospitalLayoutCandidate" in src
    assert "adjacencyScore" in src
    assert "adjacencySummary" in src
    assert "strategy<6" in src
    assert "layoutOptions = [best]" in src
    assert "hospital_program:group_corridor_adjacency_scored" in src


def test_hospital_grouping_keeps_related_rooms_in_small_corridor_wrapped_units():
    src = app_source()

    assert "maxPerGroup: 3" in src
    assert "const HOSPITAL_GROUP_INTERNAL_GAP_CELLS = 0" in src
    assert "function hospitalRowWidth" in src
    assert "function advanceHospitalModuleColumn" in src
    assert "markHospitalInternalCorridorGap" in src
    assert "응급-관찰-처치 group" in src
    assert "영상검사 group" in src
    assert "검체-진단-병리 group" in src
    assert "수술 core group" in src
    assert "groupKey" in src
    assert "hospital_program:group_corridor_adjacency_scored" in src


def test_large_hospital_groups_are_split_into_facing_rows_not_single_lumps():
    src = app_source()

    assert "if (mods.length <= 3) return [mods]" in src
    assert "const rowCount = Math.ceil(mods.length / 3)" in src
    assert "const half = Math.ceil(rowsOut.length / 2)" in src
    assert "blockHasFacingRows" in src


def test_related_rooms_touch_inside_a_cluster_but_different_blocks_keep_corridor_buffer():
    src = app_source()

    assert "const HOSPITAL_GROUP_INTERNAL_GAP_CELLS = 0" in src
    assert "같은 block 내부의 실은 붙이되" in src
    assert "function canPlaceDepartmentBlockWithBuffer" in src
    assert "if (grid[r][c] !== 0 && grid[r][c] !== 1) return false" in src
    assert "keep a corridor buffer between different functional blocks" in src


def test_hospital_option_panel_explains_adjacency_logic():
    src = app_source()

    assert "인접성 점수" in src
    assert "수술 cluster" in src
    assert "응급-영상 cluster" in src
    assert "검사 cluster" in src
