from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_selected_layout_has_3d_view_button_and_panel():
    text = source()
    assert "View Selected Layout in 3D" in text
    assert "id=\"threeDPanel\"" in text
    assert "id=\"threeDCanvas\"" in text
    assert "renderSelectedLayout3D" in text


def test_3d_viewer_builds_room_masses_from_current_grid_not_dummy_data():
    text = source()
    assert "function build3DMassesFromGrid" in text
    assert "function greedyRectangulateValue" in text
    assert "for (let r=0; r<rows; r++)" in text
    assert "grid[r][c]" in text
    assert "moduleCodes.negative_pressure_patient_room" in text
    assert "moduleCodes.controlled_corridor" in text


def test_3d_viewer_supports_rotation_zoom_and_clear_warning():
    text = source()
    assert "threeDRotation" in text
    assert "threeDZoom" in text
    assert "mousedown" in text and "wheel" in text
    assert "No selected layout to view in 3D" in text
    assert "3D mass viewer" in text


def test_3d_ward_suite_masses_are_split_by_cluster_outline_not_only_color():
    text = source()
    assert "function rectangulateClusteredValue" in text
    assert "clusterGrid" in text
    assert "clusterId" in text
    build_window = text[text.index("function build3DMassesFromGrid"):text.index("function shadeHex")]
    assert "rectangulateClusteredValue(valueGrid, value, clusterSource)" in build_window
    assert "clusterId: rect.clusterId" in build_window


def test_3d_viewer_uses_threejs_webgl_floor_before_room_plates():
    text = source()
    assert "cdnjs.cloudflare.com/ajax/libs/three.js" in text
    assert "new THREE.WebGLRenderer" in text
    assert "preserveDrawingBuffer: true" in text
    render_window = text[text.index("function renderSelectedLayout3D"):text.index("threeDCanvas.addEventListener")]
    assert "initThreeViewer(sorted)" in render_window
    assert "sceneCenterFromMasses" in text
    assert "addWardFloorsAndWalls3D(sorted)" in render_window
    assert "THREE_ROOM_HEIGHT" in text
    assert "shared floor slab" in text


def test_3d_viewer_uses_one_unified_floor_datum_for_all_masses():
    text = source()
    assert "const GROUND_Z = 0" in text
    assert "const FLOOR_PLANE_Z = -0.03" in text
    assert "const FINISHED_FLOOR_Z = GROUND_Z" in text
    assert "baseZ: GROUND_Z" in text
    draw_window = text[text.index("function drawMassBox"):text.index("function renderSelectedLayout3D")]
    assert "const z0 = mass.baseZ" in draw_window
    assert "const z1 = mass.baseZ + mass.h * Z_HEIGHT_SCALE" in draw_window
    assert "same flat room floor plate" in text


def test_3d_viewer_adds_architectural_furniture_templates_by_module_type():
    text = source()
    assert "const FURNITURE_LIBRARY" in text
    assert "patient_bed" in text
    assert "headwall" in text
    assert "toilet_fixture" in text
    assert "shower_zone" in text
    assert "nurse_counter" in text
    assert "supply_shelving" in text
    assert "waste_bin" in text
    assert "function furnitureTemplateForMass" in text
    assert "function buildFurnitureFromMass" in text


def test_3d_viewer_repeats_identical_furniture_inside_modular_suite_clusters():
    text = source()
    assert "furnitureSignature" in text
    build_window = text[text.index("function build3DMassesFromGrid"):text.index("function shadeHex")]
    assert "furnitureSignature: furnitureSignatureForValue(value)" in build_window
    assert "clusterId: mass.clusterId" in text
    render_window = text[text.index("function renderSelectedLayout3D"):text.index("threeDCanvas.addEventListener")]
    assert "buildFurnitureFromMass" in render_window
    assert "addFurnitureItem3D" in render_window
    assert render_window.index("addWardFloorsAndWalls3D") < render_window.index("addFurnitureItem3D")


def test_3d_viewer_has_model_backed_architectural_visual_cues_not_only_solid_blocks():
    text = source()
    assert "new THREE.WebGLRenderer" in text
    assert "function addWardFloorsAndWalls3D" in text
    assert "function addFurnitureItem3D" in text
    assert "Three.js/WebGL ward viewer" in text
    assert "GLB-backed low-poly medical furniture models" in text
    assert "primitive fallback" in text


