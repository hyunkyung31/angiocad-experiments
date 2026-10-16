# 포트폴리오 카드

**프로젝트명:** 관상동맥조영술 영상 분석: 분할에서 환자 단위 Fusion까지

**한 줄 설명:** 데이터 감사와 환자 단위 분할을 바탕으로 혈관 분할·협착 분류·영상–임상 정보 결합의 가능성과 한계를 비교한 개인 실험.

**핵심 성과**

1. DCA1 134장의 이미지 단위 5-fold OOF에서 U-Net128 Raw Dice 0.7259와 16px 후처리 0.7323을 구분하고, 혈관을 함께 지우는 Hough 정책을 기각했습니다. AngioCAD 적용은 GT 없는 정성 사례로 분리했습니다.
2. AngioCAD 개발 303명의 환자 OOF에서 Clinical과 XCA를 1:1로 결합해 AUROC 0.8662를 얻었습니다. Clinical-only의 0.8257보다 높지만 민감도 0.7637→0.7089의 손실도 함께 확인했습니다.

**기술 스택:** Python, PyTorch, torchvision, scikit-learn, OpenCV, pandas, NumPy, Matplotlib, MedicalSAM3, MedSAM2/CA-SAM2, Qwen2.5-VL, OpenAI API.

**대표 이미지:** `figures/portfolio_cover.png`

**대안:** `figures/fusion_tradeoff.png` — 모달리티 결합의 이득과 손실을 강조할 때 사용합니다.

모든 그림은 집계 수치만 사용합니다. 원본 의료영상이나 환자별 mask는 카드에 추가하지 않았습니다. 카드의 수치는 기존 저장 결과이며 새 실험이 아닙니다.
