# AngioCAD | 실험 결과 및 평가 기준

관상동맥조영술(XCA) 영상을 활용한 혈관 분할, 협착 분류, 임상정보 기반 예측 및 Late Fusion 실험의 결과를 정리했습니다.

이번 프로젝트에서는 U-Net, MedicalSAM3, ResNet 계열 모델과 임상정보 기반 머신러닝 모델을 비교했습니다.

실험마다 사용한 데이터셋과 예측 대상이 달랐기 때문에 **평가 조건을 구분하고, 성능 지표가 의미하는 범위를 함께 살펴보는 것**에 중점을 두었습니다.

주요 평가 과정은 다음과 같습니다.

| 실험 | 데이터셋 | 주요 평가 지표 |
|---|---|---|
| 혈관 분할 | DCA1 | Dice Score |
| 협착 등급 분류 | AngioCAD | QWK, Balanced Accuracy, AUROC |
| 근위부 혈관 분류 | AngioCAD | ROC-AUC, Sensitivity, Specificity |
| Clinical-only 모델 비교 | AngioCAD | Sensitivity, Specificity, ROC-AUC |
| Clinical / XCA Late Fusion | AngioCAD | AUROC, Sensitivity, Specificity |

각 실험의 상세 수치는 [metrics.csv](metrics.csv)에 정리했습니다.

---

## 1. DCA1 혈관 분할 모델 평가

### 평가 데이터 및 방법

DCA1 데이터셋의 관상동맥조영술 영상 134장과 픽셀 단위 정답 마스크를 사용했습니다.

U-Net 128과 U-Net 256 모델을 학습하고, 이미지 단위 5-fold Out-of-Fold(OOF) 방식으로 평가했습니다.

DCA1에는 환자 ID 정보가 없어 환자 단위 분할은 보장할 수 없었습니다.

혈관 분할 성능은 예측 마스크와 정답 마스크의 겹침 정도를 나타내는 Dice Score로 비교했습니다.

### U-Net 분할 결과

| 모델 및 방법 | 평가 기준 | Pooled Dice |
|---|---|---:|
| **U-Net 128 Raw** | 128×128 GT | **0.725928** |
| **U-Net 128 + 16px 후처리** | 128×128 GT | **0.732256** |
| U-Net 128 + 32px 후처리 후보 | 128×128 GT | 0.732281 |
| U-Net 128 + Hough 후처리 후보 | 128×128 GT | 0.732002 |
| U-Net 256 Raw | 256×256 GT | 0.709043 |

U-Net 128의 기본 Dice는 0.725928이었습니다.

예측 마스크에서 16px 미만의 작은 연결 요소를 제거했을 때 Dice는 0.732256으로 증가했습니다.

32px 후처리 후보는 0.732281을 기록했지만, 최종적으로 사용한 16px 기준과는 구분했습니다.

### 후처리 결과 분석

작은 연결 요소를 제거하는 방법은 노이즈를 줄이는 데 도움이 됐지만, 일부 영상에서는 실제 혈관 영역도 함께 제거됐습니다.

특히 카테터 제거를 위해 적용한 Hough 기반 후처리에서는 특정 영상의 Dice가 16px 후처리 대비 약 0.1105 감소했습니다.

이에 따라 Hough 기반 후처리는 채택하지 않았습니다.

이번 결과에서 중요하게 확인한 점은 **평균 Dice가 개선되더라도 모든 영상의 혈관 구조가 더 잘 보존되는 것은 아니라는 것**입니다.

또한 후처리 방법을 동일한 OOF 결과를 참고해 선택했기 때문에, 그 개선 수치를 별도의 독립 Test 성능으로 해석하지 않았습니다.

관련 코드:
- [U-Net 128 혈관 분할](../notebooks/04_AngioCAD_DCA1_UNet_혈관분할.ipynb)

---

## 2. U-Net 128과 U-Net 256 비교

입력 해상도에 따른 차이를 확인하기 위해 U-Net 256 모델도 학습했습니다.