def test_3d_furniture_is_grounded_on_shared_floor_datum_not_floating():
    text = source()
    furniture_window = text[text.index("function buildFurnitureFromMass"):text.index("function build3DMassesFromGrid")]
    assert "baseZ: groundedFurnitureBaseForHeight(item.h)" in furniture_window
    assert "GROUND_Z + 0.035" not in furniture_window
    assert "base is locked to the same flat room floor plate" in furniture_window


def test_3d_rooms_use_webgl_cutaway_walls_instead_of_only_solid_colored_boxes():
    text = source()
    assert "const THREE_WALL_HEIGHT" in text
    assert "function addWardFloorsAndWalls3D" in text
    render_window = text[text.index("function renderSelectedLayout3D"):text.index("threeDCanvas.addEventListener")]
    assert "addWardFloorsAndWalls3D(sorted)" in render_window
    wall_window = text[text.index("function addWardFloorsAndWalls3D"):text.index("function addFurnitureItem3D")]
    assert "cutaway wall" in wall_window
    assert "room floor plate" in wall_window
    assert "for (const mass of sorted) drawMassBox" not in render_window


def test_3d_wall_segments_are_cutaway_lines_not_tall_room_boxes():
    text = source()
    assert "const WALL_HEIGHT = 0.24" in text
    wall_window = text[text.index("function drawWallSegment"):text.index("function drawDoorSwing")]
    assert "drawMassBox" not in wall_window
    assert "drawCutawayWallLine" in wall_window
    assert "setLineDash" in wall_window


def test_scroll_wheel_zoom_is_explicit_for_plan_and_3d_canvas():
    text = source()
    assert "let planZoom" in text
    assert "function applyPlanCanvasZoom" in text
    assert "canvas.addEventListener('wheel'" in text
    assert "threeDCanvas.addEventListener('wheel'" in text
    assert "wheel to zoom" in text


def test_zoom_limits_are_large_enough_for_close_architectural_inspection():
    text = source()
    assert "const PLAN_ZOOM_MAX = 4.0" in text
    assert "const THREE_D_ZOOM_MAX = 18.0" in text
    assert "const THREE_D_WHEEL_ZOOM_IN = 1.28" in text
    assert "const THREE_D_WHEEL_ZOOM_OUT = 0.82" in text
    assert "Math.min(PLAN_ZOOM_MAX" in text
    assert "Math.min(THREE_D_ZOOM_MAX" in text


def test_3d_viewer_supports_right_or_middle_drag_pan_after_zoom():
    text = source()
    assert "let threeDPan" in text
    assert "let threeDDragMode" in text
    assert "function panThreeCameraByScreenDelta" in text
    assert "setFromMatrixColumn(threeCamera.matrixWorld, 0)" in text
    assert "setFromMatrixColumn(threeCamera.matrixWorld, 1)" in text
    assert "threeDCanvas.addEventListener('contextmenu'" in text
    controls_window = text[text.index("threeDCanvas.addEventListener('contextmenu'"):text.index("canvas.addEventListener('wheel'")]
    assert "e.button === 0" in controls_window
    assert "'rotate'" in controls_window
    assert "'pan'" in controls_window
    assert "panThreeCameraByScreenDelta(dx, dy)" in controls_window
    assert "applyThreeCameraZoom()" in controls_window


def test_wall_height_is_low_cutaway_not_full_height():
    text = source()
    match = re.search(r"const WALL_HEIGHT = ([0-9.]+);", text)
    assert match, "WALL_HEIGHT constant missing"
    assert float(match.group(1)) <= 0.42
    assert "low cutaway wall" in text


def test_furniture_uses_shaped_3d_renderers_not_generic_box_masses():
    text = source()
    assert "function drawPatientBed" in text
    assert "function drawToiletFixture" in text
    assert "function drawNurseCounter" in text
    assert "function drawFurnitureVolume" in text
    assert "function drawFurnitureContactShadow" in text
    draw_window = text[text.index("function drawFurnitureItem"):text.index("function buildWallSegmentsFromMass")]
    assert "drawGenericFurnitureVolume(item" in draw_window
    assert "drawFurnitureFootprint(item" not in draw_window
    furniture_volume_window = text[text.index("function drawFurnitureVolume"):text.index("function drawFurnitureTopDetail")]
    assert "drawMassBox" not in furniture_volume_window
    assert "FURNITURE_HEIGHT_SCALE" in furniture_volume_window or "furnitureVisualHeight(item" in furniture_volume_window


