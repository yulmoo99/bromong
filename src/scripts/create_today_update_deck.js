const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const outDir = path.join(__dirname, 'outputs');
fs.mkdirSync(outDir, { recursive: true });

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Hermes Agent';
pptx.subject = 'Graduation Hospital Planner update deck';
pptx.title = '감염병동 모듈 자동배치 툴 개선 리포트';
pptx.company = 'Graduation_Hospital_Planner';
pptx.lang = 'ko-KR';
pptx.theme = {
  headFontFace: 'Malgun Gothic',
  bodyFontFace: 'Malgun Gothic',
  lang: 'ko-KR'
};
pptx.defineLayout({ name: 'CUSTOM_WIDE', width: 13.333, height: 7.5 });
pptx.layout = 'CUSTOM_WIDE';
pptx.margin = 0;
pptx.defineSlideMaster({
  title: 'MASTER',
  background: { color: 'F7F4ED' },
  objects: [
    { line: { x: 0.45, y: 7.12, w: 12.43, h: 0, line: { color: 'D6CCBB', width: 1 } } },
    { text: { text: 'Graduation Hospital Planner · Auto Layout v2', options: { x: 0.55, y: 7.18, w: 4.8, h: 0.18, fontFace: 'Malgun Gothic', fontSize: 7.5, color: '6B665C' } } },
    { text: { text: '2026.06.01', options: { x: 11.35, y: 7.18, w: 1.4, h: 0.18, fontFace: 'Malgun Gothic', fontSize: 7.5, align: 'right', color: '6B665C' } } },
  ],
  slideNumber: { x: 12.83, y: 7.18, color: '6B665C' },
});