| 항목 | U-Net 128 | U-Net 256 |
|---|---:|---:|
| 입력 해상도 | 128×128 | 256×256 |
| Pooled Dice | 0.725928 | 0.709043 |
| Macro Mean Dice | 0.723326 | 0.707051 |

U-Net 256의 Pooled Dice는 0.709043으로, 이번 실험에서는 U-Net 128보다 낮았습니다.

같은 영상 ID를 기준으로 이미지별 결과를 비교한 분석도 진행했습니다.

| 항목 | 결과 |
|---|---:|
| Macro Dice 차이 (256 - 128) | -0.016275 |
| 95% 신뢰구간 | [-0.024094, -0.008740] |
| Win / Tie / Loss | 48 / 0 / 86 |

다만 두 모델은 각 해상도로 변환한 GT에서 평가했고 학습 과정도 동일하지 않았습니다.

따라서 이 결과를 동일한 정답 마스크 조건에서 순수하게 해상도 효과만 비교한 결과로 해석할 수는 없습니다.

입력 해상도를 높인다고 반드시 분할 성능이 개선되는 것은 아니었으며, 학습 설정과 정답 마스크의 처리 방식도 함께 고려해야 했습니다.

관련 코드:
- [U-Net 256 실험](../notebooks/05_AngioCAD_DCA1_UNet256.ipynb)

---

## 3. MedicalSAM3 혈관 분할 비교

### 평가 방법

사전학습된 MedicalSAM3를 사용해 Text Prompt와 Bounding Box 기반 혈관 분할을 비교했습니다.

DCA1 영상에서 고정된 `coronary artery` Prompt를 적용한 평가와, 추가 Prompt 및 정답 기반 Bounding Box를 제공한 진단 실험을 진행했습니다.

다만 두 실험은 사용한 입력 정보와 평가 해상도, Dice 집계 방식이 다릅니다.

### MedicalSAM3 평가 결과

| 입력 방식 | 평가 기준 | Dice |
|---|---|---:|
| `coronary artery` 고정 Text Prompt | 128×128 Pooled Dice | 0.256543 |
| `coronary blood vessel` | Native 300, Macro Mean Dice | 0.426336 |
| `blood vessel` | Native 300, Macro Mean Dice | 0.302312 |
| GT 기반 Bounding Box | Native 300, Macro Mean Dice | 0.710780 |

[MedicalSAM3 Prompt 진단 그래프](../figures/sam3_prompt_diagnostics.png)

### 결과 분석

고정 Text Prompt를 이용한 자동 혈관 분할의 Pooled Dice는 0.256543이었습니다.

반면 GT에서 생성한 Bounding Box를 제공한 진단 실험에서는 Macro Mean Dice 0.710780을 기록했습니다.

그러나 GT 기반 Bounding Box에는 이미 정답 혈관의 위치 정보가 포함되어 있습니다.

따라서 이 결과를 위치 정보 없이 자동으로 혈관을 찾아낸 모델의 성능으로 소개할 수는 없습니다.

또한 Text Prompt 실험과 GT-box 실험은 평가 기준 자체가 다르므로 Dice 수치를 직접 비교해 성능 향상 폭을 계산하지 않았습니다.

### 추가 Prompt 실험에서 확인한 문제

Qwen2.5-VL 및 GPT-4o를 활용해 혈관 위치와 Prompt를 생성하는 실험도 진행했습니다.

이 과정에서 서로 다른 혈관 이름인 LM과 LCX를 입력했는데도 생성된 마스크 사이의 Dice가 약 0.996인 사례가 있었습니다.

이 수치는 GT와의 비교 결과가 아니라 **서로 다른 Prompt에서 생성된 두 마스크 사이의 유사도**입니다.

이처럼 출력 형식이 정상적이거나 마스크가 생성됐다고 해서 원하는 혈관을 정확히 구분했다고 판단할 수는 없었습니다.

