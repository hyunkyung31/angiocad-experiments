# 실행 환경과 입력 준비

## 집계 결과 보기

Python3.12 환경에서 `requirements.txt`를 사용합니다. Matplotlib/Pandas는 `results/metrics.csv`만 읽어 그래프를 만들고, 정적 검사는 노트북 코드를 실행하지 않습니다. 현재 제공한 그림은 이 경로로 생성했습니다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/plot_results.py
python scripts/review_public_files.py
```

`requirements.txt`는 집계 그래프·노트북 형식/구문 검사용입니다. 전체 의료영상 학습 의존성을 설치하는 파일이 아닙니다.

## 과거 노트북 환경

원본은 Colab 중심이며 U-Net은 TeslaT4, SAM계열은 NVIDIAL4에서 실행한 출력이 있습니다. 일부 세션은 PyTorch2.11.0+cu128/torchvision0.26.0+cu128을 기록합니다. SAM3관련 세션에는 Python3.13과NumPy/SciPy ABI 조정 이력이 있습니다. SAM3의NumPy1.26요구와다른패키지의2.x요구가충돌한기록도있어전부를한환경에설치하지않는것이좋습니다.

작업별 주요 패키지:

| 작업 | 의존성·외부 도구 |
|---|---|
| 데이터 감사·전처리 | pandas,numpy,openpyxl,Pillow,OpenCV,Matplotlib,tqdm,unrar/unar |
| U-Net·분류·MIL | PyTorch,torchvision,scipy,scikit-learn,OpenCV |
| Clinical-only | pandas,scikit-learn,joblib |
| MedicalSAM3 | 외부저장소의해당commit 설치문서와공식checkpoint |
| Qwen | transformers,qwen-vl-utils,bitsandbytes,accelerate 및GPU |
| MedSAM2/CA-SAM2 | MedSAM2/SAM2,Hydra,HuggingFace Hub 및checkpoint |
| GPT-4o controller | openai 및사용자가설정한key; 외부전송은기본비활성 |

공개사본은위학습환경전체에서재실행하지않았습니다. GPU·데이터·이전manifest·모델을확보한뒤셀의선행정의를확인해야합니다. API응답·prompt진단·threshold경고등과거문제를새로해결한버전은아닙니다.

## 입력과 경로

개인계정·팀폴더이름은 `research-data`라는 일반 예제 경로로 바꿨습니다. Colab mount방식은유지했으며,주요예제는 `/content/drive/MyDrive/research-data/03_data/AngioCAD`입니다. 원래노트북마다폴더재구성·자동탐색방식이달라각경로설정셀을확인해야합니다. Drive전체를기존개인폴더이름으로검색하는조건도일반예제이름으로바꿨습니다.

필요한자료는AngioCAD RAR/Labels/Features,DCA1원본/GT,감사·전처리·split CSV,학습checkpoint와OOF파일입니다. 공개폴더에없으며 `data/`, `private/`, `artifacts/` 등에권한을제한해보관합니다. `.gitignore`는사고예방도구일뿐접근통제가아닙니다.

- `ANGIOCAD_CLEANING_RULES`: 원본N01c92의환자별정정표를외부비공개CSV로분리했습니다. 필요한열은 `patient_id,column,raw_value,clean_value,action,reason`입니다. 공개사본에서실제정정행을재구성하거나빈규칙으로대체하지않습니다. 권한있는원본규칙을지정해야합니다.
- `CASE_PATIENT_ID`, `CASE_SERIES_ID`, `CASE_FRAME_NAME`: N08A/N12의선택사례를사용자가지정합니다. 실제원본사례ID·frame은공개하지않았습니다.
- `NEXT_SERIES_ID`, `NEXT_FRAME_NAME`: N08A의추가프레임선택입니다.
- `CASE_POINT_X`, `CASE_POINT_Y`: N12의수동point입니다. 선택영상에서직접확인해야합니다.
- `ALLOW_EXTERNAL_MEDICAL_API=1`: 데이터의외부전송권한을확인한경우에만N08c25의GPT호출을허용합니다. 기본은차단입니다. 인증값은 `OPENAI_API_KEY` 환경변수로만읽습니다.

`.env.example`은변수명목록이며자동로드하지않습니다. 실제값을공개파일에쓰지않고노트북프로세스환경에설정하세요. 사본에서바꾼case입력은기존사례의동일조건재현을보장하지않습니다. 과거결과는분리된집계파일에그대로남겼습니다.

노트북을다시실행하면환자별표·영상·mask·API전송이발생할수있습니다. 새출력을공유하기전에별도로검토해야합니다.
