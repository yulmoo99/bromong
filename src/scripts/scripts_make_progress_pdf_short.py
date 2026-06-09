from pathlib import Path
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.units import mm
import textwrap
import os
import platform

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "exports" / "graduation_hospital_planner_progress_deck_short.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

win_dir = os.environ.get("SystemRoot", "C:/Windows")
if platform.system() == "Windows":
    FONT_REGULAR = f"{win_dir}/Fonts/malgun.ttf"
    FONT_BOLD = f"{win_dir}/Fonts/malgunbd.ttf"
else:
    if Path('/mnt/c/Windows/Fonts/malgun.ttf').exists():
        FONT_REGULAR = '/mnt/c/Windows/Fonts/malgun.ttf'
        FONT_BOLD = '/mnt/c/Windows/Fonts/malgunbd.ttf'
    else:
        FONT_REGULAR = 'malgun.ttf'
        FONT_BOLD = 'malgunbd.ttf'

pdfmetrics.registerFont(TTFont("Malgun", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("Malgun-Bold", FONT_BOLD))

W, H = landscape(A4)
M = 24 * mm
BLUE = colors.HexColor("#1F5FD0")
DARK = colors.HexColor("#222222")
GRAY = colors.HexColor("#666666")
LIGHT = colors.HexColor("#F4F7FB")
ORANGE = colors.HexColor("#F4A261")
YELLOW = colors.HexColor("#FFE066")
TEAL = colors.HexColor("#70C1B3")
RED = colors.HexColor("#E76F51")
GREEN = colors.HexColor("#95D5B2")
WC_BLUE = colors.HexColor("#9BD0FF")
CORRIDOR = colors.HexColor("#BFC7D5")

c = canvas.Canvas(str(OUT), pagesize=(W, H))
slide_no = 0


def footer():
    c.setFont("Malgun", 8)
    c.setFillColor(GRAY)
    c.drawString(M, 11*mm, "Graduation Hospital Planner · Compact Ward Auto-layout Tool")
    c.drawRightString(W-M, 11*mm, str(slide_no))


def new_slide(title, subtitle=""):
    global slide_no
    if slide_no:
        c.showPage()
    slide_no += 1
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFont("Malgun-Bold", 25)
    c.setFillColor(DARK)
    c.drawString(M, H-31*mm, title)
    if subtitle:
        c.setFont("Malgun", 11)
        c.setFillColor(GRAY)
        c.drawString(M, H-40*mm, subtitle)
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    c.line(M, H-46*mm, W-M, H-46*mm)
    footer()


def bullets(items, x, y, width=58, size=11, leading=14):
    c.setFont("Malgun", size)
    c.setFillColor(DARK)
    cur = y
    for item in items:
        if isinstance(item, tuple):
            head, body = item
            c.setFont("Malgun-Bold", size)
            c.drawString(x, cur, f"• {head}")
            cur -= leading
            c.setFont("Malgun", size)
            for line in textwrap.wrap(body, width):
                c.drawString(x+10, cur, line)
                cur -= leading
        else:
            lines = textwrap.wrap(item, width)
            for i, line in enumerate(lines):
                c.drawString(x, cur, ("• " if i == 0 else "  ") + line)
                cur -= leading
        cur -= 3
    return cur


def box(x, y, w, h, fill, label, sub=""):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 3*mm, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Malgun-Bold", 10)
    c.drawCentredString(x+w/2, y+h/2+2, label)
    if sub:
        c.setFont("Malgun", 7)
        c.drawCentredString(x+w/2, y+3.2*mm, sub)


def section_label(x, y, text):
    c.setFillColor(BLUE)
    c.roundRect(x, y, 34*mm, 8*mm, 2*mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Malgun-Bold", 9)
    c.drawCentredString(x+17*mm, y+2.5*mm, text)

# 1
new_slide("병원 평면 자동배치 툴 진행 요약", "큰 그리드에서 병동 외곽을 그리고, 필수 병동 모듈을 배치·검토하는 프로토타입")
section_label(M, H-65*mm, "목표")
bullets([
    "사용자가 병원 한 층의 사용 가능 영역을 그리드로 지정한다.",
    "툴이 좁은 감염병 병동에 필요한 최소 모듈을 자동 배치한다.",
    "각 모듈의 법적/설계 근거와 신뢰도를 분리해 표시한다.",
    "최종적으로 2D 배치를 3D 모듈 매싱으로 연결한다."
], M, H-80*mm, 70, 12, 16)
section_label(W/2+5*mm, H-65*mm, "현재 범위")
bullets([
    "병동 건물 우선",
    "필수 모듈 중심",
    "법적 완전검토가 아닌 설계 논리 검토용 prototype checker",
    "공식 기준 확인값과 source-needed 값을 명확히 분리"
], W/2+5*mm, H-80*mm, 58, 12, 16)
# mini flow
py = 34*mm
for i, (lab, col) in enumerate([("Grid", BLUE), ("Modules", ORANGE), ("Rule Check", GREEN), ("3D Next", YELLOW)]):
    x = M + i*48*mm
    box(x, py, 36*mm, 12*mm, col, lab)
    if i < 3:
        c.setStrokeColor(GRAY); c.line(x+38*mm, py+6*mm, x+46*mm, py+6*mm)

# 2
new_slide("구현 현황", "Grid UX + Compact Ward Module Layout + Rule Checker")
left_items = [
    ("Grid UX", "Streamlit shell 안에 HTML Canvas를 삽입해 drag UX 구현. pencil / rectangle, paint / erase, localStorage 유지, JSON 저장/불러오기 지원."),
    ("Compact Ward Layout", "data/modules_ward_v01.json을 읽어 7개 필수 병동 모듈을 색상 블록으로 배치."),
    ("Source/Confidence 표시", "마우스 hover 시 모듈명, confidence, 근거 요약 표시. 다운로드 JSON에도 metadata 포함."),
    ("Rule Checker", "면적, 전실/WC/복도 인접, 청결-오염 직접 인접 금지, 간호스테이션 거리 등을 prototype 수준으로 체크."),
]
bullets(left_items, M, H-66*mm, 62, 11, 14)
# grid diagram
x0, y0, s = W/2+18*mm, 34*mm, 6.2*mm
for r in range(12):
    for col in range(20):
        fill = LIGHT if 1 <= r <= 10 and 1 <= col <= 18 else colors.white
        c.setFillColor(fill); c.setStrokeColor(colors.HexColor("#DDDDDD"))
        c.rect(x0+col*s, y0+r*s, s, s, fill=1, stroke=1)
for col in range(1,19):
    c.setFillColor(CORRIDOR); c.rect(x0+col*s, y0+5*s, s, s, fill=1, stroke=1)
for col in [7,12,17]:
    c.setFillColor(ORANGE); c.rect(x0+col*s, y0+6*s, 2*s, 2*s, fill=1, stroke=1)
    c.setFillColor(YELLOW); c.rect(x0+col*s, y0+5*s, 2*s, s, fill=1, stroke=1)
    c.setFillColor(WC_BLUE); c.rect(x0+(col+2)*s, y0+6*s, s, 2*s, fill=1, stroke=1)
c.setFillColor(TEAL); c.rect(x0+2*s, y0+7*s, 3*s, 2*s, fill=1, stroke=1)
c.setFillColor(GREEN); c.rect(x0+5*s, y0+7*s, 2*s, 2*s, fill=1, stroke=1)
c.setFillColor(RED); c.rect(x0+2*s, y0+3*s, 2*s, 2*s, fill=1, stroke=1)

# 3
new_slide("병동 모듈과 확인된 기준", "공식 근거가 확인된 값과 추가조사가 필요한 값을 분리")
modules = [
    ("R", "음압격리병실", ORANGE, "공식 면적 기준 확인"),
    ("A", "전실/PPE·손위생 버퍼", YELLOW, "필수 관계 확인, 면적 필요"),
    ("WC", "병실 내부 화장실·샤워실", WC_BLUE, "필수 관계 확인, 면적 필요"),
    ("C", "통제 복도", CORRIDOR, "폭 기준 추가조사"),
    ("N", "간호스테이션", TEAL, "운영상 필수, 치수 추가조사"),
    ("CL", "청결물품 알코브", GREEN, "compact placeholder"),
    ("D", "오염물·폐기물 임시보관", RED, "compact placeholder"),
]
for i, (code, name, col, note) in enumerate(modules):
    y = H-68*mm-i*14*mm
    box(M, y, 16*mm, 9*mm, col, code)
    c.setFont("Malgun-Bold", 10); c.setFillColor(DARK); c.drawString(M+20*mm, y+5*mm, name)
    c.setFont("Malgun", 8.5); c.setFillColor(GRAY); c.drawString(M+20*mm, y+1*mm, note)

bullets([
    ("보건복지부 고시 2024", "일반입원실 음압병실은 병상 1개당 10㎡ 이상."),
    ("면적 제외", "음압격리병실 면적에는 전실 및 화장실/샤워실 면적이 포함되지 않음."),
    ("전실", "음압병실 출입구에 설치하며, 병실문과 전실문은 동시에 개폐되지 않도록 계획."),
    ("음압/환기", "음압차 -2.5Pa 이상, 음압병상이 있는 공간과 전실은 6회/시간 이상 환기."),
    ("주의", "현재 checker는 법적 인증이 아니라 설계 논리 검토용이다."
    )
], W/2+4*mm, H-70*mm, 54, 11, 14)

# 4
new_slide("현재 한계와 앞으로의 계획", "아직 멀었기 때문에, 다음 단계는 근거 보강과 배치 로직 정교화")
bullets([
    ("현재 한계", "전실 최소 면적, 화장실/샤워실 면적, 복도 폭, 간호스테이션 및 지원실 치수는 아직 source-needed 상태."),
    ("배치 로직", "현재는 compact ward 기본형 배치. 다음은 병실 수, 한쪽/중앙/양쪽 복도형, 병실-전실-복도 관계를 옵션화."),
    ("규칙 체크", "전실이 실제로 복도와 병실 사이에 있는지, WC가 병실에 직접 붙는지, 청결/오염 지원공간 분리 여부를 더 엄격하게 체크."),
    ("근거 DB", "국내 기준을 우선으로 하고, 부족한 치수는 CDC/IHFG/WHO 등으로 보조하되 confidence를 명시."),
    ("3D 계획", "2D grid의 module code를 기반으로 Plotly 또는 Three.js에서 모듈 박스 매싱을 생성해 발표용 다이어그램으로 확장.")
], M, H-66*mm, 90, 12, 16)

c.save()
print(OUT)
