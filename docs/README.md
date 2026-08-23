# Reference studies

This folder contains research papers related to occlusion handling in object detection, person re-identification, tracking, gait recognition, and supporting neural-network components.

Each summary explains:

- **Purpose:** The problem studied by the paper.
- **Approach:** The proposed method.
- **Result:** The main reported outcome.
- **Limitation:** An important restriction or remaining problem.

> **Note:** The limitations include points reported by the authors and short critical observations based on each paper's datasets and evaluation scope. Paper numbering follows the filenames, and `paper36.pdf` is not present.

## Paper summaries

### Paper 1 — [CAE-YOLOV8](paper/paper1.pdf)

- **Purpose:** Detect industrial objects reliably when they are partly hidden, especially for robotic grasping.
- **Approach:** Adds CBAM attention, AKConv and an EffCIoU loss to YOLOv8s.
- **Result:** Reached 91.8% accuracy at 60% occlusion, compared with 88.8% for the original model.
- **Limitation:** Tested on a small, specialised tool dataset containing many artificially occluded images.

### Paper 2 — [Improving Prohibited Item Detection in X-Ray Images](paper/paper2.pdf)

- **Purpose:** Improve prohibited-item detection in cluttered and heavily overlapping X-ray images.
- **Approach:** Compares Faster R-CNN, an STN-enhanced Faster R-CNN and RFBNet, with occlusion-aware augmentation.
- **Result:** STN Faster R-CNN produced the best result, with an mAP of 42.85%.
- **Limitation:** The spatial transformer sometimes learned an almost unchanged transformation, and the experiments used only a subset of SIXray.

### Paper 3 — [AODet](paper/paper3.pdf)

- **Purpose:** Detect tiny, occluded people in drone images using RGB and thermal information.
- **Approach:** Uses cross-level query selection, dense distinct queries and RGB–thermal feature fusion.
- **Result:** Achieved 47.66% mAP50 overall and 49.40% for tiny people on RGBTDronePerson.
- **Limitation:** Requires aligned RGB and thermal images and was evaluated mainly on drone-based person datasets.

### Paper 4 — [Impact of Occlusion-Level Distribution](paper/paper4.pdf)

- **Purpose:** Understand how the amount and variety of training occlusion affect detector robustness.
- **Approach:** Trains YOLOv8 models on datasets with different average occlusion levels and distributions.
- **Result:** Moderate training occlusion, around 40%, generally produced the most reliable performance.
- **Limitation:** Most occlusions were synthetically generated, so the best distribution may differ in real environments.

### Paper 5 — [Occlusion Handling in Generic Object Detection: A Review](paper/paper5.pdf)

- **Purpose:** Review major methods for handling occlusion in general object detection.
- **Approach:** Organises research into areas such as data augmentation, GANs, amodal perception, segmentation and compositional models.
- **Result:** Provides a useful taxonomy and identifies important future research directions.
- **Limitation:** It is a literature review rather than a newly tested model and focuses mainly on still images.

### Paper 6 — [Deep Occlusion-Aware Instance Segmentation With Overlapping BiLayers](paper/paper6.pdf)

- **Purpose:** Segment an object while also understanding which object is hiding it.
- **Approach:** Uses a bilayer graph structure to model the occluder and occluded object separately.
- **Result:** Produced consistent improvements on COCO and KINS, particularly for strongly overlapping objects.
- **Limitation:** The two-layer representation may be insufficient for scenes containing several overlapping depth layers.

### Paper 7 — [Compositional Convolutional Neural Networks](paper/paper7.pdf)

- **Purpose:** Make object recognition more robust and interpretable under partial occlusion.
- **Approach:** Replaces the normal classifier head with a part-based compositional model that separates object parts, pose and background.
- **Result:** Outperformed standard CNN classifiers on synthetic and real occlusion tests.
- **Limitation:** The model is more complex than a conventional classifier and has a trade-off between recognition and occluder localisation.

### Paper 8 — [Occlude Them All](paper/paper8.pdf)

