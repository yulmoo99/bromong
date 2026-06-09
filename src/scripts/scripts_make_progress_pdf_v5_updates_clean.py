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
    c.drawString(M, 7 * mm, 'Hospital Floor Auto-Layout - Major Updates Progress Report')
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


# =========================================================================
# PAGE 1: 주요 업데이트 요약 (Major Updates Summary)
# =========================================================================
new_slide('자동배치 툴 주요 업데이트 요약')

# 3 cards showing the 3 biggest evolutions since last time
draw_card(M, H - 76 * mm, 80 * mm, 36 * mm, '1. 법규/비율 기준 구체화', ['MOHW 2024 법적 기준 분리', 'iHFG 비례 가로세로비 도입'])
draw_card(M + 88 * mm, H - 76 * mm, 80 * mm, 36 * mm, '2. 형태 인지 복도망 수립', ['고정형 배치 완전 탈피', '최장 경로 BFS 복도망 생성'])
draw_card(M + 176 * mm, H - 76 * mm, 80 * mm, 36 * mm, '3. 다단계 가변식 병실배치', ['공간 한계 깊이 자동 파악', 'Deluxe / Std / Compact 선택'])

# Detailed changes list
bullet_block([
    '고정 템플릿 채우기 방식에서, 비정형 형태를 스스로 읽고 대처하는 지능형 알고리즘으로의 비약적 진화.',
    '국내 의료법/보건복지부 고시와 국제 가이드라인(iHFG)의 규격을 모듈 DB와 실시간 룰체커에 전면 통합 완료.',
    '그리드 크기에 따라 병실 크기(3x4, 3x3)와 위생 세트가 유기적으로 가변 조절되어 실제적인 평면 구성 생성.'
], M + 4 * mm, H - 105 * mm, 48, 14, 8.5 * mm)


# =========================================================================
# PAGE 2: 업데이트 1 & 2 - 법규/비율 구체화 및 형태 검사
# =========================================================================
new_slide('1 & 2. 법규·비율 구체화 및 실시간 검증')

# Left bullet block for DB restructuring
bullet_block([
    '법적 병실 기준분리: 병상당 최소 10㎡ 확보 필수 (전실/화장실 면적 제외) 및 가이드라인 계획값(20.25㎡)의 완벽 구분 검증.',
    'iHFG 정방형 비례: 침대 주변 1200mm 작업 여유 공간을 확보하는 1:1.06 가이드라인 비례 원칙 수립.',
    '실시간 비율 검증: 면적만 맞추고 길쭉하게 뽑은 불합리한 기형 평면 차단을 위해 Aspect Ratio warning 및 hard limit 계산.'
], M + 4 * mm, H - 65 * mm, 26, 12, 7.5 * mm)

# Right side: Comparison table carefully calculated and positioned to avoid right-edge cutoff
rx = 410
ry = H - 120 * mm
table_w = 360
table_h = 75 * mm
header_h = 8 * mm

# Draw background container
c.setFillColor(colors.HexColor('#F8FAFC'))
c.roundRect(rx, ry, table_w, table_h, 4 * mm, fill=1, stroke=0)

# Draw blue header background
c.setFillColor(BLUE)
c.roundRect(rx, ry + table_h - header_h, table_w, header_h, 4 * mm, fill=1, stroke=0)
c.rect(rx, ry + table_h - header_h, table_w, header_h / 2, fill=1, stroke=0)

# Header labels
c.setFillColor(colors.white)
c.setFont('Malgun-Bold', 10.5)
c.drawString(rx + 10, ry + table_h - 16, '구분')
c.drawString(rx + 90, ry + table_h - 16, '수정 전 (v0.1)')
c.drawString(rx + 195, ry + table_h - 16, '수정 후 (v0.2)')

table_rows = [
    ('병실 기준', '임시 20㎡ 고정 배치', 'MOHW 최소 10㎡ 분리 검증'),
    ('가로세로비', '검사 기능 없음', '임상실 1.5 이내 검증 및 제한'),
    ('전실 크기', '임시 크기 고정', 'MOHW 요구 및 가이드라인 9㎡'),
    ('복도 폭', '수동 고정형 배치', '최소 폭 2칸(3.0m) 선형 검증'),
    ('룰체커 연동', '인접 관계만 검사', '면적+인접+비율 일체형 검사'),
    ('Hover 정보', '이름만 표시', '계획면적+비율+근거 표시'),
    ('DB 버전', 'v0.1 (임시값 중심)', 'v0.2 (근거구분 검증)')
]

