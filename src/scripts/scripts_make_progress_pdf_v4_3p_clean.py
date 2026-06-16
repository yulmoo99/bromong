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

OUT = ROOT / 'exports' / 'graduation_hospital_planner_progress_deck_3p_clean.pdf'
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
    c.drawString(M, 7 * mm, 'Hospital Floor Auto-Layout Progress Report')
    c.drawRightString(W - M, 7 * mm, f"{slide_no} / 3")


def wrap(text, chars):
    return textwrap.wrap(text, width=chars, break_long_words=False, replace_whitespace=False)


def draw_card(x, y, w, h, head, lines, fill=BLUE_SOFT, head_color=BLUE):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 5 * mm, fill=1, stroke=0)
    header_h = 10 * mm
    c.setFillColor(head_color)
    c.roundRect(x, y + h - header_h, w, header_h, 5 * mm, fill=1, stroke=0)
    c.rect(x, y + h - header_h, w, header_h / 2, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Malgun-Bold', 14)
    c.drawCentredString(x + w / 2, y + h - 7 * mm, head)
    c.setFillColor(DARK)
    c.setFont('Malgun-Bold', 12)
    line_gap = 7.5 * mm
    total = len(lines) * line_gap
    cur = y + (h - header_h) / 2 + total / 2 - 4 * mm
    for line in lines:
        c.drawCentredString(x + w / 2, cur, line)
        cur -= line_gap


def bullet_block(items, x, y, width_chars=40, size=15, leading=8.5 * mm):
    cur = y
    for text in items:
        c.setFillColor(BLUE)
        c.circle(x + 2.8 * mm, cur + 1.8 * mm, 1.4 * mm, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.setFont('Malgun-Bold', size)
        first = True
        for line in wrap(text, width_chars):
            c.drawString(x + 8 * mm, cur, line)
            cur -= leading
            first = False
        cur -= 2.5 * mm
    return cur


def module_tag(x, y, w, h, color, code, size=13):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, 3 * mm, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont('Malgun-Bold', size)
    c.drawCentredString(x + w / 2, y + h / 2 - size / 4 + 1, code)


def legend_row(x, y, color, label):
    module_tag(x, y, 10 * mm, 6.0 * mm, color, '', 1)
    c.setFillColor(DARK)
    c.setFont('Malgun-Bold', 11)
    c.drawString(x + 13 * mm, y + 1.2 * mm, label)


# =========================================================================
# PAGE 1: 병원 평면 자동배치 툴 개요 (Overview)
# =========================================================================
new_slide('병원 평면 자동배치 툴 개요')

# 3 cards for workflow
draw_card(M, H - 76 * mm, 80 * mm, 36 * mm, '1. 외곽 영역 그리기', ['사용자가 마우스 드래그로', '병동/병원 한 층 영역 지정'])
draw_card(M + 88 * mm, H - 76 * mm, 80 * mm, 36 * mm, '2. 복도망 및 실 배치', ['최장 BFS 경로 복도망 생성', '가로세로 비율 대응 자동 배치'])
draw_card(M + 176 * mm, H - 76 * mm, 80 * mm, 36 * mm, '3. 법규 검증 & 출력', ['실시간 면적 및 형태 검사', 'JSON 저장 및 3D 매싱 연계'])

# Summary bullet block
bullet_block([
    '병원/감염병동의 평면 기획안을 1.8m x 1.8m 모듈러 그리드 단위로 빠르게 검토한다.',
    '복도 네트워크와 전실-화장실-병실 위생 세트가 실제 가이드라인에 입각해 결합한다.',
    '사용자가 그린 ㄷ자, ㄱ자, ㅁ자 등 다양하고 유연한 형상에 실시간으로 맞춤 작동한다.',
    '법적 음압격리병실 면적(10㎡ 이상)과 가이드라인 비례를 즉시 확인해 설계 리스크를 제로화한다.'
], M + 4 * mm, H - 105 * mm, 62, 16, 9 * mm)


# =========================================================================
# PAGE 2: 다이나믹 모듈 크기 및 공간 가이드라인
# =========================================================================
new_slide('다이나믹 모듈 크기 및 가이드라인')

# Left side: standards info
cur_y = bullet_block([
    '법적 음압격리병실: 병상당 10㎡ 이상 확보 필수 (전실 및 화장실 면적 제외).',
    'iHFG 격리병실 표준: 18㎡ 권장 (약 4.2m x 4.45m), 거의 1:1에 가까운 정방형 형태.',
    '가로세로비 제한: 병실·진찰실 등 임상실은 침대 주변 clearance 확보 위해 1:1.5 이내 권장.',
    '공간 인지형 가변 모듈: 툴에서 외곽 깊이에 맞춰 3가지 세트를 자동 선택배치.'
], M + 4 * mm, H - 65 * mm, 45, 14, 8.5 * mm)

# 3 sub-cards for our presets
card_y = 20 * mm
draw_card(M, card_y, 76 * mm, 38 * mm, '디럭스 병실 세트 (Deluxe)', ['병실: 3x4 (27.0㎡) - 중증/여유형', '화장실: 2x2 (9.0㎡)', '전실: 3x1 (6.75㎡)'])
draw_card(M + 82 * mm, card_y, 76 * mm, 38 * mm, '스탠다드 병실 세트 (Std)', ['병실: 3x3 (20.25㎡) - 일반계획안', '화장실: 2x2 (9.0㎡)', '전실: 3x1 (6.75㎡)'])
draw_card(M + 164 * mm, card_y, 76 * mm, 38 * mm, '콤팩트 병실 세트 (Compact)', ['병실: 3x3 (20.25㎡) - 콤팩트형', '화장실: 2x1 (4.5㎡)', '전실: 2x1 (4.5㎡)'])

# Right side: Visual database table
rx = W / 2 + 30 * mm
ry = H - 120 * mm
c.setFillColor(colors.HexColor('#F8FAFC'))
c.roundRect(rx, ry, 110 * mm, 75 * mm, 4 * mm, fill=1, stroke=0)
c.setFillColor(BLUE)
c.roundRect(rx, ry + 67 * mm, 110 * mm, 8 * mm, 4 * mm, fill=1, stroke=0)
c.rect(rx, ry + 67 * mm, 110 * mm, 4 * mm, fill=1, stroke=0)

c.setFillColor(colors.white)
c.setFont('Malgun-Bold', 12)
c.drawString(rx + 4 * mm, ry + 70 * mm, '실 구분')
c.drawString(rx + 45 * mm, ry + 70 * mm, '권장 크기')
c.drawString(rx + 80 * mm, ry + 70 * mm, '권장 비율')

table_rows = [
    ('R 음압격리병실', '3x3 cells (20.25㎡)', '1.0 ~ 1.4'),
    ('A 전실 / 버퍼', '2x2 cells (9.00㎡)', '1.0 ~ 1.5'),
    ('WC 화장실·샤워', '2x2 cells (9.00㎡)', '1.0 ~ 1.5'),
    ('N 간호스테이션', '2x3 cells (13.50㎡)', '1.0 ~ 1.8'),
    ('CL 청결물품', '2x2 cells (9.00㎡)', '1.0 ~ 1.8'),
    ('D 오염물 보관', '2x3 cells (13.50㎡)', '1.0 ~ 1.8'),
    ('C 통제 복도', '폭 2cells (3.0m)', '선형 (예외)')
]
c.setFont('Malgun-Bold', 10)
for idx, (name, size, ratio) in enumerate(table_rows):
    y_row = ry + 59 * mm - idx * 8 * mm
    c.setFillColor(DARK)
    c.drawString(rx + 4 * mm, y_row, name)
    c.setFillColor(colors.HexColor('#1E40AF') if 'R' in name or 'A' in name else GRAY)
    c.drawString(rx + 45 * mm, y_row, size)
    c.drawString(rx + 80 * mm, y_row, ratio)


# =========================================================================
# PAGE 3: 형태 인식 배치 알고리즘 및 위반 체크
# =========================================================================
new_slide('형태 인식 배치 및 규칙 검증')

# Left side: shape algorithm description
bullet_block([
    '최장 경로 BFS 알고리즘: 사용자가 그린 자유로운 모양(ㄱ자, ㅁ자, 대형 사각)을 완벽히 인식하여 막힘없는 연결 복도망 생성.',
    '상하/좌우 자동 회전: 복도망의 방향(수평/수직)에 맞추어 안방 전실과 화장실이 자동으로 회전 조립되어 일체 배치.',
    '주변 지원실 배치: 간호스테이션(N), 청결(CL), 오염(D)이 복도의 최적 지점에 adaptive하게 자동 포지셔닝.',
    '실시간 비례 및 형태 룰체커: 실별 가로세로비 정책을 실시간 연산하여 비정상적으로 길쭉한 불합리 평면에 즉시 warning 점등.'
], M + 4 * mm, H - 60 * mm, 52, 14, 8.0 * mm)

# Right side: Summary box for results
sb_x = W - M - 90 * mm
sb_y = 20 * mm
c.setFillColor(colors.HexColor('#F0FDF4'))
c.roundRect(sb_x, sb_y, 90 * mm, 50 * mm, 4 * mm, fill=1, stroke=0)
c.setStrokeColor(colors.HexColor('#16A34A'))
c.setLineWidth(1.2)
c.roundRect(sb_x, sb_y, 90 * mm, 50 * mm, 4 * mm, fill=0, stroke=1)

c.setFillColor(colors.HexColor('#15803D'))
c.setFont('Malgun-Bold', 15)
c.drawString(sb_x + 6 * mm, sb_y + 40 * mm, '✨ 현재 툴의 핵심 성과')
c.setFont('Malgun-Bold', 11)
c.setFillColor(DARK)
c.drawString(sb_x + 6 * mm, sb_y + 30 * mm, '- ㄱ자, ㄷ자, ㅁ자 비정형 외곽 자동배치 성공')
c.drawString(sb_x + 6 * mm, sb_y + 22 * mm, '- 디럭스/스탠다드/콤팩트 3단계 모듈 가변 자동 제어')
c.drawString(sb_x + 6 * mm, sb_y + 14 * mm, '- MOHW 고시 법정 음압병실 면적(10㎡) 완벽 충족')
c.drawString(sb_x + 6 * mm, sb_y + 6 * mm, '- iHFG 가이드라인 기반 가로세로 비율 자동 검증')

c.save()
print("PDF_GENERATED_SUCCESSFULLY", OUT)