- **Purpose:** Improve person re-identification when important body regions are hidden.
- **Approach:** Generates occlusions during training and uses an attention-guided mask to reduce the influence of hidden regions.
- **Result:** Reached 62.6% Rank-1 accuracy and 46.1% mAP on Occluded-Duke.
- **Limitation:** Its effectiveness depends on how well the generated occlusions represent real-world conditions.

### Paper 9 — [Occluded and Overlapping Tomato Leaf Disease Detection](paper/paper9.pdf)

- **Purpose:** Detect diseases on tomato leaves when leaves overlap or are covered by other material.
- **Approach:** Improves YOLOv3-tiny with inverse residual blocks, multi-scale training and foreground-focused annotations.
- **Result:** Reached 98.3% mAP for deeply separated leaves, 92.1% under debris occlusion and 90.2% for overlapping leaves.
- **Limitation:** Evaluated on a self-created tomato dataset, so performance on other plants and environments is uncertain.

### Paper 10 — [Face Detection Under Occlusion and Non-Uniform Illumination](paper/paper10.pdf)

- **Purpose:** Detect faces when lighting is uneven or facial areas are covered.
- **Approach:** Combines YCbCr, HSV and Lab colour information with histogram equalisation, morphology and facial-feature checks.
- **Result:** Reduced false detections and improved accuracy over the compared traditional methods.
- **Limitation:** Hand-designed colour rules can struggle with unusual lighting, darker skin tones, extreme poses and very small faces.

### Paper 11 — [Remote-Sensing Object Tracking With Deep Reinforcement Learning](paper/paper11.pdf)

- **Purpose:** Keep tracking remote-sensing objects when clouds or other objects hide them.
- **Approach:** Uses deep reinforcement learning with appearance, movement and temporal context to choose tracking actions.
- **Result:** Reported 92.6% precision at a 20-pixel threshold.
- **Limitation:** Tracking can fail when an object is completely hidden by multiple clouds.

### Paper 12 — [DSW-YOLO](paper/paper12.pdf)

- **Purpose:** Detect ground-planted strawberries under different levels of leaf and fruit occlusion.
- **Approach:** Adds DCNv3, Shuffle Attention and WIoU to YOLOv7.
- **Result:** Achieved 86.7% mAP50 and approximately 10.9 frames per second on Jetson Xavier NX.
- **Limitation:** Strong sunlight, overexposure and severe occlusion still caused missed or incorrect detections.

### Paper 13 — [Occlusion Target Detection Based on Improved YOLOv5](paper/paper13.pdf)

- **Purpose:** Improve tool detection under target-to-target and background occlusion.
- **Approach:** Introduces Coordinate Attention, CIoU and a kCIoU-based non-maximum suppression method.
- **Result:** At 60% occlusion, accuracy reached 83.8% for target occlusion and 87.6% for background occlusion.
- **Limitation:** The experiments used a limited set of tools and controlled occlusion conditions.

### Paper 14 — [YOLO-Owl](paper/paper14.pdf)

- **Purpose:** Detect occluded objects in poorly illuminated environments.
- **Approach:** Uses multi-scale feature refinement, feature enhancement and an occlusion-aware attention module.
- **Result:** Achieved 78.18% mAP on an expanded ExDark dataset.
- **Limitation:** Accuracy still decreases as occlusion becomes more severe, and testing focused mainly on low-light images.

### Paper 15 — [Improved PP-YOLOE and DeepSORT](paper/paper15.pdf)

- **Purpose:** Detect and track pedestrians when they are partly hidden.
- **Approach:** Adds spatial attention and lightweight convolution to PP-YOLOE, then uses DeepSORT for tracking.
- **Result:** Reached 81.10% mAP at 72 FPS, while DeepSORT achieved 57.5 MOTA.
- **Limitation:** Detection delays and identity errors can still occur in complex, heavily occluded scenes.

### Paper 16 — [Occlusion Handling and Multi-Scale Pedestrian Detection: A Review](paper/paper16.pdf)

