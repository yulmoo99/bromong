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

OUT = ROOT / 'exports' / 'graduation_hospital_planner_progress_deck_4p_clean.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont('Malgun', FONT_REGULAR))
pdfmetrics.registerFont(TTFont('Malgun-Bold', FONT_BOLD))

W, H = landscape(A4)
M = 14 * mm
TITLE = colors.HexColor('#111827')
DARK = colors.HexColor('#1F2937')
GRAY = colors.HexColor('#64748B')
BLUE = colors.HexColor('#2563EB')
BLUE_SOFT = colors.HexColor('#EAF2FF')
LIGHT = colors.HexColor('#F4F7FB')
ORANGE = colors.HexColor('#F4A261')
YELLOW = colors.HexColor('#FFE066')
TEAL = colors.HexColor('#70C1B3')
RED = colors.HexColor('#E76F51')
GREEN = colors.HexColor('#95D5B2')
WC_BLUE = colors.HexColor('#9BD0FF')
CORRIDOR = colors.HexColor('#BFC7D5')
CREAM = colors.HexColor('#FFF4D6')
GRIDLINE = colors.HexColor('#D7DEE8')

c = canvas.Canvas(str(OUT), pagesize=(W, H))
slide_no = 0


def new_slide(title):
    global slide_no
    if slide_no:
        c.showPage()
    slide_no += 1
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TITLE)
    c.setFont('Malgun-Bold', 34)
    c.drawString(M, H - 24 * mm, title)
    c.setStrokeColor(BLUE)
    c.setLineWidth(2.4)
    c.line(M, H - 33 * mm, W - M, H - 33 * mm)
    c.setFillColor(GRAY)
    c.setFont('Malgun', 9)
    c.drawString(M, 7 * mm, 'Compact Ward Auto-layout Tool')
    c.drawRightString(W - M, 7 * mm, str(slide_no))


def wrap(text, chars):
    return textwrap.wrap(text, width=chars, break_long_words=False, replace_whitespace=False)


