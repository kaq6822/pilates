# 앞톱니근 이미지 기록

전달된 `pilates_anatomy_serratus_full_v5_noscript.html`의 삽화를 개별 파일로 추출하고, 주요 움직임과 기능 카드 3개에는 각각 다른 이미지를 새로 생성했습니다. 새 이미지 3장은 같은 개념을 설명하는 `주요 이해`와 `움직임과 기능` 탭에서 함께 사용합니다. 모든 이미지는 **검토용 시안**이며 독립적인 해부학 QA와 UI QA 승인을 받지 않았습니다.

| 이미지 파일 | 첫 사용 위치 | Anatomy QA | UI QA |
|---|---|---|---|
| `hero_anatomy.jpg` | 이미지 1: hero_anatomy | 대기 | 대기 |
| `view_front.jpg` | 이미지 2: view_front | 대기 | 대기 |
| `view_side.jpg` | 이미지 3: view_side | 대기 | 대기 |
| `view_back.jpg` | 이미지 4: view_back | 대기 | 대기 |
| `exercise_wall_push.jpg` | 이미지 8: exercise_wall_push | 대기 | 대기 |
| `exercise_push_up.jpg` | 이미지 9: exercise_push_up | 대기 | 대기 |
| `exercise_overhead_reach.jpg` | 이미지 10: exercise_overhead_reach | 대기 | 대기 |
| `caution_winging.jpg` | 이미지 11: caution_winging | 대기 | 대기 |
| `movement_protraction_simple_v2.jpg` | 주요 이해·움직임과 기능: 내밈 | 대기 | 대기 |
| `movement_upward_rotation_simple_v2.jpg` | 주요 이해·움직임과 기능: 위쪽돌림 | 대기 | 대기 |
| `movement_stability_simple_v2.jpg` | 주요 이해·움직임과 기능: 흉곽에 대한 어깨뼈 유지 | 대기 | 대기 |

## 새 이미지 제작 기록

- 제작 방식: 내장 ImageGen으로 독립 이미지 3장 생성 후 웹 표시용 JPEG로 저장
- 공통 표현: 실제형 3D 의학 일러스트, 빨간색 앞톱니근, 밝은 뼈, 어두운 배경, 이미지 내부 텍스트 없음
- 내밈: 오른쪽 가쪽 갈비뼈의 톱니 모양 기시부터 반투명 어깨뼈 (견갑골) 안쪽모서리 앞면까지 보이고, 팔을 앞으로 뻗는 자세
- 위쪽돌림: 같은 부착 관계를 유지하면서 팔을 머리 위로 올린 자세와 어깨뼈 (견갑골)의 위쪽돌림 표현
- 어깨뼈 유지: 손을 지지한 자세에서 앞톱니근이 어깨뼈 (견갑골) 깊은쪽에 있는 관계 표현
- 내밈 이미지의 첫 생성물은 척추 쪽에서 시작하는 근육처럼 보여 사용하지 않고 다시 생성함
- 검토 근거: 원본 `M002_serratus-anterior.md`와 [StatPearls — Serratus Anterior Muscles](https://www.ncbi.nlm.nih.gov/books/NBK531457/). 생성 이미지 자체는 해부학 근거 자료가 아님

## 단순화 버전 v2

사용자 참고 이미지에 맞춰 흰 배경·아이보리색 뼈·빨간 앞톱니근·파란 화살표로 다시 생성했습니다. 주요 이해와 움직임과 기능 탭에 동일하게 연결하며, 전체 그림이 잘리지 않게 표시합니다. 상세 프롬프트는 [IMAGE_PROMPTS_V2.md](IMAGE_PROMPTS_V2.md)에 기록했습니다. 이전 사실형 이미지는 파일로 보존하지만 페이지에서는 참조하지 않습니다. 전문 해부학 감수는 대기 상태입니다.

## 추가 섹션 이미지

내장 ImageGen으로 각 근육의 위치도 1장과 기능도 3장을 독립 제작했습니다. 기능도는 주요 이해와 움직임과 기능 탭에서 같은 개념을 설명합니다. 원본 MD와 해당 StatPearls 자료에 근거해 내용을 작성했으며 전문 해부학 감수는 대기 중입니다. 프롬프트는 [IMAGE_PROMPTS_NEW_LESSONS.md](IMAGE_PROMPTS_NEW_LESSONS.md)에 기록했습니다.

| 파일 | 용도 | 해부학 감수 |
|---|---|---|
| `assets/images/gluteus_medius_hero.jpg` | 중간볼기근 위치 | 대기 |
| `assets/images/gluteus_medius_abduction.jpg` | 중간볼기근: 고관절 벌림 | 대기 |
| `assets/images/gluteus_medius_support.jpg` | 중간볼기근: 한발 지지의 골반 조절 | 대기 |
| `assets/images/gluteus_medius_rotation.jpg` | 중간볼기근: 관절 위치에 따른 역할 | 대기 |
| `assets/images/rectus_abdominis_hero.jpg` | 배곧은근 위치 | 대기 |
| `assets/images/rectus_abdominis_flexion.jpg` | 배곧은근: 몸통 굽힘 | 대기 |
| `assets/images/rectus_abdominis_tension.jpg` | 배곧은근: 복벽 장력과 압력 조절 | 대기 |
| `assets/images/rectus_abdominis_exhalation.jpg` | 배곧은근: 강제 날숨에 협력 | 대기 |

## 앞톱니근 형식 통일 v3

메인·보조 시점·운동·주의 그림 8장을 흰 배경의 단순한 교재형 이미지로 교체했습니다. 기존 단순화 움직임 그림 3장은 같은 형식이므로 두 탭에서 계속 공유합니다. 이전 시안 파일은 보존하며 페이지에서는 참조하지 않습니다. 내장 ImageGen 사용, 전문 해부학 감수 대기. 실제 프롬프트는 [IMAGE_PROMPTS_SERRATUS_V3.md](IMAGE_PROMPTS_SERRATUS_V3.md)에 있습니다.

| 이전 파일 | 현재 연결 파일 |
|---|---|
| `hero_anatomy.jpg` | `assets/images/serratus_hero_simple_v3.jpg` |
| `view_front.jpg` | `assets/images/serratus_front_simple_v3.jpg` |
| `view_side.jpg` | `assets/images/serratus_side_simple_v3.jpg` |
| `view_back.jpg` | `assets/images/serratus_back_simple_v3.jpg` |
| `exercise_wall_push.jpg` | `assets/images/serratus_wall_push_simple_v3.jpg` |
| `exercise_push_up.jpg` | `assets/images/serratus_push_up_simple_v3.jpg` |
| `exercise_overhead_reach.jpg` | `assets/images/serratus_overhead_simple_v3.jpg` |
| `caution_winging.jpg` | `assets/images/serratus_winging_simple_v3.jpg` |
