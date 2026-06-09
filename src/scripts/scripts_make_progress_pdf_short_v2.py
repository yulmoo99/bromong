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

OUT = ROOT / 'exports' / 'graduation_hospital_planner_progress_deck_short_v2_large.pdf'
OUT.parent.mkdir(parents=True, exist_ok=True)

pdfmetrics.registerFont(TTFont('Malgun', FONT_REGULAR))
pdfmetrics.registerFont(TTFont('Malgun-Bold', FONT_BOLD))

W, H = landscape(A4)
M = 12 * mm
TITLE = colors.HexColor('#111827')
DARK = colors.HexColor('#1F2937')
GRAY = colors.HexColor('#5B6472')
LIGHT = colors.HexColor('#F3F6FA')
BLUE = colors.HexColor('#2563EB')
PALE_BLUE = colors.HexColor('#EAF2FF')
ORANGE = colors.HexColor('#F4A261')
YELLOW = colors.HexColor('#FFE066')
TEAL = colors.HexColor('#70C1B3')
RED = colors.HexColor('#E76F51')
GREEN = colors.HexColor('#95D5B2')
WC_BLUE = colors.HexColor('#9BD0FF')
CORRIDOR = colors.HexColor('#BFC7D5')
GRIDLINE = colors.HexColor('#D8DEE8')

c = canvas.Canvas(str(OUT), pagesize=(W, H))
slide_no = 0


def footer():
    c.setFont('Malgun', 9)
    c.setFillColor(GRAY)
    c.drawString(M, 7 * mm, 'Compact Ward Auto-layout Tool')
    c.drawRightString(W - M, 7 * mm, str(slide_no))