MedSAM2와 CA-SAM2를 이용한 단일 사례에서는 생성된 세 후보 마스크 모두 지정한 Positive Point를 포함하지 않는 문제도 확인했습니다.

따라서 Prompt 기반 분할 결과의 정확성을 평가하려면 정답 마스크나 전문가의 수동 검토가 추가로 필요합니다.

관련 코드:
- [MedicalSAM3 혈관 분할](../notebooks/07_AngioCAD_MedicalSAM3_혈관분할_.ipynb)
- [Qwen 및 MedicalSAM3 Prompt 실험](../notebooks/08A_AngioCAD_MedicalSAM3_mLLM_LCX_실험.ipynb)
- [MedSAM2 / CA-SAM2 실험](../notebooks/12_AngioCAD_MedSAM2_vessel_segmentation.ipynb)

---

## 4. ResNet50 협착 등급 분류

### 평가 방법

AngioCAD 영상을 이용해 관상동맥 15개 분절의 협착 등급을 분류하는 ResNet50 모델을 실험했습니다.

초기에는 7등급 분류를 진행했고, 이후 라벨을 3개 구간으로 단순화하면서 학습 설정도 조정했습니다.

Validation 데이터는 66명으로 구성됐으며, 평가 대상에는 131개 Patient-View와 980개 Patient-View-Artery 단위가 포함됐습니다.

### 모델별 결과

| 평가 지표 | 7등급 실험 | 3-bin 실험 |
|---|---:|---:|
| QWK | 0.352706 | 0.389810 |
| Balanced Accuracy | 0.273112 | 0.502628 |
| Over 50% ROC-AUC | 0.819144 | 0.806758 |
| Over 50% Average Precision | 0.815564 | 0.836409 |

### 결과 분석

3-bin 실험에서는 QWK와 Balanced Accuracy가 높아졌습니다.

하지만 50% 초과 협착 여부를 구분하는 ROC-AUC는 0.819144에서 0.806758로 감소했습니다.

반면 Average Precision은 0.815564에서 0.836409로 증가했습니다.

라벨 구간과 학습 설정이 함께 변경됐고 등급 분류의 대상도 달라졌기 때문에, QWK나 Balanced Accuracy의 차이를 동일 과제에서의 순수한 개선 폭으로 해석하기는 어렵습니다.

또한 분류 성능이 개선됐다고 해서 협착 병변의 위치까지 정확하게 찾았다고 볼 수는 없습니다.

위 결과는 Validation 기준이며, 해당 실험의 최종 Test 결과는 확보하지 못했습니다.

관련 코드:
- [ResNet50 협착 등급 분류](../notebooks/08_AngioCAD_협착등급_Classifier.ipynb)

---

## 5. ResNet18 근위부 혈관 분류

### 평가 방법

ResNet18을 이용해 근위부 LCX와 LAD 혈관의 정상(NL) 및 이상(Abnormal) 여부를 분류했습니다.

이 실험은 ResNet50 협착 등급 분류와 별도로 진행했습니다.

환자 단위 70/15/15 데이터 분할을 사용했으며, Test 데이터는 62명, 총 780개 Frame으로 구성됐습니다.

Frame별 결과와 환자별 평균 확률을 이용한 결과를 구분해 평가했습니다.

### ROC-AUC 비교

| 분류 대상 | Frame 단위 ROC-AUC | 환자 단위 ROC-AUC |
|---|---:|---:|
| Prox LCX | 0.704335 | **0.718954** |
| Prox LAD | 0.583256 | **0.639254** |

[근위부 혈관 분류 그래프](../figures/prox_classification.png)

### 환자 단위 평가 결과

| 지표 | Prox LCX | Prox LAD |
|---|---:|---:|
| ROC-AUC | 0.718954 | 0.639254 |
| Sensitivity | 0.882353 | 0.625000 |
| Specificity | 0.355556 | 0.578947 |
| Accuracy | 0.500000 | 0.596774 |