const C = {
  bg: 'F7F4ED', dark: '18332F', green: '2F6B5F', teal: '3AA99E', mint: 'DDEFE9', sand: 'EEE5D4', gold: 'D99B3D', red: 'B85042', ink: '24312F', muted: '706B62', white: 'FFFFFF', line: 'CDBFAD', room: 'BFD8FF', ante: 'F3D9A4', wc: 'C9E6C7', corr: '7BC6B4', reserve: 'D8CFBD'
};
const W = 13.333, H = 7.5;
function addSlide(title, kicker='TODAY UPDATE') {
  const s = pptx.addSlide('MASTER');
  s.background = { color: C.bg };
  s.addText(kicker, { x: 0.62, y: 0.34, w: 2.7, h: 0.2, fontSize: 8, bold: true, color: C.green, charSpace: 1.3, margin: 0 });
  s.addText(title, { x: 0.6, y: 0.58, w: 11.9, h: 0.48, fontSize: 23, bold: true, color: C.dark, margin: 0, fit: 'shrink' });
  return s;
}
function titleSlide() {
  const s = pptx.addSlide();
  s.background = { color: C.dark };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: H, fill: { color: C.dark }, line: { color: C.dark } });
  s.addShape(pptx.ShapeType.arc, { x: 8.55, y: -0.35, w: 5.4, h: 5.4, line: { color: '315F55', transparency: 20, width: 3 }, adjustPoint: 0.2, rotate: 15 });
  s.addShape(pptx.ShapeType.arc, { x: 9.7, y: 1.3, w: 3.9, h: 3.9, line: { color: C.gold, transparency: 35, width: 2 }, rotate: 65 });
  s.addText('감염병동 모듈\n자동배치 툴 개선 리포트', { x: 0.72, y: 0.95, w: 7.4, h: 1.55, fontSize: 33, bold: true, color: C.white, breakLine: false, margin: 0.02, fit: 'shrink' });
  s.addText('오늘 수정사항 중심 · 배치 미감 / 빈 공간 / 3개 대안 생성 개선', { x: 0.76, y: 2.72, w: 7.3, h: 0.36, fontSize: 14.5, color: 'DCEAE5', margin: 0 });
  s.addShape(pptx.ShapeType.roundRect, { x: 0.78, y: 3.45, w: 2.0, h: 0.68, rectRadius: 0.08, fill: { color: C.teal }, line: { color: C.teal } });
  s.addText('25 tests passed', { x: 0.92, y: 3.62, w: 1.72, h: 0.22, fontSize: 13, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addShape(pptx.ShapeType.roundRect, { x: 3.0, y: 3.45, w: 2.55, h: 0.68, rectRadius: 0.08, fill: { color: 'F2D49B' }, line: { color: 'F2D49B' } });
  s.addText('3 distinct options', { x: 3.18, y: 3.62, w: 2.18, h: 0.22, fontSize: 13, bold: true, color: C.dark, align: 'center', margin: 0 });
  drawMiniPlan(s, 8.0, 3.2, 4.5, 2.65, 'dark');
  s.addText('Graduation_Hospital_Planner / Auto Layout v2', { x: 0.78, y: 6.83, w: 5.0, h: 0.25, fontSize: 9.5, color: 'ADC8C1', margin: 0 });
}
function bullet(s, x, y, title, body, color=C.green) {
  s.addShape(pptx.ShapeType.ellipse, { x, y: y+0.04, w: 0.18, h: 0.18, fill: { color }, line: { color } });
  s.addText(title, { x: x+0.31, y, w: 4.8, h: 0.22, fontSize: 14, bold: true, color: C.ink, margin: 0 });
  s.addText(body, { x: x+0.31, y: y+0.32, w: 5.1, h: 0.48, fontSize: 10.5, color: C.muted, breakLine: false, margin: 0.01, fit: 'shrink' });
}
function metric(s, x, y, value, label, color=C.green) {
  s.addShape(pptx.ShapeType.roundRect, { x, y, w: 2.35, h: 1.05, rectRadius: 0.08, fill: { color: C.white }, line: { color: C.line, width: 1 } });
  s.addText(value, { x: x+0.12, y: y+0.14, w: 2.1, h: 0.38, fontSize: 24, bold: true, color, align: 'center', margin: 0 });
  s.addText(label, { x: x+0.15, y: y+0.63, w: 2.05, h: 0.22, fontSize: 9.5, color: C.muted, align: 'center', margin: 0 });
}
function drawSuite(s, x, y, w, h, mode='front') {
  const lw = 1.2;
  if (mode === 'front') {
    s.addShape(pptx.ShapeType.rect, { x, y, w, h: h*0.64, fill: { color: C.room }, line: { color: '6A9ED6', width: lw } });
    s.addText('병실 R', { x, y: y+h*0.26, w, h: 0.22, fontSize: 12, bold: true, color: '275177', align: 'center', margin: 0 });
    s.addShape(pptx.ShapeType.rect, { x, y: y+h*0.64, w: w*0.48, h: h*0.36, fill: { color: C.ante }, line: { color: 'C48833', width: lw } });
    s.addShape(pptx.ShapeType.rect, { x: x+w*0.48, y: y+h*0.64, w: w*0.52, h: h*0.36, fill: { color: C.wc }, line: { color: '6DA36A', width: lw } });
    s.addText('전실 A', { x, y: y+h*0.77, w: w*0.48, h: 0.18, fontSize: 9.8, bold: true, color: '7A541D', align: 'center', margin: 0 });
    s.addText('WC', { x: x+w*0.48, y: y+h*0.77, w: w*0.52, h: 0.18, fontSize: 9.8, bold: true, color: '386E36', align: 'center', margin: 0 });
  } else {
    s.addShape(pptx.ShapeType.rect, { x, y, w: w*0.58, h: h, fill: { color: C.room }, line: { color: '6A9ED6', width: lw } });
    s.addShape(pptx.ShapeType.rect, { x: x+w*0.58, y: y, w: w*0.42, h: h*0.38, fill: { color: C.wc }, line: { color: '6DA36A', width: lw } });
    s.addShape(pptx.ShapeType.rect, { x: x+w*0.58, y: y+h*0.38, w: w*0.42, h: h*0.62, fill: { color: C.ante }, line: { color: 'C48833', width: lw } });
    s.addText('R', { x, y: y+h*0.45, w: w*0.58, h: 0.18, fontSize: 12, bold: true, color: '275177', align: 'center', margin: 0 });
    s.addText('WC', { x: x+w*0.58, y: y+h*0.13, w: w*0.42, h: 0.16, fontSize: 8.5, bold: true, color: '386E36', align: 'center', margin: 0 });
    s.addText('A', { x: x+w*0.58, y: y+h*0.63, w: w*0.42, h: 0.16, fontSize: 8.5, bold: true, color: '7A541D', align: 'center', margin: 0 });
  }
}
function drawMiniPlan(s, x, y, w, h, theme='light') {
  const line = theme === 'dark' ? 'BFE9DF' : '2F6B5F';
  s.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: theme === 'dark' ? '244A44' : C.white, transparency: theme === 'dark' ? 4 : 0 }, line: { color: line, width: 1.2 } });
  s.addShape(pptx.ShapeType.rect, { x: x+w*0.12, y: y+h*0.45, w: w*0.76, h: h*0.13, fill: { color: C.corr }, line: { color: C.corr } });
  for (let i=0;i<4;i++) drawSuite(s, x+w*(0.14+i*0.18), y+h*0.12, w*0.13, h*0.28, 'front');
  for (let i=0;i<3;i++) drawSuite(s, x+w*(0.22+i*0.21), y+h*0.62, w*0.13, h*0.28, 'front');
  s.addShape(pptx.ShapeType.rect, { x: x+w*0.72, y: y+h*0.63, w: w*0.13, h: h*0.22, fill: { color: C.reserve }, line: { color: 'B6AA98' } });
}
function optionCard(s, x, y, title, subtitle, sig, accent) {
  s.addShape(pptx.ShapeType.roundRect, { x, y, w: 3.75, h: 1.58, rectRadius: 0.08, fill: { color: C.white }, line: { color: accent, width: 1.4 } });
  s.addShape(pptx.ShapeType.rect, { x, y, w: 0.12, h: 1.58, fill: { color: accent }, line: { color: accent } });
  s.addText(title, { x: x+0.25, y: y+0.15, w: 3.2, h: 0.25, fontSize: 13, bold: true, color: C.ink, margin: 0 });
  s.addText(subtitle, { x: x+0.25, y: y+0.50, w: 3.2, h: 0.22, fontSize: 9.5, color: C.muted, margin: 0 });
  s.addText(sig, { x: x+0.25, y: y+0.88, w: 3.25, h: 0.38, fontSize: 9, color: accent, bold: true, margin: 0, fit: 'shrink' });
}