for idx, (name, before, after) in enumerate(table_rows):
    y_row = ry + table_h - 36 - idx * 24
    if idx % 2 == 1:
        c.setFillColor(colors.HexColor('#F1F5F9'))
        c.rect(rx + 4, y_row - 6, table_w - 8, 20, fill=1, stroke=0)
    c.setFillColor(DARK)
    c.setFont('Malgun-Bold', 9)
    c.drawString(rx + 10, y_row, name)
    c.setFillColor(GRAY)
    c.drawString(rx + 90, y_row, before)
    c.setFillColor(colors.HexColor('#1E40AF') if idx in (0, 1, 4) else DARK)
    c.drawString(rx + 195, y_row, after)

# 3 sub-cards for our presets
card_y = 20 * mm
draw_card(M, card_y, 76 * mm, 38 * mm, '디럭스 병실 세트 (Deluxe)', ['병실: 3x4 (27.0㎡) - 중증/여유형', '화장실: 2x2 (9.0㎡)', '전실: 3x1 (6.75㎡)'])
draw_card(M + 82 * mm, card_y, 76 * mm, 38 * mm, '스탠다드 병실 세트 (Std)', ['병실: 3x3 (20.25㎡) - 일반계획안', '화장실: 2x2 (9.0㎡)', '전실: 3x1 (6.75㎡)'])
draw_card(M + 164 * mm, card_y, 76 * mm, 38 * mm, '콤팩트 병실 세트 (Compact)', ['병실: 3x3 (20.25㎡) - 콤팩트형', '화장실: 2x1 (4.5㎡)', '전실: 2x1 (4.5㎡)'])


# =========================================================================
# PAGE 3: 업데이트 3 & 4 - 형태 인지 복도망 및 다단계 가변 배치
# =========================================================================
new_slide('3 & 4. 형태 인지 복도망 및 가변형 실 배치')

# Left side description
bullet_block([
    '최장 경로 BFS 알고리즘: ㄱ, ㅁ, ㄷ자 형태에 매끄럽게 연결되는 복도 네트워크 자동 피팅.',
    '상하/좌우 자동 회전: 복도망의 흐름(수평/수직)에 맞춰 전실과 화장실이 유기적으로 자동 90도 회전 조립.',
    '지원실 최적 포지셔닝: 간호스테이션, 청결/오염실이 복도 핵심 거점에 알아서 안착.',
    '실시간 비례 룰체커: 가로세로비 hard limit 검사 기능으로 모듈러 설계의 공간성 및 시공 타당성 대폭 강화.'
], M + 4 * mm, H - 65 * mm, 30, 12, 7.5 * mm)

# Right side Highlight Box (Clean Green Box)
sb_x = 485
sb_y = 20 * mm
sb_w = 285
sb_h = 50 * mm
c.setFillColor(colors.HexColor('#F0FDF4'))
c.roundRect(sb_x, sb_y, sb_w, sb_h, 4 * mm, fill=1, stroke=0)
c.setStrokeColor(colors.HexColor('#16A34A'))
c.setLineWidth(1.2)
c.roundRect(sb_x, sb_y, sb_w, sb_h, 4 * mm, fill=0, stroke=1)

c.setFillColor(colors.HexColor('#15803D'))
c.setFont('Malgun-Bold', 14)
c.drawString(sb_x + 12, sb_y + 40 * mm, '✨ 비정형 대응 시각 배치 효과')
c.setFont('Malgun-Bold', 9.5)
c.setFillColor(DARK)
c.drawString(sb_x + 12, sb_y + 30 * mm, '- ㄷ자, ㄱ자 꺾임 모양에 복도망 자동 피팅 완료')
c.drawString(sb_x + 12, sb_y + 22 * mm, '- 한 도면 내에 대/중/소 병실이 조화롭게 혼합 배치')
c.drawString(sb_x + 12, sb_y + 14 * mm, '- 넓은 중심부와 좁은 끝자락의 완벽한 밀도 최적화')
c.drawString(sb_x + 12, sb_y + 6 * mm, '- 직교형 모듈러 시공 논리에 부합하는 가변 배치안')

c.save()
print("PDF_GENERATED_SUCCESSFULLY", OUT)
