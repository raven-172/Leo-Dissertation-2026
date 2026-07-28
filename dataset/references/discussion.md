# Review of Three Studies on Video Frame Selection and the Rationale for Selecting SHIFT

## 1. Purpose of the Review

This review examines three studies:

1. Yoon and Choi (2023);
2. Yang *et al.* (2024);
3. Avena *et al.* (2026).

The purpose is to establish an academic basis for selecting a subset of frames from video to construct a training dataset for computer vision models, and to explain the decision to use **SHIFT** when the annotation budget is set at **10% of the total number of frames**.

The analysis below uses only information reported by the authors of the three papers. Their results are not treated as directly equivalent where the studies use different tasks, datasets, models or evaluation metrics.

---

## 2. Yoon and Choi (2023)

### 2.1. Research Problem

Yoon and Choi (2023) investigate whether the size of a training dataset can be reduced by exploiting redundancy between consecutive video frames. The task evaluated in the paper is **instance segmentation**.

The authors state that collecting and annotating large datasets is costly, while video contains many frames with similar content. The paper therefore evaluates whether keyframe extraction can reduce the number of training samples while maintaining model performance.

### 2.2. Frame-Selection Methods

The paper investigates two main groups of strategies:

- **Uniform Frame Sampling (UFS):** frames are selected using an adjusted temporal stride.
- **Adaptive Frame Sampling (AFS):** frames are selected according to inter-frame dissimilarity using:
  - optical flow;
  - the Structural Similarity Index Measure (SSIM);
  - feature representations.

These dissimilarity measures are applied without separately training a frame-selection model.

The paper also evaluates simple copy-paste augmentation to reduce the mAP gap caused by using fewer training frames.

### 2.3. Experimental Setting

Yoon and Choi (2023) use:

- BDD100K MOTS;
- Mask R-CNN;
- reduced training datasets created using UFS and AFS;
- mAP to evaluate instance-segmentation performance.

### 2.4. Main Results

The authors report that:

- using **20% of the data** can achieve performance close to the mAP obtained with the complete dataset;
- using **33% of the data** can exceed the mAP obtained with the complete dataset.

The results show that removing redundant frames can maintain or improve performance in the instance-segmentation setting investigated in the paper (Yoon and Choi, 2023).

### 2.5. Scope of the Evidence

The paper provides evidence concerning frame sampling for **instance segmentation**, rather than an object-detection experiment using YOLO. Consequently, the original mAP results reported by Yoon and Choi (2023) cannot be compared directly with the object-detection mAP results reported by Avena *et al.* (2026).

---

## 3. Yang et al. (2024)

### 3.1. Research Problem

Yang *et al.* (2024) investigate the selection of initial frames to support a semi-automated annotation workflow for cataract surgery videos.

The workflow consists of:

1. selecting an initial set of frames;
2. annotating the selected frames;
3. training an object-detection model;
4. using the model to predict bounding boxes on the remaining frames;
5. evaluating the number of actions required to correct the predictions.

The primary evaluation objective is therefore the **efficiency of an annotation-assistance workflow**, rather than the generalisation performance of a detector on independent test videos.

### 3.2. Frame-Selection Methods

The paper compares three methods.

#### Feature Clustering

Yang *et al.* (2024) apply the following procedure:

1. use a base-size Vision Transformer, pre-trained on ImageNet-1K using MAE, to extract features from all frames;
2. apply Principal Component Analysis;
3. retain the components explaining 90% of the variance;
4. use Affinity Propagation to determine the number of clusters automatically;
5. select the exemplars corresponding to the clusters as the initial frames.

#### Temporal Every-10th-Frame Sampling

This method selects every tenth frame in the video sequence.

#### Temporal Same-Size Sampling

This method samples frames uniformly over time while selecting the same number of frames produced by feature clustering.

### 3.3. Experimental Setting

The paper uses:

- 12 cataract surgery videos;
- a recording rate of 30 FPS;
- eight object classes;
- the small version of YOLOv8;
- the remaining frames to evaluate predictions and annotation-correction workload.

The same initial frame set is used as the training, validation and test set during YOLOv8 training. The authors explicitly state that this setting is intended to encourage the model to overfit to the selected representative frames in order to improve predictions on the remaining frames from the same data.

### 3.4. Results on the All-Frame Experiments

| Method | Accuracy | Total edits | Action cost |
|---|---:|---:|---:|
| Feature clustering | **92.0%** | **4,523** | **6,112** |
| Temporal every-10th-frame | 84.1% | 6,240 | 11,690 |
| Temporal same-size | 90.1% | 5,124 | 6,786 |
| Manual | 100% | 20,727 | 41,454 |

In the all-frame experiments, feature clustering produces:

