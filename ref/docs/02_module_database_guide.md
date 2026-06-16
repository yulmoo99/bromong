# Hospital Module Database Guide (모듈 데이터베이스 구조 및 가이드)

이 문서는 병원 평면 자동배치 툴에서 사용되는 **모듈 데이터베이스 스키마(Schema)** 및 **v0.1 컴팩트 병동 필수 모듈 데이터 구조**를 설명하는 설계 가이드라인입니다.

자동배치 엔진이 동작하기 전, 모든 실의 설계 치수, 면적, 인접 조건, 감염 격리 구역 지정 등이 이 규격에 의해 정의됩니다.

---

## 1. 모듈 조사 근거 및 수집 범위
정확하고 신뢰성 높은 배치를 위해 데이터베이스는 다음과 같은 국내외 공식 기준 및 임상 사례를 지속적으로 수집하여 반영하도록 설계되어 있습니다.
- **국내 의료법 및 의료기관 시설규격** (음압격리병실 설치/운영 기준 최신 고시)
- **국제 보건의료시설 가이드라인** (IHFG, CDC, WHO 병원건축 가이드라인)
- **신뢰성 등급 체계 (Confidence Level):**
  - `verified_law` : 국내 건축/의료 법령에 직접적인 수치가 고시되어 있는 확실한 법정 기준. (예: 음압병실 면적 10㎡ 이상)
  - `guideline` : 명문화된 국내 면적 규정은 없으나, iHFG 등 국제 표준 가이드라인에 명시된 권장 치수.
  - `placeholder` : 초기 개발 및 알고리즘 구동을 위해 가정한 임시 기획 수치. (추후 리서치를 통한 고도화 필요)

---

## 2. 모듈 데이터 필드 규격 (Database Schema)

모듈 데이터베이스는 `JSON` 포맷으로 관리되며, 각 실은 다음과 같은 속성 스키마를 따릅니다:

```json
{
  "id": "module_unique_id",
  "name_ko": "실 한국어 이름",
  "name_en": "English name of the room",
  "department": "ward / surgery / emergency / diagnosis / support / logistics / public",
  "infection_zone": "clean / controlled / contaminated / public / service",
  "min_area_m2": 10.0,
  "planning_area_m2": 20.25,
  "min_width_m": 3.0,
  "min_depth_m": 3.0,
  "preferred_grid_sizes": [[3, 3], [3, 4]],
  "shape_policy": {
    "shape_type": "rectangular / L-shape / custom",
    "aspect_ratio_preferred_max": 1.5,
    "aspect_ratio_hard_max": 2.0
  },
  "requires_corridor_access": true,
  "corridor_type": "clean / dirty / both / public / service",
  "requires_anteroom": false,
  "pressure_requirement": "positive / negative / neutral / unknown",
  "adjacency_rules": {
    "adjacency_required": ["anteroom_id"],
    "adjacency_preferred": ["nurse_station_id"],
    "adjacency_forbidden": ["soiled_waste_id"]
  },
  "flow_notes": "동선, 전실, 청결/오염 전환에 관한 설계 코멘트",
  "legal_basis": ["보건복지부 고시 제2024-X호 등"],
  "design_sources": ["iHFG Isolation Rooms Standard Component 등"],
  "confidence": "verified_law / guideline / placeholder"
}
```

---

## 3. v0.1 컴팩트 감염병동 필수 모듈 정의

좁은 대지나 소규모(1500㎡급) 감염병 대응센터에 먼저 적용하기 위해, 1차적으로 **7개의 감염격리병동 핵심 필수 모듈**을 선정하여 DB화했습니다.

| 코드 | 모듈명 (KO) | 모듈명 (EN) | 감염 구역 (Infection Zone) | 음압 기준 (Pressure) | 신뢰 등급 (Confidence) |
|---|---|---|---|---|---|
| **C** | 통제 복도 | Controlled Corridor | controlled | neutral | guideline |
| **R** | 음압격리병실 | Negative Pressure Patient Room | contaminated | negative (≤ -2.5Pa) | **verified_law** |
| **A** | 전실 | Anteroom | clean/buffer | intermediate (≤ -2.5Pa) | **verified_required** |
| **WC** | 전용 화장실/샤워실 | Ensuite Toilet & Shower | contaminated | negative | **verified_required** |
| **N** | 간호스테이션 | Nurse Station | clean | neutral | guideline |
| **CL** | 청결물품 알코브 | Clean Supply Alcove | clean | neutral | guideline |
| **D** | 오염물/폐기물 임시보관 | Soiled Waste Holding | contaminated | negative | guideline |

### 3.1 주요 모듈 세부 적용 기준 (v0.1)

#### ① 음압격리병실 (R)
- **법정 근거:** 보건복지부 고시, 「음압격리병실 설치 및 운영에 관한 고시」 [별표], 2024-10-25 시행.
- **면적 기준:** **병상 1개당 최소 10㎡ 이상**. (화장실 및 전실 면적은 법적으로 이 면적에서 완전히 배제해야 함)
- **환기 및 배기:** 시간당 6회 이상 환기 및 -2.5Pa 이상의 상시 음압 유지 필수.

#### ② 전실 / PPE·손위생 완충 버퍼 (A)
- **법정 근거:** 국내 고시상 "출입구 설치 의무" 및 "이중문 인터락(동시 개폐 금지)" 설치 요구. 구체적인 최소 면적 수치는 고시되어 있지 않음.
- **가이드라인 계획 치수:** iHFG Anteroom 기준인 **6㎡** (2.1m x 2.85m) 또는 1.8m 그리드 연계를 고려하여 2x2 그리드인 **12.96㎡** 점유 계획을 추천.

#### ③ 병실 전용 화장실/샤워실 (WC)
- **법정 근거:** 국내 고시상 "음압병상이 있는 공간 내에 전용 샤워/화장실을 설치할 것" 명시. (단, 병실 10㎡ 면적 계산에서 화장실 공간은 제외)
- **가이드라인 계획 치수:** iHFG ensuite 6㎡ 및 휠체어 회전 반경을 완벽히 흡수하기 위해 2x2 그리드인 **9㎡** 계획 추천.

---

## 4. 데이터 파일 및 소스코드 연계
- 본 DB 마크업은 실제 프로젝트 루트 폴더인 `data/modules_ward_v01.json`에 완전하게 JSON 파일로 탑재되어 있습니다.
- Streamlit 프로토타입 실행 시 `grid_drag_canvas_app.py`가 부팅될 때 이 JSON 파일을 즉각 읽어들이며, 그리드에서 임의의 모듈에 마우스를 호버링(Hover)하면 해당 모듈의 면적, 전실 유무, 출처 데이터(`confidence` 등)가 인터랙티브하게 실시간으로 동적 렌더링되도록 코딩되어 있습니다.
