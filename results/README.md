# 집계 결과의 범위와 출처

`metrics.csv`는당시노트북의저장출력과개인ClinicalPDF에서확인한수치입니다. 새학습·새모델추론결과가아닙니다. `source_id`, `source_file`, `source_cells`, `evidence_level`, `pdf_pages`를통해근거를연결했습니다. 원본cell번호는Markdown·빈셀을포함한1-based번호이며공개사본에서도유지했습니다.

빈칸은미기록/해당없음입니다. 서로다른dataset·phase·evaluation_unit·gt_canvas·threshold를합쳐하나의성능으로보면안됩니다. PR-AUC는확인한코드에서average precision입니다. 소수자리수는저장출력/기존집계의정밀도를유지했습니다. LR/SVM의PDF수치를가짜노트북결과로채우지않았습니다.

| 모델 | 데이터 | 평가 단계·단위 | 근거 |
|---|---|---|---|
| UNet128 Raw | DCA1 | 5-fold OOF raw / pooled_pixels | [N04](../notebooks/04_AngioCAD_DCA1_UNet_혈관분할.ipynb) c31 |
| UNet128 small16 | DCA1 | OOF-selected postprocessing / pooled_pixels | [N04](../notebooks/04_AngioCAD_DCA1_UNet_혈관분할.ipynb) c35 |
| UNet128 small32 diagnostic | DCA1 | unselected diagnostic candidate / pooled_pixels | [N04](../notebooks/04_AngioCAD_DCA1_UNet_혈관분할.ipynb) c33 |
| UNet128 Hough rejected | DCA1 | rejected diagnostic candidate / pooled_pixels | [N04](../notebooks/04_AngioCAD_DCA1_UNet_혈관분할.ipynb) c37-38 |
| UNet256 Raw | DCA1 | 5-fold OOF raw / pooled_pixels | [N05](../notebooks/05_AngioCAD_DCA1_UNet256.ipynb) c18 |
| MedicalSAM3 fixed text | DCA1 | pretrained inference / pooled_pixels | [N07](../notebooks/07_AngioCAD_MedicalSAM3_혈관분할_.ipynb) c15-18 |
| MedicalSAM3 coronary blood vessel | DCA1 | diagnostic inference / image_macro_mean | [N07](../notebooks/07_AngioCAD_MedicalSAM3_혈관분할_.ipynb) c20 |
| MedicalSAM3 blood vessel | DCA1 | diagnostic inference / image_macro_mean | [N07](../notebooks/07_AngioCAD_MedicalSAM3_혈관분할_.ipynb) c20 |
| MedicalSAM3 GT box | DCA1 | diagnostic inference / image_macro_mean | [N07](../notebooks/07_AngioCAD_MedicalSAM3_혈관분할_.ipynb) c20 |
| ResNet50 7-grade | AngioCAD | validation model selection / patient-view/artery grades + view over50 AUC | [N08](../notebooks/08_AngioCAD_협착등급_Classifier.ipynb) c12 |
| ResNet50 3-bin | AngioCAD | validation model selection / patient-view/artery grades + view over50 AUC | [N08](../notebooks/08_AngioCAD_협착등급_Classifier.ipynb) c17 |
| ResNet18 Prox LCX | AngioCAD | separate 70/15/15 patient split test / frame | [N11](../notebooks/11_AngioCAD_classification_gradcam.ipynb) c10 |
| ResNet18 Prox LCX | AngioCAD | separate 70/15/15 patient split test / patient | [N11](../notebooks/11_AngioCAD_classification_gradcam.ipynb) c10 |
| ResNet18 Prox LAD | AngioCAD | separate 70/15/15 patient split test / frame | [N11](../notebooks/11_AngioCAD_classification_gradcam.ipynb) c18 |
| ResNet18 Prox LAD | AngioCAD | separate 70/15/15 patient split test / patient | [N11](../notebooks/11_AngioCAD_classification_gradcam.ipynb) c18 |
| Clinical AdaBoost | AngioCAD | development 5-fold OOF / patient | [N10](../notebooks/10_AngioCAD_XCA_Clinical_Fusion.ipynb) c14 |
| XCA attention MIL | AngioCAD | development 5-fold OOF / patient | [N10](../notebooks/10_AngioCAD_XCA_Clinical_Fusion.ipynb) c14 |
| Equal late fusion | AngioCAD | development 5-fold OOF / patient | [N10](../notebooks/10_AngioCAD_XCA_Clinical_Fusion.ipynb) c14 |
| SVM RBF | AngioCAD | development 5-fold OOF / patient | [N09](../notebooks/09_AngioCAD_clinical_only.ipynb) c10 |
| SVM sigmoid kernel | AngioCAD | development 5-fold OOF / patient | [N09](../notebooks/09_AngioCAD_clinical_only.ipynb) c10 |
| SVM polynomial | AngioCAD | development 5-fold OOF / patient | [N09](../notebooks/09_AngioCAD_clinical_only.ipynb) c10 |
| Random Forest | AngioCAD | development 5-fold OOF / patient | [N09](../notebooks/09_AngioCAD_clinical_only.ipynb) c10 |
| SVM linear | AngioCAD | development 5-fold OOF / patient | [N09](../notebooks/09_AngioCAD_clinical_only.ipynb) c10 |

## 그림 재생성

`python scripts/plot_results.py`는이CSV만읽습니다. 환자별자료·원본이미지·GT·모델가중치를읽지않습니다. [그림manifest](../figures/manifest.json)는입력CSV와생성script의hash,각PNG의hash·설명을담습니다. 그래프는비교조건을분리했으며계산하지않은ROC곡선·calibration곡선·신뢰구간을임의생성하지않았습니다.

DCA1공식128pooled와진단native300 macro mean은다른그림에있습니다. U-Net256은256GT입니다. AngioCADFusion은환자303명OOF이고ProxLCX/LAD는별도Test62명입니다. Specificity일부는저장confusion matrix로계산한값이며CSV notes에표시했습니다.