- **Purpose:** Review methods for detecting pedestrians at different sizes and occlusion levels.
- **Approach:** Examines part-based models, attention, feature fusion, specialised losses and occlusion-aware NMS.
- **Result:** Shows that visible-region supervision and attention mechanisms are particularly useful.
- **Limitation:** It does not introduce a new experimental model, and heavy occlusion remains an unsolved problem.

### Paper 17 — [CBAM and Coordinate Attention Placement in YOLOv8n](paper/paper17.pdf)

- **Purpose:** Determine where attention modules should be placed for occluded vehicle detection.
- **Approach:** Tests CBAM and Coordinate Attention in the backbone, neck and both locations of YOLOv8n.
- **Result:** CBAM in the neck performed best, reaching 68.3% mAP50 and 47.6% mAP50–95.
- **Limitation:** The experiment used one model size and a modified KITTI dataset, so the best placement may not generalise.

### Paper 18 — [Improved YOLOv7-Tiny for Occluded Vehicles and Pedestrians](paper/paper18.pdf)

- **Purpose:** Improve real-time road-user detection under occlusion.
- **Approach:** Adds Coordinate Attention, global attention, modified convolution blocks and Focal-CIoU.
- **Result:** Achieved 82.2% mAP50, an improvement of 2.8 percentage points.
- **Limitation:** Small, heavily occluded vehicles remain difficult, and testing was limited to PASCAL VOC.

### Paper 19 — [DSONet](paper/paper19.pdf)

- **Purpose:** Detect densely arranged, overlapping ships while keeping the model lightweight.
- **Approach:** Uses dual-feature processing, adaptive upsampling, an additional small-object feature layer and an oriented detection head.
- **Result:** Delivered a strong balance of detection accuracy, model size and speed across several ship datasets.
- **Limitation:** Occlusion above approximately 70% still produced false positives and missed ships.

### Paper 20 — [YOLO-Ball](paper/paper20.pdf)

- **Purpose:** Detect fast-moving sports balls under occlusion and motion blur.
- **Approach:** Adds multi-branch occlusion attention, a shallow bidirectional feature pyramid and a dynamic NWD–IoU loss.
- **Result:** Achieved 82.2% precision and 70.9% mAP50, improving over several recent YOLO models.
- **Limitation:** It handles partially visible balls but cannot identify a ball that is completely invisible.

### Paper 21 — [GPT-4 for Occlusion Order Recovery](paper/paper21.pdf)

- **Purpose:** Determine which object is in front when objects overlap.
- **Approach:** Prompts GPT-4 with an image and object categories, then converts its pairwise answers into an occlusion-order matrix.
- **Result:** Improved occlusion-order accuracy over simple position, area and bounding-box rules on COCOA and InstaOrder.
- **Limitation:** GPT-4 can give ambiguous answers, does not provide object boxes and may create reproducibility or service-cost concerns.

### Paper 22 — [AodeMar](paper/paper22.pdf)

- **Purpose:** Detect partially occluded vessels for autonomous maritime systems.
- **Approach:** Combines coordinate-aware position enhancement with spatial-pyramid and Swin Transformer feature processing.
- **Result:** Achieved 95.43% mAP50, 82.57% mAP50–95 and 99.01 FPS.
- **Limitation:** Objects split into very small or disconnected visible fragments remain difficult to detect.

### Paper 23 — [Efficient Person Re-Identification With Progressive Filter Pruning](paper/paper23.pdf)

- **Purpose:** Create a smaller person ReID model while preserving body-part information.
- **Approach:** Combines body-part-aware feature learning with Progressive Soft Filter Pruning.
- **Result:** Reduced FLOPs by about 37% and memory by 16.7% while retaining more than 91% of the original performance.
- **Limitation:** Pruning still caused an accuracy reduction, and the method was evaluated mainly in image-based, closed-set ReID.

### Paper 24 — [YOLO11-Occ](paper/paper24.pdf)