def test_furniture_is_visually_grounded_on_flat_room_floor_with_shadow():
    text = source()
    assert "const FINISHED_FLOOR_Z = GROUND_Z" in text
    assert "const FURNITURE_SINK_Z" in text
    assert "const FURNITURE_BASE_Z = FINISHED_FLOOR_Z" in text
    assert "function furnitureZ(item) { return item.baseZ; }" in text
    assert "drawFurnitureContactShadow(item" in text
    furniture_window = text[text.index("function buildFurnitureFromMass"):text.index("function build3DMassesFromGrid")]
    assert "baseZ: groundedFurnitureBaseForHeight(item.h)" in furniture_window
    assert "base is locked to the same flat room floor plate" in furniture_window


def test_cutaway_walls_are_visible_translucent_panels_not_absent_lines():
    text = source()
    assert "function drawCutawayWallPanel" in text
    wall_window = text[text.index("function drawWallSegment"):text.index("function drawDoorSwing")]
    assert "drawCutawayWallPanel(segment" in wall_window
    assert "rgba(148,163,184,0.18)" in wall_window
    assert "drawMassBox" not in wall_window


def test_furniture_height_scale_is_strong_enough_to_read_as_3d_objects():
    text = source()
    match = re.search(r"const FURNITURE_HEIGHT_SCALE = ([0-9.]+);", text)
    assert match, "FURNITURE_HEIGHT_SCALE constant missing"
    assert float(match.group(1)) >= 1.15
    assert "FURNITURE_MIN_VISUAL_HEIGHT" in text
    furniture_volume_window = text[text.index("function drawFurnitureVolume"):text.index("function drawFurnitureTopDetail")]
    assert "FURNITURE_MIN_VISUAL_HEIGHT" in furniture_volume_window or "furnitureVisualHeight(item" in furniture_volume_window


def test_furniture_contact_is_drawn_slightly_into_floor_not_visually_hovering():
    text = source()
    assert "const FURNITURE_FLOOR_INTERSECT_Z" in text
    assert "const FURNITURE_GROUND_SHADOW_Z" in text
    assert "function furnitureVisualBaseZ" in text
    volume_window = text[text.index("function drawFurnitureVolume"):text.index("function drawFurnitureTopDetail")]
    assert "furnitureVisualBaseZ(item)" in volume_window
    assert "item.baseZ" not in volume_window.split("function drawFurnitureVolume", 1)[1].split("const z1", 1)[0]
    shadow_window = text[text.index("function drawFurnitureContactShadow"):text.index("function drawFurnitureVolume")]
    assert "FURNITURE_GROUND_SHADOW_Z" in shadow_window


def test_furniture_top_details_follow_the_same_visual_height_used_for_volume():
    text = source()
    assert "function furnitureVisualHeight" in text
    detail_window = text[text.index("function drawFurnitureTopDetail"):text.index("function childFurniture")]
    assert "furnitureVisualBaseZ(item) + furnitureVisualHeight(item)" in detail_window
    assert "item.h * FURNITURE_HEIGHT_SCALE" not in detail_window


def test_primary_furniture_uses_low_3d_objects_not_flat_soft_symbols():
    text = source()
    assert "function drawSoftFurniturePill" not in text
    assert "function drawSoftBedSymbol" not in text
    assert "function drawSoftToiletSymbol" not in text
    assert "function drawProjectedFurnitureOutline" not in text
    bed_window = text[text.index("function drawPatientBed"):text.index("function drawHeadwall")]
    toilet_window = text[text.index("function drawToiletFixture"):text.index("function drawShowerZone")]
    nurse_window = text[text.index("function drawNurseCounter"):text.index("function drawWorkstation")]
    assert "drawFurnitureVolume" in bed_window
    assert "drawRoundedProjectedTop" in bed_window
    assert "drawIsoEllipseCap" in bed_window
    assert "pillow" in bed_window and "railLeft" in bed_window and "railRight" in bed_window
    assert "drawCylinderFixture" in toilet_window
    assert "drawIsoEllipseCap" in toilet_window
    assert "plinth" in toilet_window and "bowl" in toilet_window and "tank" in toilet_window
    assert "drawFurnitureVolume" in nurse_window
    assert "drawRoundedProjectedTop" in nurse_window
    assert "returnWing" in nurse_window


def test_all_furniture_categories_are_dispatched_to_specific_3d_renderers():
    text = source()
    dispatch_window = text[text.index("function drawFurnitureItem"):text.index("function buildWallSegmentsFromMass")]
    for fn in [
        "drawPatientBed", "drawHeadwall", "drawToiletFixture", "drawShowerZone",
        "drawWashbasin", "drawBench", "drawCabinetOrShelving", "drawNurseCounter",
        "drawWorkstation", "drawTrolleyOrBin",
    ]:
        assert fn in dispatch_window
    for item_type in [
        "patient_bed", "headwall", "toilet_fixture", "shower_zone", "washbasin",
        "handwash_sink", "ppe_bench", "donning_cabinet", "supply_shelving",
        "nurse_counter", "workstation", "meds_trolley", "waste_bin", "medical_cart",
    ]:
        assert item_type in dispatch_window