- the highest accuracy among the three frame-selection methods;
- the lowest total number of edits;
- the lowest action cost.

The paper reports that feature clustering saves 85.2% of the time required for manual labelling and is 9.9% faster than temporal same-size sampling according to the action-cost measure defined in the paper (Yang *et al.*, 2024).

However, the authors also state that the accuracy achieved by feature clustering is not significantly higher than that achieved by temporal same-size sampling.

### 3.5. Results on the Preliminary Dataset

The results on the preliminary dataset differ from those obtained in the all-frame experiments:

- temporal every-10th-frame: 90.3% accuracy;
- temporal same-size: approximately 89.1%;
- feature clustering: approximately 88.5%.

Yang *et al.* (2024) state that factors such as video length, frame rate and the total number of frames may affect method selection, and that further research is required to identify an appropriate threshold or cut-off.

### 3.6. Scope of the Evidence

The results reported by Yang *et al.* (2024) demonstrate the benefit of feature clustering within the annotation-assistance workflow examined in the paper. The study does not use an independent held-out video protocol comparable to that used by Avena *et al.* (2026), and it does not report a direct comparison with SHIFT.

---

## 4. Avena et al. (2026)

### 4.1. Research Problem

Avena *et al.* (2026) directly investigate the selection of a subset of video frames in order to:

1. send the selected frames to annotators;
2. create bounding-box labels;
3. use only the selected frames to train an object detector;
4. evaluate the detector on the complete test split.

The paper introduces:

- the AVADiP-DFS benchmark;
- the SHIFT method;
- a multi-budget protocol for evaluating frame selection for object-detector training.

### 4.2. Dataset and Evaluation Protocol

AVADiP-DFS contains:

- 160 driving videos;
- 10 seconds per video;
- 30 FPS;
- 48,000 frames in total;
- bounding-box annotations for all frames;
- six classes: Person, Motorcycle, Animal, Bicycle, Car and Heavy Vehicle.

The videos are divided at video level into:

- 110 training videos;
- 15 validation videos;
- 35 testing videos.

No video contributes frames to more than one split.

Frame-selection methods operate only on the training split. The detector is evaluated on the complete test split at the original rate of 30 FPS.

All experiments use:

- YOLO11X;
- COCO-pre-trained weights;
- the same number of gradient updates;
- the same hyperparameters.

Avena *et al.* (2026) state that the selected frame set is the only experimental variable.

### 4.3. The SHIFT Method

SHIFT does not require ground-truth annotations or a previously trained detector during frame selection.

The method consists of two stages.

#### Stage 1: Temporal Information Rate Allocation

For two consecutive frames, the paper calculates:

\[
v_t = 1 - \operatorname{SSIM}(f_t, f_{t-1})
\]

It then calculates a cumulative variation signal:

\[
I(t)=\sum_{s=1}^{t}v_s
\]

Candidate frames are sampled uniformly in cumulative-variation space rather than uniformly in time. According to the paper, this allocation selects more frames from dynamic segments and fewer frames from static segments.

#### Stage 2: Feature-Space Entropy Maximisation

Each candidate frame is encoded using a pre-trained visual backbone. SHIFT uses pairwise cosine similarities to construct a kernel and selects the final subset using a log-determinant objective.

Greedy selection adds the frame with the greatest marginal entropy gain at each step until the budget \(K\) is reached. The purpose of this stage is to prioritise frames that contribute complementary information and reduce the selection of frames with similar embeddings.

Only after the final subset has been selected are the frames sent to annotators for bounding-box labelling.

### 4.4. Results Across Annotation Budgets

Avena *et al.* (2026) report the following mAP@0.5:0.95 results:

| Method | 1.0% | 1.7% | 3.3% | 6.7% | **10.0%** | 16.7% | 33.3% |
|---|---:|---:|---:|---:|---:|---:|---:|
| RFS | 19.8 | 19.9 | 21.8 | 22.2 | 24.4 | 25.4 | 25.4 |
| UFS | 20.8 | 21.3 | 21.7 | 23.7 | 24.9 | 25.4 | 26.3 |
| AFS-FSD | 17.2 | 19.3 | 20.9 | 21.6 | 27.2 | 25.5 | 25.2 |
| AFS-OFVD | 18.7 | 18.6 | 17.5 | 19.2 | 24.6 | 25.2 | 24.3 |
| AFS-SSVD | 17.8 | 18.4 | 19.1 | 20.4 | 27.1 | 22.6 | 24.9 |
| CSOD | 18.6 | 20.1 | 20.3 | 21.9 | 24.8 | 27.0 | 24.7 |
| **SHIFT** | **28.9** | **29.1** | **31.3** | **30.9** | **31.6** | **31.8** | **31.9** |