- **Purpose:** Improve YOLO11 detection when objects are partially hidden.
- **Approach:** Uses superpixel segmentation, graph convolution, occlusion attention and an occlusion-focused loss.
- **Result:** Improved mAP50 by 10.28 percentage points over the original YOLO11 on KITTI.
- **Limitation:** Superpixel and graph processing add complexity, and evaluation was limited to one driving dataset.

### Paper 25 — [POANET](paper/paper25.pdf)

- **Purpose:** Reduce interference from occluding objects in person ReID.
- **Approach:** Detects the location and extent of occlusion, suppresses hidden regions and extracts head, torso and leg features.
- **Result:** Achieved state-of-the-art CNN performance and was competitive with larger transformer models using fewer parameters.
- **Limitation:** Training depends on large synthetic data, body-part information and generated occlusion examples.

### Paper 26 — [Strategic Feature Integration for Person ReID](paper/paper26.pdf)

- **Purpose:** Improve ReID by combining reliable local body features with global appearance.
- **Approach:** Uses human parsing to locate parts and a correlation-aware module to fuse part and global features.
- **Result:** Improved Rank-1 accuracy by 10.6 points and mAP by 16 points over the nearest competitor on Occluded-ReID.
- **Limitation:** Human-parsing errors and very severe occlusion can reduce performance.

### Paper 27 — [Attention and Part-Based Gait Recognition](paper/paper27.pdf)

- **Purpose:** Recognise people from walking patterns despite viewpoint and appearance changes.
- **Approach:** Combines global silhouette features, CBAM attention and structural body-part representations.
- **Result:** Outperformed the evaluated baseline methods across multiple camera viewpoints.
- **Limitation:** Performance depends on accurate silhouettes and can be affected by clothing, carried objects and difficult backgrounds.

### Paper 28 — [Body-Part-Based Feral Cat Identification](paper/paper28.pdf)

- **Purpose:** Identify individual feral cats when the entire animal is not clearly visible.
- **Approach:** Trains models on the body, front leg, back leg and tail, then combines their features.
- **Result:** The full-body region reached 91% accuracy, while combined part features reached 92%.
- **Limitation:** The dataset contained only ten cats, and the method depends on obtaining suitable body-part crops.

### Paper 29 — [Part-Based Gait Recognition With Ensemble Learning](paper/paper29.pdf)

- **Purpose:** Make gait recognition more robust to clothing and carried objects.
- **Approach:** Divides gait energy images into five horizontal parts and fuses predictions from separate CNN models.
- **Result:** Outperformed the compared methods on CASIA-B, CASIA-C and Outdoor-Gait.
- **Limitation:** It relies on accurate silhouettes and uses several part models, increasing computational cost.

### Paper 30 — [Advanced Contextual Reconstruction Architecture](paper/paper30.pdf)

- **Purpose:** Reconstruct useful object features when much of an object is missing.
- **Approach:** Combines contextual reconstruction, diffusion-based feature completion, adaptive attention and a fragment-aware loss.
- **Result:** Reported 93.2% mAP50 under heavy occlusion, improving by 21.4 percentage points.
- **Limitation:** The architecture is computationally complex and was evaluated mainly on COCO-style still images.

### Paper 31 — [Dual-Branch Occlusion-Aware ReID Network](paper/paper31.pdf)

- **Purpose:** Extract reliable identity features while also reconstructing hidden body regions.
- **Approach:** One branch selects visible semantic parts, while a second branch reconstructs occluded person information.
- **Result:** Outperformed existing methods across occluded, partial and standard person ReID datasets.
- **Limitation:** It depends on human-parsing supervision, and reconstructed features can be unreliable for rare or severe occlusions.

### Paper 32 — [CBAM](paper/paper32.pdf)

- **Purpose:** Help CNNs focus on important feature channels and spatial locations.
- **Approach:** Applies channel attention followed by spatial attention as a lightweight plug-in module.
- **Result:** Consistently improved classification and detection on ImageNet, COCO and VOC with relatively small overhead.
- **Limitation:** CBAM is a general attention module and does not explicitly recover information missing because of occlusion.

