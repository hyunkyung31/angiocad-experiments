# 실험 흐름과 남은 문제

근거는 `docs/source_manifest.json`의 원본commit·파일·셀 번호에 연결됩니다. 공개 사본에서도 셀 개수와 순서를 유지했습니다. 저장 출력은 제거했고 결과는 `results/metrics.csv`에 따로 보존했습니다.

| 파일 | 진행한 작업 | 실제 완료 범위와 한계 |
|---|---|---|
| 01 데이터확인 | 폴더·frame·label·Clinical 연결, 이상값·정제 | 구조/범위 감사 출력 있음. 환자별 정정값은 공개하지 않음 |
| 02 전처리 | pixel hash, 모델 cohort, CLAHE·P0/P1/P2 QC | 전체119,046frame QC 출력. 마지막 일부 Gate의상수만으로 독립 재검증했다고 해석하지 않음 |
| 03 분할 | seed42 환자split, Development5-fold | 영상412명→329/83. Clinical가용376명→303/73 |
| 04 U-Net128 | DCA1 5-fold OOF, small-component/Hough | Raw/16px 정책 완료. Hough는 실제혈관 제거 위험으로 기각 |
| 05 U-Net256 | 같은DCA1 fold, 256입력 학습·OOF | 초기tiny기준미달→연장학습복구. 전체OOF는128보다낮음 |
| 06 정성적용 | U-Net128 checkpoint remap, AngioCAD36frame | 저장OOF 재현 비교·추론 출력 있음. AngioCAD 픽셀GT 없음 |
| 07 MedicalSAM3 | pretrained text/GT-box, DCA1·AngioCAD | DCA1 정량완료, baseline개선실패. AngioCAD 사람채점 남음 |
| 08 Classifier | ResNet50 7등급→3-bin, Grad-CAM; 후반GPT/SAM3 | VAL 완료, Test출력없음. 36framecontroller 실행과 유효box는 정확도평가 아님 |
| 08A Qwen LCX | Qwen2.5-VL-7B 4bit→SAM3 box, prompt 비교 | 단일사례연결. uncertain 실패·수동판정미완료. 입력series와 저장전역변수의불일치가 남음 |
| 09 Clinical-only | AngioCAD57후보→MI25, training내undersampling | 6모델5-fold OOF. UCI RF와 다른데이터/target |
| 10 Fusion | 환자bag ResNet50 attentionMIL +Clinical확률평균 | 고정8epoch,5-fold OOF,1:1평균,bootstrap. Test없음 |
| 11 Prox분류 | ResNet18 LCX/LAD NL/abnormal, CAM | 별도70/15/15 split의Test완료. CAM 병변위치평가없음 |
| 12 MedSAM2/CA-SAM2 | 관상동맥가중치471key strict load,1frame point | 추론완료. 3candidate 모두point_inside=False. 수동확정·GT평가없음 |

## 평균 개선만으로 채택하지 않은 후처리

U-Net128 Raw pooled Dice는0.725928, 16px후처리는0.732256입니다(04 c31/c35). 같은OOF에서 정책을 골랐으므로 추가Test가 필요합니다. 32px탐색후보0.732281을 최종채택값과 바꾸지 않았습니다.

Hough최고후보는0.732002였고, 한영상에서는small16대비−0.110458로 악화했습니다(04 c37–38). 직선카테터를 지우려다 실제혈관까지 제거할수있어 정책을기각했습니다.

## 해상도와 평가 canvas

256의pooled Dice0.709043과128의0.725928은각자의resized GT에서계산했습니다. 이미지별macro delta는−0.016275,95%CI[−0.024094,−0.008740],win/tie/loss48/0/86입니다(05 c18). 이짝지음은 같은영상ID 비교이지공통native GT 평가가 아닙니다.

## Prompt가 위치 정보를 대신하지 못한 경우

07 c18의공식SAM3 text결과는128pooled입니다. c20의다른text/GT-box는native300 macro mean 진단입니다. GTbox에는정답위치정보가들어가므로자동성능으로소개하지않습니다.

08A c28의LM/LCX mask간Dice0.996은정답과의Dice가아니라서로다른prompt출력의유사도입니다. c15의bbox·점Gate도좌표형식과모델self-check를검사한것이며해부학적정답판정이아닙니다. c19수동평가칸은공란입니다.

12 c8은point포함후보가없으면전체최고score로fallback하지만선택이름은point포함선택처럼남습니다. 내부score0.668을실제Dice로해석하지않습니다. 이문제를공개용정리과정에서해결했다고주장하지않았습니다.

## 분류와 위치 탐지는 다른 과제

08의VAL은66환자의131patient-view·980patient-view-artery단위입니다. 11은다른split의Test62명과780frame입니다. 결과를하나의Test성능으로합치지않습니다. Grad-CAM pseudo-mask에는위치GT평가가없습니다.

## Fusion의 이득과 손실

10 c14–15는동일AngioCAD303명의환자OOF를비교했습니다. Fusion−Clinical AUROC차이는+.0405[+.0169,+.0657],recall차이는−.0549[−.0928,−.0169]입니다. Bootstrap은이OOF표본의불확실성을보며모델재학습·모델선택·외부cohort변동까지포함하지않습니다.

## 재실행 전에

원본노트북은Colab의여러세션과Drive산출물에의존합니다. 일부셀은다시정의하거나이전checkpoint를읽습니다. 이번사본은실험기록을보존한코드이며통합된학습패키지는아닙니다. 의료자료로재실행하면새출력과환자별파일이생기므로그산출물을그대로공개하면안됩니다. [환경과입력](environment.md)을먼저확인하세요.
