
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
OUT = ROOT / "exports" / "graduation_hospital_planner_progress_deck.pdf"
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
M = 26 * mm
BLUE = colors.HexColor("#1F5FD0")
DARK = colors.HexColor("#222222")
GRAY = colors.HexColor("#666666")
LIGHT = colors.HexColor("#F4F7FB")
ORANGE = colors.HexColor("#F4A261")
YELLOW = colors.HexColor("#FFE066")
TEAL = colors.HexColor("#70C1B3")
RED = colors.HexColor("#E76F51")
GREEN = colors.HexColor("#95D5B2")

c = canvas.Canvas(str(OUT), pagesize=(W, H))

slide_no = 0

def draw_footer():
    c.setFont("Malgun", 8)
    c.setFillColor(GRAY)
    c.drawString(M, 12*mm, "Graduation Hospital Planner · AI/Robot-friendly One-stop Modular Infectious Disease Hospital")
    c.drawRightString(W-M, 12*mm, f"{slide_no}")


def title(text, subtitle=None):
    c.setFont("Malgun-Bold", 28)
    c.setFillColor(DARK)
    c.drawString(M, H-36*mm, text)
    if subtitle:
        c.setFont("Malgun", 12)
        c.setFillColor(GRAY)
        c.drawString(M, H-45*mm, subtitle)
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    c.line(M, H-51*mm, W-M, H-51*mm)


def bullet_lines(items, x, y, width_chars=58, leading=16, size=12, color=DARK):
    c.setFont("Malgun", size)
    c.setFillColor(color)
    cur = y
    for item in items:
        if isinstance(item, tuple):
            head, body = item
            c.setFont("Malgun-Bold", size)
            c.drawString(x, cur, f"• {head}")
            cur -= leading
            c.setFont("Malgun", size)
            for line in textwrap.wrap(body, width_chars):
                c.drawString(x + 12, cur, line)
                cur -= leading
        else:
            lines = textwrap.wrap(item, width_chars)
            for i, line in enumerate(lines):
                prefix = "• " if i == 0 else "  "
                c.drawString(x, cur, prefix + line)
                cur -= leading
        cur -= 4
    return cur


