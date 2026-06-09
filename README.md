# Graduation Hospital Planner (병원 평면 자동배치 툴)

졸업작품용 **AI·로봇 친화적 모듈러 감염병 전문병원 / 소규모 감염병 대응센터 평면 자동 배치 툴** 프로젝트입니다.

## 💡 핵심 아이디어
큰 그리드 안에서 사용자가 드래그/칸 선택으로 병원 한 층의 외곽 형태(사용 가능 영역)를 정하면, 툴이 그 내부에 병실, 전실, 복도 등 병원 기능 모듈을 감염 통제 규칙과 공간 비율 설계 기준에 맞춰 자동 배치합니다.

- 제한된 격자 판 안에
- 크기와 형태가 다른 모듈들을
- 건축 법규, 인접 조건, 위생 조건에 맞춰 똑똑하게 끼워 넣는 방식입니다.

---

## ☁️ Streamlit Cloud 배포

이 프로젝트는 루트의 `streamlit_app.py`를 배포 엔트리포인트로 사용합니다.

Streamlit Community Cloud에서 새 앱을 만들 때:

- Repository: 이 프로젝트를 올린 GitHub 저장소
- Branch: `main`
- Main file path: `streamlit_app.py`
- Python dependencies: `requirements.txt` 자동 인식

`src/graduation_hospital_planner/grid_drag_canvas_app.py`가 실제 앱 본체이고, `streamlit_app.py`는 Cloud가 안정적으로 찾을 수 있게 해주는 얇은 wrapper입니다. `assets/models/ward_furniture/*.glb`와 `data/modules_ward_v01.json`은 repo에 포함되어야 3D GLB 가구와 모듈 DB가 배포 환경에서도 로딩됩니다.

---

## 🚀 다른 컴퓨터에서 실행하기 (무설치 원스톱 방법)

새로운 컴퓨터나 환경에서 이 툴을 사용하는 가장 빠르고 안전한 방법입니다:

1. **ZIP 압축 풀기:** 이 프로젝트 폴더를 새 컴퓨터의 원하는 위치에 압축 해제합니다.
2. **배치파일 실행:** 폴더 안의 `setup_and_run.bat` 파일을 더블클릭합니다.
3. **자동 세팅:** 처음 실행 시 Python 설치 여부를 체크하고, 로컬 가상환경(`.venv`)을 자동 생성한 후 필요한 패키지(`Streamlit`, `ReportLab` 등)를 알아서 다운로드 및 설치합니다.
4. **브라우저 실행:** 세팅이 완료되면 자동으로 브라우저가 열리며 `Hospital Floor Grid Painter Prototype` 앱이 구동됩니다.

### 💻 수동 실행 방법 (개발자용)
만약 터미널에서 수동으로 설치하고 기동하려는 경우 다음 명령을 수행합니다:
```bat
cd Graduation_Hospital_Planner
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run src\graduation_hospital_planner\grid_drag_canvas_app.py
```

---

## 📁 프로젝트 폴더 트리 및 파일 구성

- 📂 `src/graduation_hospital_planner/`
  - `grid_drag_canvas_app.py` : HTML Canvas와 Python Streamlit이 결합된 핵심 그리드 페인터 및 자동배치 앱
  - `grid_logic.js` : 과거 JS 로직 분리/참조 파일
- 📂 `src/scripts/`
  - 발표 PDF/PPTX 생성용 보조 스크립트
- 📂 `prototype/`
  - `grid_drag_canvas_app.py` : 과거 실행 경로 호환용 wrapper
- 📂 `data/`
  - `modules_ward_v01.json` : 음압병실, 전실, 화장실, 복도 등 병동 핵심 실들의 면적과 속성이 담긴 모듈 DB
- 📂 `ref/docs/`
  - `01_development_blueprint.md` : 프로젝트 요구사항, 컨셉 및 개발 로드맵 청사진
  - `02_module_database_guide.md` : 병원 모듈 데이터베이스 설계 스키마 및 가이드
  - `03_architectural_standards_research.md` : 보건복지부 고시, 의료법 시행규칙 및 국제 가이드라인(iHFG)에 기반한 건축 표준 및 가로세로비 설계 기준 연구
- 📂 `exports/`
  - 발표 및 진척도 공유용 PDF 파일 보관함
- 📂 `ref/research_sources/`
  - `korea_negative_pressure_isolation_standard_2024.pdf` : 국내 최신 음압격리병실 설치 및 운영 규정 PDF 원본
- 📄 `requirements.txt` : 필요한 파이썬 라이브러리 목록
- 📄 `setup_and_run.bat` : 원스톱 가상환경 구축 및 앱 빌더 스크립트
- 📄 `run_grid_drag_app.bat` : 기본 실행용 스크립트
- 📄 `NEXT_SESSION_HANDOFF.md` : 대화 세션 전환을 위한 진척 상황 백업 및 설계 컨텍스트 인수인계 파일

---

## ⚠️ 주의 사항
- 새로운 컴퓨터에 **Python 3(3.8 ~ 3.11 권장)**이 반드시 설치되어 있어야 합니다. (설치 시 "Add python.exe to PATH" 체크 필수)
- 컴퓨터별로 파이썬 구동 환경이 달라 충돌을 유발할 수 있으므로, 용량이 큰 `.venv` 폴더는 압축 해제 대상에 포함시키지 않았습니다. `setup_and_run.bat`을 실행하면 새 환경에 맞춰 안전하게 재생성됩니다.
- 브라우저에 화면이 바로 뜨지 않는다면, 터미널에 출력된 `http://localhost:8501` 주소를 직접 복사하여 브라우저에 붙여넣어 주십시오.