def draw_card(x, y, w, h, head, lines, fill=BLUE_SOFT, head_color=BLUE):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 5 * mm, fill=1, stroke=0)
    header_h = 12 * mm
    c.setFillColor(head_color)
    c.roundRect(x, y + h - header_h, w, header_h, 5 * mm, fill=1, stroke=0)
    # square off lower header edge for cleaner geometry
    c.rect(x, y + h - header_h, w, header_h / 2, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Malgun-Bold', 18)
    c.drawCentredString(x + w / 2, y + h - 8 * mm, head)
    c.setFillColor(DARK)
    c.setFont('Malgun-Bold', 17)
    line_gap = 8.3 * mm
    total = len(lines) * line_gap
    cur = y + (h - header_h) / 2 + total / 2 - 5 * mm
    for line in lines:
        c.drawCentredString(x + w / 2, cur, line)
        cur -= line_gap


def bullet_block(items, x, y, width_chars=40, size=18, leading=10.5 * mm):
    cur = y
    for text in items:
        c.setFillColor(BLUE)
        c.circle(x + 2.8 * mm, cur + 1.8 * mm, 1.6 * mm, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.setFont('Malgun-Bold', size)
        first = True
        for line in wrap(text, width_chars):
            c.drawString(x + 8 * mm, cur, line if first else line)
            cur -= leading
            first = False
        cur -= 3.5 * mm
    return cur


def module_tag(x, y, w, h, color, code, size=15):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, 3 * mm, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont('Malgun-Bold', size)
    c.drawCentredString(x + w / 2, y + h / 2 - size / 4 + 2, code)


def draw_grid(x0, y0, s):
    rows, cols = 10, 18
    c.setStrokeColor(GRIDLINE)
    c.setLineWidth(0.45)
    for r in range(rows):
        for col in range(cols):
            c.setFillColor(LIGHT if 1 <= r <= 8 and 1 <= col <= 16 else colors.white)
            c.rect(x0 + col * s, y0 + r * s, s, s, fill=1, stroke=1)
    for col in range(1, 17):
        c.setFillColor(CORRIDOR)
        c.rect(x0 + col * s, y0 + 4 * s, s, s, fill=1, stroke=1)
    for col in [6, 11, 14]:
        c.setFillColor(ORANGE); c.rect(x0 + col * s, y0 + 5 * s, 2 * s, 2 * s, fill=1, stroke=1)
        c.setFillColor(YELLOW); c.rect(x0 + col * s, y0 + 4 * s, 2 * s, s, fill=1, stroke=1)
        c.setFillColor(WC_BLUE); c.rect(x0 + (col + 2) * s, y0 + 5 * s, s, 2 * s, fill=1, stroke=1)
    c.setFillColor(TEAL); c.rect(x0 + 2 * s, y0 + 6 * s, 3 * s, 2 * s, fill=1, stroke=1)
    c.setFillColor(GREEN); c.rect(x0 + 5 * s, y0 + 6 * s, s, 2 * s, fill=1, stroke=1)
    c.setFillColor(RED); c.rect(x0 + 2 * s, y0 + 2 * s, 2 * s, 2 * s, fill=1, stroke=1)
    c.setStrokeColor(DARK)
    c.setLineWidth(1.4)
    c.rect(x0, y0, cols * s, rows * s, fill=0, stroke=1)


def legend_row(x, y, color, label):
    module_tag(x, y, 11 * mm, 6.5 * mm, color, '', 1)
    c.setFillColor(DARK)
    c.setFont('Malgun-Bold', 12)
    c.drawString(x + 14 * mm, y + 1.3 * mm, label)

# 1
new_slide('병원 평면 자동배치 툴')
draw_card(M, H - 84 * mm, 78 * mm, 38 * mm, '입력', ['병동 외곽', '그리드 지정'])
draw_card(M + 92 * mm, H - 84 * mm, 78 * mm, 38 * mm, '처리', ['모듈 자동 배치', '규칙 위반 확인'])
draw_card(M + 184 * mm, H - 84 * mm, 78 * mm, 38 * mm, '출력', ['배치안 저장', '3D 시각화 연계'])
bullet_block([
    '병동 한 층의 사용 가능 영역을 빠르게 그린다.',
    '필수 병동 모듈을 배치하고 근거 수준을 함께 확인한다.',
    '초기 배치안을 저장해 다음 설계 검토와 3D 시각화에 활용한다.'
], M + 4 * mm, H - 112 * mm, 54, 19)

# 2
new_slide('구현 현황')
card_w = 80 * mm
card_h = 39 * mm
draw_card(M, H - 84 * mm, card_w, card_h, '그리드 조작', ['연필 / 사각형', '칠하기 / 지우기', '선택 영역 유지'])
draw_card(M + 91 * mm, H - 84 * mm, card_w, card_h, '모듈 배치', ['7개 필수 모듈', '색상 블록 배치', '근거 정보 표시'])
draw_card(M + 182 * mm, H - 84 * mm, card_w, card_h, '규칙 확인', ['면적 기준', '인접 관계', '동선 분리'])
x0, y0, s = M + 7 * mm, 28 * mm, 8.1 * mm
draw_grid(x0, y0, s)
# legend placed far right, no overlap with grid
lx, ly = M + 165 * mm, 74 * mm
legend_row(lx, ly, ORANGE, 'R  음압격리병실')
legend_row(lx, ly - 10 * mm, YELLOW, 'A  전실')
legend_row(lx, ly - 20 * mm, WC_BLUE, 'WC  화장실·샤워실')
legend_row(lx, ly - 30 * mm, CORRIDOR, 'C  통제 복도')
legend_row(lx, ly - 40 * mm, TEAL, 'N  간호스테이션')
legend_row(lx, ly - 50 * mm, GREEN, 'CL  청결물품')
legend_row(lx, ly - 60 * mm, RED, 'D  오염물 보관')

# 3
new_slide('병동 모듈과 근거 수준')
mods = [
    ('R', '음압격리병실', ORANGE, '공식 면적 기준 확인'),
    ('A', '전실 / 손위생 버퍼', YELLOW, '관계 기준 확인, 면적 추가조사'),
    ('WC', '병실 내부 화장실·샤워실', WC_BLUE, '관계 기준 확인, 면적 추가조사'),
    ('C', '통제 복도', CORRIDOR, '폭 기준 추가조사'),
    ('N', '간호스테이션', TEAL, '운영상 필수, 치수 추가조사'),
    ('CL', '청결물품 알코브', GREEN, '임시 계획값'),
    ('D', '오염물·폐기물 임시보관', RED, '임시 계획값'),
]
left_x = M + 2 * mm
right_x = W / 2 + 8 * mm
for i, (code, name, color, note) in enumerate(mods):
    x = left_x if i < 4 else right_x
    y = H - 60 * mm - (i % 4) * 24 * mm
    module_tag(x, y, 21 * mm, 14 * mm, color, code, 16)
    c.setFillColor(DARK); c.setFont('Malgun-Bold', 17); c.drawString(x + 28 * mm, y + 8 * mm, name)
    c.setFillColor(GRAY); c.setFont('Malgun', 13); c.drawString(x + 28 * mm, y + 1.5 * mm, note)
# standard banner
banner_x, banner_y, banner_w, banner_h = M, 24 * mm, W - 2 * M, 28 * mm
c.setFillColor(CREAM)
c.roundRect(banner_x, banner_y, banner_w, banner_h, 5 * mm, fill=1, stroke=0)
c.setFillColor(DARK)
c.setFont('Malgun-Bold', 16)
c.drawString(banner_x + 7 * mm, banner_y + 16 * mm, '보건복지부 고시 2024')
c.setFont('Malgun', 15)
c.drawString(banner_x + 7 * mm, banner_y + 7 * mm, '일반입원실 음압병실은 병상 1개당 10㎡ 이상, 전실 및 화장실·샤워실 면적은 제외')

# 4
new_slide('현재 한계와 다음 계획')
draw_card(M, H - 78 * mm, 124 * mm, 34 * mm, '현재 한계', ['일부 치수는 추가 근거 필요', '자동배치는 초기 단계'])
draw_card(W - M - 124 * mm, H - 78 * mm, 124 * mm, 34 * mm, '다음 개발', ['근거 DB 보강', '배치 옵션 고도화'])
bullet_block([
    '전실 면적, 화장실·샤워실 면적, 복도 폭 기준을 추가 조사한다.',
    '병실 수와 복도 유형을 조절할 수 있는 배치 옵션을 만든다.',
    '병실-전실-복도 관계와 청결/오염 동선 분리를 더 엄격하게 검사한다.',
    '2D 배치 결과를 3D 모듈 매싱으로 변환해 발표용 다이어그램으로 확장한다.'
], M + 4 * mm, H - 103 * mm, 62, 17)

c.save()
print(OUT)