Specificity는 저장된 Confusion Matrix를 기준으로 계산한 값입니다.

### 결과 분석

LCX는 환자 단위 ROC-AUC 0.7190, LAD는 0.6393을 기록했습니다.

LCX의 Sensitivity는 상대적으로 높았지만 Specificity는 낮아, 정상 환자를 이상으로 분류하는 사례도 많았습니다.

따라서 AUROC만 보고 실용적인 선별 성능이 확보됐다고 판단하기는 어렵습니다.

또한 Grad-CAM을 통해 모델이 참고한 영역을 확인했지만, 병변 위치 GT와 직접 비교한 평가가 없으므로 정확한 협착 위치 탐지 성능으로 해석할 수 없습니다.

관련 코드:
- [ResNet18 근위부 혈관 분류 및 Grad-CAM](../notebooks/11_AngioCAD_classification_gradcam.ipynb)

---

## 6. AngioCAD Clinical-only 모델 비교

### 평가 방법

AngioCAD의 임상정보만을 사용해 협착 여부를 예측하는 머신러닝 모델도 비교했습니다.

Development 환자 303명을 대상으로 환자 단위 5-fold OOF 평가를 진행했습니다.

전처리와 학습 과정에서는 다음 사항을 고려했습니다.

- 임상 변수 후보 57개 검토
- Mutual Information 기반 25개 변수 선택
- 학습 Fold 내부에서 결측값 처리와 스케일링
- 클래스 불균형을 고려한 학습 데이터 내부 Undersampling

이 실험은 별도의 Clinical RF 프로젝트에서 사용한 UCI Z-Alizadeh Sani 데이터와 다른 코호트 및 예측 대상을 사용합니다.

### 모델별 결과

| 모델 | Sensitivity | Specificity | ROC-AUC |
|---|---:|---:|---:|
| SVM RBF | 0.7637 | 0.7424 | 0.8032 |
| SVM Sigmoid Kernel | 0.7595 | 0.7424 | **0.8222** |
| SVM Polynomial | 0.6540 | **0.8030** | 0.7787 |
| Random Forest | 0.7384 | 0.7121 | 0.8166 |
| SVM Linear | 0.7300 | 0.6667 | 0.7557 |

### 결과 분석

모델마다 Sensitivity와 Specificity 사이에 차이가 나타났습니다.

SVM Sigmoid Kernel은 비교 모델 중 가장 높은 ROC-AUC를 기록했으며, SVM Polynomial은 Specificity가 가장 높았지만 Sensitivity는 상대적으로 낮았습니다.

이 결과만으로 하나의 모델이 모든 지표에서 가장 우수하다고 판단하기는 어려웠습니다.

후속 Fusion 비교에서는 별도로 구성된 AdaBoost 기반 Clinical 모델의 환자 단위 OOF 예측을 사용했습니다.

따라서 위의 Clinical-only 후보 모델 비교 결과와 Fusion 단계의 AdaBoost 성능을 같은 모델의 결과로 취급하지 않았습니다.

관련 코드:
- [AngioCAD Clinical-only 모델 비교](../notebooks/09_AngioCAD_clinical_only.ipynb)

---

## 7. Clinical AI와 XCA 영상의 Late Fusion

### 7.1 평가 방법

AngioCAD Development 데이터에서 임상정보와 XCA 영상을 모두 사용할 수 있는 환자 303명을 대상으로 환자 단위 5-fold OOF 평가를 진행했습니다.

예측 대상은 `any_definite_over_50`이며, 분류 Threshold는 0.5를 사용했습니다.

비교 대상은 다음과 같습니다.

| 모델 | 방법 |
|---|---|
| Clinical-only | AdaBoost 기반 임상정보 분류 |
| XCA-only | ResNet50 기반 Attention MIL |
| Equal Late Fusion | 두 모델의 예측 확률을 1:1 평균 |

### 7.2 모델별 평가 결과