def chip(x, y, label, fill, w=46*mm):
    c.setFillColor(fill)
    c.roundRect(x, y, w, 10*mm, 3*mm, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont("Malgun-Bold", 9)
    c.drawCentredString(x+w/2, y+3.2*mm, label)


def new_slide(t, sub=None):
    global slide_no
    if slide_no:
        c.showPage()
    slide_no += 1
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    title(t, sub)
    draw_footer()

# 1
new_slide("병원 평면 자동배치 툴 진행 보고", "AI·로봇 친화적 원스톱 모듈러 감염병 전문병원 · 병동 모듈 우선 개발")
c.setFont("Malgun-Bold", 18); c.setFillColor(BLUE)
c.drawString(M, H-78*mm, "목표")
bullet_lines([
    "큰 그리드에서 병원 한 층의 사용 가능 영역을 정하고, 그 안에 감염병 병동 모듈을 자동 배치하는 설계 보조 툴을 만든다.",
    "최종적으로는 2D 평면 배치를 기반으로 3D 모듈 매싱까지 연결한다.",
    "현재 단계는 법적 기준이 확인된 값과 임시 계획값을 분리하면서, 병동부터 작게 검증하는 단계이다."
], M, H-90*mm, 76, 17)
chip(M, 38*mm, "Grid UX", BLUE, 34*mm)
chip(M+39*mm, 38*mm, "Ward Modules", ORANGE, 42*mm)
chip(M+86*mm, 38*mm, "Rule Check", GREEN, 38*mm)
chip(M+129*mm, 38*mm, "Future 3D", YELLOW, 38*mm)

# 2
new_slide("졸업작품 맥락", "CO-EXISTENCE: AI·로봇 친화적 원스톱 모듈러 감염병 전문병원")
bullet_lines([
    ("핵심 문제", "기존의 대형·개방형 병원은 일반 진료 효율에는 유리하지만 팬데믹 상황에서는 감염 확산과 병동 마비에 취약하다."),
    ("설계 방향", "중앙 허브와 분산형 병동, 원스톱 진료, AI 커맨드센터, 로봇 물류, 치유 중정, 평상시/위기시 전환 시스템을 결합한다."),
    ("툴의 역할", "아이디어를 단순 도식이 아니라, 실제 병동 모듈·전실·복도·지원공간의 배치 가능성으로 검토하는 보조 도구로 만든다.")
], M, H-70*mm, 82, 17)

# 3
new_slide("툴 컨셉", "MapleStory ‘유니온 배치’처럼, 제한된 그리드 안에 병원 모듈을 배치")
# diagram board
x0, y0 = M, 38*mm
cell=7*mm
for r in range(8):
    for col in range(18):
        c.setStrokeColor(colors.HexColor("#DDDDDD")); c.setFillColor(colors.white)
        if 2 <= r <= 6 and 2 <= col <= 15:
            c.setFillColor(colors.HexColor("#E8F0FF"))
        c.rect(x0+col*cell, y0+r*cell, cell, cell, fill=1, stroke=1)
# modules
for col in range(4, 14):
    c.setFillColor(colors.HexColor("#BFC7D5")); c.rect(x0+col*cell, y0+4*cell, cell, cell, fill=1, stroke=1)
for col in [6,10,14]:
    c.setFillColor(ORANGE); c.rect(x0+col*cell, y0+5*cell, cell*2, cell, fill=1, stroke=1)
    c.setFillColor(YELLOW); c.rect(x0+col*cell, y0+4*cell, cell*2, cell, fill=1, stroke=1)
c.setFillColor(TEAL); c.rect(x0+3*cell, y0+5*cell, cell*2, cell, fill=1, stroke=1)
bullet_lines([
    "사용자: rectangle/pencil로 병동 외곽 또는 사용 가능 영역을 선택",
    "툴: 병동 필수 모듈을 색상 블록으로 배치",
    "리포트: 면적·인접·분리·거리 조건을 간단히 체크",
    "출력: JSON 저장 → 이후 3D 매싱/리포트 생성에 활용"
], W/2+10*mm, H-73*mm, 46, 16)

# 4
new_slide("구현 완료 ① Grid UX", "Streamlit + HTML Canvas 조합")
bullet_lines([
    "Streamlit 기본 위젯은 drag/mousemove 처리에 약하므로, 그리드 조작은 HTML Canvas + JavaScript로 처리했다.",
    "pencil: 세부 수정용 연필 칠하기",
    "rectangle: 큰 병동 외곽을 빠르게 지정하는 사각형 드래그",
    "paint / erase 모드 지원",
    "Tool/Mode 변경 시 초기화되지 않도록 browser localStorage에 grid 상태 저장",
    "Download JSON / Load JSON으로 외곽과 배치를 파일화"
], M, H-70*mm, 82, 16)

# 5
new_slide("구현 완료 ② 병동 모듈 DB v0.1", "좁은 병동 건물용 필수 모듈만 우선 적용")
left = [
    "R  음압격리병실",
    "A  전실 / PPE·손위생 버퍼",
    "WC 병실 내부 화장실·샤워실",
    "C  통제 복도",
    "N  간호스테이션",
    "CL 청결물품 알코브",
    "D  오염물·폐기물 임시보관",
]
for i, (txt, col) in enumerate(zip(left, [ORANGE,YELLOW,colors.HexColor('#9BD0FF'),colors.HexColor('#BFC7D5'),TEAL,GREEN,RED])):
    chip(M, H-75*mm-i*13*mm, txt, col, 62*mm)
bullet_lines([
    "좁은 병동이므로 큰 휴게실, 로봇 스테이션, 별도 착의/탈의실, 약제실 등은 2차 이후로 미룸",
    "전실에 PPE·손위생 기능을 통합하는 compact 전략",
    "모듈마다 legal/design basis와 confidence를 분리 기록"
], W/2, H-78*mm, 44, 17)

# 6
new_slide("확인된 공식 기준", "보건복지부 고시 2024: 음압격리병실 설치 및 운영 기준")
bullet_lines([
    "일반입원실 음압병실: 병상 1개당 10㎡ 이상",
    "다인실 일반입원 음압병실: 병상 1개당 6.3㎡ 이상",
    "음압격리병실 면적에는 화장실/샤워실 및 전실 면적 불포함",
    "전실은 음압병실 출입구에 설치, 병실문과 전실문 동시 개폐 방지",
    "화장실/샤워시설은 음압병상이 있는 공간에 설치. 중환자실은 제외 가능",
    "음압병상 공간-전실, 음압구역-비음압구역 간 음압차 각각 -2.5Pa 이상",
    "음압병상이 있는 공간과 전실은 6회/시간 이상 환기"
], M, H-70*mm, 88, 16)
c.setFont("Malgun", 9); c.setFillColor(GRAY)
c.drawString(M, 28*mm, "Source: 보건복지부 고시 「음압격리병실 설치 및 운영에 관한 고시」 [별표], 시행 2024.10.25")

# 7
new_slide("구현 완료 ③ Compact Ward Layout", "DB 기반 모듈 배치 + source/confidence 표시")
bullet_lines([
    "Place Compact Ward Modules 버튼으로 7개 필수 병동 모듈 배치",
    "음압병실은 1.8m 계획 그리드 기준 3×3칸 = 29.16㎡ 점유로 배치: 공식 최소 10㎡ 이상을 안전하게 넘기는 계획 블록",
    "전실/WC/간호스테이션/지원실은 필요 관계는 반영하되, 치수는 source-needed로 표시",
    "마우스 hover 시 모듈명, confidence, 근거 요약 표시",
    "Download JSON에 grid, module_codes, module_metadata, module_database_version 저장"
], M, H-70*mm, 84, 17)

# 8
new_slide("구현 완료 ④ Prototype Rule Checker", "법적 완전검토가 아닌, 설계 논리 확인용 체크")
bullet_lines([
    "음압격리병실 면적이 10㎡ 이상인지 확인",
    "음압병실이 전실과 붙어 있는지 확인",
    "음압병실이 화장실/샤워실과 붙어 있는지 확인",
    "전실이 통제복도와 붙어 있는지 확인",
    "청결물품 알코브와 오염물/폐기물 보관이 직접 붙지 않는지 확인",
    "간호스테이션과 음압병실의 grid distance가 너무 멀지 않은지 확인",
    "Check Ward Rules 버튼으로 점수와 경고를 표시"
], M, H-70*mm, 88, 16)

# 9
new_slide("현재 한계", "아직 ‘진짜 자동설계’가 아니라, 배치 논리 검증 프로토타입")
bullet_lines([
    ("아직 source-needed", "전실 최소 면적, 화장실/샤워실 면적, 복도 폭, 간호스테이션 면적, 청결/오염 지원공간 면적"),
    ("배치 알고리즘", "현재는 compact ward 기본형을 배치하는 수준이며, 최적화/대안 생성/충돌 해결은 아직 미구현"),
    ("법적 지위", "현재 checker는 법적 적합성 인증이 아니라 졸업작품 설계 논리를 점검하는 prototype checker"),
    ("공간 논리", "청결/오염 동선, 압력구배, 전실 방향성, 환자/의료진/폐기물 동선은 다음 단계에서 더 정교화 필요")
], M, H-70*mm, 84, 17)

# 10
new_slide("앞으로의 계획", "모듈 확대보다 먼저: 병동 로직을 정확하게")
items = [
    ("1. 병동 배치 옵션", "한쪽 복도형 / 중앙 복도형 / 양쪽 복도형, 병실 수 2·4·6·8개 선택"),
    ("2. 근거 데이터 보강", "전실·WC·복도·간호스테이션·오염물 보관 치수 기준 추가 조사 및 confidence 갱신"),
    ("3. 규칙 체크 고도화", "전실이 복도와 병실 사이에 있는지, WC가 병실에 직접 붙는지, 청결/오염 지원공간 분리 여부 확인"),
    ("4. 자동배치 개선", "면적 효율, 간호 관찰거리, 전실/복도 관계를 점수화해 여러 후보안 생성"),
    ("5. 3D 매싱", "2D grid의 모듈 코드를 기반으로 Plotly/Three.js로 3D box 모듈을 연결 표시")
]
bullet_lines(items, M, H-70*mm, 78, 15)

# 11
new_slide("최종 목표 이미지", "2D 배치 → 검증 리포트 → 3D 모듈 매싱")
bullet_lines([
    "사용자가 병동 외곽을 그린다.",
    "툴이 병동 모듈을 자동 배치한다.",
    "각 모듈의 법적/설계 근거와 confidence가 표시된다.",
    "규칙 체크 결과가 점수와 경고로 출력된다.",
    "같은 데이터가 3D 모듈 매싱으로 전환되어 발표용 다이어그램이 된다."
], M, H-72*mm, 76, 18)
# pipeline
px, py = M, 42*mm
for i, (lab, col) in enumerate([("Grid", BLUE), ("Modules", ORANGE), ("Rules", GREEN), ("3D", YELLOW)]):
    chip(px+i*45*mm, py, lab, col, 34*mm)
    if i < 3:
        c.setStrokeColor(GRAY); c.setLineWidth(1.5)
        c.line(px+i*45*mm+35*mm, py+5*mm, px+(i+1)*45*mm-3*mm, py+5*mm)

# 12
new_slide("파일 위치", "현재 산출물과 실행 위치")
bullet_lines([
    "프로젝트 폴더: (설치 경로)\\Graduation_Hospital_Planner",
    "앱 실행: run_grid_drag_app.bat",
    "프로토타입 코드: prototype\\grid_drag_canvas_app.py",
    "병동 모듈 DB: data\\modules_ward_v01.json",
    "근거 정리 문서: docs\\06_ward_module_database_v01.md",
    "국내 기준 PDF: research_sources\\korea_negative_pressure_isolation_standard_2024.pdf",
    "이번 발표자료 PDF: exports\\graduation_hospital_planner_progress_deck.pdf"
], M, H-70*mm, 96, 16)

c.save()
print(OUT)
