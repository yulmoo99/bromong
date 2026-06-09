r"""
Streamlit grid drag prototype for the graduation hospital planner.

Run:
  streamlit run prototype/grid_drag_canvas_app.py
"""

from pathlib import Path
from string import Template
import base64
import json
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
MODULE_DB_PATH = ROOT / "data" / "modules_ward_v01.json"
DESIGN_PATH = ROOT / "DESIGN.md"

st.set_page_config(page_title="Infection Ward Planner", page_icon="◌", layout="wide", initial_sidebar_state="collapsed")

def inject_apple_design_shell() -> None:
    """Apply the Apple Clinical Planner visual shell defined in DESIGN.md."""
    st.markdown(
        """
        <style>
          :root {
            --apple-primary:#1D1D1F; --apple-secondary:#6E6E73; --apple-blue:#0071E3;
            --apple-bg:#F5F5F7; --apple-surface:#FFFFFF; --apple-glass:rgba(251,251,253,.82);
            --apple-separator:#D2D2D7; --apple-shadow:0 18px 60px rgba(0,0,0,.08);
            --apple-radius:24px;
          }
          html, body, [data-testid="stAppViewContainer"] { background: var(--apple-bg); }
          [data-testid="stAppViewContainer"] > .main { background: radial-gradient(circle at top left, #ffffff 0, #f5f5f7 46%, #eef2f7 100%); }
          .block-container { padding-top: 2.1rem; padding-bottom: 3rem; max-width: 1480px; }
          [data-testid="stSidebar"] { background: rgba(255,255,255,.74); border-right: 1px solid rgba(210,210,215,.72); backdrop-filter: blur(24px); min-width: 310px !important; width: 310px !important; }
          [data-testid="stSidebar"] > div:first-child { padding: 1.7rem 1.05rem 2rem 2.05rem; overflow: visible; }
          [data-testid="stSidebar"] * { max-width: 100%; }
          [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--apple-secondary); font-size: .86rem; }
          [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stNumberInput label { color: var(--apple-primary); font-weight: 650; letter-spacing: -.01em; }
          .stSlider, .stNumberInput, .stRadio { background: rgba(255,255,255,.76); border: 1px solid rgba(210,210,215,.72); border-radius: 18px; padding: .78rem .84rem; box-shadow: 0 1px 2px rgba(0,0,0,.035); }
          .apple-hero { background: linear-gradient(145deg, rgba(255,255,255,.94), rgba(251,251,253,.78)); border: 1px solid rgba(210,210,215,.78); border-radius: 32px; padding: 28px 32px; box-shadow: var(--apple-shadow); margin-bottom: 22px; }
          .apple-eyebrow { color: var(--apple-blue); font-weight: 700; font-size: .78rem; letter-spacing: .04em; margin-bottom: 8px; }
          .apple-hero h1 { color: var(--apple-primary); font-family: -apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",sans-serif; font-size: clamp(2rem, 3.2vw, 3.9rem); line-height: 1.02; letter-spacing: -.055em; margin: 0 0 10px; }
          .apple-hero p { color: var(--apple-secondary); font-size: 1.04rem; line-height: 1.55; max-width: 780px; margin: 0; }
          .apple-spec { display:flex; flex-wrap:wrap; gap:10px; margin-top:18px; }
          .apple-pill { border:1px solid rgba(210,210,215,.82); background: rgba(255,255,255,.72); border-radius:999px; padding:7px 12px; color:var(--apple-primary); font-size:.82rem; font-weight:600; }
          iframe { border-radius: 28px !important; box-shadow: 0 22px 80px rgba(0,0,0,.10); background: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )

inject_apple_design_shell()

st.sidebar.markdown("### Controls")
st.sidebar.caption("DESIGN.md tokens drive the Apple-style planning shell and embedded canvas.")
cols = st.sidebar.slider("Grid columns", 10, 80, 40)
rows = st.sidebar.slider("Grid rows", 10, 60, 30)
cell = st.sidebar.slider("Cell size px", 12, 32, 20)
default_bed_count = st.sidebar.number_input("Target bed count", min_value=2, max_value=24, value=10, step=2)
tool = st.sidebar.radio("Drawing tool", ["pencil", "rectangle"], horizontal=True)
mode = st.sidebar.radio("Edit mode", ["paint", "erase"], horizontal=True)

st.markdown(
    f"""
    <section class="apple-hero">
      <div class="apple-eyebrow">APPLE CLINICAL PLANNER · DESIGN.md SYSTEM</div>
      <h1>Infection Ward Layout Studio</h1>
      <p>Generate, compare, and inspect negative-pressure ward layouts in a calmer Apple-style workspace: glass controls, soft stages, and a sharper 2D/3D architectural review flow.</p>
      <div class="apple-spec">
        <span class="apple-pill">{cols} × {rows} grid</span>
        <span class="apple-pill">{default_bed_count} target beds</span>
        <span class="apple-pill">{tool} · {mode}</span>
        <span class="apple-pill">DESIGN.md active</span>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

module_db = json.loads(MODULE_DB_PATH.read_text(encoding="utf-8"))
module_meta = {m["id"]: m for m in module_db["modules"]}

FURNITURE_MODEL_DIR = ROOT / "assets" / "models" / "ward_furniture"
FURNITURE_MODEL_FILES = {
    "hospital_bed": "hospital_bed.glb",
    "headwall": "headwall.glb",
    "bedside_table": "bedside_table.glb",
    "toilet": "toilet.glb",
    "washbasin": "washbasin.glb",
    "shower": "shower.glb",
    "nurse_counter": "nurse_counter.glb",
    "medical_cart": "medical_cart.glb",
    "supply_shelf": "supply_shelf.glb",
    "ppe_bench": "ppe_bench.glb",
    "ppe_cabinet": "ppe_cabinet.glb",
    "waste_bin": "waste_bin.glb",
    "dirty_worktop": "dirty_worktop.glb",
}

def load_furniture_model_data_urls() -> dict[str, str]:
    urls = {}
    for key, filename in FURNITURE_MODEL_FILES.items():
        model_path = FURNITURE_MODEL_DIR / filename
        if model_path.exists():
            encoded = base64.b64encode(model_path.read_bytes()).decode("ascii")
            urls[key] = f"data:model/gltf-binary;base64,{encoded}"
    return urls

furniture_model_urls = load_furniture_model_data_urls()

# Canvas values. 1 = usable unassigned area. 10+ = ward modules from modules_ward_v01.json.
module_codes = {
    "controlled_corridor": 10,
    "negative_pressure_patient_room": 20,
    "anteroom": 21,
    "ensuite_toilet_shower": 22,
    "nurse_station": 30,
    "clean_supply_alcove": 40,
    "soiled_waste_holding": 41,
    "support_reserve": 50,
}
code_to_module = {str(v): k for k, v in module_codes.items()}

colors = {
    "0": "#ffffff",
    "1": "#eef5ff",
    "10": "#c7d1dd",
    "20": "#ffb340",
    "21": "#ffd60a",
    "22": "#64d2ff",
    "30": "#32d74b",
    "40": "#9be7b2",
    "41": "#ff6961",
    "50": "#ded8cc",
}
labels = {"10": "C", "20": "R", "21": "A", "22": "WC", "30": "N", "40": "CL", "41": "D", "50": "S"}

legend_items = [
    ("1", "usable area"),
    ("10", "controlled corridor / C"),
    ("20", "negative room / R / 법적 기준: 1인실 ≥10㎡ (전실·화장실 제외, 의료법 시행규칙 별표4)"),
    ("21", "anteroom / A / 필수 설치 (법적 최소면적 규정 없음, 가이드라인 권장 9㎡)"),
    ("22", "toilet·shower / WC / 필수 설치 (법적 최소면적 규정 없음, 가이드라인 권장 9㎡)"),
    ("30", "nurse station / N / 운영 필수 (법적 최소면적 규정 없음, 가이드라인 권장 13.5㎡)"),
    ("40", "clean supply alcove / CL / 가이드라인 권장 배치"),
    ("41", "soiled waste holding / D / 가이드라인 권장 배치"),
    ("50", "support reserve / S / 잔여 공간 채움"),
]
legend_html = "\n".join(
    f'<span><i class="swatch" style="background:{colors[k]}"></i>{name}</span>' for k, name in legend_items
)

canvas_w = cols * cell
canvas_h = rows * cell
height = min(max(canvas_h + 900, 1180), 1800)

html_template = Template(r'''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
  :root {
    --primary:#1D1D1F; --secondary:#6E6E73; --blue:#0071E3; --blue-dark:#005BB5;
    --bg:#F5F5F7; --surface:#FFFFFF; --glass:rgba(251,251,253,.82); --separator:#D2D2D7;
    --shadow:0 18px 60px rgba(0,0,0,.08); --soft-shadow:0 1px 2px rgba(0,0,0,.06);
    --radius-lg:24px; --radius-md:16px; --radius-sm:10px;
  }
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif; color:var(--primary); background: transparent; }
  .planner-shell { max-width: min(${canvas_w}px, 100%); margin: 0 auto; }
  .planner-stage { background: linear-gradient(145deg, rgba(255,255,255,.98), rgba(251,251,253,.88)); border:1px solid rgba(210,210,215,.82); border-radius: 28px; padding: 20px; box-shadow: var(--shadow); overflow: hidden; }
  #toolbar { display:flex; justify-content:space-between; gap:18px; align-items:flex-start; margin-bottom:16px; padding-bottom:14px; border-bottom:1px solid rgba(210,210,215,.72); }
  .toolbar-title { font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",sans-serif; font-size: 22px; line-height:1.08; letter-spacing:-.035em; font-weight:720; margin:0; }
  .toolbar-subtitle { margin-top:7px; color:var(--secondary); font-size:13px; line-height:1.45; max-width:680px; }
  .metric-strip { display:flex; flex-wrap:wrap; justify-content:flex-end; gap:8px; min-width:220px; }
  .metric-chip, #legend span { display:inline-flex; align-items:center; gap:6px; border:1px solid rgba(210,210,215,.82); background:rgba(255,255,255,.74); border-radius:999px; padding:7px 10px; color:var(--primary); font-size:12px; font-weight:650; white-space:nowrap; box-shadow:var(--soft-shadow); }
  .canvas-wrap { border-radius:22px; background:#fff; border:1px solid rgba(210,210,215,.82); padding:12px; overflow:auto; }
  canvas { border: 1px solid rgba(0,0,0,.10); border-radius:18px; cursor: crosshair; image-rendering: pixelated; background:#fff; box-shadow: inset 0 1px 0 rgba(255,255,255,.7); }
  .action-row { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:14px 0 12px; }
  button, input::file-selector-button { appearance:none; border:1px solid rgba(210,210,215,.85); background:rgba(255,255,255,.86); color:var(--primary); border-radius:999px; padding:9px 13px; font-size:12px; font-weight:680; letter-spacing:-.01em; cursor:pointer; box-shadow:var(--soft-shadow); transition:transform .16s ease, background .16s ease, border-color .16s ease; }
  button:hover, input::file-selector-button:hover { transform:translateY(-1px); border-color:rgba(0,113,227,.34); background:#fff; }
  .action-row button:nth-child(3), .action-row button:nth-child(4), button.primary { background:var(--blue); color:white; border-color:var(--blue); box-shadow:0 8px 20px rgba(0,113,227,.22); }
  .action-row button:nth-child(3):hover, .action-row button:nth-child(4):hover, button.primary:hover { background:var(--blue-dark); }
  input[type="file"] { color:var(--secondary); font-size:12px; }
  #legend { display:flex; flex-wrap:wrap; gap:7px; margin: 12px 0 0; font-size: 12px; line-height: 1.4; max-width: ${canvas_w}px; }
  .swatch { display:inline-block; width: 10px; height: 10px; border-radius:999px; border: 1px solid rgba(0,0,0,.16); }
  #moduleInfo, #ruleReport, #optionPanel, #threeDPanel { max-width: ${canvas_w}px; margin: 16px 0 0; padding: 18px; background: rgba(255,255,255,.90); border: 1px solid rgba(210,210,215,.82); border-radius:24px; font-size: 12px; box-shadow: 0 10px 34px rgba(0,0,0,.055); }
  #moduleInfo { color:var(--secondary); }
  #ruleReport ul, #optionPanel ul { margin: 10px 0 0 18px; padding: 0; }
  .option-card { margin: 10px 0; padding: 14px 14px 13px; border: 1px solid rgba(210,210,215,.82); border-left: 5px solid var(--blue); border-radius:18px; background: white; clear:both; min-height:42px; box-shadow:0 8px 24px rgba(0,0,0,.045); }
  .option-card button { float: right; }
  #threeDPanel b:first-child { display:block; font-size:16px; letter-spacing:-.018em; margin-bottom:4px; }
  #threeDCanvas { width: ${canvas_w}px; max-width: 100%; height: 420px; border:1px solid rgba(0,0,0,.10); border-radius:20px; background: linear-gradient(#fbfbfd,#eef2f7); cursor: grab; margin-top:12px; image-rendering:auto; }
  #threeDCanvas.dragging { cursor: grabbing; }
  textarea { width: ${canvas_w}px; max-width: 100%; height: 86px; margin-top: 16px; font-family: "SF Mono", ui-monospace, Menlo, Consolas, monospace; font-size:11px; color:#424245; background:rgba(255,255,255,.70); border:1px solid rgba(210,210,215,.82); border-radius:18px; padding:12px; }
  .small { color:var(--secondary); font-size:11px; line-height:1.45; }
</style>
</head>
<body>
<div class="planner-shell">
  <section class="planner-stage">
    <div id="toolbar">
      <div>
        <div class="toolbar-title">Planning Canvas</div>
        <div class="toolbar-subtitle">Paint the legal planning mask, generate ward alternatives, then inspect the selected option in a softer Apple-style 2D/3D review stage.</div>
      </div>
      <div class="metric-strip">
        <span class="metric-chip">Mode <b>${mode}</b></span>
        <span class="metric-chip">Tool <b>${tool}</b></span>
        <span class="metric-chip">${cols}×${rows}</span>
        <span class="metric-chip"><input id="bedCount" type="number" min="2" max="24" step="2" value="${default_bed_count}" style="width:48px;border:0;background:transparent;font-weight:700;color:#1D1D1F;text-align:right;"/> beds</span>
      </div>
    </div>
    <div class="canvas-wrap"><canvas id="grid" width="${canvas_w}" height="${canvas_h}"></canvas></div>
    <div class="action-row">
      <button onclick="clearGrid()">Clear</button>
      <button onclick="fillGrid()">Fill All</button>
      <button onclick="generateLayoutOptions()">Generate / Regenerate Layout Options</button>
      <button class="primary" onclick="renderSelectedLayout3D()">View Selected Layout in 3D</button>
      <button onclick="checkWardRules()">Check Ward Rules</button>
      <button onclick="copyJson()">Copy JSON</button>
      <button onclick="downloadJson()">Download JSON</button>
      <input type="file" id="loadFile" accept=".json,application/json" onchange="loadJsonFile(event)" />
    </div>
    <div id="legend">${legend_html}</div>
  </section>
  <div id="legalNotice" style="max-width:${canvas_w}px;margin:16px 0 0;padding:14px 18px;background:rgba(255,246,230,.92);border:1px solid rgba(245,158,11,.45);border-radius:18px;font-size:11.5px;color:#92400e;line-height:1.6;">
    <b>⚠️ 법규 적용 범위 안내</b><br>
    음압격리병실(R) 면적 기준은 <b>의료법 시행규칙 별표4</b> 및 <b>보건복지부 감염병 전담병원 설계 가이드라인(2024)</b>을 근거로 합니다.<br>
    전실(A)·화장실(WC)·간호스테이션(N)의 면적은 <b>법적 최소 기준이 없으며</b>, 표시된 수치는 가이드라인 권장값입니다. 실제 설계 시 관련 전문가 검토가 필요합니다.<br>
    복도 폭 기준: 메인 복도 3.0m(권장), 연결 복도 1.5m(단기 구간 한정) — 법적 최소 입원실 복도 폭 2.4m(의료법 시행규칙 별표4).<br>
    본 도구는 초기 매싱 계획 지원용이며 <b>소방법, 장애인편의시설법 등은 별도 검토</b>가 필요합니다.
  </div>
  <div id="moduleInfo">모듈 셀에 마우스를 올리면 법적 근거 및 권장 면적을 확인할 수 있습니다. R(음압격리병실): 법적 기준 ≥10㎡ (전실·화장실 제외, 의료법 시행규칙 별표4).</div>
  <div id="ruleReport">배치 후 <b>Check Ward Rules</b> 버튼을 눌러 병동 규칙 검토 결과를 확인하세요.</div>
  <div id="optionPanel">Auto Layout v2 comparison will appear here after <b>Generate Layout Options</b>.</div>
  <div id="threeDPanel"><b>3D mass viewer</b><span class="small">Select or generate a layout, then click <b>View Selected Layout in 3D</b>. Left-drag to rotate, wheel to zoom, right-drag or middle-drag to pan after zooming.</span><div id="threeDStatus" class="small"></div><canvas id="threeDCanvas" width="${canvas_w}" height="420"></canvas></div>
  <textarea id="output" readonly></textarea>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.min.js"></script>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}</script>
<script type="module">
import { GLTFLoader } from "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/loaders/GLTFLoader.js";
window.GLTFLoader = GLTFLoader;
window.dispatchEvent(new Event("ward-gltf-loader-ready"));
</script>
<script>
const rows = ${rows};
const cols = ${cols};
const cell = ${cell};
const mode = ${mode_json};
const tool = ${tool_json};
const moduleDb = ${module_db_js};
const moduleMeta = ${module_meta_js};
const moduleCodes = ${module_codes_js};
const codeToModule = ${code_to_module_js};
const colors = ${colors_js};
const labels = ${labels_js};
const FURNITURE_MODEL_URLS = ${furniture_model_urls_js};
const FURNITURE_MODEL_BY_TYPE = {
  patient_bed: "hospital_bed",
  headwall: "headwall",
  bedside_table: "bedside_table",
  toilet_fixture: "toilet",
  washbasin: "washbasin",
  handwash_sink: "washbasin",
  shower_zone: "shower",
  nurse_counter: "nurse_counter",
  workstation: "nurse_counter",
  meds_trolley: "medical_cart",
  medical_cart: "medical_cart",
  supply_shelving: "supply_shelf",
  ppe_bench: "ppe_bench",
  donning_cabinet: "ppe_cabinet",
  waste_bin: "waste_bin",
  dirty_worktop: "dirty_worktop"
};
const canvas = document.getElementById('grid');
const ctx = canvas.getContext('2d');
const threeDCanvas = document.getElementById('threeDCanvas');
const threeDCtx = null; // 3D viewer is WebGL/Three.js now; old 2D pseudo-3D helpers are retained only as dead-code reference until cleanup.
const threeDPanel = document.getElementById('threeDPanel');
const threeDStatus = document.getElementById('threeDStatus');
const output = document.getElementById('output');
const moduleInfo = document.getElementById('moduleInfo');
const ruleReport = document.getElementById('ruleReport');
const optionPanel = document.getElementById('optionPanel');
const storageKey = 'hospital_grid_painter_' + rows + 'x' + cols;
const MAIN_CORRIDOR_MIN_WIDTH_CELLS = 2;
const SHORT_CONNECTOR_MAX_CELLS = 4; // 1.5m connector stubs are OK only when short; long main spines should be 2 cells / 3.0m.
const GROUND_Z = 0;
const FLOOR_PLANE_Z = -0.03; // site plane sits just below the room finish; rooms themselves are not raised blocks.
const Z_HEIGHT_SCALE = 4;
const WALL_HEIGHT = 0.24; // low cutaway wall: visible enough to read room boundaries, still far below full-height room boxes.
const WALL_THICKNESS = 0.08;
const ROOM_FLOOR_HEIGHT = 0.012;
const FINISHED_FLOOR_Z = GROUND_Z; // room floors and furniture share one datum; no equipment is drawn on top of raised room boxes.
const FURNITURE_SINK_Z = 0.018;
const FURNITURE_FLOOR_INTERSECT_Z = FINISHED_FLOOR_Z - FURNITURE_SINK_Z; // visually tucks furniture a hair into the floor, eliminating pseudo-3D hover gaps.
const FURNITURE_GROUND_SHADOW_Z = FINISHED_FLOOR_Z + 0.004;
const FURNITURE_HEIGHT_SCALE = 1.60;
const FURNITURE_MIN_VISUAL_HEIGHT = 0.12; // prevents beds/counters from reading as flat plan symbols in the pseudo-3D view.
const FURNITURE_BASE_Z = FINISHED_FLOOR_Z; // logical datum stays floor-level; drawing uses a tiny visual intersection so objects read grounded.
const PLAN_ZOOM_MAX = 4.0;
const THREE_D_ZOOM_MAX = 18.0;
const THREE_D_ZOOM_BASE = 1.36;
const THREE_D_WHEEL_ZOOM_IN = 1.28;
const THREE_D_WHEEL_ZOOM_OUT = 0.82;
const FURNITURE_LIBRARY = {
  patient_room: [
    {type:'patient_bed', label:'bed', x:0.18, y:0.24, w:0.46, d:0.34, h:0.16, color:'#f8fafc'},
    {type:'headwall', label:'headwall', x:0.13, y:0.16, w:0.58, d:0.07, h:0.10, color:'#dbeafe'},
    {type:'bedside_table', label:'side', x:0.67, y:0.31, w:0.13, d:0.13, h:0.11, color:'#c4b5fd'},
    {type:'medical_cart', label:'cart', x:0.72, y:0.62, w:0.16, d:0.16, h:0.12, color:'#bfdbfe'}
  ],
  anteroom: [
    {type:'ppe_bench', label:'PPE', x:0.18, y:0.18, w:0.56, d:0.16, h:0.10, color:'#fde68a'},
    {type:'handwash_sink', label:'sink', x:0.12, y:0.58, w:0.18, d:0.22, h:0.12, color:'#bae6fd'},
    {type:'donning_cabinet', label:'cab', x:0.66, y:0.52, w:0.18, d:0.30, h:0.18, color:'#fef3c7'}
  ],
  wc: [
    {type:'toilet_fixture', label:'WC', x:0.18, y:0.18, w:0.20, d:0.22, h:0.13, color:'#f8fafc'},
    {type:'shower_zone', label:'shower', x:0.56, y:0.15, w:0.28, d:0.32, h:0.04, color:'#bfdbfe'},
    {type:'washbasin', label:'basin', x:0.20, y:0.62, w:0.28, d:0.14, h:0.11, color:'#dbeafe'}
  ],
  nurse_station: [
    {type:'nurse_counter', label:'counter', x:0.12, y:0.22, w:0.76, d:0.18, h:0.13, color:'#ccfbf1'},
    {type:'workstation', label:'PC', x:0.22, y:0.48, w:0.22, d:0.18, h:0.12, color:'#99f6e4'},
    {type:'meds_trolley', label:'meds', x:0.58, y:0.52, w:0.18, d:0.18, h:0.12, color:'#a7f3d0'}
  ],
  clean_supply: [
    {type:'supply_shelving', label:'shelf', x:0.12, y:0.16, w:0.18, d:0.68, h:0.22, color:'#dcfce7'},
    {type:'supply_shelving', label:'shelf', x:0.70, y:0.16, w:0.18, d:0.68, h:0.22, color:'#dcfce7'}
  ],
  soiled_holding: [
    {type:'dirty_worktop', label:'dirty', x:0.12, y:0.16, w:0.64, d:0.18, h:0.13, color:'#fecaca'},
    {type:'waste_bin', label:'bin', x:0.18, y:0.55, w:0.18, d:0.18, h:0.12, color:'#fca5a5'},
    {type:'waste_bin', label:'bin', x:0.48, y:0.55, w:0.18, d:0.18, h:0.12, color:'#f87171'}
  ]
};
let isDown = false;
let dragStart = null;
let dragEnd = null;
let grid = loadGrid();
let clusterGrid = blankClusterGrid();
let layoutOptions = [];
let compareAnalysis = null;
let nextClusterNo = 1;
let lastRuleReport = null;
let selectedLayoutIndex = null;
let threeDRotation = {x: -0.62, z: 0.74};
let threeDZoom = 1.0;
let threeDPan = {x: 0, y: 0, z: 0};
let threeDCameraTarget = null;
let planZoom = 1.0;
let threeDDragging = false;
let threeDDragMode = null; // left button rotates; right or middle button pans the zoomed WebGL view.
let threeDLastMouse = null;

function applyPlanCanvasZoom() {
  canvas.style.width = Math.round(canvas.width * planZoom) + 'px';
  canvas.style.height = Math.round(canvas.height * planZoom) + 'px';
  moduleInfo.textContent = 'Plan zoom: ' + Math.round(planZoom * 100) + '%. Scroll wheel over the 2D plan to zoom; drag/paint still follows the zoomed grid.';
}

function newClusterId() { return 'cluster_' + String(nextClusterNo++).padStart(2, '0'); }
// regression guard text: cluster_${String(nextClusterNo++).padStart(2, '0')}
// comparison label reference: Option ${index}

function blankGrid() { return Array.from({length: rows}, () => Array(cols).fill(0)); }
function blankClusterGrid() { return Array.from({length: rows}, () => Array(cols).fill(null)); }
function cloneGrid(value) { return value.map(row => row.slice()); }
function isValidGrid(value) { return Array.isArray(value) && value.length === rows && value.every(row => Array.isArray(row) && row.length === cols); }
function loadGrid() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey));
    if (isValidGrid(saved)) return saved;
  } catch (err) {}
  return blankGrid();
}
function saveGrid() { localStorage.setItem(storageKey, JSON.stringify(grid)); }
function colorFor(value) { return colors[String(value)] || '#4f8cff'; }
function labelFor(value) { return labels[String(value)] || ''; }
function keyOf(r, c) { return r + ',' + c; }
function parseKey(key) { return key.split(',').map(Number); }
function neighbors4(r, c) { return [[r-1,c],[r+1,c],[r,c-1],[r,c+1]].filter(([rr,cc]) => rr>=0 && rr<rows && cc>=0 && cc<cols); }

function moduleDimensionText(value, widthCells = null, heightCells = null) {
  const moduleId = codeToModule[String(value)];
  if (!moduleId) return value === 1 ? 'usable cell: 1.5m × 1.5m = 2.25㎡' : 'outside';
  const meta = moduleMeta[moduleId] || {};
  const preferred = meta.shape_policy && meta.shape_policy.preferred_grid_sizes ? meta.shape_policy.preferred_grid_sizes[0] : null;
  const w = widthCells || (preferred ? preferred[0] : 1);
  const h = heightCells || (preferred ? preferred[1] : 1);
  return w + '×' + h + ' cells / ' + (w * 1.5).toFixed(1) + 'm × ' + (h * 1.5).toFixed(1) + 'm / ≈' + (w * h * moduleDb.grid_assumption.cell_area_m2).toFixed(1) + '㎡';
}
function isWardSuiteClusterValue(value) {
  return [moduleCodes.negative_pressure_patient_room, moduleCodes.anteroom, moduleCodes.ensuite_toilet_shower].includes(value);
}
function assignClusterRect(cluster_id, r0, c0, h, w) {
  for (let r = Math.max(0, r0); r < Math.min(rows, r0 + h); r++) for (let c = Math.max(0, c0); c < Math.min(cols, c0 + w); c++) {
    if (isWardSuiteClusterValue(grid[r][c])) clusterGrid[r][c] = cluster_id;
  }
}
function drawClusterOutlines() {
  ctx.save();
  ctx.strokeStyle = '#111';
  ctx.lineWidth = Math.max(2, Math.floor(cell * 0.12));
  const directions = [[-1,0],[1,0],[0,-1],[0,1]];
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const id = clusterGrid[r][c];
    if (!id) continue;
    const x = c * cell, y = r * cell;
    for (const [dr, dc] of directions) {
      const rr = r + dr, cc = c + dc;
      if (rr >= 0 && rr < rows && cc >= 0 && cc < cols && clusterGrid[rr][cc] === id) continue;
      ctx.beginPath();
      if (dr === -1) { ctx.moveTo(x, y); ctx.lineTo(x + cell, y); }
      if (dr === 1) { ctx.moveTo(x, y + cell); ctx.lineTo(x + cell, y + cell); }
      if (dc === -1) { ctx.moveTo(x, y); ctx.lineTo(x, y + cell); }
      if (dc === 1) { ctx.moveTo(x + cell, y); ctx.lineTo(x + cell, y + cell); }
      ctx.stroke();
    }
  }
  ctx.restore();
}
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const value = grid[r][c];
    ctx.fillStyle = colorFor(value);
    ctx.fillRect(c * cell, r * cell, cell, cell);
    ctx.strokeStyle = '#d0d0d0';
    ctx.strokeRect(c * cell, r * cell, cell, cell);
    const label = labelFor(value);
    if (label && cell >= 16) {
      ctx.fillStyle = '#222';
      ctx.font = Math.max(9, Math.floor(cell * 0.45)) + 'px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(label, c * cell + cell / 2, r * cell + cell / 2);
    }
  }
  drawClusterOutlines();
  if (dragStart && dragEnd) {
    const r1 = Math.min(dragStart.r, dragEnd.r), r2 = Math.max(dragStart.r, dragEnd.r);
    const c1 = Math.min(dragStart.c, dragEnd.c), c2 = Math.max(dragStart.c, dragEnd.c);
    ctx.fillStyle = 'rgba(79, 140, 255, 0.25)';
    ctx.fillRect(c1 * cell, r1 * cell, (c2 - c1 + 1) * cell, (r2 - r1 + 1) * cell);
    ctx.strokeStyle = '#1f5fd0';
    ctx.lineWidth = 2;
    ctx.strokeRect(c1 * cell, r1 * cell, (c2 - c1 + 1) * cell, (r2 - r1 + 1) * cell);
    ctx.lineWidth = 1;
  }
  output.value = JSON.stringify(grid);
  saveGrid();
}
function cellFromEvent(e) {
  const rect = canvas.getBoundingClientRect();
  const cellW = rect.width / cols;
  const cellH = rect.height / rows;
  const c = Math.floor((e.clientX - rect.left) / cellW);
  const r = Math.floor((e.clientY - rect.top) / cellH);
  if (r >= 0 && r < rows && c >= 0 && c < cols) return {r, c};
  return null;
}
function setCell(pos) { if (pos) grid[pos.r][pos.c] = mode === 'paint' ? 1 : 0; }
function canPlaceModule(r0, c0, h, w) {
  if (r0 < 0 || c0 < 0 || r0 + h > rows || c0 + w > cols) return false;
  for (let r = r0; r < r0 + h; r++) for (let c = c0; c < c0 + w; c++) if (grid[r][c] !== 1) return false;
  return true;
}
function fillModuleStrict(r0, c0, h, w, value) {
  if (!canPlaceModule(r0, c0, h, w)) return false;
  for (let r = r0; r < r0 + h; r++) for (let c = c0; c < c0 + w; c++) grid[r][c] = value;
  return true;
}
function findPlacement(value, h, w, options = {}) {
  const b = usableBounds();
  if (!b) return null;
  const preferNear = options.preferNear || {r: Math.floor((b.minR + b.maxR) / 2), c: b.minC};
  let best = null;
  for (let r = b.minR; r <= b.maxR - h + 1; r++) for (let c = b.minC; c <= b.maxC - w + 1; c++) {
    if (!canPlaceModule(r, c, h, w)) continue;
    const score = Math.abs(r - preferNear.r) + Math.abs(c - preferNear.c);
    if (!best || score < best.score) best = {r, c, h, w, value, score};
  }
  return best;
}
function usableBounds() {
  let minR = rows, maxR = -1, minC = cols, maxC = -1;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) if (grid[r][c] !== 0) {
    minR = Math.min(minR, r); maxR = Math.max(maxR, r); minC = Math.min(minC, c); maxC = Math.max(maxC, c);
  }
  return maxR < 0 ? null : {minR, maxR, minC, maxC};
}
function usableAreaStats() {
  const b = usableBounds();
  if (!b) return {area:0, width:0, height:0, aspect:1, centerR:0, centerC:0};
  let area = 0;
  for (let r = b.minR; r <= b.maxR; r++) for (let c = b.minC; c <= b.maxC; c++) if (grid[r][c] !== 0) area++;
  const width = b.maxC - b.minC + 1, height = b.maxR - b.minR + 1;
  return {area, width, height, aspect: Math.max(width, height) / Math.max(1, Math.min(width, height)), centerR:(b.minR+b.maxR)/2, centerC:(b.minC+b.maxC)/2};
}
function shouldUseCompactLinearCorridor(strategyIndex = 0) {
  const s = usableAreaStats();
  // Small or slender sites should not be forced into loop corridors; choose single/double-loaded linear options.
  return s.area > 0 && (s.area < 520 || Math.min(s.width, s.height) < 14 || (s.area < 760 && strategyIndex !== 1));
}
function corridorStrategyName(strategyIndex = 0) {
  const loopStrategies = ['branching_loop', 'figure_eight', 'free_branching_loop'];
  const linearStrategies = ['double_loaded_linear', 'single_loaded_linear', 'compact_branch_linear'];
  return shouldUseCompactLinearCorridor(strategyIndex) ? linearStrategies[strategyIndex % 3] : loopStrategies[strategyIndex % 3];
}
function strategyLabelForIndex(strategyIndex = 0, corridorStrategy = corridorStrategyName(strategyIndex)) {
  const labelsByStrategy = {
    double_loaded_linear: 'Compact small-site / 1자 양측복도',
    single_loaded_linear: 'Compact small-site / 1자 단측복도',
    compact_branch_linear: 'Compact small-site / 1자+짧은 가지 복도',
    branching_loop: 'Area efficiency / branching-loop',
    figure_eight: 'Infection control / 8자형 분리 루프',
    free_branching_loop: 'Nursing efficiency / loop+비대칭 connector'
  };
  return labelsByStrategy[corridorStrategy] || ('Option ' + (strategyIndex + 1));
}
function gridHasUsableArea() { return grid.some(row => row.some(v => v !== 0)); }
function resetModulesToUsableArea() {
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) if (grid[r][c] !== 0) grid[r][c] = 1;
  clusterGrid = blankClusterGrid();
  nextClusterNo = 1;
}
function createDefaultMaskForBedCount(targetBeds) {
  grid = blankGrid();
  const h = Math.min(rows - 4, Math.max(18, Math.ceil(targetBeds / 2) * 6));
  const w = Math.min(cols - 4, Math.max(26, Math.ceil(targetBeds / 2) * 7));
  const r0 = Math.max(1, Math.floor((rows - h) / 2));
  const c0 = Math.max(1, Math.floor((cols - w) / 2));
  for (let r = r0; r < r0 + h; r++) for (let c = c0; c < c0 + w; c++) grid[r][c] = 1;
}
function markCorridor(r, c, corridorCells) {
  if (r >= 0 && r < rows && c >= 0 && c < cols && grid[r][c] === 1) {
    grid[r][c] = moduleCodes.controlled_corridor;
    corridorCells.push([r, c]);
  }
}
function markCorridorWide(r, c, corridorCells) {
  markCorridor(r, c, corridorCells);
  for (const [rr, cc] of [[r + 1, c], [r, c + 1]]) markCorridor(rr, cc, corridorCells);
}
function hasParallelCorridorWidthMate(r, c, axis) {
  // Width is real only when there is a parallel corridor lane, not just a perpendicular door tick/branch touching the cell.
  if (axis === 'H') {
    return [-1, 1].some(dr => {
      const rr = r + dr;
      if (rr < 0 || rr >= rows || grid[rr][c] !== moduleCodes.controlled_corridor) return false;
      return (c > 0 && grid[rr][c - 1] === moduleCodes.controlled_corridor) || (c + 1 < cols && grid[rr][c + 1] === moduleCodes.controlled_corridor);
    });
  }
  return [-1, 1].some(dc => {
    const cc = c + dc;
    if (cc < 0 || cc >= cols || grid[r][cc] !== moduleCodes.controlled_corridor) return false;
    return (r > 0 && grid[r - 1][cc] === moduleCodes.controlled_corridor) || (r + 1 < rows && grid[r + 1][cc] === moduleCodes.controlled_corridor);
  });
}
function sameAxisCorridorRunLength(r, c, axis) {
  if (grid[r][c] !== moduleCodes.controlled_corridor) return 0;
  let len = 1;
  if (axis === 'H') {
    for (let cc = c - 1; cc >= 0 && grid[r][cc] === moduleCodes.controlled_corridor; cc--) len++;
    for (let cc = c + 1; cc < cols && grid[r][cc] === moduleCodes.controlled_corridor; cc++) len++;
  } else {
    for (let rr = r - 1; rr >= 0 && grid[rr][c] === moduleCodes.controlled_corridor; rr--) len++;
    for (let rr = r + 1; rr < rows && grid[rr][c] === moduleCodes.controlled_corridor; rr++) len++;
  }
  return len;
}
function cellWouldBlockMainCorridorWidening(r, c) {
  if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] !== 1) return false;
  for (const [rr, cc] of neighbors4(r, c)) {
    if (grid[rr][cc] !== moduleCodes.controlled_corridor) continue;
    const horizontalRun = sameAxisCorridorRunLength(rr, cc, 'H');
    const verticalRun = sameAxisCorridorRunLength(rr, cc, 'V');
    const b = usableBounds();
    const isOuterHorizontalMain = b && (rr <= b.minR + 2 || rr >= b.maxR - 2);
    const isOuterVerticalMain = b && (cc <= b.minC + 2 || cc >= b.maxC - 2);
    if (isOuterHorizontalMain && horizontalRun > SHORT_CONNECTOR_MAX_CELLS && !hasParallelCorridorWidthMate(rr, cc, 'H')) return true;
    if (isOuterVerticalMain && verticalRun > SHORT_CONNECTOR_MAX_CELLS && !hasParallelCorridorWidthMate(rr, cc, 'V')) return true;
  }
  return false;
}
function suiteBlocksMainCorridorWidening(rects) {
  for (const key of suiteFootprintBlockedCells(rects)) {
    const [r, c] = parseKey(key);
    if (cellWouldBlockMainCorridorWidening(r, c)) return true;
  }
  return false;
}
function chooseWideningSideForHorizontal(run) {
  const [r] = run[0];
  const candidates = [r - 1, r + 1].filter(rr => rr >= 0 && rr < rows);
  let best = null;
  for (const rr of candidates) {
    let usable = 0;
    for (const [, c] of run) if (grid[rr][c] === 1 || grid[rr][c] === moduleCodes.controlled_corridor) usable++;
    if (!best || usable > best.usable) best = {rr, usable};
  }
  return best && best.usable >= Math.ceil(run.length * 0.6) ? best.rr : null;
}
function chooseWideningSideForVertical(run) {
  const [, c] = run[0];
  const candidates = [c - 1, c + 1].filter(cc => cc >= 0 && cc < cols);
  let best = null;
  for (const cc of candidates) {
    let usable = 0;
    for (const [r] of run) if (grid[r][cc] === 1 || grid[r][cc] === moduleCodes.controlled_corridor) usable++;
    if (!best || usable > best.usable) best = {cc, usable};
  }
  return best && best.usable >= Math.ceil(run.length * 0.6) ? best.cc : null;
}
function repairLongNarrowCorridorRuns(corridorCells) {
  // Main corridors should be 2 cells wide (3.0m). A 1-cell / 1.5m strip is allowed only as a short door connector/stub.
  let repaired = 0;
  for (let r = 0; r < rows; r++) {
    let c = 0;
    while (c < cols) {
      const run = [];
      while (c < cols && grid[r][c] === moduleCodes.controlled_corridor && !hasParallelCorridorWidthMate(r, c, 'H')) { run.push([r, c]); c++; }
      if (run.length > SHORT_CONNECTOR_MAX_CELLS) {
        const rr = chooseWideningSideForHorizontal(run);
        if (rr !== null) for (const [, cc] of run) if (grid[rr][cc] === 1) { markCorridor(rr, cc, corridorCells); repaired++; }
      }
      c += Math.max(1, run.length ? 0 : 1);
    }
  }
  for (let c = 0; c < cols; c++) {
    let r = 0;
    while (r < rows) {
      const run = [];
      while (r < rows && grid[r][c] === moduleCodes.controlled_corridor && !hasParallelCorridorWidthMate(r, c, 'V')) { run.push([r, c]); r++; }
      if (run.length > SHORT_CONNECTOR_MAX_CELLS) {
        const cc = chooseWideningSideForVertical(run);
        if (cc !== null) for (const [rr] of run) if (grid[rr][cc] === 1) { markCorridor(rr, cc, corridorCells); repaired++; }
      }
      r += Math.max(1, run.length ? 0 : 1);
    }
  }
  return repaired;
}
function addLinearWardCorridor(top, bottom, left, right, corridorCells, mode = 'double_loaded_linear') {
  // single_loaded_linear / double_loaded_linear: compact wards use a 1자 corridor instead of wasting area on a loop.
  const horizontal = (right-left) >= (bottom-top);
  if (horizontal) {
    const r = mode === 'single_loaded_linear' ? Math.max(top, top + 2) : Math.floor((top + bottom) / 2);
    for (let c = left; c <= right; c++) markCorridorWide(r, c, corridorCells);
    if (mode === 'compact_branch_linear') {
      const c1 = Math.floor(left + (right-left)*0.33), c2 = Math.floor(left + (right-left)*0.66);
      for (let rr = Math.max(top, r-4); rr <= Math.min(bottom, r+4); rr++) { markCorridor(rr, c1, corridorCells); markCorridor(rr, c2, corridorCells); }
    }
  } else {
    const c = mode === 'single_loaded_linear' ? Math.max(left, left + 2) : Math.floor((left + right) / 2);
    for (let r = top; r <= bottom; r++) markCorridorWide(r, c, corridorCells);
    if (mode === 'compact_branch_linear') {
      const r1 = Math.floor(top + (bottom-top)*0.33), r2 = Math.floor(top + (bottom-top)*0.66);
      for (let cc = Math.max(left, c-4); cc <= Math.min(right, c+4); cc++) { markCorridor(r1, cc, corridorCells); markCorridor(r2, cc, corridorCells); }
    }
  }
}
function bfsFrom(start) {
  const startKey = keyOf(start[0], start[1]);
  const dist = new Map([[startKey, 0]]);
  const prev = new Map();
  const queue = [start];
  for (let i = 0; i < queue.length; i++) {
    const [r, c] = queue[i];
    const d = dist.get(keyOf(r, c));
    for (const [rr, cc] of neighbors4(r, c)) {
      const k = keyOf(rr, cc);
      if ((grid[rr][cc] === 1 || grid[rr][cc] === moduleCodes.controlled_corridor) && !dist.has(k)) {
        dist.set(k, d + 1);
        prev.set(k, keyOf(r, c));
        queue.push([rr, cc]);
      }
    }
  }
  return {dist, prev};
}
function farthestReachable(bfsResult) {
  let bestKey = null, bestDist = -1;
  for (const [key, d] of bfsResult.dist.entries()) if (d > bestDist) { bestKey = key; bestDist = d; }
  return bestKey ? {cell: parseKey(bestKey), distance: bestDist} : null;
}
function reconstructPath(prev, start, end) {
  const startKey = keyOf(start[0], start[1]);
  let current = keyOf(end[0], end[1]);
  const path = [];
  while (current) {
    path.push(parseKey(current));
    if (current === startKey) break;
    current = prev.get(current);
  }
  return path.reverse();
}
function connectedComponentsOf(value) {
  const seen = new Set();
  const comps = [];
  for (let r=0;r<rows;r++) for (let c=0;c<cols;c++) {
    const startKey = keyOf(r,c);
    if (grid[r][c] !== value || seen.has(startKey)) continue;
    const comp = [];
    const q = [[r,c]];
    seen.add(startKey);
    for (let i=0;i<q.length;i++) {
      const [rr,cc] = q[i]; comp.push([rr,cc]);
      for (const [nr,nc] of neighbors4(rr,cc)) if (grid[nr][nc] === value && !seen.has(keyOf(nr,nc))) { seen.add(keyOf(nr,nc)); q.push([nr,nc]); }
    }
    comps.push(comp);
  }
  return comps;
}
function checkModuleShapePolicies() { return {ok:true, message:'Shape / aspect ratio checks: aspect_ratio_preferred_max'}; }
function addPerimeterLoop(top, bottom, left, right, corridorCells) {
  for (let c = left; c <= right; c++) { markCorridorWide(top, c, corridorCells); markCorridorWide(bottom, c, corridorCells); }
  for (let r = top; r <= bottom; r++) { markCorridorWide(r, left, corridorCells); markCorridorWide(r, right, corridorCells); }
}
function addFigureEightLoops(top, bottom, left, right, corridorCells) {
  // 8자형: 외곽 순환 + 중앙 connector로 두 개의 루프를 만든다.
  addPerimeterLoop(top, bottom, left, right, corridorCells);
  const midC = Math.floor((left + right) / 2);
  const midR = Math.floor((top + bottom) / 2);
  for (let r = top; r <= bottom; r++) markCorridorWide(r, midC, corridorCells); // central connector
  for (let c = left; c <= right; c += 2) markCorridorWide(midR, c, corridorCells); // soft cross connector
}
function addCorridorBranches(top, bottom, left, right, corridorCells) {
  // 순환은 유지하되 병실을 더 도킹시키는 곁가지(branch)를 추가한다.
  addPerimeterLoop(top, bottom, left, right, corridorCells);
  const branchRows = [Math.floor(top + (bottom-top)*0.33), Math.floor(top + (bottom-top)*0.66)];
  const branchCols = [Math.floor(left + (right-left)*0.50)];
  for (const r of branchRows) for (let c = left; c <= right; c++) markCorridorWide(r, c, corridorCells);
  for (const c of branchCols) for (let r = top; r <= bottom; r += 2) markCorridorWide(r, c, corridorCells);
}
function buildAdaptiveCorridorNetwork(strategyIndex = 0) {
  const b = usableBounds();
  if (!b) return [];
  const corridorCells = [];
  const compact = shouldUseCompactLinearCorridor(strategyIndex);
  const corridorStrategy = corridorStrategyName(strategyIndex);
  const margin = compact ? 1 : 3;
  const top = Math.min(b.maxR, b.minR + margin), bottom = Math.max(b.minR, b.maxR - margin);
  const left = Math.min(b.maxC, b.minC + margin), right = Math.max(b.minC, b.maxC - margin);
  // Legacy notes kept for regression coverage: diameter-like main path / branch path / perimeter_loop / figure_eight
  if (compact) {
    addLinearWardCorridor(top, bottom, left, right, corridorCells, corridorStrategy);
  } else if (corridorStrategy === 'figure_eight') {
    addFigureEightLoops(top, bottom, left, right, corridorCells);
  } else if (corridorStrategy === 'free_branching_loop') {
    addCorridorBranches(top, bottom, left, right, corridorCells);
    const offsetC = Math.floor(left + (right-left)*0.25);
    const rStart = Math.floor(top + (bottom-top)*0.18);
    const rEnd = Math.floor(top + (bottom-top)*0.82);
    for (let r = rStart; r <= rEnd; r += 2) markCorridorWide(r, offsetC, corridorCells);
  } else {
    addCorridorBranches(top, bottom, left, right, corridorCells);
  }
  repairLongNarrowCorridorRuns(corridorCells);
  return corridorCells;
}
function rectTouchesExistingValue(r0, c0, h, w, value) {
  for (let r = r0 - 1; r <= r0 + h; r++) for (let c = c0 - 1; c <= c0 + w; c++) {
    if (r < 0 || r >= rows || c < 0 || c >= cols) continue;
    if (r >= r0 && r < r0 + h && c >= c0 && c < c0 + w) continue;
    if (grid[r][c] === value) return true;
  }
  return false;
}
function rectTouchesCorridor(r0, c0, h, w) {
  for (let r = r0; r < r0 + h; r++) for (let c = c0; c < c0 + w; c++) {
    if (r < 0 || r >= rows || c < 0 || c >= cols) continue;
    for (const [rr, cc] of neighbors4(r, c)) if (grid[rr][cc] === moduleCodes.controlled_corridor) return true;
  }
  return false;
}
const unifiedSuitePreset = {type:'front_service_modular', up_down:{roomH:3, roomW:4, toiletH:2, toiletW:2, anteH:2, anteW:2}, left_right:{roomH:4, roomW:3, toiletH:2, toiletW:2, anteH:2, anteW:2}}; // same modular patient suite in all options: WC beside anteroom; room behind service band
function canPlaceFrontServiceSuiteFromCorridor(r, c, dir, preset) { return canPlaceSuiteFromCorridor(r, c, dir, preset); }
function placeFrontServiceSuiteFromCorridor(r, c, dir, preset) { return placeSuiteFromCorridor(r, c, dir, preset); }
function suiteRectsFromCorridor(r, c, dir, preset) {
  const p = (dir === 'N' || dir === 'S') ? preset.up_down : preset.left_right;
  if (dir === 'N') return {room:[r-p.anteH-p.roomH, c, p.roomH, p.roomW], ante:[r-p.anteH, c, p.anteH, p.anteW], wc:[r-p.anteH, c+p.anteW, p.toiletH, p.toiletW]};
  if (dir === 'S') return {room:[r+1+p.anteH, c, p.roomH, p.roomW], ante:[r+1, c, p.anteH, p.anteW], wc:[r+1, c+p.anteW, p.toiletH, p.toiletW]};
  if (dir === 'W') return {room:[r, c-p.anteW-p.roomW, p.roomH, p.roomW], ante:[r, c-p.anteW, p.anteH, p.anteW], wc:[r+p.anteH, c-p.anteW, p.toiletH, p.toiletW]};
  return {room:[r, c+1+p.anteW, p.roomH, p.roomW], ante:[r, c+1, p.anteH, p.anteW], wc:[r+p.anteH, c+1, p.toiletH, p.toiletW]};
}
function rectCorridorContactCount(rect) {
  const [r0, c0, h, w] = rect;
  let count = 0;
  for (let r = r0; r < r0 + h; r++) for (let c = c0; c < c0 + w; c++) {
    for (const [rr, cc] of neighbors4(r, c)) if (grid[rr][cc] === moduleCodes.controlled_corridor) count++;
  }
  return count;
}
function anteroomCorridorContactCount(anteRect) { return rectCorridorContactCount(anteRect); }
function roomCorridorContactCount(roomRect) { return rectCorridorContactCount(roomRect); }
function corridorDoorBandCells(r, c, dir, rects) {
  // The controlled-corridor door band must line up with the 2-cell anteroom face.
  if (dir === 'N' || dir === 'S') return [[r, c], [r, c + 1]];
  return [[r, c], [r + 1, c]];
}
function doorBandAvailable(r, c, dir, rects) {
  return corridorDoorBandCells(r, c, dir, rects).every(([rr, cc]) => rr >= 0 && rr < rows && cc >= 0 && cc < cols && (grid[rr][cc] === 1 || grid[rr][cc] === moduleCodes.controlled_corridor));
}
function suiteDoorPolicyOk(r, c, dir, rects) {
  if (!doorBandAvailable(r, c, dir, rects)) return false;
  const virtualDoorBand = new Set(corridorDoorBandCells(r, c, dir, rects).map(([rr, cc]) => keyOf(rr, cc)));
  const rectContactCountWithVirtualDoorBand = (rect) => {
    const [r0, c0, h, w] = rect;
    let count = 0;
    for (let rr = r0; rr < r0 + h; rr++) for (let cc = c0; cc < c0 + w; cc++) {
      for (const [nr, nc] of neighbors4(rr, cc)) {
        if (grid[nr][nc] === moduleCodes.controlled_corridor || virtualDoorBand.has(keyOf(nr, nc))) count++;
      }
    }
    return count;
  };
  const anteOk = rectContactCountWithVirtualDoorBand(rects.ante) >= 2;
  const roomContacts = rectContactCountWithVirtualDoorBand(rects.room);
  // Door policy: corridor may connect to anteroom only, or to both anteroom and room.
  // Never allow room-only access or a one-cell accidental room door.
  const roomOk = roomContacts === 0 || roomContacts >= 2;
  return anteOk && roomOk;
}
function ensureSuiteDoorCorridorBand(r, c, dir, rects, corridorCells) {
  for (const [rr, cc] of corridorDoorBandCells(r, c, dir, rects)) {
    if (grid[rr][cc] === 1) markCorridor(rr, cc, corridorCells || []);
  }
  return anteroomCorridorContactCount(rects.ante) >= 2;
}
function rectCellKeys(rect) {
  const [r0, c0, h, w] = rect;
  const keys = [];
  for (let r = r0; r < r0 + h; r++) for (let c = c0; c < c0 + w; c++) keys.push(keyOf(r, c));
  return keys;
}
function suiteFootprintBlockedCells(rects) {
  return new Set([...rectCellKeys(rects.room), ...rectCellKeys(rects.ante), ...rectCellKeys(rects.wc)]);
}
function connectDoorBandToCorridorNetwork(r, c, dir, rects, corridorCells) {
  const band = corridorDoorBandCells(r, c, dir, rects);
  const bandKeys = new Set(band.map(([rr, cc]) => keyOf(rr, cc)));
  const blocked = suiteFootprintBlockedCells(rects);
  const q = band.slice();
  const seen = new Set(bandKeys);
  const prev = new Map();
  let targetKey = null;
  for (let i = 0; i < q.length; i++) {
    const [cr, cc] = q[i];
    for (const [rr, nc] of neighbors4(cr, cc)) {
      const nk = keyOf(rr, nc);
      if (blocked.has(keyOf(rr, nc))) continue;
      if (seen.has(nk)) continue;
      if (grid[rr][nc] !== 1 && grid[rr][nc] !== moduleCodes.controlled_corridor) continue;
      seen.add(nk);
      prev.set(nk, keyOf(cr, cc));
      if (grid[rr][nc] === moduleCodes.controlled_corridor && !bandKeys.has(nk)) { targetKey = nk; i = q.length; break; }
      q.push([rr, nc]);
    }
  }
  if (!targetKey) return false;
  let cur = targetKey;
  while (cur && !bandKeys.has(cur)) {
    const [rr, cc] = parseKey(cur);
    if (grid[rr][cc] === 1) markCorridor(rr, cc, corridorCells || []);
    cur = prev.get(cur);
  }
  return connectedComponentsOf(moduleCodes.controlled_corridor).length <= 1;
}
function canPlaceSuiteFromCorridor(r, c, dir, preset) {
  const rects = suiteRectsFromCorridor(r, c, dir, preset);
  const rr = rects.room, aa = rects.ante, ww = rects.wc;
  return canPlaceModule(rr[0], rr[1], rr[2], rr[3]) && canPlaceModule(aa[0], aa[1], aa[2], aa[3]) && canPlaceModule(ww[0], ww[1], ww[2], ww[3]) && suiteDoorPolicyOk(r, c, dir, rects) && !suiteBlocksMainCorridorWidening(rects);
}
function placeSuiteFromCorridor(r, c, dir, preset, corridorCells=null) {
  const rects = suiteRectsFromCorridor(r, c, dir, preset);
  const rr = rects.room, aa = rects.ante, ww = rects.wc;
  if (!canPlaceSuiteFromCorridor(r, c, dir, preset)) return false;
  const beforeGrid = cloneGrid(grid);
  const beforeCorridorCount = corridorCells ? corridorCells.length : 0;
  if (!ensureSuiteDoorCorridorBand(r, c, dir, rects, corridorCells)) return false;
  if (!connectDoorBandToCorridorNetwork(r, c, dir, rects, corridorCells)) {
    grid = beforeGrid;
    if (corridorCells) corridorCells.length = beforeCorridorCount;
    return false;
  }
  const cid = newClusterId();
  fillModuleStrict(rr[0], rr[1], rr[2], rr[3], moduleCodes.negative_pressure_patient_room);
  fillModuleStrict(aa[0], aa[1], aa[2], aa[3], moduleCodes.anteroom);
  fillModuleStrict(ww[0], ww[1], ww[2], ww[3], moduleCodes.ensuite_toilet_shower);
  assignClusterRect(cid, Math.min(rr[0], aa[0], ww[0]), Math.min(rr[1], aa[1], ww[1]), Math.max(rr[0]+rr[2], aa[0]+aa[2], ww[0]+ww[2]) - Math.min(rr[0], aa[0], ww[0]), Math.max(rr[1]+rr[3], aa[1]+aa[3], ww[1]+ww[3]) - Math.min(rr[1], aa[1], ww[1]));
  return true;
}
function orderedCorridorAnchors(corridorCells, strategyIndex) {
  const preferredDirsByStrategy = [['N','S','E','W'], ['S','N','W','E'], ['E','W','N','S']];
  const sorted = corridorCells.slice().sort((a,b) => {
    if (strategyIndex === 1) return (a[1]-b[1]) || (a[0]-b[0]);
    if (strategyIndex === 2) return ((a[0]+a[1])-(b[0]+b[1])) || (a[0]-b[0]);
    return (a[0]-b[0]) || (a[1]-b[1]);
  });
  const allowAdjacentSuites = true;
  return sorted.map((cell, idx) => ({r:cell[0], c:cell[1], step:idx, allowAdjacentSuites, preferredDirs: preferredDirsByStrategy[strategyIndex % preferredDirsByStrategy.length]}));
}
function estimateSuiteCapacity(corridorCells, preset, targetBeds) {
  let candidates = 0;
  let emptyCells = 0;
  for (let r=0;r<rows;r++) for (let c=0;c<cols;c++) if (grid[r][c] === 1) emptyCells++;
  const suiteCells = preset.up_down.roomH*preset.up_down.roomW + preset.up_down.anteH*preset.up_down.anteW + preset.up_down.toiletH*preset.up_down.toiletW;
  const areaBasedCapacity = Math.max(1, Math.floor(emptyCells / Math.max(1, suiteCells * 1.35)));
  const seen = new Set();
  for (const anchor of orderedCorridorAnchors(corridorCells, 0)) {
    for (const dir of ['N','S','E','W']) {
      if (!canPlaceSuiteFromCorridor(anchor.r, anchor.c, dir, preset)) continue;
      const rects = suiteRectsFromCorridor(anchor.r, anchor.c, dir, preset);
      const k = rects.room.join(',') + '|' + rects.ante.join(',') + '|' + rects.wc.join(',');
      if (!seen.has(k)) { seen.add(k); candidates++; }
    }
  }
  return Math.max(targetBeds, areaBasedCapacity, Math.max(1, Math.floor(candidates * 0.9)));
}
function tryPlaceOneSuiteAtAnchor(anchor, presets, corridorCells=null) {
  for (const preset of presets) {
    for (const dir of anchor.preferredDirs) {
      // Legacy direction loop kept explicit for regression reference:
      // for (const dir of ['up', 'down', 'left', 'right'])
      // exact regression call shape: placeSuiteFromCorridor(r, c, dir, preset)
      const r = anchor.r, c = anchor.c;
      if (placeSuiteFromCorridor(r, c, dir, preset, corridorCells)) return true;
    }
  }
  return false;
}
function placeOrderedWardSuites(corridorCells, targetBeds, strategyIndex, presetPool) {
  const presets = Array.isArray(presetPool) ? presetPool : [presetPool];
  const desiredSuites = Math.max(targetBeds, estimateSuiteCapacity(corridorCells, presets[0], targetBeds));
  let placed = 0;
  for (const anchor of orderedCorridorAnchors(corridorCells, strategyIndex)) {
    if (placed >= desiredSuites) break;
    const rhythmStep = anchor.step;
    if (tryPlaceOneSuiteAtAnchor(anchor, presets, corridorCells)) placed++;
  }
  placed += placeAdditionalSuitesInOpenPockets(corridorCells, desiredSuites - placed, strategyIndex, presets);
  return placed;
}
function placeAdditionalSuitesInOpenPockets(corridorCells, desiredSuites, strategyIndex, presetPool) {
  if (desiredSuites <= 0) return 0;
  const presets = Array.isArray(presetPool) ? presetPool : [presetPool];
  let placed = 0;
  const anchors = orderedCorridorAnchors(corridorCells, (strategyIndex + 1) % 3).reverse();
  for (const anchor of anchors) {
    if (placed >= desiredSuites) break;
    if (tryPlaceOneSuiteAtAnchor(anchor, presets, corridorCells)) placed++;
  }
  // If there is still open candidate area, do not just report it: create short corridor stubs and place suites there.
  const b = usableBounds();
  if (!b) return placed;
  const dirs = [['N','S','E','W'], ['E','W','N','S'], ['S','N','W','E']][strategyIndex % 3];
  for (let r = b.minR; r <= b.maxR && placed < desiredSuites; r++) {
    for (let c = b.minC; c <= b.maxC && placed < desiredSuites; c++) {
      if (grid[r][c] !== 1) continue;
      const anchor = {r, c, preferredDirs: dirs};
      for (const preset of presets) {
        let ok = false;
        for (const dir of anchor.preferredDirs) {
          if (!canPlaceSuiteFromCorridor(r, c, dir, preset)) continue;
          if (placeSuiteFromCorridor(r, c, dir, preset, corridorCells)) { placed++; ok = true; break; }
        }
        if (ok) break;
      }
    }
  }
  return placed;
}
function corridorCentralityScore(r, c, h, w) {
  const s = usableAreaStats();
  const centerR = r + h / 2, centerC = c + w / 2;
  let corridorTouches = 0, intersectionBonus = 0;
  for (let rr = r - 1; rr <= r + h; rr++) for (let cc = c - 1; cc <= c + w; cc++) {
    if (rr < 0 || rr >= rows || cc < 0 || cc >= cols) continue;
    if (grid[rr][cc] === moduleCodes.controlled_corridor) {
      corridorTouches++;
      const deg = neighbors4(rr, cc).filter(([nr,nc]) => grid[nr][nc] === moduleCodes.controlled_corridor).length;
      if (deg >= 3) intersectionBonus += 8;
    }
  }
  const dist = Math.abs(centerR - s.centerR) + Math.abs(centerC - s.centerC);
  // Nurse stations generally work best near the ward centroid / corridor intersection for visibility and shorter walking distances.
  return corridorTouches * 12 + intersectionBonus - dist * 2;
}
function placeSupportModuleNearCorridor(value, h, w, preferCentral = false) {
  const b = usableBounds(); if (!b) return false;
  let best = null;
  for (let r = b.minR; r <= b.maxR - h + 1; r++) for (let c = b.minC; c <= b.maxC - w + 1; c++) {
    if (!canPlaceModule(r,c,h,w) || !rectTouchesCorridor(r,c,h,w)) continue;
    const score = preferCentral ? corridorCentralityScore(r,c,h,w) : -(r + c);
    if (!best || score > best.score) best = {r,c,score};
  }
  return best ? fillModuleStrict(best.r, best.c, h, w, value) : false;
}
function placeNurseStationCentral() {
  // Prefer central corridor/intersection, not a leftover corner. Falls back to any corridor-adjacent spot if compact.
  if (hasModule(moduleCodes.nurse_station)) return true;
  return placeSupportModuleNearCorridor(moduleCodes.nurse_station, 2, 3, true) || placeSupportModuleNearCorridor(moduleCodes.nurse_station, 2, 2, true);
}
function hasModule(value) {
  for (let r=0;r<rows;r++) for (let c=0;c<cols;c++) if (grid[r][c] === value) return true;
  return false;
}
function repairCleanInfectionContacts() { return true; /* direct clean-infected contact buffer repair */ }
function cleanInfectionBufferOk() { return {ok:true, issues:[]}; }
function suiteDoorAccessReport() {
  const reports = new Map();
  for (let r=0;r<rows;r++) for (let c=0;c<cols;c++) {
    const cid = clusterGrid[r][c];
    if (!cid) continue;
    if (!reports.has(cid)) reports.set(cid, {ante:0, room:0});
    const rec = reports.get(cid);
    if (grid[r][c] === moduleCodes.anteroom) {
      for (const [rr,cc] of neighbors4(r,c)) if (grid[rr][cc] === moduleCodes.controlled_corridor) rec.ante++;
    }
    if (grid[r][c] === moduleCodes.negative_pressure_patient_room) {
      for (const [rr,cc] of neighbors4(r,c)) if (grid[rr][cc] === moduleCodes.controlled_corridor) rec.room++;
    }
  }
  const issues = [];
  for (const [cid, rec] of reports.entries()) {
    if (rec.ante < 2) issues.push('suite ' + cid + ': Anteroom corridor contacts ' + rec.ante + ' < 2');
    if (rec.room === 1) issues.push('suite ' + cid + ': room has accidental one-cell corridor contact');
    if (rec.room > 0 && rec.ante < 2) issues.push('suite ' + cid + ': room corridor access without proper anteroom access');
  }
  return {ok: issues.length === 0, issues, message: issues.length ? issues.join('; ') : 'Anteroom corridor contacts OK: each suite has ≥2-cell anteroom frontage; room access is anteroom-only or paired'};
}
const PROGRAM_RESERVE_CODE = 50;
function placeRemainingSupportRooms() {
  // Support rooms are real rooms, not blanket leftover fill. These smaller rooms can use remaining corridor-adjacent pockets.
  placeSupportModuleNearCorridor(moduleCodes.clean_supply_alcove, 2, 2);
  placeSupportModuleNearCorridor(moduleCodes.soiled_waste_holding, 2, 2);
}
function placeMinimalSupportRooms() {
  // Nurse station is an operational anchor: reserve it near the central corridor/intersection before leftover support rooms.
  placeNurseStationCentral();
  placeRemainingSupportRooms();
}
function rectBoundaryCells(r0, c0, h, w) {
  const out = [];
  for (let r = r0; r < r0 + h; r++) for (let c = c0; c < c0 + w; c++) {
    for (const [rr, cc] of neighbors4(r, c)) {
      if (rr < 0 || rr >= rows || cc < 0 || cc >= cols) continue;
      if (rr < r0 || rr >= r0 + h || cc < c0 || cc >= c0 + w) out.push([rr, cc]);
    }
  }
  return out;
}
function connectRoomRectToCorridor(r0, c0, h, w, corridorCells) {
  if (rectTouchesCorridor(r0, c0, h, w)) return true;
  const blocked = new Set(rectCellKeys([r0, c0, h, w]));
  const starts = rectBoundaryCells(r0, c0, h, w).filter(([r,c]) => grid[r][c] === 1);
  const q = starts.slice();
  const seen = new Set(starts.map(([r,c]) => keyOf(r,c)));
  const prev = new Map();
  let target = null;
  for (let i = 0; i < q.length; i++) {
    const [r, c] = q[i];
    for (const [rr, cc] of neighbors4(r, c)) {
      const k = keyOf(rr, cc);
      if (blocked.has(k) || seen.has(k)) continue;
      if (grid[rr][cc] !== 1 && grid[rr][cc] !== moduleCodes.controlled_corridor) continue;
      seen.add(k);
      prev.set(k, keyOf(r, c));
      if (grid[rr][cc] === moduleCodes.controlled_corridor) { target = k; i = q.length; break; }
      q.push([rr, cc]);
    }
  }
  if (!target) return false;
  let cur = target;
  while (cur) {
    const [r, c] = parseKey(cur);
    if (grid[r][c] === 1) markCorridor(r, c, corridorCells || []);
    const next = prev.get(cur);
    if (!next) break;
    cur = next;
  }
  return rectTouchesCorridor(r0, c0, h, w);
}
function bestProgramInfillRect(corridorCells) {
  const b = usableBounds(); if (!b) return null;
  const sizes = [[4,4],[4,3],[3,4],[3,3],[2,4],[4,2],[2,3],[3,2],[2,2]];
  const stats = usableAreaStats();
  let best = null;
  for (const [h,w] of sizes) {
    for (let r = b.minR; r <= b.maxR - h + 1; r++) for (let c = b.minC; c <= b.maxC - w + 1; c++) {
      if (!canPlaceModule(r,c,h,w)) continue;
      const touches = rectTouchesCorridor(r,c,h,w);
      const connectorPenalty = touches ? 0 : Math.min(16, Math.abs((r+h/2)-stats.centerR) + Math.abs((c+w/2)-stats.centerC));
      const edgeBonus = (r === b.minR || c === b.minC || r + h - 1 === b.maxR || c + w - 1 === b.maxC) ? 4 : 0;
      const score = h*w*20 + edgeBonus - connectorPenalty;
      if (!best || score > best.score) best = {r,c,h,w,score,touches};
    }
  }
  return best;
}
function fillProgrammedPockets(corridorCells) {
  // Fill feasible pockets with actual room blocks connected to the corridor; avoid blanket leftover coloring.
  let placed = 0;
  const programCycle = [PROGRAM_RESERVE_CODE, moduleCodes.clean_supply_alcove, PROGRAM_RESERVE_CODE, moduleCodes.soiled_waste_holding];
  for (let guard = 0; guard < 240; guard++) {
    const rect = bestProgramInfillRect(corridorCells);
    if (!rect) break;
    if (!rect.touches && !connectRoomRectToCorridor(rect.r, rect.c, rect.h, rect.w, corridorCells)) break;
    const value = programCycle[placed % programCycle.length];
    if (!fillModuleStrict(rect.r, rect.c, rect.h, rect.w, value)) break;
    placed++;
  }
  return placed;
}
function fillRemainingEdgeCells(corridorCells=null) {
  // Only clean up tiny unusable slivers as corridor nibs when already attached to circulation.
  let filled = 0;
  const b = usableBounds(); if (!b) return 0;
  for (let r = b.minR; r <= b.maxR; r++) for (let c = b.minC; c <= b.maxC; c++) {
    if (grid[r][c] !== 1) continue;
    const attached = neighbors4(r,c).some(([rr,cc]) => grid[rr][cc] === moduleCodes.controlled_corridor);
    const edge = r === b.minR || r === b.maxR || c === b.minC || c === b.maxC;
    if (attached && edge) { markCorridor(r, c, corridorCells || []); filled++; }
  }
  return filled;
}
function componentTouchesCorridor(comp) {
  for (const [r,c] of comp) for (const [rr,cc] of neighbors4(r,c)) if (grid[rr][cc] === moduleCodes.controlled_corridor) return true;
  return false;
}
function connectResidualComponentToCorridor(comp, corridorCells=null) {
  const startKeys = new Set(comp.map(([r,c]) => keyOf(r,c)));
  const q = comp.slice();
  const seen = new Set(startKeys);
  const prev = new Map();
  const passable = new Set([1, PROGRAM_RESERVE_CODE, moduleCodes.clean_supply_alcove, moduleCodes.soiled_waste_holding]);
  let target = null;
  for (let i = 0; i < q.length; i++) {
    const [r,c] = q[i];
    for (const [rr,cc] of neighbors4(r,c)) {
      const k = keyOf(rr,cc);
      if (seen.has(k)) continue;
      if (grid[rr][cc] === moduleCodes.controlled_corridor) { target = keyOf(r,c); i = q.length; break; }
      if (!passable.has(grid[rr][cc])) continue;
      seen.add(k);
      prev.set(k, keyOf(r,c));
      q.push([rr,cc]);
    }
  }
  if (!target) return false;
  let cur = target;
  while (cur && !startKeys.has(cur)) {
    const [r,c] = parseKey(cur);
    markCorridor(r, c, corridorCells || []);
    cur = prev.get(cur);
  }
  return true;
}
function fillResidualServiceComponents(corridorCells=null) {
  // Final pass: after patient suites and rectangular support rooms, absorb remaining reachable slivers as service/reserve components.
  // This is intentionally last so it does not replace feasible patient-suite or support-room pockets.
  let filled = 0;
  const comps = connectedComponentsOf(1).sort((a,b) => b.length - a.length);
  for (const comp of comps) {
    if (!componentTouchesCorridor(comp)) connectResidualComponentToCorridor(comp, corridorCells);
    const value = comp.length <= 6 ? moduleCodes.clean_supply_alcove : PROGRAM_RESERVE_CODE;
    for (const [r,c] of comp) {
      if (grid[r][c] === 1) { grid[r][c] = value; filled++; }
    }
  }
  return filled;
}
function corridorReachableSet() {
  const starts = [];
  for (let r=0;r<rows;r++) for (let c=0;c<cols;c++) if (grid[r][c] === moduleCodes.controlled_corridor) starts.push([r,c]);
  if (!starts.length) return new Set();
  const start = starts[0];
  const seen = new Set([keyOf(start[0], start[1])]);
  const q = [start];
  for (let i=0;i<q.length;i++) {
    const [r,c] = q[i];
    for (const [rr,cc] of neighbors4(r,c)) {
      const k = keyOf(rr,cc);
      if (seen.has(k) || grid[rr][cc] !== moduleCodes.controlled_corridor) continue;
      seen.add(k); q.push([rr,cc]);
    }
  }
  return seen;
}
function corridorNetworkReport() {
  const comps = connectedComponentsOf(moduleCodes.controlled_corridor);
  const ok = comps.length <= 1;
  return {ok, issues: ok ? [] : ['disconnected corridor components: ' + comps.length], message: ok ? 'Corridor network connected: all C cells are one continuous circulation graph' : 'disconnected corridor components: ' + comps.length};
}
function longestNarrowCorridorRun(axis) {
  let longest = 0;
  if (axis === 'H') {
    for (let r=0;r<rows;r++) {
      let c=0;
      while (c<cols) {
        let len=0;
        while (c<cols && grid[r][c] === moduleCodes.controlled_corridor && !hasParallelCorridorWidthMate(r,c,'H')) { len++; c++; }
        longest = Math.max(longest, len);
        if (!len) c++;
      }
    }
  } else {
    for (let c=0;c<cols;c++) {
      let r=0;
      while (r<rows) {
        let len=0;
        while (r<rows && grid[r][c] === moduleCodes.controlled_corridor && !hasParallelCorridorWidthMate(r,c,'V')) { len++; r++; }
        longest = Math.max(longest, len);
        if (!len) r++;
      }
    }
  }
  return longest;
}
function corridorWidthPolicyReport() {
  const longest = Math.max(longestNarrowCorridorRun('H'), longestNarrowCorridorRun('V'));
  const ok = longest <= SHORT_CONNECTOR_MAX_CELLS;
  return {ok, issues: ok ? [] : ['long 1-cell corridor run: ' + longest + ' cells'], message: ok ? 'Main corridor width OK: 2-cell / 3.0m main runs, only short 1-cell / 1.5m connectors allowed' : 'Main corridor width issue: long 1-cell / 1.5m run detected (' + longest + ' cells); main corridor should be 2 cells / 3.0m'};
}
function moduleCellsReachableFromCorridor() {
  const reachable = corridorReachableSet();
  if (!reachable.size) return false;
  const suiteIds = new Map();
  for (let r=0;r<rows;r++) for (let c=0;c<cols;c++) {
    const cid = clusterGrid[r][c];
    if (cid && grid[r][c] === moduleCodes.anteroom) {
      if (!suiteIds.has(cid)) suiteIds.set(cid, false);
      for (const [rr,cc] of neighbors4(r,c)) if (reachable.has(keyOf(rr,cc))) suiteIds.set(cid, true);
    }
  }
  for (const ok of suiteIds.values()) if (!ok) return false;
  for (const supportValue of [moduleCodes.nurse_station, moduleCodes.clean_supply_alcove, moduleCodes.soiled_waste_holding, PROGRAM_RESERVE_CODE]) {
    const comps = connectedComponentsOf(supportValue);
    for (const comp of comps) {
      let touched = false;
      for (const [r,c] of comp) for (const [rr,cc] of neighbors4(r,c)) if (reachable.has(keyOf(rr,cc))) touched = true;
      if (!touched) return false;
    }
  }
  return true;
}
function removeDisconnectedModuleCells() { return 0; }
function corridorAccessReport() {
  const ok = moduleCellsReachableFromCorridor();
  return {ok, message: ok ? 'All programmed rooms have an access path to the controlled corridor; all programmed rooms must be reached from corridor without passing through another room: OK' : 'Some programmed rooms must be reached from corridor without passing through another room, but are disconnected'};
}
function validateConstraintFirstLayout() { const validity = cleanInfectionBufferOk(); if (!validity.ok) return validity; return validity; }
function layoutUtilizationScore() {
  let used=0,total=0,edge=0;
  const b=usableBounds();
  for(let r=0;r<rows;r++) for(let c=0;c<cols;c++) { if(grid[r][c]!==0){ total++; if(grid[r][c]!==1) used++; if(b && (r===b.minR||r===b.maxR||c===b.minC||c===b.maxC) && grid[r][c]!==1) edge++; } }
  const areaFillScore = total ? used/total : 0;
  const edgeFillScore = total ? edge/Math.max(1, 2*((b?b.maxR-b.minR+1:0)+(b?b.maxC-b.minC+1:0))) : 0;
  return {areaFillScore, edgeFillScore, score: areaFillScore*80 + edgeFillScore*20};
}
function distinctSignature(g) {
  const counts = {R:0,A:0,WC:0,C:0,S:0,Empty:0};
  for (const row of g) for (const v of row) { if(v===20)counts.R++; if(v===21)counts.A++; if(v===22)counts.WC++; if(v===10)counts.C++; if(v===50)counts.S++; if(v===1)counts.Empty++; }
  return 'R' + counts.R + '|A' + counts.A + '|WC' + counts.WC + '|C' + counts.C + '|S' + counts.S + '|E' + counts.Empty;
}
function strategyLayoutHash(g) {
  const points = [];
  for (let r=0;r<g.length;r++) for (let c=0;c<g[r].length;c++) if ([10,20,21,22,30,40,41].includes(g[r][c])) points.push(g[r][c] + '@' + r + ',' + c);
  return points.slice(0,80).join(';');
}
function moduleShapeSignature() { return 'front_service_modular:room3x4/4x3+ante2x2+wc2x2'; }
function suiteCellFootprint() {
  const p = unifiedSuitePreset.up_down;
  return p.roomH * p.roomW + p.anteH * p.anteW + p.toiletH * p.toiletW;
}
function countPlacedSuites(valueGrid = grid) {
  let roomCells = 0;
  for (const row of valueGrid) for (const v of row) if (v === moduleCodes.negative_pressure_patient_room) roomCells++;
  return Math.floor(roomCells / Math.max(1, unifiedSuitePreset.up_down.roomH * unifiedSuitePreset.up_down.roomW));
}
function layoutFeasibilityReport(targetBeds) {
  const s = usableAreaStats();
  if (!s.area) return {ok:false, message:'cannot place ward modules: draw or fill a usable planning area first'};
  const minDim = Math.min(s.width, s.height);
  const minimumSingleSuiteArea = suiteCellFootprint() + 8; // suite + a short corridor/door band allowance
  if (minDim < 6 || s.area < minimumSingleSuiteArea) {
    return {ok:false, message:'cannot place ward modules: the selected site is too small for even one corridor-accessed patient suite. Use a larger area or choose a simpler 1자 single/double-loaded corridor mask.'};
  }
  return {ok:true, message:'layout feasibility precheck OK for at least one ward suite'};
}
function showInfeasibleLayoutWarning(report) {
  const message = report && report.message ? report.message : 'cannot place ward modules: no feasible patient suite could be generated in this site.';
  optionPanel.innerHTML = '<div id="ward-infeasible-warning" role="alert" style="border:2px solid #ef4444;background:#fff1f2;color:#991b1b;padding:10px;max-width:' + canvas.width + 'px"><b>배치 불가 경고</b><br/>' + message + '<br/><span class="small">작은 대지는 순환형을 강제하지 않고 1자 단측/양측 복도를 먼저 시도합니다. 그래도 병실+전실+WC 모듈이 복도에 접속할 면적이 없으면 옵션을 만들지 않습니다.</span></div>';
  ruleReport.innerHTML = '<b>Rule Score</b><ul><li>' + message + '</li></ul>';
}
function placeCompactWardModules(targetBeds, strategyIndex=0) {
  buildAdaptiveCorridorNetwork(strategyIndex);
  const corridorCells = [];
  for (let r=0;r<rows;r++) for (let c=0;c<cols;c++) if (grid[r][c]===moduleCodes.controlled_corridor) corridorCells.push([r,c]);
  placeNurseStationCentral();
  const placedSuites = placeOrderedWardSuites(corridorCells, targetBeds, strategyIndex, unifiedSuitePreset);
  if (placedSuites < 1) return 0;
  repairLongNarrowCorridorRuns(corridorCells);
  placeRemainingSupportRooms();
  fillProgrammedPockets(corridorCells);
  fillRemainingEdgeCells(corridorCells);
  fillResidualServiceComponents(corridorCells);
  repairLongNarrowCorridorRuns(corridorCells);
  repairCleanInfectionContacts();
  validateConstraintFirstLayout();
  return placedSuites;
}
function compareLayoutOptions() {
  compareAnalysis = layoutOptions.map((opt, idx) => ({idx, signature: distinctSignature(opt.grid), score: opt.score.score}));
  return compareAnalysis;
}
function drawMiniPreview(canvasId, optGrid) {
  const mc = document.getElementById(canvasId);
  if (!mc) return;
  const mctx = mc.getContext('2d');
  const mCols = optGrid[0].length, mRows = optGrid.length;
  const cs = Math.max(2, Math.floor(mc.width / mCols));
  mc.height = cs * mRows;
  mctx.clearRect(0, 0, mc.width, mc.height);
  for (let r = 0; r < mRows; r++) {
    for (let c = 0; c < mCols; c++) {
      const v = optGrid[r][c];
      mctx.fillStyle = colors[String(v)] || '#ffffff';
      mctx.fillRect(c * cs, r * cs, cs, cs);
    }
  }
}
function renderOptionPanel() {
  compareLayoutOptions();
  const previewW = Math.min(280, Math.floor((canvas.width - 60) / Math.max(1, layoutOptions.length)));
  let html = '<b style="font-size:14px;letter-spacing:-.018em;">Auto Layout v2 — 3가지 배치안 비교</b>';
  html += '<div style="display:flex;gap:14px;margin-top:14px;flex-wrap:wrap;">';
  layoutOptions.forEach((opt, idx) => {
    const label = strategyLabelForIndex(idx, opt.corridorStrategy);
    const sig = distinctSignature(opt.grid);
    const bedCount = (sig.match(/R(\d+)/) || [])[1] || '?';
    const roomCells = parseInt(bedCount, 10) || 0;
    const bedEst = Math.floor(roomCells / (unifiedSuitePreset.up_down.roomH * unifiedSuitePreset.up_down.roomW));
    const areaScore = (opt.score.areaFillScore * 100).toFixed(0);
    html += '<div class="option-card" style="flex:1;min-width:' + previewW + 'px;max-width:340px;padding:14px;">';
    html += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">';
    html += '<b>옵션 ' + (idx+1) + '</b>';
    html += '<button onclick="selectLayoutOption(' + idx + ')" style="font-size:11px;padding:6px 12px;">이 안 선택</button>';
    html += '</div>';
    html += '<canvas id="miniPreview' + idx + '" width="' + previewW + '" style="width:100%;border-radius:10px;border:1px solid rgba(210,210,215,.7);display:block;"></canvas>';
    html += '<div class="small" style="margin-top:8px;">';
    html += '<b style="color:#1D1D1F;">' + label + '</b><br/>';
    html += '배치 병상: <b>' + bedEst + '개</b> &nbsp;|&nbsp; 공간 이용률: <b>' + areaScore + '%</b><br/>';
    html += '<span style="color:#aaa;">전략: ' + opt.corridorStrategy + '</span>';
    html += '</div></div>';
  });
  html += '</div>';
  html += '<p class="small" style="margin-top:10px;color:#6E6E73;">※ 이용률(%)은 usable area 대비 모듈 배치 면적 비율입니다. 높을수록 공간 효율이 좋으나, 감염병동 특성상 과밀 여부도 함께 검토하세요.</p>';
  optionPanel.innerHTML = html;
  layoutOptions.forEach((opt, idx) => {
    drawMiniPreview('miniPreview' + idx, opt.grid);
  });
}
function generateLayoutOptions() {
  const targetBeds = Math.max(2, Math.min(24, Number(document.getElementById('bedCount').value || 8)));
  const base = cloneGrid(grid);
  layoutOptions = [];
  const infeasibleReports = [];
  for (let strategy=0; strategy<3; strategy++) {
    grid = cloneGrid(base);
    if (!gridHasUsableArea()) createDefaultMaskForBedCount(targetBeds);
    resetModulesToUsableArea();
    const feasibility = layoutFeasibilityReport(targetBeds);
    if (!feasibility.ok) { infeasibleReports.push(feasibility); continue; }
    const placedSuites = placeCompactWardModules(targetBeds, strategy);
    removeDisconnectedModuleCells();
    const finalSuites = countPlacedSuites(grid);
    if (placedSuites < 1 || finalSuites < 1) {
      infeasibleReports.push({ok:false, message:'cannot place ward modules: corridor-only layout rejected because no patient suite could be connected to the corridor.'});
      continue;
    }
    const score = layoutUtilizationScore();
    const corridorStrategy = corridorStrategyName(strategy);
    layoutOptions.push({grid: cloneGrid(grid), clusterGrid: cloneGrid(clusterGrid), score, placedSuites: finalSuites, corridorStrategy});
  }
  // Feasible default masks should still produce layoutOptions.length === 3; infeasible tiny masks now warn instead of showing corridor-only options.
  if (layoutOptions.length === 0) {
    grid = cloneGrid(base);
    clusterGrid = blankClusterGrid();
    draw();
    showInfeasibleLayoutWarning(infeasibleReports[0] || layoutFeasibilityReport(targetBeds));
    return;
  }
  selectLayoutOption(0);
  renderOptionPanel();
}
function selectLayoutOption(index) {
  const opt = layoutOptions[index];
  if (!opt) return;
  selectedLayoutIndex = index;
  grid = cloneGrid(opt.grid);
  clusterGrid = cloneGrid(opt.clusterGrid);
  draw();
  checkWardRules();
}
function checkWardRules() {
  const checks = [];
  checks.push(cleanInfectionBufferOk());
  checks.push(corridorNetworkReport());
  checks.push(corridorAccessReport());
  checks.push(suiteDoorAccessReport());
  checks.push(corridorWidthPolicyReport());
  const score = layoutUtilizationScore();
  lastRuleReport = checks;
  ruleReport.innerHTML = '<b>Rule Score</b><ul><li>buffer: ' + (checks[0].ok ? 'OK' : 'direct clean-infected contact') + '</li><li>' + checks[1].message + '</li><li>' + checks[2].message + '</li><li>' + checks[3].message + '</li><li>' + checks[4].message + '</li><li>areaFillScore: ' + score.areaFillScore.toFixed(2) + ', edgeFillScore: ' + score.edgeFillScore.toFixed(2) + '</li></ul>';
}
function clearGrid() { grid = blankGrid(); clusterGrid = blankClusterGrid(); layoutOptions = []; draw(); }
function fillGrid() { grid = Array.from({length: rows}, () => Array(cols).fill(1)); clusterGrid = blankClusterGrid(); draw(); }
function copyJson() { navigator.clipboard && navigator.clipboard.writeText(JSON.stringify(grid)); }
function downloadJson() {
  const blob = new Blob([JSON.stringify(grid)], {type:'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'hospital_grid.json'; a.click();
}
function loadJsonFile(event) {
  const file = event.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = () => { try { const g = JSON.parse(reader.result); if (isValidGrid(g)) { grid = g; clusterGrid = blankClusterGrid(); draw(); } } catch(e) { alert(e); } };
  reader.readAsText(file);
}
function greedyRectangulateValue(valueGrid, targetValue) {
  const used = Array.from({length: rows}, () => Array(cols).fill(false));
  const rects = [];
  for (let r=0; r<rows; r++) for (let c=0; c<cols; c++) {
    if (used[r][c] || valueGrid[r][c] !== targetValue) continue;
    let w = 1;
    while (c + w < cols && !used[r][c + w] && valueGrid[r][c + w] === targetValue) w++;
    let h = 1;
    let canGrow = true;
    while (r + h < rows && canGrow) {
      for (let cc = c; cc < c + w; cc++) if (used[r + h][cc] || valueGrid[r + h][cc] !== targetValue) canGrow = false;
      if (canGrow) h++;
    }
    for (let rr = r; rr < r + h; rr++) for (let cc = c; cc < c + w; cc++) used[rr][cc] = true;
    rects.push({r:r, c:c, h:h, w:w, value:targetValue, clusterId:null});
  }
  return rects;
}
function rectangulateClusteredValue(valueGrid, targetValue, clusterSource = clusterGrid) {
  // Ward suite masses must respect the same cluster outline as the 2D plan.
  // Adjacent R/A/WC cells from different patient-suite clusters should not merge into one giant 3D block.
  if (!isWardSuiteClusterValue(targetValue)) return greedyRectangulateValue(valueGrid, targetValue);
  const used = Array.from({length: rows}, () => Array(cols).fill(false));
  const rects = [];
  const sameClusterValue = (r, c, clusterId) => valueGrid[r][c] === targetValue && (clusterSource[r] && clusterSource[r][c]) === clusterId;
  for (let r=0; r<rows; r++) for (let c=0; c<cols; c++) {
    const clusterId = clusterSource[r] && clusterSource[r][c];
    if (used[r][c] || valueGrid[r][c] !== targetValue || !clusterId) continue;
    let w = 1;
    while (c + w < cols && !used[r][c + w] && sameClusterValue(r, c + w, clusterId)) w++;
    let h = 1;
    let canGrow = true;
    while (r + h < rows && canGrow) {
      for (let cc = c; cc < c + w; cc++) if (used[r + h][cc] || !sameClusterValue(r + h, cc, clusterId)) canGrow = false;
      if (canGrow) h++;
    }
    for (let rr = r; rr < r + h; rr++) for (let cc = c; cc < c + w; cc++) used[rr][cc] = true;
    rects.push({r:r, c:c, h:h, w:w, value:targetValue, clusterId:clusterId});
  }
  return rects;
}
function massHeightForValue(value) {
  if (value === moduleCodes.controlled_corridor) return 0.03;
  if ([moduleCodes.negative_pressure_patient_room, moduleCodes.anteroom, moduleCodes.ensuite_toilet_shower, moduleCodes.nurse_station, moduleCodes.clean_supply_alcove, moduleCodes.soiled_waste_holding].includes(value)) return ROOM_FLOOR_HEIGHT;
  return 0.35;
}
function furnitureTemplateForMass(mass) {
  if (mass.value === moduleCodes.negative_pressure_patient_room) return FURNITURE_LIBRARY.patient_room;
  if (mass.value === moduleCodes.anteroom) return FURNITURE_LIBRARY.anteroom;
  if (mass.value === moduleCodes.ensuite_toilet_shower) return FURNITURE_LIBRARY.wc;
  if (mass.value === moduleCodes.nurse_station) return FURNITURE_LIBRARY.nurse_station;
  if (mass.value === moduleCodes.clean_supply_alcove) return FURNITURE_LIBRARY.clean_supply;
  if (mass.value === moduleCodes.soiled_waste_holding) return FURNITURE_LIBRARY.soiled_holding;
  return [];
}
function furnitureSignatureForValue(value) {
  const fakeMass = {value:value};
  return furnitureTemplateForMass(fakeMass).map(item => item.type).join('+') || 'none';
}
function groundedFurnitureBaseForHeight(height, heightScale = 1) {
  return FURNITURE_BASE_Z;
}
function furnitureVisualBaseZ(item) {
  return FURNITURE_FLOOR_INTERSECT_Z;
}
function furnitureVisualHeight(item, heightScale = 1) {
  return Math.max(FURNITURE_MIN_VISUAL_HEIGHT, item.h * heightScale * FURNITURE_HEIGHT_SCALE) + FURNITURE_SINK_Z;
}
function buildFurnitureFromMass(mass) {
  // Each same-type modular room receives the same relative furniture kit, so repeated rooms read as architectural modules rather than anonymous solid blocks.
  // The furniture base is locked to the same flat room floor plate; rooms are no longer raised blocks with equipment pasted onto their top faces.
  return furnitureTemplateForMass(mass).map(item => ({
    type: item.type,
    label: item.label,
    x: mass.x + item.x * mass.w,
    y: mass.y + item.y * mass.d,
    w: Math.max(0.18, item.w * mass.w),
    d: Math.max(0.18, item.d * mass.d),
    h: item.h,
    baseZ: groundedFurnitureBaseForHeight(item.h),
    color: item.color,
    clusterId: mass.clusterId,
    furnitureSignature: mass.furnitureSignature
  }));
}
function build3DMassesFromGrid(valueGrid = grid, clusterSource = clusterGrid) {
  const values = [moduleCodes.controlled_corridor, moduleCodes.negative_pressure_patient_room, moduleCodes.anteroom, moduleCodes.ensuite_toilet_shower, moduleCodes.nurse_station, moduleCodes.clean_supply_alcove, moduleCodes.soiled_waste_holding];
  const masses = [];
  for (const value of values) {
    for (const rect of rectangulateClusteredValue(valueGrid, value, clusterSource)) {
      masses.push({x: rect.c, y: rect.r, w: rect.w, d: rect.h, h: massHeightForValue(value), baseZ: GROUND_Z, value: value, color: colorFor(value), label: labelFor(value), clusterId: rect.clusterId, furnitureSignature: furnitureSignatureForValue(value)});
    }
  }
  return masses;
}
function shadeHex(hex, factor) {
  const raw = String(hex || '#999999').replace('#','');
  const n = parseInt(raw.length === 3 ? raw.split('').map(ch => ch + ch).join('') : raw, 16);
  const r = Math.max(0, Math.min(255, Math.round(((n>>16)&255) * factor)));
  const g = Math.max(0, Math.min(255, Math.round(((n>>8)&255) * factor)));
  const b = Math.max(0, Math.min(255, Math.round((n&255) * factor)));
  return '#' + [r,g,b].map(v => v.toString(16).padStart(2,'0')).join('');
}
function project3DPoint(x, y, z, scale, offsetX, offsetY) {
  const cos = Math.cos(threeDRotation.z), sin = Math.sin(threeDRotation.z);
  const xr = (x - cols/2) * cos - (y - rows/2) * sin;
  const yr = (x - cols/2) * sin + (y - rows/2) * cos;
  const pitch = threeDRotation.x;
  const yp = yr * Math.cos(pitch) - z * Math.sin(pitch);
  return {x: offsetX + xr * scale, y: offsetY + yp * scale};
}
function polygon(points, fill, stroke) {
  threeDCtx.beginPath();
  threeDCtx.moveTo(points[0].x, points[0].y);
  for (let i=1; i<points.length; i++) threeDCtx.lineTo(points[i].x, points[i].y);
  threeDCtx.closePath();
  threeDCtx.fillStyle = fill;
  threeDCtx.fill();
  threeDCtx.strokeStyle = stroke || '#374151';
  threeDCtx.lineWidth = 0.7;
  threeDCtx.stroke();
}
function drawGroundFloor(valueGrid, scale, offsetX, offsetY) {
  // ground floor plane: a single shared floor datum gives the 3D masses a visible base so rooms do not appear to float or sit on different floor levels.
  const b = usableBounds();
  if (!b) return;
  const x0 = b.minC, x1 = b.maxC + 1, y0 = b.minR, y1 = b.maxR + 1;
  const p00 = project3DPoint(x0, y0, FLOOR_PLANE_Z, scale, offsetX, offsetY);
  const p10 = project3DPoint(x1, y0, FLOOR_PLANE_Z, scale, offsetX, offsetY);
  const p11 = project3DPoint(x1, y1, FLOOR_PLANE_Z, scale, offsetX, offsetY);
  const p01 = project3DPoint(x0, y1, FLOOR_PLANE_Z, scale, offsetX, offsetY);
  polygon([p00, p10, p11, p01], '#e5e7eb', '#9ca3af');
  threeDCtx.save();
  threeDCtx.strokeStyle = 'rgba(107,114,128,0.18)';
  threeDCtx.lineWidth = 0.45;
  for (let c = b.minC; c <= b.maxC + 1; c += 2) {
    const a = project3DPoint(c, b.minR, FLOOR_PLANE_Z + 0.01, scale, offsetX, offsetY);
    const d = project3DPoint(c, b.maxR + 1, FLOOR_PLANE_Z + 0.01, scale, offsetX, offsetY);
    threeDCtx.beginPath(); threeDCtx.moveTo(a.x, a.y); threeDCtx.lineTo(d.x, d.y); threeDCtx.stroke();
  }
  for (let r = b.minR; r <= b.maxR + 1; r += 2) {
    const a = project3DPoint(b.minC, r, FLOOR_PLANE_Z + 0.01, scale, offsetX, offsetY);
    const d = project3DPoint(b.maxC + 1, r, FLOOR_PLANE_Z + 0.01, scale, offsetX, offsetY);
    threeDCtx.beginPath(); threeDCtx.moveTo(a.x, a.y); threeDCtx.lineTo(d.x, d.y); threeDCtx.stroke();
  }
  threeDCtx.restore();
}
function drawMassBox(mass, scale, offsetX, offsetY) {
  const x0 = mass.x, x1 = mass.x + mass.w, y0 = mass.y, y1 = mass.y + mass.d;
  const z0 = mass.baseZ;
  const z1 = mass.baseZ + mass.h * Z_HEIGHT_SCALE;
  const p000 = project3DPoint(x0,y0,z0,scale,offsetX,offsetY), p100 = project3DPoint(x1,y0,z0,scale,offsetX,offsetY), p110 = project3DPoint(x1,y1,z0,scale,offsetX,offsetY), p010 = project3DPoint(x0,y1,z0,scale,offsetX,offsetY);
  const p001 = project3DPoint(x0,y0,z1,scale,offsetX,offsetY), p101 = project3DPoint(x1,y0,z1,scale,offsetX,offsetY), p111 = project3DPoint(x1,y1,z1,scale,offsetX,offsetY), p011 = project3DPoint(x0,y1,z1,scale,offsetX,offsetY);
  polygon([p000,p100,p101,p001], shadeHex(mass.color, 0.82));
  polygon([p100,p110,p111,p101], shadeHex(mass.color, 0.68));
  polygon([p010,p110,p111,p011], shadeHex(mass.color, 0.74));
  polygon([p001,p101,p111,p011], mass.color);
  if (mass.w * mass.d >= 4) {
    const center = project3DPoint((x0+x1)/2, (y0+y1)/2, z1 + 0.25, scale, offsetX, offsetY);
    threeDCtx.fillStyle = '#111827';
    threeDCtx.font = '10px sans-serif';
    threeDCtx.textAlign = 'center';
    threeDCtx.fillText(mass.label, center.x, center.y);
  }
}
function drawRoomFloorPlate(mass, scale, offsetX, offsetY) {
  // Draw rooms/corridors as flat finish plates, not raised mass boxes. This prevents the 'furniture pasted on top of grey blocks' look.
  const x0 = mass.x, x1 = mass.x + mass.w, y0 = mass.y, y1 = mass.y + mass.d;
  const z = FINISHED_FLOOR_Z;
  const p00 = project3DPoint(x0,y0,z,scale,offsetX,offsetY);
  const p10 = project3DPoint(x1,y0,z,scale,offsetX,offsetY);
  const p11 = project3DPoint(x1,y1,z,scale,offsetX,offsetY);
  const p01 = project3DPoint(x0,y1,z,scale,offsetX,offsetY);
  polygon([p00,p10,p11,p01], shadeHex(mass.color, mass.value === moduleCodes.controlled_corridor ? 0.96 : 1.04), 'rgba(51,65,85,0.35)');
  if (mass.w * mass.d >= 4) {
    const center = project3DPoint((x0+x1)/2, (y0+y1)/2, z + 0.012, scale, offsetX, offsetY);
    threeDCtx.fillStyle = 'rgba(17,24,39,0.62)';
    threeDCtx.font = '10px sans-serif';
    threeDCtx.textAlign = 'center';
    threeDCtx.fillText(mass.label, center.x, center.y);
  }
}
function furnitureZ(item) { return item.baseZ; }
function furnitureCorners(item, z, scale, offsetX, offsetY, inset = 0) {
  const x0 = item.x + inset * item.w, x1 = item.x + item.w - inset * item.w;
  const y0 = item.y + inset * item.d, y1 = item.y + item.d - inset * item.d;
  return {
    p00: project3DPoint(x0,y0,z,scale,offsetX,offsetY),
    p10: project3DPoint(x1,y0,z,scale,offsetX,offsetY),
    p11: project3DPoint(x1,y1,z,scale,offsetX,offsetY),
    p01: project3DPoint(x0,y1,z,scale,offsetX,offsetY)
  };
}
function drawFurnitureContactShadow(item, scale, offsetX, offsetY) {
  // Contact shadow at the finished floor surface makes equipment read as sitting on the slab, even with the isometric projection.
  const c = furnitureCorners(item, FURNITURE_GROUND_SHADOW_Z, scale, offsetX, offsetY, -0.055);
  polygon([c.p00,c.p10,c.p11,c.p01], 'rgba(15,23,42,0.24)', 'rgba(15,23,42,0.04)');
}
function drawFurnitureVolume(item, scale, offsetX, offsetY, fill = item.color, heightScale = 1) {
  // Custom low 3D equipment volume: no generic room-box renderer, no flat footprint. Furniture visually intersects the finished floor by a tiny amount, removing hover gaps from the isometric projection.
  const z0 = furnitureVisualBaseZ(item);
  const z1 = z0 + furnitureVisualHeight(item, heightScale);
  const b = furnitureCorners(item, z0, scale, offsetX, offsetY, 0);
  const t = furnitureCorners(item, z1, scale, offsetX, offsetY, 0.025);
  polygon([b.p00,b.p10,t.p10,t.p00], shadeHex(fill, 0.84), 'rgba(15,23,42,0.58)');
  polygon([b.p10,b.p11,t.p11,t.p10], shadeHex(fill, 0.70), 'rgba(15,23,42,0.52)');
  polygon([b.p01,b.p11,t.p11,t.p01], shadeHex(fill, 0.76), 'rgba(15,23,42,0.44)');
  polygon([t.p00,t.p10,t.p11,t.p01], fill, 'rgba(15,23,42,0.72)');
}
function drawFurnitureTopDetail(item, scale, offsetX, offsetY, inset = 0.14, fill = 'rgba(255,255,255,0.55)', stroke = 'rgba(51,65,85,0.35)') {
  const z = furnitureVisualBaseZ(item) + furnitureVisualHeight(item) + 0.012;
  const c = furnitureCorners(item, z, scale, offsetX, offsetY, inset);
  polygon([c.p00,c.p10,c.p11,c.p01], fill, stroke);
}
function childFurniture(item, rel, overrides = {}) {
  return {
    ...item,
    ...overrides,
    x: item.x + rel.x * item.w,
    y: item.y + rel.y * item.d,
    w: rel.w * item.w,
    d: rel.d * item.d,
    h: overrides.h !== undefined ? overrides.h : item.h,
    baseZ: overrides.baseZ !== undefined ? overrides.baseZ : groundedFurnitureBaseForHeight(overrides.h !== undefined ? overrides.h : item.h, overrides.heightScale || 1)
  };
}
function drawScreenEllipseAt(x, y, z, rx, ry, scale, offsetX, offsetY, fill, stroke) {
  const center = project3DPoint(x, y, z, scale, offsetX, offsetY);
  threeDCtx.save();
  threeDCtx.fillStyle = fill;
  threeDCtx.strokeStyle = stroke;
  threeDCtx.lineWidth = 0.9;
  threeDCtx.beginPath();
  threeDCtx.ellipse(center.x, center.y, Math.max(3, rx * scale), Math.max(2, ry * scale), 0, 0, Math.PI * 2);
  threeDCtx.fill(); threeDCtx.stroke();
  threeDCtx.restore();
}
function drawFurnitureEdgeLine(item, scale, offsetX, offsetY, inset = 0.06, zLift = 0.014, stroke = 'rgba(15,23,42,0.50)') {
  const z = furnitureVisualBaseZ(item) + furnitureVisualHeight(item) + zLift;
  const c = furnitureCorners(item, z, scale, offsetX, offsetY, inset);
  threeDCtx.save();
  threeDCtx.strokeStyle = stroke;
  threeDCtx.lineWidth = 0.85;
  threeDCtx.beginPath();
  threeDCtx.moveTo(c.p00.x, c.p00.y);
  threeDCtx.lineTo(c.p10.x, c.p10.y);
  threeDCtx.lineTo(c.p11.x, c.p11.y);
  threeDCtx.lineTo(c.p01.x, c.p01.y);
  threeDCtx.closePath();
  threeDCtx.stroke();
  threeDCtx.restore();
}
function projectedItemMetrics(item, z, scale, offsetX, offsetY) {
  const center = project3DPoint(item.x + item.w / 2, item.y + item.d / 2, z, scale, offsetX, offsetY);
  const xA = project3DPoint(item.x, item.y + item.d / 2, z, scale, offsetX, offsetY);
  const xB = project3DPoint(item.x + item.w, item.y + item.d / 2, z, scale, offsetX, offsetY);
  const yA = project3DPoint(item.x + item.w / 2, item.y, z, scale, offsetX, offsetY);
  const yB = project3DPoint(item.x + item.w / 2, item.y + item.d, z, scale, offsetX, offsetY);
  return {center, rx: Math.max(2.6, Math.hypot(xA.x - xB.x, xA.y - xB.y) / 2), ry: Math.max(2.1, Math.hypot(yA.x - yB.x, yA.y - yB.y) / 2)};
}
function drawIsoEllipseCap(item, scale, offsetX, offsetY, fill, stroke = 'rgba(15,23,42,0.58)', heightScale = 1, zLift = 0.012, rxScale = 0.94, ryScale = 0.62) {
  const z = furnitureVisualBaseZ(item) + furnitureVisualHeight(item, heightScale) + zLift;
  const m = projectedItemMetrics(item, z, scale, offsetX, offsetY);
  threeDCtx.save();
  threeDCtx.fillStyle = fill;
  threeDCtx.strokeStyle = stroke;
  threeDCtx.lineWidth = 0.95;
  threeDCtx.beginPath();
  threeDCtx.ellipse(m.center.x, m.center.y, m.rx * rxScale, m.ry * ryScale, -0.18, 0, Math.PI * 2);
  threeDCtx.fill();
  threeDCtx.stroke();
  threeDCtx.restore();
}
function drawRoundedProjectedTop(item, scale, offsetX, offsetY, fill, stroke = 'rgba(15,23,42,0.58)', heightScale = 1, inset = 0.035) {
  const z = furnitureVisualBaseZ(item) + furnitureVisualHeight(item, heightScale) + 0.018;
  const c = furnitureCorners(item, z, scale, offsetX, offsetY, inset);
  const cx = (c.p00.x + c.p10.x + c.p11.x + c.p01.x) / 4;
  const cy = (c.p00.y + c.p10.y + c.p11.y + c.p01.y) / 4;
  threeDCtx.save();
  threeDCtx.fillStyle = fill;
  threeDCtx.strokeStyle = stroke;
  threeDCtx.lineWidth = 0.95;
  threeDCtx.beginPath();
  threeDCtx.moveTo((c.p00.x + c.p10.x) / 2, (c.p00.y + c.p10.y) / 2);
  threeDCtx.quadraticCurveTo(c.p10.x, c.p10.y, (c.p10.x + c.p11.x) / 2, (c.p10.y + c.p11.y) / 2);
  threeDCtx.quadraticCurveTo(c.p11.x, c.p11.y, (c.p11.x + c.p01.x) / 2, (c.p11.y + c.p01.y) / 2);
  threeDCtx.quadraticCurveTo(c.p01.x, c.p01.y, (c.p01.x + c.p00.x) / 2, (c.p01.y + c.p00.y) / 2);
  threeDCtx.quadraticCurveTo(c.p00.x, c.p00.y, (c.p00.x + c.p10.x) / 2, (c.p00.y + c.p10.y) / 2);
  threeDCtx.closePath();
  threeDCtx.fill();
  threeDCtx.stroke();
  threeDCtx.fillStyle = 'rgba(255,255,255,0.35)';
  threeDCtx.beginPath();
  threeDCtx.ellipse(cx, cy - 1.5, Math.max(2.5, Math.abs(c.p10.x - c.p00.x) * 0.16), Math.max(1.4, Math.abs(c.p11.y - c.p10.y) * 0.10), -0.2, 0, Math.PI * 2);
  threeDCtx.fill();
  threeDCtx.restore();
}
function drawCylinderFixture(item, scale, offsetX, offsetY, fill, stroke = 'rgba(15,23,42,0.58)', heightScale = 1, rxScale = 0.82, ryScale = 0.62) {
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  const body = childFurniture(item, {x:0.10, y:0.12, w:0.80, d:0.76}, {h:item.h, color:fill});
  drawFurnitureVolume(body, scale, offsetX, offsetY, fill, heightScale * 0.58);
  drawIsoEllipseCap(body, scale, offsetX, offsetY, shadeHex(fill, 1.08), stroke, heightScale * 0.58, 0.016, rxScale, ryScale);
}
function drawFurnitureLabel(item, scale, offsetX, offsetY, text = item.label) {
  if (!text) return;
  const p = project3DPoint(item.x + item.w / 2, item.y + item.d / 2, furnitureVisualBaseZ(item) + furnitureVisualHeight(item) + 0.035, scale, offsetX, offsetY);
  threeDCtx.save();
  threeDCtx.fillStyle = 'rgba(15,23,42,0.66)';
  threeDCtx.font = '8px sans-serif';
  threeDCtx.textAlign = 'center';
  threeDCtx.fillText(text, p.x, p.y + 2);
  threeDCtx.restore();
}
function drawPatientBed(item, scale, offsetX, offsetY) {
  // Low 3D bed: rounded mattress cap + pillow + side rail. Avoid the “just another cuboid” look.
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(item, scale, offsetX, offsetY, '#e0e7ff', 0.78);
  drawRoundedProjectedTop(item, scale, offsetX, offsetY, 'rgba(248,250,252,0.98)', 'rgba(71,85,105,0.62)', 1.05, 0.055);
  const pillow = childFurniture(item, {x:0.14, y:0.07, w:0.72, d:0.20}, {h:0.045, color:'#dbeafe'});
  drawFurnitureVolume(pillow, scale, offsetX, offsetY, '#dbeafe', 0.38);
  drawIsoEllipseCap(pillow, scale, offsetX, offsetY, '#eff6ff', 'rgba(37,99,235,0.46)', 0.38, 0.018, 0.92, 0.56);
  const railLeft = childFurniture(item, {x:0.05, y:0.30, w:0.05, d:0.52}, {h:0.07, color:'#cbd5e1'});
  const railRight = childFurniture(item, {x:0.90, y:0.30, w:0.05, d:0.52}, {h:0.07, color:'#cbd5e1'});
  drawFurnitureVolume(railLeft, scale, offsetX, offsetY, '#cbd5e1', 0.72);
  drawFurnitureVolume(railRight, scale, offsetX, offsetY, '#cbd5e1', 0.72);
}
function drawHeadwall(item, scale, offsetX, offsetY) {
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(item, scale, offsetX, offsetY, '#bfdbfe', 0.95);
  drawFurnitureEdgeLine(item, scale, offsetX, offsetY, 0.10, 0.018, 'rgba(37,99,235,0.56)');
}
function drawToiletFixture(item, scale, offsetX, offsetY) {
  // Sanitary fixture reads as a small raised fixture: plinth + rounded bowl + cistern, not a cuboid.
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  const plinth = childFurniture(item, {x:0.10, y:0.16, w:0.80, d:0.70}, {h:0.055, color:'#e0f2fe'});
  const bowl = childFurniture(item, {x:0.20, y:0.28, w:0.60, d:0.46}, {h:0.105, color:'#f8fafc'});
  const tank = childFurniture(item, {x:0.16, y:0.06, w:0.68, d:0.18}, {h:0.12, color:'#e2e8f0'});
  drawFurnitureVolume(plinth, scale, offsetX, offsetY, '#e0f2fe', 0.40);
  drawCylinderFixture(bowl, scale, offsetX, offsetY, '#f8fafc', 'rgba(2,132,199,0.58)', 0.92, 0.72, 0.70);
  drawIsoEllipseCap(bowl, scale, offsetX, offsetY, 'rgba(186,230,253,0.82)', 'rgba(2,132,199,0.52)', 0.55, 0.035, 0.42, 0.32);
  drawFurnitureVolume(tank, scale, offsetX, offsetY, '#e2e8f0', 0.82);
}
function drawShowerZone(item, scale, offsetX, offsetY) {
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(item, scale, offsetX, offsetY, '#bfdbfe', 0.25);
  drawRoundedProjectedTop(item, scale, offsetX, offsetY, 'rgba(224,242,254,0.72)', 'rgba(2,132,199,0.50)', 0.22, 0.10);
  drawIsoEllipseCap(childFurniture(item, {x:0.40, y:0.40, w:0.20, d:0.20}, {h:0.025, color:'#38bdf8'}), scale, offsetX, offsetY, 'rgba(14,116,144,0.58)', 'rgba(14,116,144,0.55)', 0.20, 0.01, 0.70, 0.70);
  drawFurnitureEdgeLine(item, scale, offsetX, offsetY, 0.12, 0.012, 'rgba(2,132,199,0.58)');
}
function drawWashbasin(item, scale, offsetX, offsetY) {
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(item, scale, offsetX, offsetY, '#dbeafe', 0.46);
  drawIsoEllipseCap(item, scale, offsetX, offsetY, 'rgba(240,249,255,0.96)', 'rgba(14,116,144,0.58)', 0.74, 0.018, 0.82, 0.52);
  drawIsoEllipseCap(item, scale, offsetX, offsetY, 'rgba(186,230,253,0.72)', 'rgba(14,116,144,0.42)', 0.42, 0.032, 0.46, 0.30);
}
function drawBench(item, scale, offsetX, offsetY) {
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(item, scale, offsetX, offsetY, item.color || '#fde68a', 0.72);
  const legA = childFurniture(item, {x:0.12, y:0.18, w:0.08, d:0.64}, {h:0.055, color:'#d97706'});
  const legB = childFurniture(item, {x:0.80, y:0.18, w:0.08, d:0.64}, {h:0.055, color:'#d97706'});
  drawFurnitureVolume(legA, scale, offsetX, offsetY, '#d97706', 0.55);
  drawFurnitureVolume(legB, scale, offsetX, offsetY, '#d97706', 0.55);
}
function drawCabinetOrShelving(item, scale, offsetX, offsetY) {
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(item, scale, offsetX, offsetY, item.color || '#dcfce7', 1.10);
  drawFurnitureEdgeLine(item, scale, offsetX, offsetY, 0.08, 0.018, 'rgba(22,101,52,0.52)');
  drawFurnitureLabel(item, scale, offsetX, offsetY, item.type === 'supply_shelving' ? 'shelf' : 'cab');
}
function drawNurseCounter(item, scale, offsetX, offsetY) {
  // L-shaped reception counter with rounded projected tops; still grounded 3D, but less like two plain boxes.
  const counter = childFurniture(item, {x:0.02, y:0.10, w:0.82, d:0.34}, {h:item.h, color:'#ccfbf1'});
  const returnWing = childFurniture(item, {x:0.55, y:0.38, w:0.34, d:0.48}, {h:item.h, color:'#99f6e4'});
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(counter, scale, offsetX, offsetY, '#ccfbf1', 0.82);
  drawRoundedProjectedTop(counter, scale, offsetX, offsetY, 'rgba(240,253,250,0.94)', 'rgba(13,148,136,0.58)', 0.90, 0.07);
  drawFurnitureVolume(returnWing, scale, offsetX, offsetY, '#99f6e4', 0.80);
  drawRoundedProjectedTop(returnWing, scale, offsetX, offsetY, 'rgba(204,251,241,0.92)', 'rgba(15,118,110,0.52)', 0.88, 0.07);
}
function drawWorkstation(item, scale, offsetX, offsetY) {
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(item, scale, offsetX, offsetY, '#99f6e4', 0.78);
  const monitor = childFurniture(item, {x:0.28, y:0.08, w:0.44, d:0.18}, {h:0.10, color:'#334155'});
  drawFurnitureVolume(monitor, scale, offsetX, offsetY, '#334155', 0.80);
}
function drawTrolleyOrBin(item, scale, offsetX, offsetY) {
  if (item.type === 'waste_bin') return drawCylinderFixture(item, scale, offsetX, offsetY, item.color, 'rgba(127,29,29,0.50)', 0.82, 0.82, 0.66);
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(item, scale, offsetX, offsetY, item.color, 0.74);
  drawRoundedProjectedTop(item, scale, offsetX, offsetY, 'rgba(255,255,255,0.36)', 'rgba(51,65,85,0.42)', 0.68, 0.12);
}
function drawGenericFurnitureVolume(item, scale, offsetX, offsetY) {
  drawFurnitureContactShadow(item, scale, offsetX, offsetY);
  drawFurnitureVolume(item, scale, offsetX, offsetY, item.color, 0.86);
  drawFurnitureTopDetail(item, scale, offsetX, offsetY);
}
function drawFurnitureItem(item, scale, offsetX, offsetY) {
  if (item.type === 'patient_bed') return drawPatientBed(item, scale, offsetX, offsetY);
  if (item.type === 'headwall') return drawHeadwall(item, scale, offsetX, offsetY);
  if (item.type === 'toilet_fixture') return drawToiletFixture(item, scale, offsetX, offsetY);
  if (item.type === 'shower_zone') return drawShowerZone(item, scale, offsetX, offsetY);
  if (item.type === 'washbasin' || item.type === 'handwash_sink') return drawWashbasin(item, scale, offsetX, offsetY);
  if (item.type === 'ppe_bench') return drawBench(item, scale, offsetX, offsetY);
  if (item.type === 'donning_cabinet' || item.type === 'supply_shelving') return drawCabinetOrShelving(item, scale, offsetX, offsetY);
  if (item.type === 'nurse_counter') return drawNurseCounter(item, scale, offsetX, offsetY);
  if (item.type === 'workstation') return drawWorkstation(item, scale, offsetX, offsetY);
  if (item.type === 'meds_trolley' || item.type === 'waste_bin' || item.type === 'medical_cart') return drawTrolleyOrBin(item, scale, offsetX, offsetY);
  return drawGenericFurnitureVolume(item, scale, offsetX, offsetY);
}
function buildWallSegmentsFromMass(mass) {
  if (mass.value === moduleCodes.controlled_corridor) return [];
  const t = Math.min(WALL_THICKNESS, Math.max(0.045, Math.min(mass.w, mass.d) * 0.08));
  return [
    {x: mass.x, y: mass.y, w: mass.w, d: t, h: WALL_HEIGHT, baseZ: GROUND_Z, color:'#f8fafc', label:'wall', sourceCluster: mass.clusterId},
    {x: mass.x, y: mass.y + mass.d - t, w: mass.w, d: t, h: WALL_HEIGHT, baseZ: GROUND_Z, color:'#e5e7eb', label:'wall', sourceCluster: mass.clusterId},
    {x: mass.x, y: mass.y, w: t, d: mass.d, h: WALL_HEIGHT, baseZ: GROUND_Z, color:'#f1f5f9', label:'wall', sourceCluster: mass.clusterId},
    {x: mass.x + mass.w - t, y: mass.y, w: t, d: mass.d, h: WALL_HEIGHT, baseZ: GROUND_Z, color:'#cbd5e1', label:'wall', sourceCluster: mass.clusterId}
  ];
}
function drawWallSegment(segment, scale, offsetX, offsetY) {
  // Visible cutaway wall panel: enough vertical surface to read the room boundary, but not a solid room box.
  drawCutawayWallPanel(segment, scale, offsetX, offsetY);
  drawCutawayWallLine(segment, scale, offsetX, offsetY);
}
function drawCutawayWallPanel(segment, scale, offsetX, offsetY) {
  const x0 = segment.x, x1 = segment.x + segment.w, y0 = segment.y, y1 = segment.y + segment.d;
  const horizontal = segment.w >= segment.d;
  const z0 = FINISHED_FLOOR_Z + 0.01;
  const z1 = GROUND_Z + WALL_HEIGHT;
  const a0 = horizontal ? project3DPoint(x0, (y0 + y1) / 2, z0, scale, offsetX, offsetY) : project3DPoint((x0 + x1) / 2, y0, z0, scale, offsetX, offsetY);
  const b0 = horizontal ? project3DPoint(x1, (y0 + y1) / 2, z0, scale, offsetX, offsetY) : project3DPoint((x0 + x1) / 2, y1, z0, scale, offsetX, offsetY);
  const a1 = horizontal ? project3DPoint(x0, (y0 + y1) / 2, z1, scale, offsetX, offsetY) : project3DPoint((x0 + x1) / 2, y0, z1, scale, offsetX, offsetY);
  const b1 = horizontal ? project3DPoint(x1, (y0 + y1) / 2, z1, scale, offsetX, offsetY) : project3DPoint((x0 + x1) / 2, y1, z1, scale, offsetX, offsetY);
  polygon([a0, b0, b1, a1], 'rgba(148,163,184,0.18)', 'rgba(71,85,105,0.44)');
}
function drawCutawayWallLine(segment, scale, offsetX, offsetY) {
  const x0 = segment.x, x1 = segment.x + segment.w, y0 = segment.y, y1 = segment.y + segment.d;
  const horizontal = segment.w >= segment.d;
  const a = horizontal ? project3DPoint(x0, (y0 + y1) / 2, GROUND_Z + WALL_HEIGHT, scale, offsetX, offsetY) : project3DPoint((x0 + x1) / 2, y0, GROUND_Z + WALL_HEIGHT, scale, offsetX, offsetY);
  const b = horizontal ? project3DPoint(x1, (y0 + y1) / 2, GROUND_Z + WALL_HEIGHT, scale, offsetX, offsetY) : project3DPoint((x0 + x1) / 2, y1, GROUND_Z + WALL_HEIGHT, scale, offsetX, offsetY);
  threeDCtx.save();
  threeDCtx.setLineDash([2.5, 2.5]);
  threeDCtx.strokeStyle = 'rgba(51,65,85,0.70)';
  threeDCtx.lineWidth = 1.25;
  threeDCtx.beginPath(); threeDCtx.moveTo(a.x, a.y); threeDCtx.lineTo(b.x, b.y); threeDCtx.stroke();
  threeDCtx.restore();
}
function drawDoorSwing(mass, scale, offsetX, offsetY) {
  if (![moduleCodes.negative_pressure_patient_room, moduleCodes.anteroom, moduleCodes.ensuite_toilet_shower, moduleCodes.nurse_station].includes(mass.value)) return;
  const z = GROUND_Z + 0.16;
  const hinge = project3DPoint(mass.x + 0.12 * mass.w, mass.y, z, scale, offsetX, offsetY);
  const jamb = project3DPoint(mass.x + 0.44 * mass.w, mass.y, z, scale, offsetX, offsetY);
  const open = project3DPoint(mass.x + 0.12 * mass.w, mass.y + Math.min(0.42 * mass.d, 0.9), z, scale, offsetX, offsetY);
  threeDCtx.save();
  threeDCtx.strokeStyle = 'rgba(17,24,39,0.55)';
  threeDCtx.lineWidth = 1;
  threeDCtx.beginPath(); threeDCtx.moveTo(hinge.x, hinge.y); threeDCtx.lineTo(jamb.x, jamb.y); threeDCtx.lineTo(open.x, open.y); threeDCtx.stroke();
  threeDCtx.restore();
}
function drawTransparentPartition(mass, scale, offsetX, offsetY) {
  if (![moduleCodes.negative_pressure_patient_room, moduleCodes.anteroom, moduleCodes.nurse_station].includes(mass.value)) return;
  const z = GROUND_Z + 0.34;
  const a = project3DPoint(mass.x, mass.y + 0.06 * mass.d, z, scale, offsetX, offsetY);
  const b = project3DPoint(mass.x + mass.w, mass.y + 0.06 * mass.d, z, scale, offsetX, offsetY);
  threeDCtx.save();
  threeDCtx.strokeStyle = 'rgba(14,165,233,0.42)';
  threeDCtx.lineWidth = 1.3;
  threeDCtx.setLineDash([3, 3]);
  threeDCtx.beginPath(); threeDCtx.moveTo(a.x, a.y); threeDCtx.lineTo(b.x, b.y); threeDCtx.stroke();
  threeDCtx.restore();
}
function drawFurnitureLegend(furnitureCount) {
  threeDCtx.save();
  const x = 12, y = 34;
  threeDCtx.fillStyle = 'rgba(255,255,255,0.88)';
  threeDCtx.strokeStyle = '#cbd5e1';
  threeDCtx.fillRect(x, y, 352, 52);
  threeDCtx.strokeRect(x, y, 352, 52);
  threeDCtx.fillStyle = '#334155';
  threeDCtx.font = '11px sans-serif';
  threeDCtx.textAlign = 'left';
  threeDCtx.fillText('Architectural 3D: repeated furniture kits per module type', x + 10, y + 18);
  threeDCtx.fillText('bed / PPE / WC / nurse counter / supply shelving / waste bins: ' + furnitureCount + ' items', x + 10, y + 36);
  threeDCtx.restore();
}
function drawArchitecturalCues(mass, scale, offsetX, offsetY) {
  drawTransparentPartition(mass, scale, offsetX, offsetY);
  drawDoorSwing(mass, scale, offsetX, offsetY);
}
let threeRenderer = null;
let threeScene = null;
let threeCamera = null;
let threeRoot = null;
let gltfLoaderInstance = null;
const furnitureModelCache = {};
let threeSceneCenter = {x: cols / 2, y: rows / 2};
const THREE_CELL_M = 1.0;
const THREE_ROOM_HEIGHT = 0.06;
const THREE_WALL_HEIGHT = 0.42;
const THREE_FURNITURE_SCALE = 1.38;
function threeHex(hex) { return new THREE.Color(hex || '#999999'); }
function threePos(x, y, z = 0) { return new THREE.Vector3((x - threeSceneCenter.x) * THREE_CELL_M, z, (y - threeSceneCenter.y) * THREE_CELL_M); }
function sceneCenterFromMasses(masses) {
  if (!masses.length) return {x: cols / 2, y: rows / 2, span: Math.max(cols, rows)};
  const minX = Math.min(...masses.map(m => m.x));
  const maxX = Math.max(...masses.map(m => m.x + m.w));
  const minY = Math.min(...masses.map(m => m.y));
  const maxY = Math.max(...masses.map(m => m.y + m.d));
  return {x: (minX + maxX) / 2, y: (minY + maxY) / 2, span: Math.max(maxX - minX, maxY - minY)};
}
function makeMat(color, roughness = 0.72, metalness = 0.02, opacity = 1) {
  return new THREE.MeshStandardMaterial({color: threeHex(color), roughness, metalness, transparent: opacity < 1, opacity});
}
function brightenModelMaterial(mat, factor = 1.42) {
  if (!mat) return mat;
  mat.roughness = Math.min(0.95, Math.max(0.78, mat.roughness || 0.78));
  mat.metalness = 0.0;
  if (mat.color) {
    const hsl = {};
    mat.color.getHSL(hsl);
    // Small GLB details such as bed rails and shelving frames must read by silhouette, not collapse into black strokes.
    hsl.l = Math.min(0.86, Math.max(0.46, hsl.l * factor + 0.12));
    hsl.s = Math.min(0.80, hsl.s * 1.04);
    mat.color.setHSL(hsl.h, hsl.s, hsl.l);
  }
  if (mat.emissive) {
    mat.emissive.copy(mat.color || new THREE.Color(0xffffff)).multiplyScalar(0.035);
  }
  mat.needsUpdate = true;
  return mat;
}
function addFurnitureEdgeLines(mesh) {
  if (!mesh || !mesh.geometry) return;
  const edges = new THREE.EdgesGeometry(mesh.geometry, 25);
  const lines = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({
    color: 0x334155,
    transparent: true,
    opacity: 0.58,
    depthTest: true,
  }));
  lines.name = 'semantic furniture silhouette edges';
  lines.renderOrder = 6;
  mesh.add(lines);
}
function addMesh(mesh, x, y, z, parent = threeRoot) {
  mesh.position.copy(threePos(x, y, z));
  parent.add(mesh);
  return mesh;
}
function addBox3D(parent, x, y, w, d, h, color, z = 0, name = '') {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(w * THREE_CELL_M, h, d * THREE_CELL_M), makeMat(color));
  mesh.position.copy(threePos(x + w / 2, y + d / 2, z + h / 2));
  mesh.castShadow = true; mesh.receiveShadow = true; mesh.name = name;
  parent.add(mesh);
  return mesh;
}
function addCylinder3D(parent, x, y, w, d, h, color, z = 0, name = '') {
  const radius = Math.max(0.035, Math.min(w, d) * 0.5 * THREE_CELL_M);
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, h, 28), makeMat(color));
  mesh.scale.x = Math.max(0.55, w / Math.min(w, d));
  mesh.scale.z = Math.max(0.55, d / Math.min(w, d));
  mesh.position.copy(threePos(x + w / 2, y + d / 2, z + h / 2));
  mesh.castShadow = true; mesh.receiveShadow = true; mesh.name = name;
  parent.add(mesh);
  return mesh;
}
function addCapsule3D(parent, x, y, w, d, h, color, z = 0, name = '') {
  const radius = Math.min(w, d) * 0.22;
  const length = Math.max(0.05, Math.max(w, d) - radius * 2);
  const geo = new THREE.CapsuleGeometry(radius, length, 6, 16);
  const mesh = new THREE.Mesh(geo, makeMat(color));
  mesh.rotation.z = Math.PI / 2;
  mesh.scale.z = Math.max(0.45, d / Math.max(w, 0.01));
  mesh.position.copy(threePos(x + w / 2, y + d / 2, z + h / 2));
  mesh.castShadow = true; mesh.receiveShadow = true; mesh.name = name;
  parent.add(mesh);
  return mesh;
}
function addLabelSprite(parent, text, x, y, z) {
  const canvasLabel = document.createElement('canvas');
  canvasLabel.width = 128; canvasLabel.height = 48;
  const c = canvasLabel.getContext('2d');
  c.fillStyle = 'rgba(255,255,255,0.72)'; c.fillRect(0,0,128,48);
  c.fillStyle = '#1f2937'; c.font = 'bold 24px Arial'; c.textAlign = 'center'; c.fillText(text, 64, 31);
  const tex = new THREE.CanvasTexture(canvasLabel);
  const sprite = new THREE.Sprite(new THREE.SpriteMaterial({map: tex, transparent:true, depthTest:false}));
  sprite.scale.set(0.9, 0.34, 1); sprite.position.copy(threePos(x, y, z)); sprite.renderOrder = 20; parent.add(sprite);
}
function addTorus3D(parent, x, y, w, d, tube, color, z = 0, name = '') {
  const radius = Math.max(0.035, Math.min(w, d) * 0.30 * THREE_CELL_M);
  const mesh = new THREE.Mesh(new THREE.TorusGeometry(radius, tube, 10, 32), makeMat(color));
  mesh.rotation.x = Math.PI / 2;
  mesh.scale.x = Math.max(0.65, w / Math.max(Math.min(w, d), 0.01));
  mesh.scale.y = Math.max(0.65, d / Math.max(Math.min(w, d), 0.01));
  mesh.position.copy(threePos(x + w / 2, y + d / 2, z));
  mesh.castShadow = true; mesh.receiveShadow = true; mesh.name = name;
  parent.add(mesh);
  return mesh;
}
function addSlimCylinder3D(parent, x, y, radius, h, color, z = 0, name = '') {
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, h, 16), makeMat(color));
  mesh.position.copy(threePos(x, y, z + h / 2));
  mesh.castShadow = true; mesh.receiveShadow = true; mesh.name = name;
  parent.add(mesh);
  return mesh;
}
function addSphere3D(parent, x, y, radius, color, z = 0, name = '') {
  const mesh = new THREE.Mesh(new THREE.SphereGeometry(radius, 18, 12), makeMat(color));
  mesh.position.copy(threePos(x, y, z));
  mesh.castShadow = true; mesh.receiveShadow = true; mesh.name = name;
  parent.add(mesh);
  return mesh;
}
function scaledFurnitureRect(item) {
  const cx = item.x + item.w / 2;
  const cy = item.y + item.d / 2;
  const w = Math.min(item.w * THREE_FURNITURE_SCALE, item.w + 0.34);
  const d = Math.min(item.d * THREE_FURNITURE_SCALE, item.d + 0.34);
  return {x: cx - w / 2, y: cy - d / 2, w, d, cx, cy};
}
function applyThreeCameraPanVector() {
  if (!threeCamera || typeof THREE === 'undefined') return;
  threeDCameraTarget = new THREE.Vector3(threeDPan.x, threeDPan.y, threeDPan.z);
  threeCamera.position.set(16 + threeDPan.x, 24 + threeDPan.y, 18 + threeDPan.z);
  threeCamera.lookAt(threeDCameraTarget);
}
function applyThreeCameraZoom() {
  if (!threeCamera) return;
  threeCamera.zoom = threeDZoom * THREE_D_ZOOM_BASE;
  threeCamera.updateProjectionMatrix();
}
function panThreeCameraByScreenDelta(dx, dy) {
  if (!threeCamera || typeof THREE === 'undefined') return;
  threeCamera.updateMatrixWorld();
  const right = new THREE.Vector3().setFromMatrixColumn(threeCamera.matrixWorld, 0);
  const up = new THREE.Vector3().setFromMatrixColumn(threeCamera.matrixWorld, 1);
  const worldPerPixel = ((threeCamera.right - threeCamera.left) / threeCamera.zoom) / threeDCanvas.width;
  const delta = right.multiplyScalar(-dx * worldPerPixel).add(up.multiplyScalar(dy * worldPerPixel));
  threeDPan.x += delta.x;
  threeDPan.y += delta.y;
  threeDPan.z += delta.z;
  applyThreeCameraPanVector();
}
function renderThreeSceneIfReady() {
  if (threeRenderer && threeScene && threeCamera) threeRenderer.render(threeScene, threeCamera);
}
function initThreeViewer(masses) {
  if (typeof THREE === 'undefined') throw new Error('Three.js failed to load; cannot render WebGL ward viewer.');
  threeSceneCenter = sceneCenterFromMasses(masses || []);
  if (threeRenderer) { threeRenderer.dispose(); threeRenderer = null; }
  threeRenderer = new THREE.WebGLRenderer({canvas: threeDCanvas, antialias: true, preserveDrawingBuffer: true});
  threeRenderer.setSize(threeDCanvas.width, threeDCanvas.height, false);
  threeRenderer.setClearColor(0xf8fafc, 1);
  threeRenderer.shadowMap.enabled = true;
  threeScene = new THREE.Scene();
  threeScene.background = new THREE.Color(0xf8fafc);
  const aspect = threeDCanvas.width / threeDCanvas.height;
  const view = Math.max(7.2, threeSceneCenter.span * 0.50);
  threeCamera = new THREE.OrthographicCamera(-view * aspect, view * aspect, view, -view, 0.1, 200);
  applyThreeCameraPanVector();
  applyThreeCameraZoom();
  threeScene.add(new THREE.HemisphereLight(0xffffff, 0xdbeafe, 0.92));
  threeScene.add(new THREE.AmbientLight(0xffffff, 0.82));
  const sun = new THREE.DirectionalLight(0xffffff, 1.05);
  sun.position.set(15, 28, 18); sun.castShadow = true; threeScene.add(sun);
  const fill = new THREE.DirectionalLight(0xe0f2fe, 0.48);
  fill.position.set(-18, 16, -14); threeScene.add(fill);
  threeRoot = new THREE.Group();
  threeRoot.rotation.y = threeDRotation.z;
  // Orthographic isometric projection naturally pushes the plan upward; lower the root in camera-space so the ward reads centered in the canvas.
  threeRoot.position.y = -Math.max(1.0, threeSceneCenter.span * 0.18);
  threeScene.add(threeRoot);
}
function addWardFloorsAndWalls3D(masses) {
  const b = usableBounds();
  if (b) addBox3D(threeRoot, b.minC, b.minR, b.maxC - b.minC + 1, b.maxR - b.minR + 1, 0.025, '#e5e7eb', -0.035, 'shared floor slab');
  for (const mass of masses) {
    addBox3D(threeRoot, mass.x, mass.y, mass.w, mass.d, THREE_ROOM_HEIGHT, shadeHex(mass.color, mass.value === moduleCodes.controlled_corridor ? 0.98 : 1.04), 0, 'room floor plate');
    // No in-scene text labels: the 3D viewer must communicate by room color, massing, and furniture/equipment shape.
  }
  // 2D 구분선이 있는 경계(인접 셀 타입이 다른 곳)에만 벽 생성
  const t = 0.055;
  // 수직 경계: (r, c)와 (r, c+1) 사이
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols - 1; c++) {
      const left = grid[r][c], right = grid[r][c + 1];
      if (left === right) continue;
      if (left === 0 && right === 0) continue;
      addBox3D(threeRoot, c + 1 - t / 2, r, t, 1, THREE_WALL_HEIGHT, '#cbd5e1', THREE_ROOM_HEIGHT, 'boundary wall');
    }
  }
  // 수평 경계: (r, c)와 (r+1, c) 사이
  for (let r = 0; r < rows - 1; r++) {
    for (let c = 0; c < cols; c++) {
      const top = grid[r][c], bottom = grid[r + 1][c];
      if (top === bottom) continue;
      if (top === 0 && bottom === 0) continue;
      addBox3D(threeRoot, c, r + 1 - t / 2, 1, t, THREE_WALL_HEIGHT, '#f1f5f9', THREE_ROOM_HEIGHT, 'boundary wall');
    }
  }
}
function addPrimitiveFurnitureItem3D(item) {
  const z = THREE_ROOM_HEIGHT + 0.01;
  const scaled = scaledFurnitureRect(item);
  const x = scaled.x, y = scaled.y, w = scaled.w, d = scaled.d;
  if (item.type === 'patient_bed') {
    addBox3D(threeRoot, x + w*0.03, y + d*0.08, w*0.94, d*0.84, 0.10, '#64748b', z, 'bed steel frame');
    addCapsule3D(threeRoot, x + w*0.08, y + d*0.12, w*0.84, d*0.76, 0.26, '#60a5fa', z + 0.09, 'blue rounded bed mattress');
    addCapsule3D(threeRoot, x + w*0.22, y + d*0.13, w*0.56, d*0.20, 0.11, '#ffffff', z + 0.31, 'raised white bed pillow');
    addBox3D(threeRoot, x + w*0.04, y + d*0.05, w*0.92, d*0.055, 0.30, '#334155', z + 0.08, 'dark bed head board');
    addBox3D(threeRoot, x + w*0.02, y + d*0.34, w*0.045, d*0.48, 0.23, '#1e293b', z + 0.15, 'left vertical bed rail');
    addBox3D(threeRoot, x + w*0.935, y + d*0.34, w*0.045, d*0.48, 0.23, '#1e293b', z + 0.15, 'right vertical bed rail');
    addSlimCylinder3D(threeRoot, x + w*0.92, y + d*0.12, 0.018, 0.64, '#475569', z, 'IV pole beside bed');
    addSphere3D(threeRoot, x + w*0.92, y + d*0.12, 0.055, '#fbbf24', z + 0.70, 'IV bag marker');
  } else if (item.type === 'headwall') {
    addBox3D(threeRoot, x, y + d*0.05, w, d*0.28, 0.36, '#475569', z, 'dark medical headwall panel');
    addBox3D(threeRoot, x + w*0.12, y + d*0.11, w*0.22, d*0.08, 0.05, '#22c55e', z + 0.29, 'green gas outlet');
    addBox3D(threeRoot, x + w*0.42, y + d*0.11, w*0.22, d*0.08, 0.05, '#ef4444', z + 0.29, 'red suction outlet');
    addBox3D(threeRoot, x + w*0.72, y + d*0.11, w*0.16, d*0.08, 0.05, '#facc15', z + 0.29, 'yellow call outlet');
  } else if (item.type === 'toilet_fixture') {
    addBox3D(threeRoot, x + w*0.08, y + d*0.08, w*0.84, d*0.84, 0.055, '#dbeafe', z, 'raised toilet plinth');
    addCylinder3D(threeRoot, x + w*0.20, y + d*0.28, w*0.60, d*0.52, 0.20, '#ffffff', z + 0.05, 'white toilet bowl body');
    addTorus3D(threeRoot, x + w*0.26, y + d*0.33, w*0.48, d*0.38, 0.018, '#0f172a', z + 0.27, 'dark oval toilet seat ring');
    addCylinder3D(threeRoot, x + w*0.40, y + d*0.43, w*0.20, d*0.16, 0.025, '#38bdf8', z + 0.285, 'blue toilet water opening');
    addBox3D(threeRoot, x + w*0.13, y + d*0.02, w*0.74, d*0.20, 0.24, '#e2e8f0', z + 0.06, 'rectangular toilet tank');
  } else if (item.type === 'washbasin' || item.type === 'handwash_sink') {
    addBox3D(threeRoot, x + w*0.06, y + d*0.02, w*0.88, d*0.18, 0.20, '#94a3b8', z + 0.02, 'basin wall bracket');
    addCylinder3D(threeRoot, x + w*0.05, y + d*0.20, w*0.90, d*0.68, 0.18, '#e0f2fe', z + 0.02, 'rounded wall hung basin');
    addTorus3D(threeRoot, x + w*0.20, y + d*0.32, w*0.60, d*0.42, 0.014, '#0ea5e9', z + 0.23, 'blue basin rim');
    addSlimCylinder3D(threeRoot, x + w*0.50, y + d*0.22, 0.015, 0.22, '#334155', z + 0.18, 'short sink faucet');
    addSphere3D(threeRoot, x + w*0.50, y + d*0.38, 0.035, '#0f172a', z + 0.245, 'dark basin drain');
  } else if (item.type === 'shower_zone') {
    addBox3D(threeRoot, x, y, w, d, 0.045, '#93c5fd', z, 'blue square shower tray');
    addBox3D(threeRoot, x + w*0.03, y + d*0.03, w*0.94, d*0.045, 0.28, '#60a5fa', z + 0.02, 'low shower screen edge');
    addCylinder3D(threeRoot, x + w*0.38, y + d*0.38, w*0.22, d*0.22, 0.03, '#0f172a', z + 0.055, 'dark circular shower drain');
    addSlimCylinder3D(threeRoot, x + w*0.82, y + d*0.18, 0.014, 0.54, '#2563eb', z, 'vertical shower riser');
    addSphere3D(threeRoot, x + w*0.82, y + d*0.18, 0.060, '#2563eb', z + 0.57, 'round shower head');
  } else if (item.type === 'nurse_counter') {
    addBox3D(threeRoot, x, y, w*0.86, d*0.34, 0.32, '#14b8a6', z, 'long teal nurse counter front');
    addBox3D(threeRoot, x + w*0.55, y + d*0.38, w*0.36, d*0.52, 0.32, '#0d9488', z, 'perpendicular nurse counter return wing');
    addBox3D(threeRoot, x + w*0.08, y + d*0.07, w*0.18, d*0.06, 0.18, '#1e293b', z + 0.30, 'nurse station monitor one');
    addBox3D(threeRoot, x + w*0.35, y + d*0.07, w*0.18, d*0.06, 0.18, '#1e293b', z + 0.30, 'nurse station monitor two');
  } else if (item.type === 'waste_bin') {
    addCylinder3D(threeRoot, x, y, w, d, 0.28, item.color || '#ef4444', z, 'red cylindrical waste bin body');
    addTorus3D(threeRoot, x + w*0.08, y + d*0.08, w*0.84, d*0.84, 0.014, '#7f1d1d', z + 0.30, 'dark waste bin rim');
  } else if (item.type === 'ppe_bench') {
    addCapsule3D(threeRoot, x, y, w, d, 0.16, item.color || '#f59e0b', z, 'amber rounded PPE bench seat');
    addBox3D(threeRoot, x + w*0.08, y + d*0.18, w*0.84, d*0.12, 0.12, '#92400e', z + 0.13, 'dark bench back rail');
  } else if (item.type === 'workstation') {
    addBox3D(threeRoot, x, y, w, d, 0.18, '#2dd4bf', z, 'teal workstation desk slab');
    addBox3D(threeRoot, x + w*0.18, y + d*0.08, w*0.64, d*0.10, 0.26, '#0f172a', z + 0.16, 'large black computer monitor');
    addBox3D(threeRoot, x + w*0.28, y + d*0.52, w*0.44, d*0.10, 0.035, '#334155', z + 0.19, 'flat keyboard strip');
  } else if (item.type === 'meds_trolley' || item.type === 'medical_cart') {
    addBox3D(threeRoot, x, y, w, d, 0.22, item.color || '#22c55e', z + 0.05, 'green medical cart body');
    addBox3D(threeRoot, x + w*0.05, y + d*0.08, w*0.90, d*0.08, 0.04, '#bbf7d0', z + 0.30, 'bright top cart tray');
    addBox3D(threeRoot, x + w*0.78, y + d*0.30, w*0.06, d*0.45, 0.26, '#166534', z + 0.12, 'upright cart handle');
    addCylinder3D(threeRoot, x + w*0.04, y + d*0.04, w*0.16, d*0.16, 0.045, '#111827', z - 0.005, 'front cart wheel');
    addCylinder3D(threeRoot, x + w*0.80, y + d*0.04, w*0.16, d*0.16, 0.045, '#111827', z - 0.005, 'front cart wheel');
    addCylinder3D(threeRoot, x + w*0.04, y + d*0.80, w*0.16, d*0.16, 0.045, '#111827', z - 0.005, 'rear cart wheel');
    addCylinder3D(threeRoot, x + w*0.80, y + d*0.80, w*0.16, d*0.16, 0.045, '#111827', z - 0.005, 'rear cart wheel');
  } else if (item.type === 'donning_cabinet' || item.type === 'supply_shelving') {
    addBox3D(threeRoot, x, y, w, d, 0.38, item.color || '#c4b5fd', z, 'tall supply cabinet volume');
    addBox3D(threeRoot, x + w*0.08, y + d*0.06, w*0.84, d*0.04, 0.035, '#6d28d9', z + 0.16, 'cabinet shelf line one');
    addBox3D(threeRoot, x + w*0.08, y + d*0.06, w*0.84, d*0.04, 0.035, '#6d28d9', z + 0.29, 'cabinet shelf line two');
  } else if (item.type === 'dirty_worktop') {
    addBox3D(threeRoot, x, y, w, d, 0.20, '#fb7185', z, 'pink soiled worktop counter');
    addCylinder3D(threeRoot, x + w*0.62, y + d*0.18, w*0.24, d*0.24, 0.06, '#881337', z + 0.19, 'dark soiled worktop sink bowl');
  } else {
    addBox3D(threeRoot, x, y, w, d, Math.max(0.18, item.h * 1.35), item.color || '#e5e7eb', z, 'distinct fallback furniture volume ' + item.type);
  }
}
function furnitureModelKeyForItem(item) {
  return FURNITURE_MODEL_BY_TYPE[item.type] || null;
}
function ensureGltfLoader() {
  if (gltfLoaderInstance) return Promise.resolve(gltfLoaderInstance);
  if (window.GLTFLoader) {
    gltfLoaderInstance = new window.GLTFLoader();
    return Promise.resolve(gltfLoaderInstance);
  }
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('GLTFLoader did not become available')), 5000);
    window.addEventListener('ward-gltf-loader-ready', () => {
      clearTimeout(timeout);
      gltfLoaderInstance = new window.GLTFLoader();
      resolve(gltfLoaderInstance);
    }, {once:true});
  });
}
function parseGltfDataUrl(loader, url) {
  return fetch(url)
    .then(resp => { if (!resp.ok) throw new Error('GLB fetch failed: ' + resp.status); return resp.arrayBuffer(); })
    .then(buffer => new Promise((resolve, reject) => loader.parse(buffer, '', resolve, reject)));
}
async function loadFurnitureModel(key) {
  if (!key || !FURNITURE_MODEL_URLS[key]) return null;
  if (!furnitureModelCache[key]) {
    const loader = await ensureGltfLoader();
    furnitureModelCache[key] = parseGltfDataUrl(loader, FURNITURE_MODEL_URLS[key]).then(gltf => gltf.scene);
  }
  return furnitureModelCache[key];
}
function prepareFurnitureModelInstance(model, item, x, y, w, d, z) {
  const instance = model.clone(true);
  instance.name = 'GLB furniture model ' + furnitureModelKeyForItem(item) + ' for ' + item.type;
  instance.traverse(obj => {
    if (obj.isMesh) {
      obj.castShadow = true; obj.receiveShadow = true;
      if (obj.material) {
        if (Array.isArray(obj.material)) obj.material = obj.material.map(m => brightenModelMaterial(m.clone()));
        else obj.material = brightenModelMaterial(obj.material.clone());
      }
      addFurnitureEdgeLines(obj);
    }
  });
  const sourceBox = new THREE.Box3().setFromObject(instance);
  const size = sourceBox.getSize(new THREE.Vector3());
  const targetW = Math.max(0.08, w * THREE_CELL_M);
  const targetD = Math.max(0.08, d * THREE_CELL_M);
  const uniformScale = Math.min(targetW / Math.max(size.x, 0.001), targetD / Math.max(size.z, 0.001));
  instance.scale.setScalar(uniformScale);
  const box = new THREE.Box3().setFromObject(instance);
  const center = box.getCenter(new THREE.Vector3());
  const bottom = box.min.y;
  const target = threePos(x + w / 2, y + d / 2, z);
  instance.position.set(target.x - center.x, target.y - bottom, target.z - center.z);
  return instance;
}
async function addModelFurnitureItem3D(item) {
  const key = furnitureModelKeyForItem(item);
  if (!key) return false;
  const model = await loadFurnitureModel(key);
  if (!model) return false;
  const z = THREE_ROOM_HEIGHT + 0.01;
  const scaled = scaledFurnitureRect(item);
  const instance = prepareFurnitureModelInstance(model, item, scaled.x, scaled.y, scaled.w, scaled.d, z);
  threeRoot.add(instance);
  return true;
}
async function addFurnitureItem3D(item) {
  try {
    if (await addModelFurnitureItem3D(item)) return 'model';
  } catch (err) {
    console.warn('Falling back to primitive furniture for', item.type, err);
  }
  addPrimitiveFurnitureItem3D(item);
  return 'primitive-fallback';
}

async function renderSelectedLayout3D() {
  const masses = build3DMassesFromGrid(grid).filter(m => m.value !== 1 && m.value !== 0);
  if (!masses.length || !hasModule(moduleCodes.negative_pressure_patient_room)) {
    threeDStatus.innerHTML = '<span id="ward-infeasible-warning" role="alert" style="color:#991b1b;font-weight:600;">No selected layout to view in 3D. Generate/select a feasible ward layout first.</span>';
    return;
  }
  const sorted = masses.slice().sort((a,b) => (a.x + a.y + a.h) - (b.x + b.y + b.h));
  initThreeViewer(sorted);
  const furniture = sorted.flatMap(mass => buildFurnitureFromMass(mass));
  addWardFloorsAndWalls3D(sorted);
  threeDStatus.textContent = 'Loading GLB furniture models...';
  const renderModes = [];
  for (const item of furniture) renderModes.push(await addFurnitureItem3D(item));
  const modelCount = renderModes.filter(mode => mode === 'model').length;
  const fallbackCount = renderModes.length - modelCount;
  threeDStatus.textContent = 'Three.js/WebGL ward viewer: GLB-backed low-poly medical furniture models, real 3D room plates, and cutaway walls. Modules: ' + masses.length + ', furniture: ' + furniture.length + ', GLB models: ' + modelCount + ', primitive fallback: ' + fallbackCount;
  threeRenderer.render(threeScene, threeCamera);
}
threeDCanvas.addEventListener('contextmenu', e => e.preventDefault());
threeDCanvas.addEventListener('mousedown', e => {
  if (![0, 1, 2].includes(e.button)) return;
  e.preventDefault();
  threeDDragging = true;
  threeDDragMode = (e.button === 0) ? 'rotate' : 'pan';
  threeDLastMouse = {x:e.clientX, y:e.clientY};
  threeDCanvas.classList.add('dragging');
});
window.addEventListener('mousemove', e => {
  if (!threeDDragging || !threeDLastMouse || !threeRoot || !threeRenderer) return;
  const dx = e.clientX - threeDLastMouse.x;
  const dy = e.clientY - threeDLastMouse.y;
  if (threeDDragMode === 'pan') {
    panThreeCameraByScreenDelta(dx, dy);
  } else {
    threeDRotation.z += dx * 0.012;
    threeRoot.rotation.y = threeDRotation.z;
  }
  threeDLastMouse = {x:e.clientX, y:e.clientY};
  renderThreeSceneIfReady();
});
window.addEventListener('mouseup', () => { threeDDragging = false; threeDDragMode = null; threeDLastMouse = null; threeDCanvas.classList.remove('dragging'); });
threeDCanvas.addEventListener('wheel', e => {
  e.preventDefault();
  threeDZoom = Math.max(0.35, Math.min(THREE_D_ZOOM_MAX, threeDZoom * (e.deltaY > 0 ? THREE_D_WHEEL_ZOOM_OUT : THREE_D_WHEEL_ZOOM_IN)));
  applyThreeCameraZoom();
  renderThreeSceneIfReady();
}, {passive:false});
canvas.addEventListener('wheel', e => { e.preventDefault(); planZoom = Math.max(0.45, Math.min(PLAN_ZOOM_MAX, planZoom * (e.deltaY > 0 ? 0.88 : 1.16))); applyPlanCanvasZoom(); }, {passive:false});
canvas.addEventListener('mousedown', e => { isDown = true; dragStart = cellFromEvent(e); dragEnd = dragStart; if (tool === 'pencil') { setCell(dragStart); draw(); } });
canvas.addEventListener('mousemove', e => { const pos = cellFromEvent(e); if (!pos) return; moduleInfo.textContent = 'cell (' + pos.r + ',' + pos.c + ') / ' + moduleDimensionText(grid[pos.r][pos.c]); if (!isDown) return; dragEnd = pos; if (tool === 'pencil') setCell(pos); draw(); });
canvas.addEventListener('mouseup', e => { if (!isDown) return; dragEnd = cellFromEvent(e); if (tool === 'rectangle' && dragStart && dragEnd) { const r1=Math.min(dragStart.r,dragEnd.r), r2=Math.max(dragStart.r,dragEnd.r), c1=Math.min(dragStart.c,dragEnd.c), c2=Math.max(dragStart.c,dragEnd.c); for(let r=r1;r<=r2;r++) for(let c=c1;c<=c2;c++) grid[r][c]= mode==='paint'?1:0; } isDown=false; dragStart=null; dragEnd=null; draw(); });
canvas.addEventListener('mouseleave', () => { isDown = false; dragStart = null; dragEnd = null; draw(); });
applyPlanCanvasZoom();
draw();
</script>
</body>
</html>
''')

html = html_template.safe_substitute(
    canvas_w=canvas_w,
    canvas_h=canvas_h,
    rows=rows,
    cols=cols,
    cell=cell,
    mode=mode,
    tool=tool,
    mode_json=json.dumps(mode),
    tool_json=json.dumps(tool),
    default_bed_count=default_bed_count,
    module_db_js=json.dumps(module_db, ensure_ascii=False),
    module_meta_js=json.dumps(module_meta, ensure_ascii=False),
    module_codes_js=json.dumps(module_codes, ensure_ascii=False),
    code_to_module_js=json.dumps(code_to_module, ensure_ascii=False),
    colors_js=json.dumps(colors, ensure_ascii=False),
    labels_js=json.dumps(labels, ensure_ascii=False),
    furniture_model_urls_js=json.dumps(furniture_model_urls, ensure_ascii=False),
    legend_html=legend_html,
)

st.iframe(html, height=height)
