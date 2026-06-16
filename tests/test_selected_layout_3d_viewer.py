from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "graduation_hospital_planner" / "grid_drag_canvas_app.py"


def source() -> str:
    return APP_PATH.read_text(encoding="utf-8")


def test_3d_viewer_button_panel_and_external_scripts_are_removed():
    text = source()

    assert "View Selected Layout in 3D" not in text
    assert "id=\"threeDPanel\"" not in text
    assert "id=\"threeDCanvas\"" not in text
    assert "renderSelectedLayout3D" not in text
    assert "three.js" not in text
    assert "GLTFLoader" not in text
    assert "new THREE.WebGLRenderer" not in text


def test_3d_model_and_furniture_loading_code_is_removed():
    text = source()

    assert "FURNITURE_MODEL_DIR" not in text
    assert "FURNITURE_MODEL_FILES" not in text
    assert "load_furniture_model_data_urls" not in text
    assert "FURNITURE_MODEL_URLS" not in text
    assert "const FURNITURE_LIBRARY" not in text
    assert "build3DMassesFromGrid" not in text
    assert "addFurnitureItem3D" not in text


def test_2d_plan_canvas_and_layout_generation_remain_available():
    text = source()

    assert "Planning Canvas" in text
    assert "canvas id=\"grid\"" in text
    assert "Generate / Regenerate Layout Options" in text
    assert "generateHospitalLayoutOptions" in text
    # 마우스휠 확대축소 제거: 캔버스는 카드 폭에 맞춰 고정 표시(fitPlanCanvas)
    assert "let planZoom" not in text
    assert "canvas.addEventListener('wheel'" not in text
    assert "function fitPlanCanvas" in text