### Paper 33 — [Squeeze-and-Excitation Networks](paper/paper33.pdf)

- **Purpose:** Improve CNN features by learning which channels are most useful.
- **Approach:** Globally summarises each feature channel and assigns it a learned importance weight.
- **Result:** The SENet model won ILSVRC 2017 with a 2.251% top-five error rate.
- **Limitation:** It models channel importance but not the spatial position or structure of an occluded region.

### Paper 34 — [Coordinate Attention](paper/paper34.pdf)

- **Purpose:** Add spatial position information to lightweight channel attention.
- **Approach:** Separately pools features in the horizontal and vertical directions before calculating attention.
- **Result:** Improved mobile-network performance in classification, detection and segmentation with little additional cost.
- **Limitation:** It is a general feature-enhancement component rather than a complete occlusion-handling method.

### Paper 35 — [Object Detection Using Part-Based Semantic Segmentation](paper/paper35.pdf)

- **Purpose:** Detect objects from visible sections when their complete shape cannot be observed.
- **Approach:** Labels four object quarters with an FCN or U-Net, then geometrically groups the visible quarters into object boxes.
- **Result:** The U-Net version used about 11 million parameters and required approximately 0.061 seconds per image, with accuracy comparable to Mask R-CNN.
- **Limitation:** The fixed four-part layout assumes predictable object geometry and was tested mainly on road scenes.

### Paper 37 — [YOLOv10](paper/paper37.pdf)

- **Purpose:** Produce fast, end-to-end object detection without traditional non-maximum suppression.
- **Approach:** Uses consistent dual-label assignments and jointly optimises model accuracy and computational efficiency.
- **Result:** Achieved a strong latency–accuracy balance across different YOLOv10 model sizes.
- **Limitation:** It is a general-purpose detector and does not specifically evaluate or model severe occlusion.

### Paper 38 — [YOLOv11 Architectural Overview](paper/paper38.pdf)

- **Purpose:** Explain the main architectural improvements introduced in YOLOv11.
- **Approach:** Reviews components such as C3k2, SPPF and C2PSA across different model sizes and tasks.
- **Result:** Reports improved accuracy, speed and parameter efficiency over earlier YOLO versions.
- **Limitation:** It is mainly a secondary architectural overview and contains no dedicated occlusion experiment.

### Paper 39 — [Ultralytics YOLO26](paper/paper39.pdf)

- **Purpose:** Create a unified, end-to-end real-time vision model for several computer-vision tasks.
- **Approach:** Uses an NMS-free dual-head design, removes DFL and introduces MuSGD, Progressive Loss and STAL.
- **Result:** Reported 40.9–57.5 box mAP across model sizes, with T4 inference times from 1.7 to 11.8 milliseconds.
- **Limitation:** Evaluation concentrates on standard benchmarks, and the architecture is not specifically designed for occlusion.

### Paper 40 — [eAodeMar](paper/paper40.pdf)

- **Purpose:** Make occluded-vessel detection practical on embedded maritime hardware.
- **Approach:** Creates a lighter AodeMar model using Ghost convolution and TensorRT optimisation.
- **Result:** Reduced parameters by 7% with only a 0.42-point accuracy loss and reached 37.45 FPS in testing.
- **Limitation:** Lightweight processing introduces a small accuracy trade-off, while extremely fragmented vessels remain difficult.

### Paper 41 — [LDConv](paper/paper41.pdf)

- **Purpose:** Make deformable convolution more flexible and parameter-efficient.
- **Approach:** Learns offsets for an arbitrary number and arrangement of sampling points, allowing parameters to grow linearly.
- **Result:** Improved several CNNs and datasets while providing a better accuracy–efficiency balance than standard and deformable convolutions.
- **Limitation:** The best sampling shape still requires experimentation, and LDConv does not directly solve occlusion by itself.
