"""Plot saved aggregate metrics. Does not read patient data or run models."""

from pathlib import Path

import hashlib,json,os

os.environ.setdefault('MPLCONFIGDIR',str(Path(os.environ.get('TMPDIR','/tmp'))/'portfolio-matplotlib'))

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

DF=pd.read_csv(ROOT/'results/metrics.csv')

OUT=ROOT/'figures'

OUT.mkdir(exist_ok=True)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#cbd5e1','axes.labelcolor':'#334155','text.color':'#172554','xtick.color':'#334155','ytick.color':'#64748b','figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white'})

COLORS=['#94a3b8','#0f766e','#2563eb','#e19745','#7c3aed']

manifest=[]

def row(name):
 result=DF[DF.model==name]
 if len(result)!=1:raise ValueError(f'Expected one metric row for {name}')
 return result.iloc[0]

def bars(ax,labels,values,colors=None,ylim=(0,1),digits=4):
 x=np.arange(len(labels));ax.bar(x,values,color=colors or COLORS[:len(labels)],width=.62,zorder=3)
 ax.set_xticks(x,labels);ax.set_ylim(*ylim);ax.grid(axis='y',alpha=.2,zorder=0);ax.set_axisbelow(True)
 for i,v in enumerate(values):ax.text(i,v+(ylim[1]-ylim[0])*.02,f'{v:.{digits}f}',ha='center',fontsize=10)

