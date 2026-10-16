# 데이터와 모델 출처

| 대상 | 출처 | 확인된 범위와 남은 조건 |
|---|---|---|
| AngioCAD | [Zenodo DOI](https://doi.org/10.5281/zenodo.15826856), [원 논문](https://doi.org/10.1016/j.cmpb.2026.109368) | 사용자에 의해논문의공식배포·비식별화설명이확인됨. 정확한레코드라이선스·사용버전대응은미확인 |
| DCA1 | [원본노트북의다운로드주소](http://personal.cimat.mx:8181/~ivan.cruz/DB_Angiograms_files/DB_Angiograms_134.zip) | 노트북간같은archive checksum기록있음. 원배포license·공인checksum은미확인 |
| MedicalSAM3 | [AIM-Research-Lab/Medical-SAM3](https://github.com/AIM-Research-Lab/Medical-SAM3), [가중치](https://huggingface.co/ChongCong/Medical-SAM3) | 추론용외부모델. 기록commit은4164d261b5a8c9fc1015a2e21537280a19c972c5. 코드·가중치의각조건확인필요 |
| Qwen2.5-VL | [Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) | LCX grounding의4bit pretrained inference. 정확한revision·재배포조건별도확인 |
| MedSAM2/CA-SAM2 | [MedSAM2 코드](https://github.com/bowang-lab/MedSAM2), [CA-SAM2 가중치](https://huggingface.co/Elakiya17/CA-SAM2) | `medsam2_arcade_v2.pt`사용. 데이터셋license가가중치license를대신하지않음 |

원래사용한AngioCAD RAR/Excel과DCA1 ZIP은현재공개사본에없습니다. 파일명·샘플수만으로공식배포버전과완전동일하다고판정하지않았습니다. DCA1기록SHA-256은`7161638a6e92c6a6e47a747db039292c8a1a6bad809aac0d1fd16a10a6f22a11`입니다. 이는노트북기록과의대응값이지새로배포자에게받은공인값은아닙니다.

ARCADE는기존YOLO프로젝트의직접사용데이터입니다. 이폴더의AngioCAD/DCA1실험전체에ARCADE라이선스를적용하지않습니다. CA-SAM2의파일명도정확한학습데이터버전이나접근권한을증명하지않습니다.

의료영상이라는이유만으로공개가금지되는것은아닙니다. 다만미확인라이선스자료는이번공개사본에서보류했고,자체코드와집계그래프를우선구성했습니다. 실제CC이용허락과추가접근조건이확인되면원본/파생물의허용범위를다시판단할수있습니다. 이저장소에데이터license를그대로소프트웨어license로지정하지않았습니다.