Training with the complete dataset without frame selection achieves **25.3 mAP**.

In this benchmark, SHIFT obtains the highest value at all seven reported annotation budgets.

### 4.5. Results at the 10% Budget

The source videos in AVADiP-DFS are recorded at 30 FPS. Under the paper's protocol, a 10% budget corresponds to 3 FPS.

At exactly 10%:

| Method | mAP@0.5:0.95 |
|---|---:|
| RFS | 24.4 |
| UFS | 24.9 |
| AFS-FSD | 27.2 |
| AFS-OFVD | 24.6 |
| AFS-SSVD | 27.1 |
| CSOD | 24.8 |
| **SHIFT** | **31.6** |
| Full dataset | 25.3 |

At this budget, SHIFT exceeds:

- UFS by 6.7 mAP;
- AFS-FSD by 4.4 mAP;
- AFS-SSVD by 4.5 mAP;
- the full-dataset reference by 6.3 mAP.

Avena *et al.* (2026) report that SHIFT begins to approach saturation at approximately 10% of the data. Its performance increases from 31.6 mAP at 10% to 31.8 at 16.7% and 31.9 at 33.3%.

### 4.6. Ablation Study

The ablation study at 1 FPS reports:

| Variant | mAP |
|---|---:|
| OFVD temporal allocation | 30.1 |
| Pixel-difference temporal allocation | 30.4 |
| Uniform temporal allocation | 30.9 |
| Without entropy maximisation | 29.3 |
| **Full SHIFT** | **31.3** |

The paper reports that:

- replacing SSIM with optical flow reduces performance by 1.2 mAP;
- replacing SSIM with pixel difference reduces performance by 0.9 mAP;
- replacing temporal allocation with uniform sampling reduces performance by 0.4 mAP;
- removing entropy-based diversity refinement reduces performance by 2.0 mAP.

According to the ablation analysis by Avena *et al.* (2026), removing entropy maximisation produces the largest reduction among the reported variants.

### 4.7. Frame-Selection Cost

Avena *et al.* (2026) report that:

- the overhead of UFS and RFS is negligible, and these methods are therefore omitted from the runtime plot;
- the AFS variants have fixed costs ranging from 487 seconds for AFS-SSVD to 673 seconds for AFS-OFVD;
- SHIFT increases from 535 seconds at 1.7% to 1,089 seconds at 33.3%;
- the fixed SSIM cost accounts for most of the runtime at low budgets;
- embedding extraction becomes the bottleneck at higher budgets.

The paper does not provide an exact runtime value in tabular form for the 10% budget. Therefore, an exact SHIFT runtime at 10% cannot be extracted from the paper.

---

## 5. Objective Comparison of the Three Papers

### 5.1. Differences in Evaluation Objectives

| Paper | Task | Purpose of frame selection | Model | Primary evaluation |
|---|---|---|---|---|
| Yoon and Choi (2023) | Instance segmentation | Reduce training data by removing redundant frames | Mask R-CNN | Instance-segmentation mAP |
| Yang *et al.* (2024) | Object-detection annotation | Reduce annotation corrections on the remaining frames | YOLOv8-small | Accuracy, total edits and action cost |
| Avena *et al.* (2026) | Object detection | Select a subset for annotation and detector training | YOLO11X | mAP@0.5:0.95 on independent test videos |

Because of these differences:

- the mAP reported by Yoon and Choi (2023) is not directly equated with the mAP reported by Avena *et al.* (2026);
- the accuracy and action-cost measures reported by Yang *et al.* (2024) are not converted into mAP;
- the three papers do not define a common aggregate metric.

### 5.2. Strongest Controlled Direct Comparison

The most relevant direct comparison is reported by Avena *et al.* (2026), because that paper implements:

- UFS;
- RFS;
- three AFS variants associated with the approach of Yoon and Choi (2023);
- CSOD;
- SHIFT;

using the same:

- dataset;
- training-validation-testing split;
- detector;
- hyperparameters;
- gradient-update budget;
- evaluation metric.

In this comparison, SHIFT achieves the highest mAP at every annotation budget, including the 10% budget.

### 5.3. Position of Feature Clustering

Feature clustering in Yang *et al.* (2024) produces the best results in the paper's AI-assisted annotation workflow when assessed by total edits and action cost in the all-frame experiments.

However, Yang *et al.* (2024):

- do not compare feature clustering with SHIFT;
- do not use the held-out video protocol used by Avena *et al.* (2026);
- do not report detector mAP on an independent test split;
- do not fully report the computational complexity of frame selection.

The three papers therefore do not provide evidence for concluding that the feature-clustering method of Yang *et al.* (2024) is either better or worse than SHIFT for training a detector that generalises to independent test videos.

