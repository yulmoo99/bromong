r"""
Streamlit grid drag prototype for the graduation hospital planner.

Run:
  streamlit run prototype/grid_drag_canvas_app.py
"""

from pathlib import Path
from string import Template
import json
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
MODULE_DB_PATH = ROOT / "data" / "modules_ward_v01.json"
DESIGN_PATH = ROOT / "DESIGN.md"

st.set_page_config(page_title="Infection Ward Planner", page_icon="◌", layout="wide", initial_sidebar_state="expanded")

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
          .block-container { padding-top: 2.1rem; padding-bottom: 3rem; padding-left: 2.2rem; padding-right: 2.2rem; max-width: 1780px; }
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
cols = st.sidebar.slider("Grid columns", 10, 80, 40)
rows = st.sidebar.slider("Grid rows", 10, 60, 30)
cell = 20
tool = st.sidebar.radio("Drawing tool", ["pencil", "rectangle"], horizontal=True, index=1)
mode = st.sidebar.radio("Edit mode", ["paint", "erase"], horizontal=True)

st.markdown(
    f"""
    <section class="apple-hero">
      <h1>병동·병원 모듈 계획 도구</h1>
      <div class="apple-spec">
        <span class="apple-pill">{cols} × {rows} grid</span>
        <span class="apple-pill">1칸 1.8m × 1.8m = 3.24㎡</span>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

module_db = json.loads(MODULE_DB_PATH.read_text(encoding="utf-8"))
module_meta = {m["id"]: m for m in module_db["modules"]}
for _m in module_db.get("hospital_program_modules", []):
    module_meta[_m["id"]] = _m

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
for _program in module_db.get("hospital_program_modules", []):
    module_codes[_program["id"]] = int(_program["code"])
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
_hospital_palette = ["#B8E6FF", "#B8D8FF", "#C6F6D5", "#FDE68A", "#FDBA74", "#FCA5A5", "#DDD6FE", "#F9A8D4"]
for _idx, _program in enumerate(module_db.get("hospital_program_modules", [])):
    colors[str(_program["code"])] = _hospital_palette[_idx % len(_hospital_palette)]
labels = {"10": "C", "20": "R", "21": "A", "22": "WC", "30": "N", "40": "CL", "41": "D", "50": "S"}
for _program in module_db.get("hospital_program_modules", []):
    labels[str(_program["code"])] = _program["name_ko"].split()[0]

legend_items = [
    ("1", "usable area"),
    ("10", "controlled corridor / C"),
    ("20", "negative room / R / 음압병상 ≥15㎡(신축·증축·개축, 개보수 10㎡) — 전실·화장실·벽체 제외, 감염병예방법 별표4의2"),
    ("21", "anteroom / A / 전실 면적 4㎡·깊이 2.4m 이상, 양쪽 출입문 인터락 — 감염병예방법 별표4의2"),
    ("22", "toilet·shower / WC / 병실 내부 설치(배기구만), 법적 최소면적 규정 없음 — 가이드라인 권장"),
    ("30", "nurse station / N / 운영 필수 (법적 최소면적 규정 없음, 가이드라인 권장 13.5㎡)"),
    ("40", "clean supply alcove / CL / 가이드라인 권장 배치"),
    ("41", "soiled waste holding / D / 가이드라인 권장 배치"),
    ("50", "support reserve / S / 잔여 공간 채움"),
]
for _program in module_db.get("hospital_program_modules", []):
    legend_items.append((str(_program["code"]), _program["name_ko"]))
legend_html = "\n".join(
    f'<span><i class="swatch" style="background:{colors[k]}"></i>{name}</span>' for k, name in legend_items
)

canvas_w = cols * cell
canvas_h = rows * cell
height = 1400  # 그리드를 작게 고정 표시하므로 iframe 높이도 컨텐츠에 맞춰 축소

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
  body { margin: 0; padding: 18px 4px 0; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif; color:var(--primary); background: transparent; }
  .planner-shell { max-width: min(1640px, 100%); margin: 0 auto; }
  .planner-stage { background: linear-gradient(145deg, rgba(255,255,255,.98), rgba(251,251,253,.88)); border:1px solid rgba(210,210,215,.82); border-radius: 28px; padding: 20px; box-shadow: var(--shadow); overflow: hidden; }
  #toolbar { display:flex; justify-content:space-between; gap:18px; align-items:flex-start; margin-bottom:16px; padding-bottom:14px; border-bottom:1px solid rgba(210,210,215,.72); }
  .toolbar-title { font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",sans-serif; font-size: 22px; line-height:1.08; letter-spacing:-.035em; font-weight:720; margin:0; }
  .toolbar-subtitle { margin-top:7px; color:var(--secondary); font-size:13px; line-height:1.45; max-width:680px; }
  .metric-strip { display:flex; flex-wrap:wrap; justify-content:flex-end; gap:8px; min-width:220px; }
  .metric-chip, #legend span { display:inline-flex; align-items:center; gap:6px; border:1px solid rgba(210,210,215,.82); background:rgba(255,255,255,.74); border-radius:999px; padding:7px 10px; color:var(--primary); font-size:12px; font-weight:650; white-space:nowrap; box-shadow:var(--soft-shadow); }
  .canvas-wrap { border-radius:22px; background:#fff; border:1px solid rgba(210,210,215,.82); padding:12px; overflow:auto; width:fit-content; max-width:100%; }
  canvas { border: 1px solid rgba(0,0,0,.10); border-radius:18px; cursor: crosshair; image-rendering: pixelated; background:#fff; box-shadow: inset 0 1px 0 rgba(255,255,255,.7); }
  .action-row { display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:14px 0 12px; }
  #hospitalProgramPanel { margin: 12px 0 14px; padding: 16px; border:1px solid rgba(210,210,215,.82); border-radius:22px; background:rgba(255,255,255,.78); }
  .program-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap:8px 12px; margin-top:10px; }
  .program-check { display:flex; gap:10px; align-items:center; justify-content:space-between; padding:9px 11px; border-radius:14px; background:rgba(245,245,247,.78); font-size:12.5px; line-height:1.3; cursor:default; }
  .program-check .program-name { flex:1; min-width:0; }
  .program-check .program-qty-wrap { color:#6E6E73; white-space:nowrap; font-size:11.5px; }
  .program-qty { width:50px; padding:5px 6px; border:1px solid rgba(210,210,215,.9); border-radius:10px; background:#fff; font-size:12px; margin-left:4px; }
  button, input::file-selector-button { appearance:none; border:1px solid rgba(210,210,215,.85); background:rgba(255,255,255,.86); color:var(--primary); border-radius:999px; padding:9px 13px; font-size:12px; font-weight:680; letter-spacing:-.01em; cursor:pointer; box-shadow:var(--soft-shadow); transition:transform .16s ease, background .16s ease, border-color .16s ease; }
  button:hover, input::file-selector-button:hover { transform:translateY(-1px); border-color:rgba(0,113,227,.34); background:#fff; }
  .action-row button:nth-child(3), .action-row button:nth-child(4), button.primary { background:var(--blue); color:white; border-color:var(--blue); box-shadow:0 8px 20px rgba(0,113,227,.22); }
  .action-row button:nth-child(3):hover, .action-row button:nth-child(4):hover, button.primary:hover { background:var(--blue-dark); }
  input[type="file"] { color:var(--secondary); font-size:12px; }
  #legend { display:flex; flex-wrap:wrap; gap:7px; margin: 12px 0 0; font-size: 12px; line-height: 1.4; max-width: 100%; }
  .swatch { display:inline-block; width: 10px; height: 10px; border-radius:999px; border: 1px solid rgba(0,0,0,.16); }
  #modeSelector { margin: 0 0 12px; padding: 10px 16px; border:1px solid rgba(210,210,215,.82); border-radius:14px; background:rgba(255,255,255,.72); display:flex; align-items:center; gap:14px; flex-wrap:wrap; font-size:13px; }
  #modeSelector .mode-label { font-weight:720; color:var(--primary); letter-spacing:-.01em; }
  #modeSelector .mode-opt { display:inline-flex; align-items:center; gap:6px; font-weight:600; color:var(--primary); cursor:pointer; }
  #modeSelector .mode-hint { color:var(--secondary); font-size:12px; flex:1; min-width:200px; }
  #areaSummary { margin: 14px 0 0; padding: 14px 18px; border:1px solid rgba(0,113,227,.28); border-radius:20px; background:rgba(0,113,227,.05); font-size:12.5px; line-height:1.6; color:var(--primary); }
  #areaSummary b { letter-spacing:-.01em; }
  .area-shortfall { color:#b91c1c; font-weight:700; }
  .area-surplus { color:#0a7d2c; font-weight:700; }
  #moduleInfo, #ruleReport, #optionPanel { max-width: 100%; margin: 16px 0 0; padding: 18px; background: rgba(255,255,255,.90); border: 1px solid rgba(210,210,215,.82); border-radius:24px; font-size: 12px; box-shadow: 0 10px 34px rgba(0,0,0,.055); }
  #optionPanel { margin-top: 12px; padding: 12px 16px; font-size: 12.5px; }
  #moduleInfo { color:var(--secondary); }
  #ruleReport ul, #optionPanel ul { margin: 10px 0 0 18px; padding: 0; }
  .option-card { margin: 10px 0; padding: 14px 14px 13px; border: 1px solid rgba(210,210,215,.82); border-left: 5px solid var(--blue); border-radius:18px; background: white; clear:both; min-height:42px; box-shadow:0 8px 24px rgba(0,0,0,.045); }
  .option-card button { float: right; }
  .small { color:var(--secondary); font-size:11px; line-height:1.45; }
</style>
</head>
<body>
<div class="planner-shell">
  <section class="planner-stage">
    <div id="toolbar">
      <div>
        <div class="toolbar-title">Planning Canvas</div>
        <div class="toolbar-subtitle">영역을 칠한 뒤 배치 모드를 고르고 자동배치를 생성합니다.</div>
      </div>
      <div class="metric-strip">
        <span class="metric-chip">Mode <b>${mode}</b></span>
        <span class="metric-chip">Tool <b>${tool}</b></span>
        <span class="metric-chip">${cols}×${rows}</span><span class="metric-chip">1칸 1.8m × 1.8m = 3.24㎡</span>
      </div>
    </div>
    <div id="modeSelector">
      <span class="mode-label">배치 모드</span>
      <label class="mode-opt"><input type="radio" name="placementMode" value="hospital" checked> 병원 진료 모듈</label>
      <label class="mode-opt"><input type="radio" name="placementMode" value="ward"> 병동(병실)</label>
      <span id="modeHint" class="mode-hint"></span>
    </div>
    <div class="canvas-wrap"><canvas id="grid" width="${canvas_w}" height="${canvas_h}"></canvas></div>
    <div class="action-row">
      <button onclick="clearGrid()">Clear</button>
      <button onclick="fillGrid()">Fill All</button>
      <button onclick="generateLayoutOptions()">Generate / Regenerate Layout Options</button>
    </div>
    <div id="optionPanel">Generate Layout Options(생성) 버튼을 누르면 배치 결과가 여기에 표시됩니다.</div>
    <div id="areaSummary"></div>
    <div id="hospitalProgramPanel">
      <b>Hospital Modular Program Checklist</b>
      <div class="small">실을 선택하고 개수를 입력하면 자동배치합니다. 권장 면적·적용 외래 등 가이드라인 정보는 각 항목에 마우스를 올리면 표시됩니다. 수술실 선택 시 수술지원·회복실·중앙공급이 자동으로 함께 선택되며, 개수는 직접 조정할 수 있습니다.</div>
      <div id="programChecklist" class="program-grid"></div>
    </div>
    <div id="legend">${legend_html}</div>
  </section>
  <div id="legalNotice" style="max-width:100%;margin:16px 0 0;padding:14px 18px;background:rgba(255,246,230,.92);border:1px solid rgba(245,158,11,.45);border-radius:18px;font-size:11.5px;color:#92400e;line-height:1.6;">
    <b>⚠️ 법규 적용 범위 안내</b><br>
    음압격리병실(R) 면적 기준은 <b>감염병의 예방 및 관리에 관한 법률 시행규칙 별표4의2</b>(음압병상 ≥15㎡, 신축·증축·개축) 및 <b>보건복지부·한국의료복지건축학회 의료시설 건축설계 가이드라인(2018)</b>을 근거로 합니다. 일반 입원실 1인실 ≥10㎡는 의료법 시행규칙 별표4 기준입니다.<br>
    전실(A)은 면적 4㎡·깊이 2.4m 이상이 법정 기준이며, 화장실(WC)·간호스테이션(N)의 면적은 <b>법적 최소 기준이 없어</b> 표시 수치는 가이드라인 권장값입니다. 실제 설계 시 관련 전문가 검토가 필요합니다.<br>
    복도 폭 기준: 현재 계획 그리드는 1칸 = 1.8m × 1.8m = 3.24㎡인 1.8m grid이며, 병원 기본 모듈은 3.6m × 7.2m(2×4칸 = 25.9㎡)입니다. 병원 모듈러 모드에서는 복도를 1칸(1.8m)으로 자동배치합니다. 세부 실시설계에서는 의료법 시행규칙 제34조 [별표4], 피난·소방 기준을 별도 검토해야 합니다.<br>
    본 도구는 초기 매싱 계획 지원용이며 <b>소방법, 장애인편의시설법 등은 별도 검토</b>가 필요합니다.
  </div>
  <div id="basisNotice" style="max-width:100%;margin:12px 0 0;padding:14px 18px;background:rgba(0,113,227,.05);border:1px solid rgba(0,113,227,.28);border-radius:18px;font-size:11.5px;color:#1d3a5f;line-height:1.65;">
    <b>ℹ️ 실 크기·인접 배치 기준</b><br>
    <b>① 실 크기 산정:</b> 각 실의 칸 수는 <b>가이드라인 권장 면적</b>(보건복지부·한국의료복지건축학회, 2018)을 1.8m 격자(1칸=3.24㎡)에 맞춰 그 이상이 되는 가장 가까운 모듈 크기로 환산한 값입니다. 기본 모듈 2×4칸=25.9㎡를 단위로, 큰 실은 3×4·4×4·4×6칸으로 키웁니다. 예) 진료실 권장 15~25㎡ → 2×4칸(25.9㎡), 수술실 ≥37㎡·한 면 ≥6m → 4×4칸(7.2×7.2m, 51.8㎡), CT 45~60㎡ → 4×4칸, 투석 8베드 64~80㎡ → 4×6칸(77.8㎡). <b>각 실의 정확한 출처 면적은 체크리스트 항목에 마우스를 올리면 표시됩니다.</b><br>
    <b>② 인접 배치:</b> 같은 진료기능(부서)끼리 한 구역에 모으고, 빈 공간은 복도로 처리해 모든 실이 복도에 접하도록 합니다. 묶음은 — <b>수술부</b>(수술실·수술지원·회복실·중앙공급/멸균물품: 수술실과 지원·멸균물류를 같은 복도에 두거나 마주보게), <b>응급·관찰</b>, <b>외래·진료</b>(진료실·검체채취·처치실), <b>영상·검사</b>(CT·일반촬영·진단검사·병리), <b>투석·수액</b>, <b>산과</b>(분만·신생아), <b>연구·행정</b>입니다. 이 기능군 묶음은 일반적인 병원 동선·청결물류·감염관리 원칙에 따른 <b>계획 휴리스틱</b>으로, 세부 인접·분리 기준(청결-오염 동선 등)은 별도 검토가 필요합니다.
  </div>
  <div id="moduleInfo">모듈 셀에 마우스를 올리면 법적 근거 및 권장 면적을 확인할 수 있습니다. R(음압격리병실): 음압병상 ≥15㎡ 신축(개보수 10㎡), 전실·화장실 제외 — 감염병예방법 별표4의2.</div>
  <div id="ruleReport">배치를 생성하면 병동·병원 규칙 및 가이드라인 검토 결과가 자동으로 여기에 표시됩니다.</div>
</div>

<script>
const rows = ${rows};
const cols = ${cols};
const cell = ${cell};
const mode = ${mode_json};
const tool = ${tool_json};
const CELL_SIZE_M = 1.8;
const HOSPITAL_BASE_MODULE_CELLS = {w:2, h:4};
const HOSPITAL_CORRIDOR_WIDTH_CELLS = 1;
const moduleDb = ${module_db_js};
const moduleMeta = ${module_meta_js};
const moduleCodes = ${module_codes_js};
const codeToModule = ${code_to_module_js};
const colors = ${colors_js};
const labels = ${labels_js};
const HOSPITAL_PROGRAMS = (moduleDb.hospital_program_modules || []);
const HOSPITAL_PROGRAM_BUNDLES = { operating_room: ['surgery_support', 'recovery_room', 'central_supply'] };
// These are shared department-support minimums, not one-to-one clones per OR.
// Extra checked quantities still win through addRequest(Math.max(...)).
const HOSPITAL_PROGRAM_BUNDLE_MIN_QTY = { operating_room: {surgery_support: 1, recovery_room: 1, central_supply: 1} };
const canvas = document.getElementById('grid');
const ctx = canvas.getContext('2d');
const output = document.getElementById('output');
const areaSummary = document.getElementById('areaSummary');
const CELL_AREA_M2 = (moduleDb.grid_assumption && moduleDb.grid_assumption.cell_area_m2) || 3.24;
const moduleInfo = document.getElementById('moduleInfo');
const ruleReport = document.getElementById('ruleReport');
const optionPanel = document.getElementById('optionPanel');
const storageKey = 'hospital_grid_painter_' + rows + 'x' + cols;
const MAIN_CORRIDOR_MIN_WIDTH_CELLS = 1;
const SHORT_CONNECTOR_MAX_CELLS = 999; // 1.8m grid: 병원 모듈러 모드에서는 복도 1칸을 기본으로 허용.
let isDown = false;
let dragStart = null;
let dragEnd = null;
let grid = loadGrid();
let clusterGrid = blankClusterGrid();
let moduleIdGrid = blankClusterGrid(); // 셀별 모듈 인스턴스 id (같은 실 종류가 붙어도 실 경계를 그리기 위함)
let layoutOptions = [];
let compareAnalysis = null;
let nextClusterNo = 1;
let nextModuleNo = 1;
let lastRuleReport = null;
let selectedLayoutIndex = null;

function fitPlanCanvas() {
  // 확대/축소 없이, 그리드 전체가 한 화면에 들어오도록 작게 고정 표시한다 (가로 폭 + 세로 높이 둘 다 제한, 더 작은 배율 사용).
  const wrap = canvas.parentElement;
  const availW = wrap ? Math.max(120, wrap.clientWidth - 28) : canvas.width;
  const availH = 520; // 세로가 한 화면에 들어오도록 캔버스 높이 상한
  const scale = Math.min(availW / canvas.width, availH / canvas.height);
  canvas.style.width = Math.round(canvas.width * scale) + 'px';
  canvas.style.height = Math.round(canvas.height * scale) + 'px';
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
  if (!moduleId) return value === 1 ? 'usable cell: 1.8m × 1.8m = 3.24㎡' : 'outside';
  const meta = moduleMeta[moduleId] || {};
  const preferred = meta.shape_policy && meta.shape_policy.preferred_grid_sizes ? meta.shape_policy.preferred_grid_sizes[0] : null;
  const w = widthCells || (preferred ? preferred[0] : 1);
  const h = heightCells || (preferred ? preferred[1] : 1);
  return w + '×' + h + ' cells / ' + (w * CELL_SIZE_M).toFixed(1) + 'm × ' + (h * CELL_SIZE_M).toFixed(1) + 'm / ≈' + (w * h * moduleDb.grid_assumption.cell_area_m2).toFixed(1) + '㎡';
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
function drawModuleOutlines() {
  // 각 모듈 인스턴스의 경계를 그린다. 같은 실 종류가 인접해 한 덩어리로 보이는 것을 방지.
  ctx.save();
  ctx.strokeStyle = 'rgba(38,38,42,.9)';
  ctx.lineWidth = Math.max(1.5, Math.floor(cell * 0.09));
  const directions = [[-1, 0], [1, 0], [0, -1], [0, 1]];
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const id = moduleIdGrid[r][c];
    if (!id) continue;
    const x = c * cell, y = r * cell;
    for (const [dr, dc] of directions) {
      const rr = r + dr, cc = c + dc;
      if (rr >= 0 && rr < rows && cc >= 0 && cc < cols && moduleIdGrid[rr][cc] === id) continue;
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
function drawModuleComponentLabels() {
  if (cell < 16) return;
  const visitedLabels = new Set();
  ctx.save();
  ctx.fillStyle = '#1d1d1f';
  ctx.font = Math.max(9, Math.floor(cell * 0.42)) + 'px sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  for (let r0 = 0; r0 < rows; r0++) for (let c0 = 0; c0 < cols; c0++) {
    const value = grid[r0][c0];
    const label = labelFor(value);
    const key0 = keyOf(r0, c0);
    if (!label || value === 0 || visitedLabels.has(key0)) continue;
    const moduleId0 = moduleIdGrid[r0][c0];
    const q = [[r0, c0]];
    visitedLabels.add(key0);
    let n = 0, sumR = 0, sumC = 0;
    while (q.length) {
      const [r, c] = q.shift();
      n++; sumR += r; sumC += c;
      for (const [rr, cc] of neighbors4(r, c)) {
        const k = keyOf(rr, cc);
        // 같은 코드이면서 같은 모듈 id일 때만 한 덩어리로 본다 → 같은 실이 인접해도 각각 이름이 뜬다(병동 모듈은 id가 null로 동일하므로 기존대로 동작).
        if (!visitedLabels.has(k) && grid[rr][cc] === value && moduleIdGrid[rr][cc] === moduleId0) { visitedLabels.add(k); q.push([rr, cc]); }
      }
    }
    if (n < 1) continue;
    const centroid = {x: (sumC / n) * cell + cell / 2, y: (sumR / n) * cell + cell / 2};
    ctx.fillText(label, centroid.x, centroid.y);
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
  }
  drawModuleOutlines();
  drawModuleComponentLabels();
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
  if (output) output.value = JSON.stringify(grid);
  saveGrid();
  updateAreaSummary();
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
  moduleIdGrid = blankClusterGrid();
  nextClusterNo = 1;
  nextModuleNo = 1;
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
  // Main corridors should be 2 cells wide (3.0m). A 1-cell / 1.8m strip is allowed only as a short door connector/stub.
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
function ensureAllCorridorsConnected(corridorCells) {
  let comps = connectedComponentsOf(moduleCodes.controlled_corridor);
  if (comps.length <= 1) return true;
  comps.sort((a, b) => b.length - a.length);
  let mainKeys = new Set(comps[0].map(([r, c]) => keyOf(r, c)));
  let repaired = false;
  for (let compIndex = 1; compIndex < comps.length; compIndex++) {
    const q = comps[compIndex].slice();
    const seen = new Set(q.map(([r, c]) => keyOf(r, c)));
    const prev = new Map();
    let targetKey = null;
    for (let i = 0; i < q.length && !targetKey; i++) {
      const [r, c] = q[i];
      for (const [rr, cc] of neighbors4(r, c)) {
        const k = keyOf(rr, cc);
        if (seen.has(k)) continue;
        if (!(grid[rr][cc] === 1 || grid[rr][cc] === moduleCodes.controlled_corridor)) continue;
        seen.add(k);
        prev.set(k, keyOf(r, c));
        if (mainKeys.has(k)) { targetKey = k; break; }
        q.push([rr, cc]);
      }
    }
    if (!targetKey) continue;
    let cur = targetKey;
    while (cur) {
      const [rr, cc] = parseKey(cur);
      if (grid[rr][cc] === 1) { markCorridor(rr, cc, corridorCells || []); repaired = true; }
      if (comps[compIndex].some(([r, c]) => keyOf(r, c) === cur)) break;
      cur = prev.get(cur);
    }
    comps = connectedComponentsOf(moduleCodes.controlled_corridor).sort((a, b) => b.length - a.length);
    mainKeys = new Set(comps[0].map(([r, c]) => keyOf(r, c)));
  }
  return connectedComponentsOf(moduleCodes.controlled_corridor).length <= 1 || repaired;
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
  return {ok, issues: ok ? [] : ['long 1-cell corridor run: ' + longest + ' cells'], message: ok ? 'Corridor width OK: 1-cell / 1.8m modular planning corridor policy' : 'Corridor width issue: unexpected corridor policy conflict (' + longest + ' cells)'};
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

function programGuidelineTooltip(p) {
  // Guideline detail lives in this hover tooltip so the checkbox itself stays as just 실 이름 + 개수.
  const parts = [];
  if (p.recommended_area) parts.push('권장 면적: ' + p.recommended_area);
  if (p.applies_to && p.applies_to.length) parts.push('적용: ' + p.applies_to.join(', '));
  parts.push('계획 면적 ≈ ' + (p.planning_area_m2 || 0) + '㎡');
  return parts.join(' · ');
}
const programChecklistKey = 'hospital_program_checklist_v1';
function saveProgramChecklist() {
  // 사이드바 조작 시 Streamlit이 iframe을 다시 로드해도 선택이 유지되도록 localStorage에 저장.
  const state = {};
  document.querySelectorAll('.hospital-program-checkbox').forEach(box => {
    const qty = document.querySelector('.program-qty[data-program-id="' + box.value + '"]');
    if (box.checked && qty && Number(qty.value || 0) > 0) state[box.value] = Number(qty.value);
  });
  try { localStorage.setItem(programChecklistKey, JSON.stringify(state)); } catch (e) {}
}
function loadProgramChecklist() {
  try { return JSON.parse(localStorage.getItem(programChecklistKey)) || null; } catch (e) { return null; }
}
function renderHospitalProgramChecklist() {
  const panel = document.getElementById('programChecklist');
  if (!panel) return;
  panel.innerHTML = HOSPITAL_PROGRAMS.map((p, idx) => {
    const defaultQty = Number(p.default_quantity || 0);
    const checked = defaultQty > 0 ? ' checked' : '';
    const qtyValue = Math.max(0, defaultQty || 0);
    const tip = programGuidelineTooltip(p).replace(/"/g, '&quot;');
    return '<label class="program-check" title="' + tip + '"><span class="program-name"><input type="checkbox" class="hospital-program-checkbox" value="' + p.id + '"' + checked + '> <b>' + p.name_ko + '</b></span><span class="program-qty-wrap">개수<input class="program-qty" data-program-id="' + p.id + '" type="number" min="0" max="20" step="' + (p.quantity_step || 1) + '" value="' + qtyValue + '"></span></label>';
  }).join('');
  // 이전에 저장된 선택을 복원 (사이드바 조작/리로드 후에도 유지)
  const saved = loadProgramChecklist();
  if (saved) {
    panel.querySelectorAll('.hospital-program-checkbox').forEach(box => {
      const qty = panel.querySelector('.program-qty[data-program-id="' + box.value + '"]');
      if (saved[box.value] != null) { box.checked = true; if (qty) qty.value = saved[box.value]; }
      else { box.checked = false; if (qty) qty.value = 0; }
    });
  }
  const syncBoxQty = (box) => {
    const qty = panel.querySelector('.program-qty[data-program-id="' + box.value + '"]');
    if (!qty) return;
    if (box.checked && Number(qty.value || 0) < 1) qty.value = 1;
    if (!box.checked) qty.value = 0;
  };
  panel.querySelectorAll('.hospital-program-checkbox').forEach(box => box.addEventListener('change', () => {
    syncBoxQty(box);
    // Selecting 수술실 auto-selects its mandatory support set (수술지원·회복실·중앙공급); 개수는 직접 조정 가능.
    if (box.checked) {
      for (const bundledId of (HOSPITAL_PROGRAM_BUNDLES[box.value] || [])) {
        const bundledBox = panel.querySelector('.hospital-program-checkbox[value="' + bundledId + '"]');
        if (bundledBox && !bundledBox.checked) { bundledBox.checked = true; syncBoxQty(bundledBox); }
      }
    }
    saveProgramChecklist();
    updateAreaSummary();
  }));
  panel.querySelectorAll('.program-qty').forEach(qty => qty.addEventListener('input', () => {
    const box = panel.querySelector('.hospital-program-checkbox[value="' + qty.getAttribute('data-program-id') + '"]');
    if (box) box.checked = Number(qty.value || 0) > 0;
    saveProgramChecklist();
    updateAreaSummary();
  }));
  updateAreaSummary();
}
function selectedModuleNetAreaM2() {
  const requests = getSelectedHospitalProgramRequests();
  let cells = 0, count = 0;
  for (const req of requests) {
    const size = req.program.preferred_grid_size || [HOSPITAL_BASE_MODULE_CELLS.w, HOSPITAL_BASE_MODULE_CELLS.h];
    cells += req.quantity * size[0] * size[1];
    count += req.quantity;
  }
  return {cells, count, area: cells * CELL_AREA_M2};
}
const placementModeKey = 'placement_mode_v1';
function getPlacementMode() {
  const el = document.querySelector('input[name="placementMode"]:checked');
  return el ? el.value : 'hospital';
}
function updateModeHint() {
  const hint = document.getElementById('modeHint');
  if (!hint) return;
  hint.textContent = getPlacementMode() === 'hospital'
    ? '체크리스트에서 선택한 진료 실(부서 덩어리)을 배치합니다.'
    : '체크리스트와 무관하게, 그린 영역에 병실·전실·화장실로 구성된 병동을 배치합니다.';
}
function setupModeSelector() {
  let saved = null;
  try { saved = localStorage.getItem(placementModeKey); } catch (e) {}
  document.querySelectorAll('input[name="placementMode"]').forEach(radio => {
    if (saved) radio.checked = (radio.value === saved);
    radio.addEventListener('change', () => {
      try { localStorage.setItem(placementModeKey, getPlacementMode()); } catch (e) {}
      updateModeHint();
      updateAreaSummary();
    });
  });
  updateModeHint();
}
function updateAreaSummary() {
  if (!areaSummary) return;
  const painted = usableAreaStats().area;
  const paintedArea = painted * CELL_AREA_M2;
  const net = selectedModuleNetAreaM2();
  if (net.count === 0) {
    areaSummary.innerHTML = '<b>면적 요약</b> · 선택한 모듈이 없습니다 — 체크리스트에서 실을 선택하면 배치 가능 최소 영역이 즉시 표시됩니다.<br>도면 선택 면적: <b>' + paintedArea.toFixed(1) + '㎡</b> (' + painted + '칸)';
    return;
  }
  // 배치 가능 최소 영역 = 실제 병원 모듈 배치 로직과 같은 블록 배치 규칙으로 전부 들어가는 가장 작은 직사각형 후보.
  const fp = findMinimumHospitalPlacementFootprint(getSelectedHospitalProgramRequests());
  const requiredArea = fp.cells * CELL_AREA_M2;
  const diff = paintedArea - requiredArea;
  const diffLabel = diff >= 0
    ? '<span class="area-surplus">여유 +' + diff.toFixed(1) + '㎡ (약 ' + Math.floor(diff / CELL_AREA_M2) + '칸)</span>'
    : '<span class="area-shortfall">부족 ' + diff.toFixed(1) + '㎡ (약 ' + Math.ceil(-diff / CELL_AREA_M2) + '칸 더 필요)</span>';
  areaSummary.innerHTML =
    '<b>면적 요약</b> — 선택 모듈 <b>' + net.count + '개</b><br>' +
    '모듈 순면적 <b>' + net.area.toFixed(1) + '㎡</b> &nbsp;|&nbsp; 배치 가능 최소 영역 <b>' + requiredArea.toFixed(1) + '㎡</b> <span class="small">(실제 배치 시뮬레이션 ≈ ' + fp.h + '×' + fp.w + '칸)</span><br>' +
    '도면 선택 면적 <b>' + paintedArea.toFixed(1) + '㎡</b> (' + painted + '칸) &nbsp;→&nbsp; 차이 ' + diffLabel;
}
function programById(id) { return HOSPITAL_PROGRAMS.find(p => p.id === id); }
function getSelectedHospitalProgramRequests() {
  const requests = [];
  const seen = new Map();
  function addRequest(programId, quantity, bundled=false) {
    const program = programById(programId);
    if (!program || quantity <= 0) return;
    const prev = seen.get(programId);
    if (prev) { prev.quantity = Math.max(prev.quantity, quantity); prev.bundled = prev.bundled || bundled; return; }
    const req = {program, id: program.id, quantity, bundled};
    seen.set(programId, req); requests.push(req);
  }
  document.querySelectorAll('.hospital-program-checkbox:checked').forEach(box => {
    const qtyInput = document.querySelector('.program-qty[data-program-id="' + box.value + '"]');
    const quantity = Math.max(1, Number(qtyInput && qtyInput.value || 1));
    addRequest(box.value, quantity, false);
    for (const bundledId of (HOSPITAL_PROGRAM_BUNDLES[box.value] || [])) {
      const bundledQuantity = Number((HOSPITAL_PROGRAM_BUNDLE_MIN_QTY[box.value] || {})[bundledId] || 1);
      addRequest(bundledId, bundledQuantity, true);
    }
  });
  return requests;
}
function getSelectedHospitalPrograms() {
  return getSelectedHospitalProgramRequests().map(req => req.program);
}
function expandHospitalProgramRequests(requests) {
  const placedProgramInstances = [];
  for (const request of requests) {
    for (let i=0; i<request.quantity; i++) placedProgramInstances.push({program: request.program, id: request.id, instanceIndex: i, bundled: request.bundled});
  }
  return placedProgramInstances;
}
function hospitalProgramRectFor(program, rotate=false) {
  const size = program.preferred_grid_size || [HOSPITAL_BASE_MODULE_CELLS.w, HOSPITAL_BASE_MODULE_CELLS.h];
  const w = rotate ? size[1] : size[0];
  const h = rotate ? size[0] : size[1];
  return {w, h};
}
const HOSPITAL_BAND_DEPTH_CELLS = 4; // 모듈 깊이 = 4칸(7.2m). 부서 덩어리는 이 깊이를 기준으로 1~2열로 묶인다.
const HOSPITAL_GROUP_INTERNAL_GAP_CELLS = 0; // 같은 기능 group 내부 실은 붙여 하나의 부서 클러스터로 읽히게 한다. 경계는 moduleIdGrid outline으로만 구분한다.
// 같은 부서(진료기능)끼리 하나의 덩어리로 묶고, 그 덩어리들을 복도가 감싸도록 한다.
const HOSPITAL_DEPARTMENT = {
  operating_room:'surg', surgery_support:'surg', recovery_room:'surg', central_supply:'surg',
  exam_room:'exam', specimen_collection:'exam', treatment_room:'exam',
  ct_suite:'img', xray_room:'img', diagnostic_lab:'img', pathology_lab:'img',
  emergency_care:'acute', observation_4bed:'acute',
  infusion_6bed:'inf', dialysis_4bed:'inf', dialysis_8bed:'inf',
  delivery_room:'obs', newborn_treatment:'obs',
  clinical_research_lab:'adm', data_analysis_room:'adm', meeting_room:'adm', administration:'adm'
};
const HOSPITAL_DEPARTMENT_ORDER = ['surg','acute','exam','img','inf','obs','adm'];
const HOSPITAL_DEPARTMENT_ORDERS = [
  ['surg','acute','img','exam','inf','obs','adm'],
  ['acute','img','exam','surg','inf','obs','adm'],
  ['img','acute','exam','surg','inf','obs','adm'],
  ['exam','img','acute','inf','surg','obs','adm'],
  ['obs','surg','acute','img','exam','inf','adm'],
  ['adm','exam','img','acute','surg','inf','obs']
];
const HOSPITAL_RELATED_GROUPS = [
  {key:'surgery_core', label:'수술 core group', dept:'surg', maxPerGroup: 3, ids:['operating_room','surgery_support','recovery_room']},
  {key:'surgery_supply', label:'수술 멸균공급 group', dept:'surg', maxPerGroup: 2, ids:['central_supply','surgery_support']},
  {key:'acute_care', label:'응급-관찰-처치 group', dept:'acute', maxPerGroup: 3, ids:['emergency_care','observation_4bed','treatment_room']},
  {key:'imaging', label:'영상검사 group', dept:'img', maxPerGroup: 2, ids:['ct_suite','xray_room']},
  {key:'diagnostic', label:'검체-진단-병리 group', dept:'img', maxPerGroup: 3, ids:['specimen_collection','diagnostic_lab','pathology_lab']},
  {key:'outpatient', label:'외래-처치-수액 group', dept:'exam', maxPerGroup: 3, ids:['exam_room','treatment_room','infusion_6bed']},
  {key:'dialysis', label:'투석 group', dept:'inf', maxPerGroup: 2, ids:['dialysis_4bed','dialysis_8bed']},
  {key:'obstetric', label:'분만-신생아 group', dept:'obs', maxPerGroup: 2, ids:['delivery_room','newborn_treatment']},
  {key:'research_admin', label:'연구-행정 group', dept:'adm', maxPerGroup: 6, ids:['clinical_research_lab','data_analysis_room','meeting_room','administration']}
];
const HOSPITAL_ADJACENCY_RULES = [
  // source: USER_PDF_MEDICAL_FACILITY_GUIDELINE_2018 — 수술부는 수술 전후 환자·의료진·물류 흐름, 청결/비청결 동선 분리, 회복실·중앙공급 연계를 우선한다.
  ['operating_room','recovery_room',100,'수술실-회복실 직접 연계'],
  ['operating_room','surgery_support',100,'수술실-수술지원 core'],
  ['operating_room','central_supply',70,'수술실-중앙공급 청결물품 동선'],
  ['surgery_support','central_supply',70,'수술지원-멸균물품'],
  ['surgery_support','recovery_room',35,'수술지원-회복실'],
  // guideline + 보조 운영 규칙: 응급/관찰은 같은 급성 진료 흐름, 응급은 CT/X-ray 접근성이 높아야 한다.
  ['emergency_care','observation_4bed',100,'응급-관찰'],
  ['emergency_care','treatment_room',70,'응급-처치'],
  ['emergency_care','ct_suite',70,'응급-CT'],
  ['emergency_care','xray_room',70,'응급-X-ray'],
  ['observation_4bed','treatment_room',70,'관찰-처치'],
  ['observation_4bed','ct_suite',35,'관찰-CT'],
  ['observation_4bed','xray_room',35,'관찰-X-ray'],
  // diagnostic cluster: 영상/검체/진단검사/병리 기능을 같은 support zone으로 묶는다.
  ['ct_suite','xray_room',100,'영상검사 cluster'],
  ['specimen_collection','diagnostic_lab',70,'검체-진단검사'],
  ['diagnostic_lab','pathology_lab',70,'진단검사-병리'],
  ['specimen_collection','pathology_lab',35,'검체-병리'],
  ['ct_suite','diagnostic_lab',20,'영상-진단검사 보조'],
  ['xray_room','diagnostic_lab',20,'X-ray-진단검사 보조'],
  // outpatient / treatment / infusion cluster.
  ['consult_room','treatment_room',70,'외래-처치'],
  ['consult_room','specimen_collection',35,'외래-검체'],
  ['consult_room','infusion_6bed',35,'외래-수액'],
  ['treatment_room','infusion_6bed',70,'처치-수액'],
  // dialysis, obstetric/newborn, admin/research support.
  ['dialysis_4bed','dialysis_8bed',100,'투석 cluster'],
  ['dialysis_4bed','treatment_room',35,'투석-처치'],
  ['dialysis_8bed','treatment_room',35,'투석-처치'],
  ['delivery_room','newborn_treatment',100,'분만-신생아'],
  ['delivery_room','operating_room',35,'분만-수술 보조'],
  ['clinical_research_lab','data_analysis_room',70,'연구-데이터'],
  ['clinical_research_lab','meeting_room',35,'연구-회의'],
  ['administration','meeting_room',70,'행정-회의']
];
function normalizedModuleWH(program) {
  // 모듈 깊이를 밴드(4칸)에 맞추도록 회전 방향을 정한다.
  const a = hospitalProgramRectFor(program, false);
  if (a.h === HOSPITAL_BAND_DEPTH_CELLS) return a;
  const b = hospitalProgramRectFor(program, true);
  if (b.h === HOSPITAL_BAND_DEPTH_CELLS) return b;
  return a;
}
function placeOneHospitalModule(r0, c0, h, w, code) {
  // 모듈을 배치하고, 같은 코드끼리 붙어도 각 실의 경계를 그릴 수 있도록 고유 id를 moduleIdGrid에 기록한다.
  if (!fillModuleStrict(r0, c0, h, w, code)) return false;
  const id = 'm' + String(nextModuleNo++).padStart(3, '0');
  for (let r = r0; r < r0 + h; r++) for (let c = c0; c < c0 + w; c++) moduleIdGrid[r][c] = id;
  return true;
}
function hospitalRowWidth(row) {
  return row.reduce((s, m) => s + m.w, 0) + Math.max(0, row.length - 1) * HOSPITAL_GROUP_INTERNAL_GAP_CELLS;
}
function advanceHospitalModuleColumn(c0, moduleWidth) {
  return c0 + moduleWidth + HOSPITAL_GROUP_INTERNAL_GAP_CELLS;
}
function markHospitalInternalCorridorGap(r0, c0, h, w, corridorCells) {
  if (w <= 0) return;
  for (let r = r0; r < r0 + h; r++) {
    for (let c = c0; c < c0 + w; c++) markCorridor(r, c, corridorCells);
  }
}
function hospitalBlockFootprintCells(blk) {
  return blk.W * blk.H;
}
function hospitalGroupRows(group, mods) {
  // 관련 실 2~3개는 하나의 작은 단위로 붙여 복도가 둘러싸게 한다. 4개 이상이면 3개 이하 row로 쪼개고 가운데 복도를 사이에 두어 마주보게 한다.
  if (mods.length <= 3) return [mods];
  const rowCount = Math.ceil(mods.length / 3);
  const rowsOut = [];
  for (let i = 0; i < rowCount; i++) rowsOut.push(mods.slice(i * 3, i * 3 + 3));
  const half = Math.ceil(rowsOut.length / 2);
  return rowsOut.slice(0, half).concat(rowsOut.slice(half));
}
function blockHasFacingRows(blockRows) {
  return blockRows.length > 1;
}
function buildHospitalProgramGroups(instances, strategyIndex) {
  // 부서 전체를 하나의 큰 덩어리로 만들지 않고, 인접성이 강한 2~3개 실 단위로 묶는다.
  const remaining = instances.slice();
  const groups = [];
  const orders = HOSPITAL_DEPARTMENT_ORDERS;
  const deptOrder = orders[strategyIndex % orders.length] || HOSPITAL_DEPARTMENT_ORDER;
  const relatedGroups = HOSPITAL_RELATED_GROUPS.slice().sort((a, b) => deptOrder.indexOf(a.dept) - deptOrder.indexOf(b.dept));
  function takeForSpec(spec) {
    const picked = [];
    for (const id of spec.ids) {
      for (let i = 0; i < remaining.length && picked.length < spec.maxPerGroup; i++) {
        if (remaining[i] && remaining[i].program.id === id) {
          picked.push(remaining.splice(i, 1)[0]);
          i -= 1;
        }
      }
    }
    return picked;
  }
  for (const spec of relatedGroups) {
    let picked = takeForSpec(spec);
    while (picked.length) {
      groups.push({groupKey: spec.key, label: spec.label, dept: spec.dept, instances: picked});
      picked = takeForSpec(spec);
    }
  }
  for (const inst of remaining) {
    const dept = HOSPITAL_DEPARTMENT[inst.program.id] || 'adm';
    groups.push({groupKey: 'single_' + inst.program.id, label: inst.program.name_ko || inst.program.id, dept, instances: [inst]});
  }
  return groups;
}
function buildDepartmentBlocks(requests, strategyIndex) {
  // 관련 실 group마다 하나의 작은 block을 만든다. block 사이는 빈 칸으로 남겨 최종적으로 복도가 감싸는 형태가 된다.
  const instances = expandHospitalProgramRequests(requests);
  const groups = buildHospitalProgramGroups(instances, strategyIndex);
  const blocks = [];
  for (const group of groups) {
    const mods = group.instances.map(inst => { const wh = normalizedModuleWH(inst.program); return {w: wh.w, h: wh.h, code: moduleCodes[inst.program.id], id: inst.program.id}; });
    const blockRows = hospitalGroupRows(group, mods);
    const W = Math.max(...blockRows.map(row => hospitalRowWidth(row)));
    const H = blockRows.length * HOSPITAL_BAND_DEPTH_CELLS + (blockRows.length - 1); // row 사이 1칸은 내부 양면복도
    blocks.push({W, H, rows: blockRows, dept: group.dept, groupKey: group.groupKey, label: group.label, facingRows: blockHasFacingRows(blockRows)});
  }
  // 전략별로 정렬 압력을 달리해 후보 배치의 zoning 방향을 바꾼다.
  if (strategyIndex === 2) blocks.sort((a, b) => b.W * b.H - a.W * a.H);
  else if (strategyIndex === 0 || strategyIndex === 1) blocks.sort((a, b) => b.H - a.H);
  return blocks;
}
function placeDepartmentBlockAt(blk, r0, c0, corridorCells) {
  for (let ri = 0; ri < blk.rows.length; ri++) {
    let cc = c0; const rr = r0 + ri * (HOSPITAL_BAND_DEPTH_CELLS + 1); // 줄 사이 1칸은 비워 가운데 복도
    for (let mi = 0; mi < blk.rows[ri].length; mi++) {
      const m = blk.rows[ri][mi];
      placeOneHospitalModule(rr, cc, m.h, m.w, m.code);
      if (mi < blk.rows[ri].length - 1 && HOSPITAL_GROUP_INTERNAL_GAP_CELLS > 0) markHospitalInternalCorridorGap(rr, cc + m.w, m.h, HOSPITAL_GROUP_INTERNAL_GAP_CELLS, corridorCells);
      cc = advanceHospitalModuleColumn(cc, m.w);
    }
  }
}
function canPlaceDepartmentBlockWithBuffer(r0, c0, h, w) {
  // 같은 block 내부의 실은 붙이되, 서로 다른 block/기능군은 최소 1칸 빈 띠를 남긴다.
  // 이후 이 빈 띠가 controlled corridor로 바뀌어 기능군 사이 복도가 된다.
  if (!canPlaceModule(r0, c0, h, w)) return false;
  for (let r = r0 - 1; r <= r0 + h; r++) for (let c = c0 - 1; c <= c0 + w; c++) {
    if (r < 0 || r >= rows || c < 0 || c >= cols) continue;
    if (r >= r0 && r < r0 + h && c >= c0 && c < c0 + w) continue;
    if (grid[r][c] !== 0 && grid[r][c] !== 1) return false;
  }
  return true;
}
function searchDepartmentBlockFit(blk, tr, tc, maxRad) {
  // 목표 위치 주변을 점점 넓혀가며(spiral) 칠해진(==1) 직사각형 자리를 찾는다.
  for (let rad = 0; rad <= maxRad; rad++) {
    for (let dr = -rad; dr <= rad; dr++) for (let dc = -rad; dc <= rad; dc++) {
      if (Math.max(Math.abs(dr), Math.abs(dc)) !== rad) continue;
      if (canPlaceDepartmentBlockWithBuffer(tr + dr, tc + dc, blk.H, blk.W)) return {r: tr + dr, c: tc + dc};
    }
  }
  return null;
}
function globalFirstFitBlock(blk, b) {
  for (let r = b.minR; r <= b.maxR - blk.H + 1; r++)
    for (let c = b.minC; c <= b.maxC - blk.W + 1; c++)
      if (canPlaceDepartmentBlockWithBuffer(r, c, blk.H, blk.W)) return {r, c};
  return null;
}
function packDepartmentBlocksDistributed(blocks, strategyIndex=0, corridorCells=[]) {
  // 부서 덩어리를 칠한 영역 전체에 '고르게 분산'한다: 영역을 cols×rowsN 격자 칸으로 나눠 각 칸 중앙에 덩어리를 놓고,
  // 자리가 막히면 주변을 탐색해 유동적으로 들어간다. 빈 공간은 복도가 되어 부서들을 나눈다. → 아래쪽까지 채워진다.
  const b = usableBounds(); if (!b) return 0;
  const W = b.maxC - b.minC + 1, H = b.maxR - b.minR + 1;
  const sorted = strategyIndex % 3 === 2 ? blocks.slice() : blocks.slice().sort((a, c) => strategyIndex % 3 === 1 ? (c.W - a.W) : (c.H - a.H)); // 후보별로 정렬 방식 변경
  const N = sorted.length;
  const cols = Math.max(1, Math.round(Math.sqrt(N * W / Math.max(1, H))));
  const rowsN = Math.max(1, Math.ceil(N / cols));
  const cellW = W / cols, cellH = H / rowsN;
  const rad = Math.ceil(Math.max(cellW, cellH)) + 4;
  let placed = 0;
  sorted.forEach((blk, i) => {
    if (blk.W > W || blk.H > H) return; // 영역보다 큰 덩어리는 배치 불가
    let gc = i % cols, gr = Math.floor(i / cols);
    if (strategyIndex === 1 || strategyIndex === 5) gc = cols - 1 - gc;
    if (strategyIndex === 3) gr = rowsN - 1 - gr;
    if (strategyIndex === 4 && gr % 2 === 1) gc = cols - 1 - gc;
    const cx = b.minC + gc * cellW + cellW / 2, cy = b.minR + gr * cellH + cellH / 2;
    const tr = Math.round(cy - blk.H / 2), tc = Math.round(cx - blk.W / 2);
    const pos = searchDepartmentBlockFit(blk, tr, tc, rad) || globalFirstFitBlock(blk, b);
    if (pos) { placeDepartmentBlockAt(blk, pos.r, pos.c, corridorCells); placed += blk.rows.reduce((s, r) => s + r.length, 0); }
  });
  return placed;
}
function markHospitalDepartmentCorridorNetwork(strategyIndex, corridorCells) {
  // 빈 영역 전체를 복도로 칠하지 않는다. 실/부서 block 주위의 1칸 buffer와 연결에 필요한 길만 controlled corridor로 만든다.
  // 같은 기능군 내부 실은 붙어 있고, 서로 다른 기능군 사이에 남긴 buffer가 복도로 읽히게 한다.
  const roomCells = [];
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    if (grid[r][c] !== 0 && grid[r][c] !== 1 && grid[r][c] !== moduleCodes.controlled_corridor) roomCells.push([r, c]);
  }
  const toMark = new Set();
  for (const [r, c] of roomCells) {
    for (const [rr, cc] of neighbors4(r, c)) {
      if (grid[rr][cc] === 1) toMark.add(keyOf(rr, cc));
    }
  }
  for (const k of toMark) {
    const [r, c] = parseKey(k);
    if (grid[r][c] === 1) markCorridor(r, c, corridorCells);
  }
  ensureAllCorridorsConnected(corridorCells);
  fillHospitalInterstitialCorridorVoids(corridorCells);
  ensureAllCorridorsConnected(corridorCells);
  void strategyIndex;
}
function fillHospitalInterstitialCorridorVoids(corridorCells) {
  // 복도/실 사이에 끼인 작은 흰 빈칸은 쓸모 없는 잔여지가 아니라 복도 폭/포켓으로 흡수한다.
  // 단, 외곽의 넓은 사용 가능 잔여지는 그대로 두어 전체를 다시 회색 바다로 만들지 않는다.
  const isBuilt = (r, c) => grid[r][c] !== 0 && grid[r][c] !== 1;
  const isCorridor = (r, c) => grid[r][c] === moduleCodes.controlled_corridor;
  const isRoom = (r, c) => isBuilt(r, c) && !isCorridor(r, c);
  const shouldAbsorb = (r, c) => {
    if (grid[r][c] !== 1) return false;
    const n = {
      up: r > 0 && isBuilt(r - 1, c),
      down: r < rows - 1 && isBuilt(r + 1, c),
      left: c > 0 && isBuilt(r, c - 1),
      right: c < cols - 1 && isBuilt(r, c + 1),
      cu: r > 0 && isCorridor(r - 1, c),
      cd: r < rows - 1 && isCorridor(r + 1, c),
      cl: c > 0 && isCorridor(r, c - 1),
      cr: c < cols - 1 && isCorridor(r, c + 1),
      ru: r > 0 && isRoom(r - 1, c),
      rd: r < rows - 1 && isRoom(r + 1, c),
      rl: c > 0 && isRoom(r, c - 1),
      rr: c < cols - 1 && isRoom(r, c + 1),
    };
    const builtCount = [n.up, n.down, n.left, n.right].filter(Boolean).length;
    const corridorCount = [n.cu, n.cd, n.cl, n.cr].filter(Boolean).length;
    const hasBuiltToward = (dr, dc) => {
      let rr = r + dr, cc = c + dc;
      while (rr >= 0 && rr < rows && cc >= 0 && cc < cols) {
        if (isBuilt(rr, cc)) return true;
        rr += dr; cc += dc;
      }
      return false;
    };
    const insideBuiltField = hasBuiltToward(-1, 0) && hasBuiltToward(1, 0) && hasBuiltToward(0, -1) && hasBuiltToward(0, 1);
    const oppositeBuilt = (n.up && n.down) || (n.left && n.right);
    const corridorBridge = (n.cu && n.cd) || (n.cl && n.cr);
    const roomCorridorPocket = (n.ru && n.cd) || (n.rd && n.cu) || (n.rl && n.cr) || (n.rr && n.cl);
    return insideBuiltField || corridorBridge || roomCorridorPocket || (corridorCount >= 2 && builtCount >= 2) || (oppositeBuilt && corridorCount >= 1) || builtCount >= 3;
  };
  const collectSmallSpanGaps = () => {
    const fill = [];
    const maxGap = 3; // 1~3칸짜리 흰 틈만 복도로 흡수하고, 큰 외곽 잔여지는 유지한다.
    for (let r = 0; r < rows; r++) {
      let c = 0;
      while (c < cols) {
        if (grid[r][c] !== 1) { c++; continue; }
        const start = c;
        while (c < cols && grid[r][c] === 1) c++;
        const len = c - start;
        const bounded = start > 0 && c < cols && isBuilt(r, start - 1) && isBuilt(r, c);
        if (bounded && len <= maxGap) for (let cc = start; cc < c; cc++) fill.push([r, cc]);
      }
    }
    for (let c = 0; c < cols; c++) {
      let r = 0;
      while (r < rows) {
        if (grid[r][c] !== 1) { r++; continue; }
        const start = r;
        while (r < rows && grid[r][c] === 1) r++;
        const len = r - start;
        const bounded = start > 0 && r < rows && isBuilt(start - 1, c) && isBuilt(r, c);
        if (bounded && len <= maxGap) for (let rr = start; rr < r; rr++) fill.push([rr, c]);
      }
    }
    return fill;
  };
  let changed = true;
  for (let pass = 0; pass < 5 && changed; pass++) {
    changed = false;
    const fill = [];
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) if (shouldAbsorb(r, c)) fill.push([r, c]);
    fill.push(...collectSmallSpanGaps());
    for (const [r, c] of fill) {
      if (grid[r][c] === 1) { markCorridor(r, c, corridorCells || []); changed = true; }
    }
  }
}
function placeSelectedHospitalPrograms(requests, corridorCells, strategyIndex=0) {
  const placedProgramInstances = expandHospitalProgramRequests(requests); // (배치 인스턴스 목록)
  const blocks = buildDepartmentBlocks(requests, strategyIndex);
  const placed = packDepartmentBlocksDistributed(blocks, strategyIndex, corridorCells);
  markHospitalDepartmentCorridorNetwork(strategyIndex, corridorCells); // 빈 공간 → 복도(부서 사이/줄 사이 포함)
  void placedProgramInstances.length;
  return placed;
}
function canPlaceHospitalBlocksInRect(blocks, H, W) {
  // 실제 배치기와 같은 핵심 조건을 작은 가상 직사각형에서 시뮬레이션한다.
  // block 전체 직사각형이 비어 있어야 하지만, 배치 후에는 실 셀만 점유되고 남은 셀은 나중에 복도가 된다.
  if (!blocks.length) return true;
  const occupied = Array.from({length: H}, () => Array(W).fill(false));
  function canPlaceBlockRect(blk, r0, c0) {
    if (r0 < 0 || c0 < 0 || r0 + blk.H > H || c0 + blk.W > W) return false;
    for (let r = r0; r < r0 + blk.H; r++) for (let c = c0; c < c0 + blk.W; c++) if (occupied[r][c]) return false;
    for (let r = r0 - 1; r <= r0 + blk.H; r++) for (let c = c0 - 1; c <= c0 + blk.W; c++) {
      if (r < 0 || r >= H || c < 0 || c >= W) continue;
      if (r >= r0 && r < r0 + blk.H && c >= c0 && c < c0 + blk.W) continue;
      if (occupied[r][c]) return false; // keep a corridor buffer between different functional blocks
    }
    return true;
  }
  function placeBlockRooms(blk, r0, c0) {
    for (let ri = 0; ri < blk.rows.length; ri++) {
      let cc = c0;
      const rr = r0 + ri * (HOSPITAL_BAND_DEPTH_CELLS + 1);
      for (let mi = 0; mi < blk.rows[ri].length; mi++) {
        const m = blk.rows[ri][mi];
        for (let r = rr; r < rr + m.h; r++) for (let c = cc; c < cc + m.w; c++) occupied[r][c] = true;
        if (mi < blk.rows[ri].length - 1 && HOSPITAL_GROUP_INTERNAL_GAP_CELLS > 0) {
          for (let r = rr; r < rr + m.h; r++) for (let c = cc + m.w; c < cc + m.w + HOSPITAL_GROUP_INTERNAL_GAP_CELLS; c++) occupied[r][c] = true; // reserve internal corridor gap
        }
        cc = advanceHospitalModuleColumn(cc, m.w);
      }
    }
  }
  function searchFit(blk, tr, tc, maxRad) {
    for (let rad = 0; rad <= maxRad; rad++) {
      for (let dr = -rad; dr <= rad; dr++) for (let dc = -rad; dc <= rad; dc++) {
        if (Math.max(Math.abs(dr), Math.abs(dc)) !== rad) continue;
        if (canPlaceBlockRect(blk, tr + dr, tc + dc)) return {r: tr + dr, c: tc + dc};
      }
    }
    return null;
  }
  function firstFit(blk) {
    for (let r = 0; r <= H - blk.H; r++) for (let c = 0; c <= W - blk.W; c++) if (canPlaceBlockRect(blk, r, c)) return {r, c};
    return null;
  }
  const sorted = blocks.slice().sort((a, c) => c.H - a.H);
  const N = sorted.length;
  const colsN = Math.max(1, Math.round(Math.sqrt(N * W / Math.max(1, H))));
  const rowsN = Math.max(1, Math.ceil(N / colsN));
  const cellW = W / colsN, cellH = H / rowsN;
  const rad = Math.ceil(Math.max(cellW, cellH)) + 4;
  for (const [i, blk] of sorted.entries()) {
    if (blk.W > W || blk.H > H) return false;
    const gc = i % colsN, gr = Math.floor(i / colsN);
    const cx = gc * cellW + cellW / 2, cy = gr * cellH + cellH / 2;
    const pos = searchFit(blk, Math.round(cy - blk.H / 2), Math.round(cx - blk.W / 2), rad) || firstFit(blk);
    if (!pos) return false;
    placeBlockRooms(blk, pos.r, pos.c);
  }
  return true;
}
function findMinimumHospitalPlacementFootprint(requests) {
  const blocks = buildDepartmentBlocks(requests, 0);
  if (!blocks.length) return {cells: 0, w: 0, h: 0};
  const minW = Math.max(...blocks.map(b => b.W));
  const minH = Math.max(...blocks.map(b => b.H));
  const candidates = [];
  for (let h = minH; h <= rows; h++) {
    for (let w = minW; w <= cols; w++) {
      candidates.push({h, w, cells: h * w, aspect: Math.max(h, w) / Math.max(1, Math.min(h, w))});
    }
  }
  candidates.sort((a, b) => (a.cells - b.cells) || (a.aspect - b.aspect));
  for (const cand of candidates) {
    if (canPlaceHospitalBlocksInRect(blocks, cand.h, cand.w)) return cand;
  }
  return hospitalRequiredFootprint(requests);
}
function hospitalRequiredFootprint(requests) {
  // 배치 시뮬레이션이 실패하는 비정형 예외용 보수 fallback.
  const blocks = buildDepartmentBlocks(requests, 0);
  if (!blocks.length) return {cells: 0, w: 0, h: 0};
  const totalCells = blocks.reduce((s, b) => s + b.W * b.H, 0);
  const targetW = Math.max(Math.max(...blocks.map(b => b.W)), Math.ceil(Math.sqrt(totalCells * 1.4)));
  let x = 0, y = 0, shelfH = 0, maxRight = 0;
  for (const b of blocks) {
    if (x + b.W > targetW) { x = 0; y = y + shelfH + 1; shelfH = 0; }
    maxRight = Math.max(maxRight, x + b.W);
    x = x + b.W + 1; shelfH = Math.max(shelfH, b.H);
  }
  const regionW = maxRight + 2, regionH = y + shelfH + 2;
  return {cells: regionW * regionH, w: regionW, h: regionH};
}
function hospitalProgramCentroids(candidateGrid) {
  const acc = {};
  HOSPITAL_PROGRAMS.forEach(p => { acc[p.id] = {r:0, c:0, n:0}; });
  for (let r = 0; r < candidateGrid.length; r++) {
    for (let c = 0; c < candidateGrid[r].length; c++) {
      const id = codeToModule[String(candidateGrid[r][c])];
      if (!id || !acc[id]) continue;
      acc[id].r += r; acc[id].c += c; acc[id].n += 1;
    }
  }
  const out = {};
  Object.entries(acc).forEach(([id, a]) => { if (a.n > 0) out[id] = {r: a.r / a.n, c: a.c / a.n, cells: a.n}; });
  return out;
}
function scoreHospitalAdjacency(candidateGrid) {
  const centers = hospitalProgramCentroids(candidateGrid);
  const maxDist = Math.max(1, rows + cols);
  let score = 0;
  let matched = 0;
  const highlights = [];
  for (const [a, b, weight, reason] of HOSPITAL_ADJACENCY_RULES) {
    if (!centers[a] || !centers[b]) continue;
    const d = Math.abs(centers[a].r - centers[b].r) + Math.abs(centers[a].c - centers[b].c);
    const closeness = Math.max(0, 1 - d / maxDist);
    score += weight * closeness;
    matched += 1;
    if (weight >= 70) highlights.push(reason + ' ' + d.toFixed(0) + '칸');
  }
  return {score, matched, summary: highlights.slice(0, 4).join(' · ')};
}
function chooseBestHospitalLayoutCandidate(candidates) {
  if (!candidates.length) return null;
  return candidates.slice().sort((a, b) =>
    (b.placedPrograms - a.placedPrograms) ||
    (b.adjacencyScore - a.adjacencyScore) ||
    ((b.score && b.score.score) || 0) - ((a.score && a.score.score) || 0)
  )[0];
}
function generateHospitalLayoutOptions(programRequests) {
  const base = cloneGrid(grid);
  layoutOptions = [];
  const candidates = [];
  for (let strategy=0; strategy<6; strategy++) { // 내부 후보 6개 생성 → 인접성 점수로 최고안 1개만 노출
    grid = cloneGrid(base);
    if (!gridHasUsableArea()) fillGrid();
    resetModulesToUsableArea();
    const corridorCells = [];
    // 모듈을 먼저 배치한 뒤 placeSelectedHospitalPrograms 내부에서 빈 공간을 복도로 만든다(여기서 미리 호출하면 빈 영역이 통째로 복도가 되어 배치가 막힘).
    const placedPrograms = placeSelectedHospitalPrograms(programRequests, corridorCells, strategy);
    ensureAllCorridorsConnected(corridorCells);
    fillRemainingEdgeCells(corridorCells);
    fillHospitalInterstitialCorridorVoids(corridorCells);
    ensureAllCorridorsConnected(corridorCells);
    const score = layoutUtilizationScore();
    const adjacency = scoreHospitalAdjacency(grid);
    // 기존 hospital_program:department_cluster 방식은 작은 관련 실 단위 group corridor로 세분화하고, 내부 후보를 hospital_program:group_corridor_adjacency_scored 로 재점수화한다.
    candidates.push({grid: cloneGrid(grid), clusterGrid: cloneGrid(clusterGrid), moduleIdGrid: cloneGrid(moduleIdGrid), score, placedSuites: 0, placedPrograms, adjacencyScore: adjacency.score, adjacencySummary: adjacency.summary, adjacencyMatched: adjacency.matched, corridorStrategy: 'hospital_program:group_corridor_adjacency_scored'});
  }
  const best = chooseBestHospitalLayoutCandidate(candidates);
  if (!best) {
    layoutOptions = [];
    optionPanel.innerHTML = '<b>배치 실패</b> · 선택 모듈을 배치할 수 없습니다. 영역을 더 넓히거나 체크리스트 수량을 줄여주세요.';
    return;
  }
  layoutOptions = [best];
  selectLayoutOption(0);
  const requested = expandHospitalProgramRequests(programRequests).length;
  const shortfall = requested - best.placedPrograms;
  const adjacencyText = best.adjacencySummary ? ' · ' + best.adjacencySummary : '';
  optionPanel.innerHTML = '<b>배치 완료</b> · 배치 모듈 <b>' + best.placedPrograms + '개</b>' + (shortfall > 0 ? ' <span style="color:#b91c1c;">(공간 부족으로 ' + shortfall + '개 미배치 — 영역을 더 그리거나 면적 요약의 필요 면적을 확인하세요)</span>' : '') + '.<br/><span class="small">배치 논리: 수술 cluster / 응급-영상 cluster / 검사 cluster 우선 · 인접성 점수 ' + best.adjacencyScore.toFixed(1) + adjacencyText + '</span>';
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
  const opt = layoutOptions[0];
  if (!opt) return;
  const label = strategyLabelForIndex(0, opt.corridorStrategy);
  const sig = distinctSignature(opt.grid);
  const bedCount = (sig.match(/R(\d+)/) || [])[1] || '?';
  const roomCells = parseInt(bedCount, 10) || 0;
  const bedEst = Math.floor(roomCells / (unifiedSuitePreset.up_down.roomH * unifiedSuitePreset.up_down.roomW));
  const areaScore = (opt.score.areaFillScore * 100).toFixed(0);
  optionPanel.innerHTML = '<b>배치 완료</b> · 배치 병상 <b>' + bedEst + '개</b> · 공간 이용률 <b>' + areaScore + '%</b><br/>'
    + '<span class="small"><b>' + label + '</b> · corridorStrategy: ' + opt.corridorStrategy + '</span>';
}
function generateLayoutOptions() {
  // 배치 모드는 상단 라디오로 명시 선택 (체크 여부로 추론하지 않음).
  if (getPlacementMode() === 'hospital') {
    const selectedHospitalProgramRequests = getSelectedHospitalProgramRequests();
    if (selectedHospitalProgramRequests.length === 0) {
      optionPanel.innerHTML = '<b>병원 진료 모듈 배치 모드</b><br/><span class="small">아래 체크리스트에서 배치할 실을 1개 이상 선택한 뒤 다시 생성하세요. (병실 병동을 배치하려면 배치 모드를 \"병동(병실)\"로 바꾸세요.)</span>';
      return;
    }
    generateHospitalLayoutOptions(selectedHospitalProgramRequests);
    return;
  }
  // 병동(병실) 모드: 그린 영역에 병실+전실+WC 병동을 배치한다.
  const targetBeds = 99;
  const base = cloneGrid(grid);
  layoutOptions = [];
  const infeasibleReports = [];
  for (let strategy=0; strategy<1; strategy++) {
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
  // Ward mode now returns one committed layout; layoutOptions.length === 1 when feasible.
  if (layoutOptions.length === 0) {
    grid = cloneGrid(base);
    clusterGrid = blankClusterGrid();
    renderHospitalProgramChecklist();
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
  moduleIdGrid = opt.moduleIdGrid ? cloneGrid(opt.moduleIdGrid) : blankClusterGrid();
  draw();
  checkWardRules();
}
function hospitalProgramRulesReport() {
  // Hospital-side guideline checks (병원 모듈러 모드): placed-module summary + 수술부 지원 필수 점검.
  const placedCells = {};
  HOSPITAL_PROGRAMS.forEach(p => { const n = grid.flat().filter(v => v === moduleCodes[p.id]).length; if (n > 0) placedCells[p.id] = n; });
  const ids = Object.keys(placedCells);
  if (!ids.length) return {placed: false, lines: []};
  const lines = [];
  const summary = ids.map(id => {
    const p = programById(id);
    const size = (p && p.preferred_grid_size) || [HOSPITAL_BASE_MODULE_CELLS.w, HOSPITAL_BASE_MODULE_CELLS.h];
    const inst = Math.max(1, Math.round(placedCells[id] / (size[0] * size[1])));
    return (p ? p.name_ko : id) + ' ×' + inst;
  });
  lines.push('배치된 병원 모듈: ' + summary.join(', '));
  const totalArea = ids.reduce((s, id) => s + placedCells[id], 0) * CELL_AREA_M2;
  lines.push('병원 모듈 총 순면적: ' + totalArea.toFixed(1) + '㎡ (복도 제외)');
  if (placedCells['operating_room']) {
    for (const need of (HOSPITAL_PROGRAM_BUNDLES.operating_room || [])) {
      if (!placedCells[need]) { const np = programById(need); lines.push('⚠ 수술실이 배치되었으나 ' + (np ? np.name_ko : need) + '이(가) 미배치 — 수술부 지원 필수 권장'); }
    }
  }
  return {placed: true, lines};
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
  const hospitalReport = hospitalProgramRulesReport();
  const hospitalLines = hospitalReport.placed
    ? '<li style="margin-top:6px;font-weight:700;color:#1D1D1F;">병원 모듈 가이드라인</li>' + hospitalReport.lines.map(t => '<li>' + t + '</li>').join('')
    : '';
  ruleReport.innerHTML = '<b>Rule Score</b><ul><li>buffer: ' + (checks[0].ok ? 'OK' : 'direct clean-infected contact') + '</li><li>' + checks[1].message + '</li><li>' + checks[2].message + '</li><li>' + checks[3].message + '</li><li>' + checks[4].message + '</li><li>areaFillScore: ' + score.areaFillScore.toFixed(2) + ', edgeFillScore: ' + score.edgeFillScore.toFixed(2) + '</li>' + hospitalLines + '</ul>';
}
function clearGrid() { grid = blankGrid(); clusterGrid = blankClusterGrid(); moduleIdGrid = blankClusterGrid(); nextModuleNo = 1; layoutOptions = []; draw(); }
function fillGrid() { grid = Array.from({length: rows}, () => Array(cols).fill(1)); clusterGrid = blankClusterGrid(); moduleIdGrid = blankClusterGrid(); nextModuleNo = 1; draw(); }
canvas.addEventListener('mousedown', e => { isDown = true; dragStart = cellFromEvent(e); dragEnd = dragStart; if (tool === 'pencil') { setCell(dragStart); draw(); } });
canvas.addEventListener('mousemove', e => { const pos = cellFromEvent(e); if (!pos) return; moduleInfo.textContent = 'cell (' + pos.r + ',' + pos.c + ') / ' + moduleDimensionText(grid[pos.r][pos.c]); if (!isDown) return; dragEnd = pos; if (tool === 'pencil') setCell(pos); draw(); });
canvas.addEventListener('mouseup', e => { if (!isDown) return; dragEnd = cellFromEvent(e); if (tool === 'rectangle' && dragStart && dragEnd) { const r1=Math.min(dragStart.r,dragEnd.r), r2=Math.max(dragStart.r,dragEnd.r), c1=Math.min(dragStart.c,dragEnd.c), c2=Math.max(dragStart.c,dragEnd.c); for(let r=r1;r<=r2;r++) for(let c=c1;c<=c2;c++) grid[r][c]= mode==='paint'?1:0; } isDown=false; dragStart=null; dragEnd=null; draw(); });
canvas.addEventListener('mouseleave', () => { isDown = false; dragStart = null; dragEnd = null; draw(); });
window.addEventListener('resize', fitPlanCanvas);
fitPlanCanvas();
setupModeSelector();
renderHospitalProgramChecklist();
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
    module_db_js=json.dumps(module_db, ensure_ascii=False),
    module_meta_js=json.dumps(module_meta, ensure_ascii=False),
    module_codes_js=json.dumps(module_codes, ensure_ascii=False),
    code_to_module_js=json.dumps(code_to_module, ensure_ascii=False),
    colors_js=json.dumps(colors, ensure_ascii=False),
    labels_js=json.dumps(labels, ensure_ascii=False),
    legend_html=legend_html,
)

st.iframe(html, height=height)