def new_slide(title, subtitle=''):
    global slide_no
    if slide_no:
        c.showPage()
    slide_no += 1
    c.setFillColor(colors.white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFont('Malgun-Bold', 31)
    c.setFillColor(TITLE)
    c.drawString(M, H - 22 * mm, title)
    if subtitle:
        c.setFont('Malgun', 15)
        c.setFillColor(GRAY)
        c.drawString(M, H - 31 * mm, subtitle)
    c.setStrokeColor(BLUE)
    c.setLineWidth(2.2)
    c.line(M, H - 36 * mm, W - M, H - 36 * mm)
    footer()


def wrap_lines(text, width_chars):
    return textwrap.wrap(text, width=width_chars, break_long_words=False, replace_whitespace=False)


def big_bullets(items, x, y, width_chars=34, size=16, leading=21, bullet_color=BLUE):
    cur = y
    for item in items:
        c.setFillColor(bullet_color)
        c.circle(x + 2.4 * mm, cur + 2.2 * mm, 1.3 * mm, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.setFont('Malgun-Bold' if isinstance(item, tuple) else 'Malgun', size)
        if isinstance(item, tuple):
            head, body = item
            c.drawString(x + 7 * mm, cur, head)
            cur -= leading * 0.92
            c.setFont('Malgun', size - 1)
            c.setFillColor(GRAY)
            for line in wrap_lines(body, width_chars):
                c.drawString(x + 7 * mm, cur, line)
                cur -= leading * 0.9
        else:
            first = True
            for line in wrap_lines(item, width_chars):
                c.drawString(x + 7 * mm, cur, line if first else '  ' + line)
                first = False
                cur -= leading
        cur -= 4 * mm
    return cur


def card(x, y, w, h, title, body='', fill=PALE_BLUE):
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 5 * mm, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.roundRect(x, y + h - 8 * mm, w, 8 * mm, 5 * mm, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Malgun-Bold', 15)
    c.drawString(x + 5 * mm, y + h - 6 * mm, title)
    if body:
        c.setFillColor(DARK)
        c.setFont('Malgun', 15)
        cur = y + h - 18 * mm
        for line in wrap_lines(body, max(16, int(w / (4.2 * mm)))):
            c.drawString(x + 5 * mm, cur, line)
            cur -= 7 * mm


def module_box(x, y, w, h, fill, label, sub=''):
    c.setFillColor(fill)
    c.setStrokeColor(colors.white)
    c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, 3 * mm, fill=1, stroke=1)
    c.setFillColor(DARK)
    c.setFont('Malgun-Bold', 15)
    c.drawCentredString(x + w / 2, y + h / 2 + 1.5 * mm, label)
    if sub:
        c.setFont('Malgun', 9)
        c.drawCentredString(x + w / 2, y + 3 * mm, sub)


def draw_grid_diagram(x0, y0, s):
    rows, cols = 10, 18
    c.setStrokeColor(GRIDLINE)
    c.setLineWidth(0.45)
    for r in range(rows):
        for col in range(cols):
            fill = LIGHT if 1 <= r <= 8 and 1 <= col <= 16 else colors.white
            c.setFillColor(fill)
            c.rect(x0 + col * s, y0 + r * s, s, s, fill=1, stroke=1)
    # corridor
    c.setFillColor(CORRIDOR)
    for col in range(1, 17):
        c.rect(x0 + col * s, y0 + 4 * s, s, s, fill=1, stroke=1)
    # rooms
    for col in [6, 11, 14]:
        c.setFillColor(ORANGE); c.rect(x0 + col * s, y0 + 5 * s, 2 * s, 2 * s, fill=1, stroke=1)
        c.setFillColor(YELLOW); c.rect(x0 + col * s, y0 + 4 * s, 2 * s, s, fill=1, stroke=1)
        c.setFillColor(WC_BLUE); c.rect(x0 + (col + 2) * s, y0 + 5 * s, s, 2 * s, fill=1, stroke=1)
    c.setFillColor(TEAL); c.rect(x0 + 2 * s, y0 + 6 * s, 3 * s, 2 * s, fill=1, stroke=1)
    c.setFillColor(GREEN); c.rect(x0 + 5 * s, y0 + 6 * s, s, 2 * s, fill=1, stroke=1)
    c.setFillColor(RED); c.rect(x0 + 2 * s, y0 + 2 * s, 2 * s, 2 * s, fill=1, stroke=1)
    # outline and labels
    c.setStrokeColor(DARK)
    c.setLineWidth(1.1)
    c.rect(x0, y0, cols * s, rows * s, fill=0, stroke=1)


def legend(x, y):
    items = [('R 병실', ORANGE), ('A 전실', YELLOW), ('WC', WC_BLUE), ('C 복도', CORRIDOR), ('N 간호', TEAL), ('CL 청결', GREEN), ('D 오염', RED)]
    cx, cy = x, y
    for label, col in items:
        c.setFillColor(col)
        c.roundRect(cx, cy, 8 * mm, 5 * mm, 1.5 * mm, fill=1, stroke=0)
        c.setFillColor(DARK)
        c.setFont('Malgun-Bold', 10)
        c.drawString(cx + 10 * mm, cy + 1.2 * mm, label)
        cx += 34 * mm
        if cx > W - 55 * mm:
            cx = x
            cy -= 8 * mm

# Page 1
new_slide('진행 요약', '큰 글자·넓은 여백·핵심만 남긴 4페이지 발표용 축약본')
card(M, H - 72 * mm, 84 * mm, 25 * mm, '입력', '사용자가 그리드에서 병동 사용 가능 영역을 드래그로 지정')
card(M + 91 * mm, H - 72 * mm, 84 * mm, 25 * mm, '처리', '필수 병동 모듈을 자동 배치하고 규칙 위반을 체크')
card(M + 182 * mm, H - 72 * mm, 84 * mm, 25 * mm, '출력', 'JSON 저장과 3D 모듈 매싱으로 확장 가능')
big_bullets([
    '목표는 “법적 인증 도구”가 아니라 설계 논리 검토용 프로토타입이다.',
    '공식 기준 확인값과 추가조사 필요값을 분리해 표시한다.',
    '현재는 병동 건물의 compact layout을 우선 구현했다.'
], M, H - 95 * mm, 58, 17, 23)

# Page 2
new_slide('구현 현황', '구현 항목은 한 페이지에 통합하고, 도식은 텍스트와 분리')
card(M, H - 79 * mm, 82 * mm, 35 * mm, 'Grid UX', 'pencil / rectangle, paint / erase, localStorage 유지, JSON 저장·불러오기')
card(M + 91 * mm, H - 79 * mm, 82 * mm, 35 * mm, 'Module Layout', '7개 필수 병동 모듈을 색상 블록으로 자동 배치')
card(M + 182 * mm, H - 79 * mm, 82 * mm, 35 * mm, 'Rule Checker', '면적, 인접 관계, 청결/오염 분리, 간호 거리 체크')
# big separated diagram
x0, y0, s = M + 18 * mm, 33 * mm, 7.2 * mm
draw_grid_diagram(x0, y0, s)
legend(M + 151 * mm, 64 * mm)
c.setFillColor(GRAY)
c.setFont('Malgun', 14)
c.drawString(M + 151 * mm, 51 * mm, '※ 실제 앱에서는 hover로 모듈명, confidence, 근거 요약 표시')
c.drawString(M + 151 * mm, 42 * mm, '※ 다운로드 JSON에는 module metadata와 rule report 포함')

# Page 3
new_slide('병동 모듈과 확인된 기준', '확인된 기준은 크게, source-needed 항목은 명확히 구분')
modules = [
    ('R', '음압격리병실', ORANGE, '공식 면적 기준 확인'),
    ('A', '전실 / PPE·손위생 버퍼', YELLOW, '필수 관계 확인, 면적 추가조사'),
    ('WC', '병실 내부 화장실·샤워실', WC_BLUE, '필수 관계 확인, 면적 추가조사'),
    ('C', '통제 복도', CORRIDOR, '폭 기준 추가조사'),
    ('N', '간호스테이션', TEAL, '운영상 필수, 치수 추가조사'),
    ('CL', '청결물품 알코브', GREEN, 'compact placeholder'),
    ('D', '오염물·폐기물 임시보관', RED, 'compact placeholder'),
]
col_w = (W - 2 * M - 10 * mm) / 2
for i, (code, name, col, note) in enumerate(modules):
    x = M if i < 4 else M + col_w + 10 * mm
    y = H - 60 * mm - (i % 4) * 23 * mm
    module_box(x, y, 18 * mm, 13 * mm, col, code)
    c.setFillColor(DARK); c.setFont('Malgun-Bold', 15); c.drawString(x + 24 * mm, y + 8 * mm, name)
    c.setFillColor(GRAY); c.setFont('Malgun', 12); c.drawString(x + 24 * mm, y + 2 * mm, note)
card(M, 28 * mm, W - 2 * M, 28 * mm, '확인된 핵심 기준', '보건복지부 고시 2024: 일반입원실 음압병실은 병상 1개당 10㎡ 이상. 전실 및 화장실·샤워실 면적은 병실 면적에 포함하지 않음.', fill=colors.HexColor('#FFF7E6'))

# Page 4
new_slide('한계와 다음 계획', '발표에서는 “아직 프로토타입이며, 다음 단계가 명확하다”는 점을 강조')
left_x = M
right_x = W / 2 + 5 * mm
big_bullets([
    ('현재 한계', '전실 면적, WC 면적, 복도 폭, 간호스테이션 및 지원실 치수는 추가 근거가 필요하다.'),
    ('배치 로직', '현재는 compact ward 기본형이다. 다음은 병실 수와 복도형 옵션을 조절하도록 개선한다.'),
], left_x, H - 62 * mm, 36, 16, 22)
big_bullets([
    ('규칙 체크', '전실이 병실과 복도 사이에 있는지, WC가 병실에 직접 붙는지 더 엄격히 확인한다.'),
    ('3D 확장', '2D module code를 Plotly/Three.js 박스 매싱으로 변환해 발표용 다이어그램으로 만든다.'),
], right_x, H - 62 * mm, 34, 16, 22)
card(M, 27 * mm, W - 2 * M, 24 * mm, '다음 산출물', '① 모듈 근거 DB 보강  ② 배치 옵션 고도화  ③ 3D 매싱 시각화  ④ 발표용 before/after 다이어그램', fill=PALE_BLUE)

c.save()
print(OUT)