def test_furniture_detail_renderers_keep_3d_projection_not_screen_billboard_scaling():
    text = source()
    detail_window = text[text.index("function drawFurnitureEdgeLine"):text.index("function buildWallSegmentsFromMass")]
    assert "project3DPoint" in detail_window
    assert "furnitureCorners(item" in detail_window
    assert "furnitureVisualBaseZ(item) + furnitureVisualHeight(item)" in detail_window
    assert "function projectedItemMetrics" in text
    assert "function drawIsoEllipseCap" in text
    assert "function drawRoundedProjectedTop" in text
    assert "function drawCylinderFixture" in text
    assert "quadraticCurveTo" in detail_window
    assert "ellipse" in detail_window
    assert "item.w * scale" not in detail_window
    assert "item.d * scale" not in detail_window
    assert "roundRect" not in detail_window


def test_primary_furniture_is_not_line_art_or_translucent_patch_regression():
    text = source()
    assert "function drawProjectedSoftPatch" not in text
    assert "drawProjectedSoftPatch" not in text
    assert "function projectedSoftFurnitureFootprint" not in text
    assert "function softFurnitureScreenBox" not in text
    assert "function drawFurnitureLineArtLabel" not in text
    render_window = text[text.index("function drawFurnitureItem"):text.index("function buildWallSegmentsFromMass")]
    assert "drawSoft" not in render_window
    assert "drawProjected" not in render_window


def test_threejs_furniture_uses_glb_models_without_billboard_labels():
    text = source()
    assert "const THREE_FURNITURE_SCALE = 1.38" in text
    assert "function scaledFurnitureRect" in text
    assert "GLTFLoader" in text
    assert "FURNITURE_MODEL_URLS" in text
    assert "FURNITURE_MODEL_BY_TYPE" in text
    assert "function addModelFurnitureItem3D" in text
    assert "function addPrimitiveFurnitureItem3D" in text
    assert "function addFurnitureEdgeLines" in text
    assert "THREE.EdgesGeometry" in text
    assert "semantic furniture silhouette edges" in text
    assert "function addFurnitureLabelSprite" not in text
    assert "function furnitureReadableLabel" not in text
    assert "THREE_FURNITURE_LABEL" not in text
    assert "furniture label" not in text
    assert "readable furniture labels" not in text
    assert "No in-scene text labels" in text
    assert "GLB-backed low-poly medical furniture models" in text
    assert "const view = Math.max(7.2, threeSceneCenter.span * 0.50)" in text
    furniture_window = text[text.index("function furnitureModelKeyForItem"):text.index("function renderSelectedLayout3D")]
    for cue in [
        "hospital_bed", "toilet", "washbasin", "shower", "nurse_counter",
        "medical_cart", "supply_shelf", "ppe_bench", "ppe_cabinet",
        "waste_bin", "dirty_worktop",
    ]:
        assert cue in furniture_window or cue in text
    assert "addFurnitureLabelSprite" not in furniture_window


def test_generated_glb_source_separates_bed_and_shelf_silhouettes():
    generator = (ROOT / "scripts" / "generate_ward_furniture_glb.py").read_text(encoding="utf-8")
    assert "Low, long bed silhouette" in generator
    assert "thin wheeled hospital bed deck" in generator
    assert "large rectangular blue mattress top" in generator
    assert "clear white pillow block at bed head" in generator
    assert "Open rack silhouette" in generator
    assert "thin upright shelf post" in generator
    assert "open white shelf board" in generator
    assert "blue folded linen stack" in generator
    assert "open supply shelving tall frame" not in generator


def test_glb_furniture_assets_exist_for_primary_medical_equipment():
    model_dir = ROOT / "assets" / "models" / "ward_furniture"
    for filename in [
        "hospital_bed.glb", "toilet.glb", "washbasin.glb", "shower.glb",
        "nurse_counter.glb", "medical_cart.glb", "supply_shelf.glb",
        "ppe_bench.glb", "ppe_cabinet.glb", "waste_bin.glb", "dirty_worktop.glb",
    ]:
        model_path = model_dir / filename
        assert model_path.exists(), filename
        assert model_path.read_bytes()[:4] == b"glTF"
        assert model_path.stat().st_size > 4000