---

## 6. Rationale for Selecting SHIFT

The selection of SHIFT is based on the following evidence reported by Avena *et al.* (2026).

### 6.1. The Most Relevant Experimental Objective

Avena *et al.* (2026) directly investigate the workflow:

> select frames from video → annotate the selected frames with bounding boxes → train an object detector → evaluate it on test videos.

This differs from the instance-segmentation task of Yoon and Choi (2023) and from the annotation-correction workflow applied to the remaining frames by Yang *et al.* (2024).

### 6.2. Controlled Comparison Against Alternative Methods

Avena *et al.* (2026) hold the model, hyperparameters, number of gradient updates and evaluation protocol constant. The selected frame set is the principal experimental variable.

Under this setting, SHIFT outperforms all comparison methods at every reported budget.

### 6.3. Best Result at the Selected 10% Budget

At 10%, SHIFT achieves 31.6 mAP, exceeding:

- UFS;
- RFS;
- all three AFS variants;
- CSOD;
- the detector trained using the complete dataset.

This provides the direct quantitative basis for selecting SHIFT when the budget has been fixed at 10%.

### 6.4. Near-Saturation at 10%

According to Avena *et al.* (2026), SHIFT performance approaches saturation at approximately 10%. Increasing the budget from 10% to 33.3% increases mAP from 31.6 to 31.9.

This conclusion applies only to the AVADiP-DFS benchmark investigated in the paper.

### 6.5. Both Stages Are Examined Through Ablation

The ablation study shows that:

- temporal allocation contributes to the reported result;
- entropy-based diversity refinement has a larger effect when removed;
- full SHIFT achieves the highest result among the reported ablation variants.

### 6.6. No Annotation Is Required During Frame Selection

SHIFT does not require ground-truth annotations or a previously trained detector during frame selection. Bounding-box labels are created only after the final subset has been selected.

---

## 7. Decision Derived from the Three Papers

Based on the evidence reported in the three papers:

- **UFS** is simple and has negligible overhead in the benchmark of Avena *et al.* (2026), but performs below SHIFT at the 10% budget.
- **AFS**, as represented by the direction of Yoon and Choi (2023), demonstrates the value of exploiting temporal redundancy. However, when the AFS variants are evaluated by Avena *et al.* (2026) under the same object-detection protocol, all remain below SHIFT at 10%.
- **Feature clustering** in Yang *et al.* (2024) reduces total edits and action cost within that paper's annotation workflow, but is not evaluated using held-out detector mAP and is not directly compared with SHIFT.
- **SHIFT** has the strongest direct evidence for selecting frames to train an object detector and achieves the highest mAP at the 10% budget in the controlled benchmark reported by Avena *et al.* (2026).

The selected method is therefore:

> **SHIFT with an annotation budget equal to 10% of the total number of frames.**

This decision is based on the results obtained on AVADiP-DFS. Avena *et al.* (2026) evaluate SHIFT exclusively on driving videos; the paper does not report experiments on supermarket videos or full-day retail surveillance footage. This review therefore does not claim that the value of 31.6 mAP, or the same degree of improvement, will be reproduced on retail data.

---

## References

Avena, V., Sobrinho, J.V.D., Castilho, D., Couto, R.S., Campista, M.E.M., Costa, L.H.M.K. and Carvalho, A.C.P.L.F. (2026) Which frames matter? Frame selection for training object detectors on driving videos. In: *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*. Denver, Colorado, USA, 3–4 June 2026. IEEE/CVF, pp. 2870–2879. Available from: https://www.gta.ufrj.br/ftp/gta/TechReports/ASC26.pdf [Accessed 28 July 2026].

Yang, J., Hisey, R., Bierbrier, J., Law, C., Fichtinger, G. and Holden, M. (2024) Frame selection methods to streamline surgical video annotation for tool detection tasks. In: *2024 IEEE Canadian Conference on Electrical and Computer Engineering (CCECE)*. Kingston, Ontario, Canada, 6–9 August 2024. IEEE, pp. 892–898. Available from: https://doi.org/10.1109/CCECE59415.2024.10667104 [Accessed 28 July 2026].

Yoon, J. and Choi, M.-K. (2023) Exploring video frame redundancies for efficient data sampling and annotation in instance segmentation. In: *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*. Vancouver, Canada, 18–22 June 2023. IEEE/CVF, pp. 3308–3317. Available from: https://openaccess.thecvf.com/content/CVPR2023W/VDU/html/Yoon_Exploring_Video_Frame_Redundancies_for_Efficient_Data_Sampling_and_Annotation_CVPRW_2023_paper.html [Accessed 28 July 2026].
