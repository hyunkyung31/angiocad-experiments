# 원본 대비 변경

원본은 `hyunkyung31/coronary-ai-ml-dl`의 개인 `hyunkyung/`이며 기준commit은 `28bf910207229e834893f9c92a1d4bc034855c64`입니다. 팀 저장소와 기존 YOLO 저장소는 수정하지 않았습니다. 이 저장소는 원본 Git 기록을 가져오지 않고 공개용 파일만 선별한 독립 저장소입니다.

## 공통 정리

- 개인노트북 13개를복사하고원본셀순서·개수를유지했습니다. 각셀metadata의 `original_cell_1based`와 `source_manifest.json`에서근거위치를찾을수있습니다.
- 저장출력 667개를모두제거했습니다. 이중image MIME을포함한출력은 56개입니다. 원본은그대로보존되어있습니다.
- 실행카운터,widget/Colabmetadata,cell첨부를비우고최소kernel정보만남겼습니다. 출력이없는것은실험미실행을새로판정한것이아니라공개용정리정책입니다.
- 개인계정·팀프로젝트경로를일반예제이름으로바꾸고Unicode를NFC로정규화했습니다. 정규화도셀hash변경내역에포함합니다.
- 원래저장된성능은출력에서복제한안전한집계CSV로분리했습니다. 새학습·평가결과를만들지않았습니다. 환자별표·OOF·이미지·모델은복사하지않았습니다.
- `scripts/plot_results.py`와 `scripts/review_public_files.py`는공개자료정리를위해추가한보조도구입니다. 과거실험코드로소개하지않습니다.

## 소스 변경 위치

| 파일 | 변경한 원본 셀 |
|---|---|
| `notebooks/01_AnigoCAD_데이터확인.ipynb` | 5, 16, 92 |
| `notebooks/02_AngioCAD_전처리.ipynb` | 26, 30, 51 |
| `notebooks/03_AngioCAD_환자단위_데이터분할.ipynb` | 3 |
| `notebooks/04_AngioCAD_DCA1_UNet_혈관분할.ipynb` | 2, 17, 25, 27, 28, 33, 34, 35, 37 |
| `notebooks/05_AngioCAD_DCA1_UNet256.ipynb` | 3, 5 |
| `notebooks/06_AngioCAD_UNet128_시각검증_.ipynb` | 3 |
| `notebooks/07_AngioCAD_MedicalSAM3_혈관분할_.ipynb` | 4 |
| `notebooks/08A_AngioCAD_MedicalSAM3_mLLM_LCX_실험.ipynb` | 1, 2, 6, 7, 8, 14, 20, 21, 22 |
| `notebooks/08_AngioCAD_협착등급_Classifier.ipynb` | 3, 19, 25 |
| `notebooks/09_AngioCAD_clinical_only.ipynb` | 3 |
| `notebooks/10_AngioCAD_XCA_Clinical_Fusion.ipynb` | 2, 5, 7 |
| `notebooks/11_AngioCAD_classification_gradcam.ipynb` | 2 |
| `notebooks/12_AngioCAD_MedSAM2_vessel_segmentation.ipynb` | 1, 3, 4, 5, 6, 7, 8 |

개인 경로 정리 외의 변경은 다음과 같습니다.

1. N01 c16의 `.sort_values` 괄호 오타를 고쳤습니다. 원본의저장출력을새로재현했다는뜻은아닙니다.
2. N01 c92의환자별정정값리스트를 `ANGIOCAD_CLEANING_RULES` 비공개CSV입력으로바꿨습니다. 실제정정규칙을새로만들거나실험용데이터를바꾸지않았습니다. 이입력없이는해당단계재실행이안됩니다.
3. N08A/N12의환자·series·frame·수동point를환경변수로분리했습니다. 사례표시문구도일반화했고특정series를고르던index를입력변수에연결했습니다. 원본사례와새선택사례가같다고주장하지않습니다.
4. N08 c25의key조회는표준환경변수로바꾸고외부의료영상API호출에명시적활성화조건을추가했습니다. 모델·prompt·기존결과를바꾸거나API를실행하지않았습니다.

SAM3/Qwen의series기록불일치,MedSAM2의point미포함fallback,라이브러리충돌은해결한것으로표시하지않았습니다. 학습loss·모델구조·split·성능수치는개선명목으로고치지않았습니다.

파일별·셀별원본/사본SHA-256은 [source_manifest.json](source_manifest.json), 출력제거건수는 [source_changes.csv](source_changes.csv)에있습니다. 원본코드의개인값이노출될수있어전체raw diff를공개폴더에넣지않았습니다. 사본의모든셀을정적구문검사했지만의존자료와GPU를포함한전체실행은검증하지않았습니다.

## 최종 공개 전 정리

추가 산출물이 실수로 포함되지 않도록 `.gitignore`에서 CSV·JSON·이미지는 이 저장소의 집계 파일·manifest·생성 그래프만 예외로 두었습니다. PDF·키 파일·백업·캐시도 제외합니다. 공개 검사 스크립트의 경로 탐지 규칙에는 실제 개인 계정명이나 팀 폴더명을 남기지 않았습니다. 이 정리로 실험 수치·조건이나 노트북의 학습 로직을 변경하지 않았습니다.