def save(fig,name,caption,inputs='results/metrics.csv'):
 fig.savefig(OUT/name,dpi=160,bbox_inches='tight');plt.close(fig)
 manifest.append({'path':'figures/'+name,'caption':caption,'inputs':[inputs],'kind':'aggregate_chart','contains_patient_images':False,'model_execution':False,'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()})

def note(fig,text):fig.text(.07,.025,text,fontsize=9,color='#64748b',va='bottom')

def segmentation(ax):
 names=['UNet128 Raw','UNet128 small16','MedicalSAM3 fixed text'];values=[row(n).dice for n in names]
 bars(ax,['U-Net128\nRaw @0.5','U-Net128\nsmall16 @0.5','MedicalSAM3\ntext, conf=0.1'],values)
 ax.set_title('DCA1 | pooled Dice on 128 x 128 GT',loc='left',pad=15,weight='bold');ax.set_ylabel('Pooled Dice')

def fusion(ax):
 models=['Clinical AdaBoost','XCA attention MIL','Equal late fusion'];x=np.arange(3)
 for j,(metric,label,color) in enumerate([('roc_auc','ROC-AUC','#2563eb'),('sensitivity_recall','Sensitivity','#0f766e'),('specificity','Specificity','#e19745')]):
  vals=[row(n)[metric] for n in models];pos=x+(j-1)*.23;ax.bar(pos,vals,width=.22,label=label,color=color,zorder=3)
  for a,b in zip(pos,vals):ax.text(a,b+.025,f'{b:.3f}',ha='center',fontsize=8)
 ax.set_xticks(x,['Clinical','XCA MIL','Equal fusion']);ax.set_ylim(0,1.10);ax.set_yticks(np.linspace(0,1,6));ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True);ax.legend(loc='upper center',bbox_to_anchor=(.5,-.12),ncol=3,frameon=False,fontsize=9)
 ax.set_title('AngioCAD | 303-patient development OOF',loc='left',pad=15,weight='bold')

fig,ax=plt.subplots(figsize=(10,6));segmentation(ax);fig.subplots_adjust(bottom=.20);note(fig,'134 images; U-Net: image-level 5-fold OOF; SAM3: pretrained inference.\nsmall16 policy selected on the same OOF. These are not AngioCAD Dice scores.');save(fig,'dca1_baselines.png','DCA1 134장, 공통128GT의 pooled Dice. 후처리는 동일OOF에서 선택.')
fig,ax=plt.subplots(figsize=(9,6));bars(ax,['U-Net128\n128 GT','U-Net256\n256 GT'],[row('UNet128 Raw').dice,row('UNet256 Raw').dice]);ax.set_title('DCA1 | raw U-Net resolution comparison',loc='left',weight='bold');ax.set_ylabel('Pooled Dice @0.5');fig.subplots_adjust(bottom=.20);note(fig,'Same 134 image IDs and folds; each resolution uses its own resized GT.\nTraining trajectories differ. Not a common-native-canvas evaluation.');save(fig,'unet_resolution.png','해상도별GT에서계산한Raw128/256 비교. 순수 해상도 인과효과 아님.')
fig,ax=plt.subplots(figsize=(10,6));bars(ax,['coronary\nblood vessel','blood vessel','GT-derived box\n(oracle location)'],[row(n).macro_mean_dice for n in ['MedicalSAM3 coronary blood vessel','MedicalSAM3 blood vessel','MedicalSAM3 GT box']],['#94a3b8','#94a3b8','#e19745']);ax.set_title('MedicalSAM3 | diagnostic prompts on DCA1',loc='left',weight='bold');ax.set_ylabel('Native 300 x 300 macro mean Dice');fig.subplots_adjust(bottom=.21);note(fig,'134 images; diagnostics only. GT box supplies ground-truth location.\nDifferent canvas and aggregation from the official 128 pooled score.');save(fig,'sam3_prompt_diagnostics.png','native macro mean의 진단prompt 비교. GTbox는정답위치정보사용.')
fig,ax=plt.subplots(figsize=(10,6));fusion(ax);fig.subplots_adjust(bottom=.24);note(fig,'Same AngioCAD cohort: 237 positive / 66 negative; target any_definite_over_50.\n5-fold OOF, threshold=0.5. Fusion weights=1:1. Test not evaluated.');save(fig,'fusion_tradeoff.png','AngioCAD Clinical/XCA/Fusion OOF. AUROC개선과민감도감소를함께표시.')
fig,axes=plt.subplots(1,2,figsize=(14,7));segmentation(axes[0]);fusion(axes[1]);fig.suptitle('AngioCAD experiments | vessel segmentation and patient-level fusion',fontsize=18,weight='bold',y=.98);fig.subplots_adjust(top=.84,bottom=.28,wspace=.30);note(fig,'Left: DCA1 134 images, common 128 GT; U-Net OOF vs SAM3 pretrained inference.\nRight: AngioCAD 303 patients, development 5-fold OOF. Separate datasets and tasks; no lesion-localization claim.');save(fig,'portfolio_cover.png','대표후보: DCA1분할과AngioCAD환자분류를별도패널로구분.')
fig,ax=plt.subplots(figsize=(9,6));bars(ax,['LCX\nframe','LCX\npatient','LAD\nframe','LAD\npatient'],[DF[(DF.model=='ResNet18 Prox '+t)&(DF.evaluation_unit==u)].iloc[0].roc_auc for t,u in [('LCX','frame'),('LCX','patient'),('LAD','frame'),('LAD','patient')]],['#94a3b8','#0f766e','#94a3b8','#2563eb']);ax.set_title('ResNet18 | Prox LCX / LAD test classification',loc='left',weight='bold');ax.set_ylabel('ROC-AUC');fig.subplots_adjust(bottom=.20);note(fig,'Separate 70/15/15 patient split: 62 test patients / 780 frames.\nNL vs abnormal classification; Grad-CAM masks have no lesion-GT evaluation.');save(fig,'prox_classification.png','별도 Test의 frame/환자 AUROC 비교. 위치탐지성능 아님.')


manifest_path=OUT/'manifest.json'

manifest_path.write_text(json.dumps({'generator':'scripts/plot_results.py','metrics_sha256':hashlib.sha256((ROOT/'results/metrics.csv').read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'figures':manifest},ensure_ascii=False,indent=2)+'\n')

print(f'Generated {len(manifest)} aggregate figures')