function makeSlides() {
  titleSlide();
  let s = addSlide('오늘 해결한 핵심 문제');
  s.addText('기존 상태는 “조건은 맞지만 보기 좋지 않은 평면”에 가까웠음', { x: 0.65, y: 1.18, w: 7.8, h: 0.32, fontSize: 14.5, color: C.muted, margin: 0 });
  bullet(s, 0.85, 1.88, '병동 유닛이 뻣뻣함', 'WC가 병실 뒤/측면으로 튀면서 유닛 footprint가 불규칙하고 산만해짐', C.red);
  bullet(s, 0.85, 3.02, '빈 공간이 너무 많음', '남은 usable area가 비어 보이며, 대안의 완성도가 낮아 보임', C.gold);
  bullet(s, 0.85, 4.16, '옵션이 하나처럼 보임', 'Generate Layout Options가 3안을 만들지만 실제 차이가 약하거나, 왼쪽 버튼은 단일안만 생성', C.green);
  s.addShape(pptx.ShapeType.roundRect, { x: 7.05, y: 1.45, w: 5.55, h: 4.95, rectRadius: 0.08, fill: { color: C.white }, line: { color: C.line } });
  s.addText('Before → After Target', { x: 7.38, y: 1.75, w: 4.8, h: 0.25, fontSize: 16, bold: true, color: C.dark, margin: 0 });
  drawSuite(s, 7.55, 2.4, 1.7, 1.55, 'old');
  s.addText('기존: WC가 튀는 유닛', { x: 7.28, y: 4.1, w: 2.2, h: 0.22, fontSize: 9.5, color: C.muted, align: 'center', margin: 0 });
  s.addShape(pptx.ShapeType.rightArrow, { x: 9.55, y: 2.82, w: 0.78, h: 0.42, fill: { color: C.gold }, line: { color: C.gold } });
  drawSuite(s, 10.55, 2.35, 1.7, 1.65, 'front');
  s.addText('신규: 전실+WC 병렬형', { x: 10.3, y: 4.1, w: 2.2, h: 0.22, fontSize: 9.5, color: C.muted, align: 'center', margin: 0 });

  s = addSlide('병실 유닛 재정의: Front-Service Suite');
  s.addText('화장실은 반드시 병실 입구 반대편일 필요가 없음. 중요한 것은 복도-전실-병실-WC의 관계 유지.', { x: 0.65, y: 1.18, w: 11.7, h: 0.32, fontSize: 14, color: C.muted, margin: 0 });
  s.addShape(pptx.ShapeType.roundRect, { x: 0.78, y: 1.8, w: 5.35, h: 4.45, rectRadius: 0.08, fill: { color: C.white }, line: { color: C.line } });
  drawSuite(s, 1.65, 2.3, 3.55, 2.95, 'front');
  s.addShape(pptx.ShapeType.rect, { x: 2.32, y: 5.55, w: 2.25, h: 0.32, fill: { color: C.corr }, line: { color: C.corr } });
  s.addText('복도', { x: 2.32, y: 5.62, w: 2.25, h: 0.14, fontSize: 8.5, bold: true, color: C.white, align: 'center', margin: 0 });
  bullet(s, 6.65, 1.95, '전실은 복도와 직접 접속', '격리병실 출입 전 완충공간의 역할을 유지', C.green);
  bullet(s, 6.65, 3.05, 'WC는 병실에 붙은 ensuite로 해석', '전실 옆 배치는 가능하되, 접근은 병실 내부에서 이뤄지는 것으로 설계', C.teal);
  bullet(s, 6.65, 4.15, '유닛 footprint가 정돈됨', '복도에 일정한 리듬으로 붙기 쉬워지고 빈 포켓이 줄어듦', C.gold);

  s = addSlide('배치 알고리즘 개선: 질서 + 채움');
  s.addText('“그냥 들어가는 배치”에서 “복도 리듬을 따라 정돈되는 배치”로 전환', { x: 0.65, y: 1.18, w: 10.8, h: 0.32, fontSize: 14, color: C.muted, margin: 0 });
  const steps = [
    ['1', 'Adaptive Corridor', '사용자가 그린 외곽 안에서 연결 복도 네트워크 생성'],
    ['2', 'Ordered Anchors', '복도 방향별 lane/side를 정렬해 병실 배치 리듬 형성'],
    ['3', 'Supplemental Suites', '목표 병실 수가 부족하면 남은 포켓에 보충 배치'],
    ['4', 'Neutral Infill', '남는 usable area는 support reserve로 시각적 채움']
  ];
  steps.forEach((it, i) => {
    const x = 0.78 + i*3.1;
    s.addShape(pptx.ShapeType.roundRect, { x, y: 2.0, w: 2.65, h: 2.0, rectRadius: 0.08, fill: { color: i%2?C.white:C.mint }, line: { color: C.line } });
    s.addShape(pptx.ShapeType.ellipse, { x: x+0.18, y: 2.22, w: 0.52, h: 0.52, fill: { color: [C.green,C.teal,C.gold,C.red][i] }, line: { color: [C.green,C.teal,C.gold,C.red][i] } });
    s.addText(it[0], { x: x+0.18, y: 2.34, w: 0.52, h: 0.12, fontSize: 11, bold: true, color: C.white, align: 'center', margin: 0 });
    s.addText(it[1], { x: x+0.83, y: 2.2, w: 1.55, h: 0.22, fontSize: 12.5, bold: true, color: C.dark, margin: 0 });
    s.addText(it[2], { x: x+0.27, y: 2.9, w: 2.15, h: 0.6, fontSize: 9.5, color: C.muted, margin: 0.01, fit: 'shrink' });
  });
  drawMiniPlan(s, 2.15, 4.65, 9.1, 1.55, 'light');

  s = addSlide('3개 배치 타입이 실제로 생성되도록 수정');
  s.addText('이제 버튼을 누르면 3개의 이름 있는 대안이 생성되고, 각 대안은 서로 다른 suite 우선순위를 사용', { x: 0.65, y: 1.18, w: 11.5, h: 0.32, fontSize: 14, color: C.muted, margin: 0 });
  optionCard(s, 0.78, 1.85, 'Option 1 · 면적효율 우선안', 'front_service 우선 · compact footprint', 'R96 | A53 | WC32 | C174', C.green);
  optionCard(s, 4.78, 1.85, 'Option 2 · 감염통제 우선안', 'deluxe/standard 중심 · 완충 안정성', 'R96 | A38 | WC32 | C190', C.gold);
  optionCard(s, 8.78, 1.85, 'Option 3 · 간호효율 우선안', 'standard/compact 중심 · 짧은 동선', 'R72 | A38 | WC32 | C190', C.teal);
  s.addShape(pptx.ShapeType.roundRect, { x: 1.2, y: 4.25, w: 10.95, h: 1.32, rectRadius: 0.08, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText('브라우저 검증 결과: optionCount 3 · cardCount 3 · distinct layout 3 · 병실 8/8/8', { x: 1.45, y: 4.72, w: 10.45, h: 0.28, fontSize: 16, bold: true, color: C.white, align: 'center', margin: 0 });

  s = addSlide('UI 버그 수정: 왼쪽 버튼도 3개 대안 생성');
  s.addText('사용자가 누르는 첫 번째 버튼이 단일 평면만 생성하던 문제를 제거', { x: 0.65, y: 1.18, w: 9.8, h: 0.32, fontSize: 14, color: C.muted, margin: 0 });
  s.addShape(pptx.ShapeType.roundRect, { x: 0.9, y: 1.9, w: 5.3, h: 2.8, rectRadius: 0.08, fill: { color: C.white }, line: { color: C.line } });
  s.addText('Before', { x: 1.2, y: 2.15, w: 1.2, h: 0.22, fontSize: 14, bold: true, color: C.red, margin: 0 });
  s.addText('Place Compact Ward Modules\n→ placeCompactWardModules()\n→ 단일 평면만 표시', { x: 1.2, y: 2.75, w: 4.3, h: 0.9, fontSize: 15, color: C.ink, margin: 0.02, breakLine: false });
  s.addShape(pptx.ShapeType.rightArrow, { x: 6.45, y: 2.92, w: 0.78, h: 0.45, fill: { color: C.gold }, line: { color: C.gold } });
  s.addShape(pptx.ShapeType.roundRect, { x: 7.45, y: 1.9, w: 5.0, h: 2.8, rectRadius: 0.08, fill: { color: C.mint }, line: { color: C.green } });
  s.addText('After', { x: 7.75, y: 2.15, w: 1.2, h: 0.22, fontSize: 14, bold: true, color: C.green, margin: 0 });
  s.addText('Place Compact Ward Modules\n→ generateLayoutOptions()\n→ 3개 대안 카드 표시', { x: 7.75, y: 2.75, w: 4.2, h: 0.9, fontSize: 15, color: C.ink, margin: 0.02, breakLine: false });
  metric(s, 2.05, 5.25, '3', '옵션 카드', C.green); metric(s, 5.5, 5.25, '3', '실제 다른 평면', C.teal); metric(s, 8.95, 5.25, '25', '회귀 테스트 통과', C.gold);

  s = addSlide('검증 결과 요약');
  s.addText('코드 수준 테스트와 실제 브라우저 실행을 모두 확인', { x: 0.65, y: 1.18, w: 8.0, h: 0.32, fontSize: 14, color: C.muted, margin: 0 });
  metric(s, 0.9, 1.85, '25', 'pytest passed', C.green);
  metric(s, 3.65, 1.85, '100%', '면적/외곽 채움', C.teal);
  metric(s, 6.4, 1.85, '3', 'distinct options', C.gold);
  metric(s, 9.15, 1.85, 'OK', '복도 연결성', C.red);
  s.addShape(pptx.ShapeType.roundRect, { x: 0.9, y: 3.55, w: 11.55, h: 2.15, rectRadius: 0.08, fill: { color: C.white }, line: { color: C.line } });
  s.addText('확인된 hard constraints', { x: 1.2, y: 3.85, w: 3.3, h: 0.24, fontSize: 15, bold: true, color: C.dark, margin: 0 });
  const checks = ['음압병실 ↔ 전실 인접', '음압병실 ↔ WC 인접', '전실 ↔ 통제복도 인접', '모든 프로그램 실 복도 접근성', '청결/오염 직접접촉 방지'];
  checks.forEach((t,i)=>{ s.addText('✓ ' + t, { x: 1.25 + (i%2)*5.3, y: 4.35 + Math.floor(i/2)*0.42, w: 4.8, h: 0.2, fontSize: 12.2, color: i%2?C.teal:C.green, bold: true, margin: 0 }); });

  s = addSlide('남은 개선 방향');
  s.addText('오늘은 생성 안정성과 보기 좋은 대안 구조를 우선 해결. 다음은 “평면 미감 점수”와 지원공간 세분화.', { x: 0.65, y: 1.18, w: 11.6, h: 0.32, fontSize: 14, color: C.muted, margin: 0 });
  bullet(s, 0.9, 1.95, 'Aesthetic Score 분리', '법규 점수와 별개로 정렬감, 리듬, 잔여공간 품질을 평가하는 미감 점수 도입', C.green);
  bullet(s, 0.9, 3.12, 'Support Program 세분화', 'S reserve를 설비실/창고/대기/비품실 등 프로그램으로 더 촘촘히 변환', C.teal);
  bullet(s, 0.9, 4.29, '실제 기준 치수 보강', '국내 전실·화장실·간호지원실 최소면적 기준을 추가 조사해 rule checker 강화', C.gold);
  s.addShape(pptx.ShapeType.roundRect, { x: 7.05, y: 1.85, w: 5.25, h: 3.65, rectRadius: 0.08, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText('다음 목표', { x: 7.45, y: 2.25, w: 2.0, h: 0.28, fontSize: 17, bold: true, color: C.white, margin: 0 });
  s.addText('“법규를 통과하는 배치”에서\n“발표용으로 설득력 있는 평면”으로', { x: 7.45, y: 3.1, w: 4.25, h: 0.8, fontSize: 20, bold: true, color: 'DDEFE9', margin: 0.02, fit: 'shrink' });
  s.addText('정돈감 · 밀도 · 대안성 · 설명가능성', { x: 7.45, y: 4.58, w: 4.3, h: 0.25, fontSize: 12.5, color: 'F2D49B', margin: 0 });
}
makeSlides();

pptx.writeFile({ fileName: path.join(outDir, 'infectious_ward_auto_layout_update_20260601.pptx') });

// HTML preview for visual QA
const html = `<!doctype html><html><head><meta charset="utf-8"><title>Deck Preview</title><style>
body{margin:0;background:#e8e1d4;font-family:'Malgun Gothic','Noto Sans KR',Arial,sans-serif;color:#24312F}.slide{width:1280px;height:720px;margin:24px auto;background:#F7F4ED;position:relative;box-shadow:0 10px 30px #0003;overflow:hidden}.dark{background:#18332F;color:white}.k{position:absolute;left:60px;top:34px;color:#2F6B5F;font-size:12px;font-weight:800;letter-spacing:2px}.t{position:absolute;left:60px;top:58px;font-size:34px;font-weight:900}.sub{position:absolute;left:64px;top:116px;color:#706B62;font-size:20px}.dark .sub{color:#DCEAE5}.card{background:white;border:2px solid #CDBFAD;border-radius:14px;padding:20px;box-sizing:border-box}.metric{background:white;border:1px solid #CDBFAD;border-radius:14px;text-align:center}.metric b{font-size:46px;color:#2F6B5F}.mini{position:absolute;border:2px solid #2F6B5F;border-radius:12px;background:white}.room{background:#BFD8FF}.ante{background:#F3D9A4}.wc{background:#C9E6C7}.corr{background:#7BC6B4}.reserve{background:#D8CFBD}.footer{position:absolute;left:58px;right:58px;bottom:25px;border-top:1px solid #D6CCBB;color:#706B62;font-size:12px;padding-top:6px}.dark .footer{border-top-color:#315F55;color:#ADC8C1}.tag{display:inline-block;border-radius:10px;padding:12px 20px;margin-right:18px;font-weight:800}.g{background:#3AA99E}.y{background:#F2D49B;color:#18332F}.col{position:absolute}.bullet{font-size:23px;font-weight:800}.bullet small{display:block;font-size:17px;font-weight:400;color:#706B62;margin-top:10px;line-height:1.45}.darkbox{background:#18332F;color:white;border-radius:14px}.opt{border-radius:14px;background:white;border:3px solid #2F6B5F;padding:20px;box-sizing:border-box}.opt small{color:#706B62}.sig{font-weight:800;color:#2F6B5F}.oldunit,.unit{position:relative}.unit div,.oldunit div{position:absolute;border:2px solid #777;box-sizing:border-box;text-align:center;font-weight:800;display:flex;align-items:center;justify-content:center}
</style></head><body>
<div class="slide dark"><div class="t" style="top:90px;font-size:54px;line-height:1.25">감염병동 모듈<br>자동배치 툴 개선 리포트</div><div class="sub" style="top:260px">오늘 수정사항 중심 · 배치 미감 / 빈 공간 / 3개 대안 생성 개선</div><div style="position:absolute;left:70px;top:330px"><span class="tag g">25 tests passed</span><span class="tag y">3 distinct options</span></div><div class="footer">Graduation_Hospital_Planner / Auto Layout v2</div></div>
<div class="slide"><div class="k">TODAY UPDATE</div><div class="t">오늘 해결한 핵심 문제</div><div class="sub">기존 상태는 “조건은 맞지만 보기 좋지 않은 평면”에 가까웠음</div><div class="col" style="left:85px;top:180px;width:520px"><p class="bullet">● 병동 유닛이 뻣뻣함<small>WC가 병실 뒤/측면으로 튀면서 footprint가 불규칙하고 산만해짐</small></p><p class="bullet">● 빈 공간이 너무 많음<small>남은 usable area가 비어 보여 평면 완성도가 낮아 보임</small></p><p class="bullet">● 옵션이 하나처럼 보임<small>3안을 만든다고 되어 있지만 실제 차이가 약하거나 왼쪽 버튼은 단일안만 생성</small></p></div><div class="card" style="position:absolute;left:690px;top:150px;width:500px;height:380px"><b style="font-size:28px">Before → After Target</b><p style="font-size:18px;color:#706B62">Rigid suite에서 front-service compact suite로</p><div class="oldunit" style="position:absolute;left:40px;top:135px;width:150px;height:150px"><div class="room" style="left:0;top:0;width:88px;height:150px">R</div><div class="wc" style="left:88px;top:0;width:62px;height:58px">WC</div><div class="ante" style="left:88px;top:58px;width:62px;height:92px">A</div></div><div style="position:absolute;left:220px;top:190px;font-size:34px;color:#D99B3D">→</div><div class="unit" style="position:absolute;left:275px;top:135px;width:155px;height:150px"><div class="room" style="left:0;top:0;width:155px;height:95px">R</div><div class="ante" style="left:0;top:95px;width:72px;height:55px">A</div><div class="wc" style="left:72px;top:95px;width:83px;height:55px">WC</div></div></div><div class="footer">Graduation Hospital Planner · Auto Layout v2</div></div>
<div class="slide"><div class="k">TODAY UPDATE</div><div class="t">병실 유닛 재정의: Front-Service Suite</div><div class="sub">중요한 것은 복도-전실-병실-WC의 관계 유지</div><div class="card" style="position:absolute;left:90px;top:180px;width:500px;height:360px"><div class="unit" style="width:340px;height:260px;margin:30px auto"><div class="room" style="left:0;top:0;width:340px;height:165px">병실 R</div><div class="ante" style="left:0;top:165px;width:160px;height:95px">전실 A</div><div class="wc" style="left:160px;top:165px;width:180px;height:95px">WC</div></div></div><div class="col" style="left:655px;top:190px;width:520px"><p class="bullet">● 전실은 복도와 직접 접속<small>격리병실 출입 전 완충공간의 역할 유지</small></p><p class="bullet">● WC는 병실에 붙은 ensuite로 해석<small>전실 옆 배치는 가능하되 접근은 병실 내부에서 이뤄지는 것으로 설계</small></p><p class="bullet">● 유닛 footprint가 정돈됨<small>복도에 일정한 리듬으로 붙기 쉬워지고 빈 포켓이 줄어듦</small></p></div><div class="footer">Graduation Hospital Planner · Auto Layout v2</div></div>
<div class="slide"><div class="k">TODAY UPDATE</div><div class="t">배치 알고리즘 개선: 질서 + 채움</div><div class="sub">복도 리듬을 따라 정돈되는 배치로 전환</div><div style="position:absolute;left:75px;top:190px;display:flex;gap:26px"><div class="card" style="width:280px;height:190px"><b>1 Adaptive Corridor</b><p>외곽 안에서 연결 복도 네트워크 생성</p></div><div class="card" style="width:280px;height:190px;background:#DDEFE9"><b>2 Ordered Anchors</b><p>lane/side 정렬로 병실 리듬 형성</p></div><div class="card" style="width:280px;height:190px"><b>3 Supplemental Suites</b><p>목표 병실 부족 시 포켓 보충 배치</p></div><div class="card" style="width:280px;height:190px;background:#DDEFE9"><b>4 Neutral Infill</b><p>잔여 공간을 support reserve로 채움</p></div></div><div class="footer">Graduation Hospital Planner · Auto Layout v2</div></div>
<div class="slide"><div class="k">TODAY UPDATE</div><div class="t">3개 배치 타입이 실제로 생성되도록 수정</div><div class="sub">각 대안은 서로 다른 suite 우선순위 사용</div><div class="opt" style="position:absolute;left:75px;top:185px;width:360px;height:170px"><b>Option 1 · 면적효율 우선안</b><br><small>front_service 우선</small><p class="sig">R96 | A53 | WC32 | C174</p></div><div class="opt" style="position:absolute;left:460px;top:185px;width:360px;height:170px;border-color:#D99B3D"><b>Option 2 · 감염통제 우선안</b><br><small>deluxe/standard 중심</small><p class="sig" style="color:#D99B3D">R96 | A38 | WC32 | C190</p></div><div class="opt" style="position:absolute;left:845px;top:185px;width:360px;height:170px;border-color:#3AA99E"><b>Option 3 · 간호효율 우선안</b><br><small>standard/compact 중심</small><p class="sig" style="color:#3AA99E">R72 | A38 | WC32 | C190</p></div><div class="darkbox" style="position:absolute;left:120px;top:430px;width:1040px;height:110px;text-align:center;padding-top:38px;font-size:24px;font-weight:900">브라우저 검증: optionCount 3 · cardCount 3 · distinct layout 3 · 병실 8/8/8</div><div class="footer">Graduation Hospital Planner · Auto Layout v2</div></div>
<div class="slide"><div class="k">TODAY UPDATE</div><div class="t">UI 버그 수정: 왼쪽 버튼도 3개 대안 생성</div><div class="sub">사용자가 누르는 첫 번째 버튼이 단일 평면만 생성하던 문제 제거</div><div class="card" style="position:absolute;left:90px;top:190px;width:500px;height:260px"><b style="color:#B85042;font-size:24px">Before</b><p style="font-size:24px;line-height:1.5">Place Compact Ward Modules<br>→ placeCompactWardModules()<br>→ 단일 평면만 표시</p></div><div class="card" style="position:absolute;left:700px;top:190px;width:500px;height:260px;background:#DDEFE9;border-color:#2F6B5F"><b style="color:#2F6B5F;font-size:24px">After</b><p style="font-size:24px;line-height:1.5">Place Compact Ward Modules<br>→ generateLayoutOptions()<br>→ 3개 대안 카드 표시</p></div><div class="footer">Graduation Hospital Planner · Auto Layout v2</div></div>
<div class="slide"><div class="k">TODAY UPDATE</div><div class="t">검증 결과 요약</div><div class="sub">코드 수준 테스트와 실제 브라우저 실행을 모두 확인</div><div style="position:absolute;left:90px;top:190px;display:flex;gap:35px"><div class="metric" style="width:220px;height:120px"><b>25</b><br>pytest passed</div><div class="metric" style="width:220px;height:120px"><b>100%</b><br>면적/외곽 채움</div><div class="metric" style="width:220px;height:120px"><b>3</b><br>distinct options</div><div class="metric" style="width:220px;height:120px"><b>OK</b><br>복도 연결성</div></div><div class="card" style="position:absolute;left:90px;top:390px;width:1090px;height:150px"><b>확인된 hard constraints</b><p>✓ 음압병실↔전실 인접　✓ 음압병실↔WC 인접　✓ 전실↔통제복도 인접<br>✓ 모든 프로그램 실 복도 접근성　✓ 청결/오염 직접접촉 방지</p></div><div class="footer">Graduation Hospital Planner · Auto Layout v2</div></div>
<div class="slide"><div class="k">TODAY UPDATE</div><div class="t">남은 개선 방향</div><div class="sub">다음은 “평면 미감 점수”와 지원공간 세분화</div><div class="col" style="left:90px;top:190px;width:600px"><p class="bullet">● Aesthetic Score 분리<small>정렬감, 리듬, 잔여공간 품질 평가</small></p><p class="bullet">● Support Program 세분화<small>S reserve를 설비실/창고/대기/비품실로 변환</small></p><p class="bullet">● 실제 기준 치수 보강<small>국내 전실·화장실·간호지원실 최소면적 기준 추가 조사</small></p></div><div class="darkbox" style="position:absolute;left:700px;top:190px;width:500px;height:330px;padding:40px;box-sizing:border-box"><b style="font-size:28px">다음 목표</b><p style="font-size:30px;font-weight:900;line-height:1.35;color:#DDEFE9">“법규를 통과하는 배치”에서<br>“발표용으로 설득력 있는 평면”으로</p><p style="color:#F2D49B;font-size:18px">정돈감 · 밀도 · 대안성 · 설명가능성</p></div><div class="footer">Graduation Hospital Planner · Auto Layout v2</div></div>
</body></html>`;
fs.writeFileSync(path.join(outDir, 'infectious_ward_auto_layout_update_20260601_preview.html'), html, 'utf8');
console.log('WROTE', path.join(outDir, 'infectious_ward_auto_layout_update_20260601.pptx'));
console.log('WROTE', path.join(outDir, 'infectious_ward_auto_layout_update_20260601_preview.html'));