| 모델 | ROC-AUC | Sensitivity | Specificity | Accuracy |
|---|---:|---:|---:|---:|
| Clinical-only | 0.8257 | **0.7637** | 0.7727 | **0.7657** |
| XCA-only MIL | 0.8197 | 0.4599 | **0.9091** | 0.5578 |
| **Equal Late Fusion** | **0.8662** | 0.7089 | 0.8788 | 0.7459 |

![Clinical, XCA, Late Fusion 성능 비교](../figures/fusion_tradeoff.png)

### 결과 분석

Late Fusion의 ROC-AUC는 0.8662로 Clinical-only의 0.8257보다 높았습니다.

Specificity 역시 0.7727에서 0.8788로 증가했습니다.

하지만 Sensitivity는 0.7637에서 0.7089로 감소했고, Accuracy도 0.7657에서 0.7459로 낮아졌습니다.

**영상과 임상정보를 결합했을 때 전반적인 판별 능력은 개선됐지만, 질환이 있는 환자를 놓치지 않는 성능은 오히려 낮아진 것**입니다.

### 7.3 Paired Bootstrap 분석

동일한 303명 환자의 OOF 예측을 이용해 Clinical-only와 Late Fusion의 성능 차이를 분석했습니다.

| 평가 항목 | Fusion - Clinical |
|---|---:|
| ROC-AUC 차이 | +0.0405 |
| ROC-AUC 95% CI | [+0.0169, +0.0657] |
| Sensitivity 차이 | -0.0549 |
| Sensitivity 95% CI | [-0.0928, -0.0169] |

이번 분석에서는 AUROC의 증가와 Sensitivity의 감소가 함께 나타났습니다.

이를 통해 **여러 모델을 결합한다고 해서 모든 평가 지표가 개선되는 것은 아니라는 점**을 확인했습니다.

특히 CAD 선별처럼 환자를 놓치는 문제가 중요한 경우에는 AUROC뿐 아니라 Sensitivity와 False Negative를 함께 고려해야 합니다.

Bootstrap 신뢰구간은 개발 OOF 환자 표본에서 확인한 성능 차이에 대한 분석입니다. 모델 재학습이나 외부 환자 집단의 변동까지 포함하는 독립 검증 결과는 아닙니다.

관련 코드:
- [XCA / Clinical Late Fusion](../notebooks/10_AngioCAD_XCA_Clinical_Fusion.ipynb)

---

## 8. 평가 결과를 해석할 때 주의할 점

이번 프로젝트에는 서로 다른 데이터셋, 정답 정보, 평가 방식이 사용됐습니다.

따라서 성능 지표를 비교할 때 다음 사항을 구분해야 합니다.

### 8.1 DCA1과 AngioCAD 분할 결과

DCA1의 U-Net Dice는 픽셀 단위 정답 마스크가 있는 데이터에서 계산했습니다.

반면 AngioCAD에 U-Net을 적용한 결과는 분할 정답 마스크가 없어 정성적으로만 검토했습니다.

DCA1에서 얻은 Dice를 AngioCAD 영상에 대한 성능으로 해석하지 않았습니다.

### 8.2 Pooled Dice와 Macro Mean Dice

Pooled Dice는 전체 평가 픽셀을 합산한 기준이며, Macro Mean Dice는 영상별 Dice를 평균한 결과입니다.

MedicalSAM3의 고정 Text Prompt와 GT-box 진단 실험은 평가 해상도와 집계 방식도 다르므로 직접 비교할 수 없습니다.

### 8.3 협착 분류와 병변 위치 탐지

ResNet 기반 협착 분류 결과는 영상 또는 혈관의 이상 여부와 등급을 예측한 결과입니다.

Grad-CAM 시각화만으로 병변의 정확한 위치를 탐지했다고 판단하지 않았습니다.

### 8.4 Validation, Test, OOF의 차이

ResNet50의 협착 등급 분류는 Validation 결과이며, ResNet18 근위부 분류는 별도의 환자 단위 Test 결과입니다.

