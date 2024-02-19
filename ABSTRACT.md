The authors collected and labeled a detection dataset named **Human Parts Dataset** which contains annotations of three categories, including person, hand and
face. The proposed dataset contains high-resolution images which are randomly selected from [AI-challenger](https://opendatalab.com/OpenDataLab/AI_Challenger) dataset.

## Motivation

Detecting the human body, face, and hand robustly in natural settings is fundamental to general object detection. This capability is essential for a variety of tasks centered around individuals, including pedestrian detection, person re-identification, facial landmarking, and driver behavior monitoring. Over decades, considerable attention has been devoted to addressing the challenges of detecting human body parts in natural environments, leading to significant advancements in recent detection algorithms. This progress is largely attributed to the evolution of deep Convolutional Neural Networks (CNNs), which have greatly enhanced person, face, and hand detection. Human body parts constitute multi-level objects, with faces and hands being sub-components of the body. Similar multi-level object structures are prevalent in everyday scenarios, such as laptops and keyboards, lungs and lung nodules, or buses and wheels. Despite this, many detection frameworks overlook the inherent correlations between these multi-level objects. Instead, they tend to treat sub-objects and objects uniformly, neglecting the nuanced relationships between them in solving multi-level object detection challenges.

In tasks involving multi-level objects using general detection algorithms, detecting large objects such as the human body typically yields relatively high performance. However, significant challenges arise in real-world applications, particularly when training detectors for small objects like faces and hands. These challenges stem from the considerable pose variations and frequent occlusions encountered, which hinder the attainment of detection capabilities comparable to those of humans. The substantial scale disparity between the body (objects) and its smaller parts (sub-objects) results in the predominance of large objects, such as the human body, occupying the majority of the image. Conversely, small objects like hands and faces typically occupy a comparatively smaller area. Consequently, during training, there tends to be an abundance of background information relative to the small objects, leading to significant interference during small object detection.

<img src="https://github.com/dataset-ninja/human-parts/assets/120389559/2ad2cf10-62fe-4ed8-b505-3dcc688561a8" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Examples of multi-level objects. Boxes in green are sub-objects of boxes in blue.</span>

## Dataset description

In their work, the authors perform the *person*, *face* and *hand* detection tasks together to explore the more efficient detection methods for the multi-level objects. They collected and labeled a detection Human Parts Dataset. The proposed dataset contains high-resolution images which were randomly selected from [AI-challenger](https://opendatalab.com/OpenDataLab/AI_Challenger) dataset. *Person* category has already been labeled in this dataset. However, the small human whose body parts are hard to distinguish or the vague ones whose body contours are hard to recognize are missed-labeled in this dataset. The authors added the missed *person* body annotations and labeled *hand* and *face* additionally in each image. The number of persons in each image range from 1 to 11. In total, dataset consists of 14,962 images (12,000 for train, 2,962 for testing) with 10,6879 annotations (35,306 persons, 27,821 faces and 43,752 hands). They have labeled every visible person, hand or face with xmin, ymin, xmax and ymax coordinates and ensured that annotations cover the entire objects including the blocked parts but without extra background. 

<img src="https://github.com/dataset-ninja/human-parts/assets/120389559/ab9dd995-398a-45e0-9657-02608e61c68f" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Samples of annotated images in the Human Parts Dataset.</span>

| DataSet        | Images   | Person | Hand | Face | Total Instance |
|----------------|----------|--------|------|------|----------------|
| Caltech        | 42,782   | X      | -    | -    | 13,674         |
| CityPersons    | 2,975    | X      | -    | -    | 19,238         |
| VGG Hand       | 4,800    | -      | X    | -    | 15,053         |
| EgoHands       | 11,194   | -      | X    | -    | 13,050         |
| FDDB           | 2,854    | -      | -    | X    | 5,171          |
| Wider Face     | 32,203   | -      | -    | X    | 393,703        |
| Human Parts    | 14,962   | X      | X    | X    | 106,879        |

<span style="font-size: smaller; font-style: italic;">Comparison of different human parts detection datasets.</span>