Fusion은 Development 데이터에 대한 5-fold OOF 결과입니다.

서로 다른 평가 단계에서 측정한 성능을 하나의 공통 Test 결과로 합치지 않았습니다.

### 8.5 내부 검증과 외부 검증

현재 결과는 각 실험에서 진행한 내부 평가 및 일부 정성 분석을 중심으로 합니다.

특히 Fusion 모델은 별도 Test 및 외부 데이터 검증을 완료하지 않았으므로, 현재 성능을 임상 적용 성능으로 해석할 수는 없습니다.

---

## 9. 결과 파일과 그래프

### 집계 성능 파일

실험별 평가 결과는 [metrics.csv](metrics.csv)에 정리했습니다.

CSV에는 모델, 사용 데이터셋, 평가 단계, 평가 단위, Threshold, 성능 지표 등이 포함되어 있습니다.

특히 다음 사항을 구분해 기록했습니다.

- DCA1과 AngioCAD 데이터셋
- 분할·분류·Fusion 실험
- Pooled Dice와 Macro Mean Dice
- Frame 단위와 환자 단위 평가
- Validation, Test, OOF 평가 단계
- 사용한 Threshold와 입력 해상도

값이 비어 있는 항목은 해당 지표가 기록되지 않았거나 적용 대상이 아닌 경우입니다.

### 그래프 재생성

저장된 집계 결과를 이용해 그래프를 생성할 수 있습니다.

저장소 최상위 폴더에서 다음 명령을 실행합니다.

`python scripts/plot_results.py`

이 스크립트는 `results/metrics.csv`를 이용해 그래프를 생성하며, 의료영상이나 학습 모델을 불러와 새로 추론하지는 않습니다.

그래프별 생성 정보는 [Figure Manifest](../figures/manifest.json)에 정리했습니다.

환자별 예측 확률이나 실제 정답 배열이 필요한 ROC Curve, Calibration Curve 등을 집계 수치만으로 임의 생성하지 않았습니다.

---

## 10. 결과 요약 및 향후 개선 방향

이번 실험에서 확인한 주요 내용은 다음과 같습니다.

1. **U-Net 분할:** 작은 연결 요소 제거는 평균 Dice를 개선했지만 일부 영상에서는 실제 혈관도 제거했습니다.
2. **입력 해상도:** U-Net 256이 U-Net 128보다 높은 성능을 보이지는 않았습니다. 다만 평가 GT와 학습 조건이 달라 해상도만의 영향으로 해석할 수 없습니다.
3. **MedicalSAM:** 정상적인 마스크 생성이나 GT-box를 이용한 높은 Dice가 자동 혈관 분할의 정확성을 보장하지는 않았습니다.
4. **협착 분류:** 라벨 구간과 학습 설정에 따라 평가 지표가 서로 다른 방향으로 변화했습니다.
5. **Clinical / XCA Fusion:** ROC-AUC와 Specificity는 증가했지만 Sensitivity는 감소했습니다.

이 결과를 통해 모델 성능을 평가할 때는 **평균 지표뿐 아니라 평가 조건과 개별 실패 사례, 실제 예측 목적을 함께 고려해야 한다**는 점을 확인했습니다.

앞으로는 AngioCAD 분할 결과의 정답 기반 평가, MedicalSAM 결과의 다환자 검증, 협착 분류 및 Fusion 모델의 독립 Test 평가가 필요합니다.

또한 실제 선별 목적에 맞는 Threshold를 검토하고, 새로운 환자 집단에서도 성능이 유지되는지 확인할 필요가 있습니다.

---

### 관련 문서

- [프로젝트 소개](../README.md)
- [실험 과정 및 문제 해결](../docs/experiments.md)
- [데이터 및 모델 출처](../docs/data_sources.md)
- [실험 환경](../docs/environment.md)

실험 결과는 기존 학습 및 평가 기록을 기준으로 정리했습니다. 전체 노트북의 재학습과 독립 외부 검증은 별도로 수행하지 않았습니다.
