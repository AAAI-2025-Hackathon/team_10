# team_10

<pre style="color: 164194;">

       #####         ####+                                                                +####        ###*                                                 
      =#####.       #####+                                                                ######      :###=                                                 
     :######-     .######+      ...          .-=-:.    ...:::.              -==-.        +######*     =###         .-==:       ....        ....      ....   
     *##+###+     ###+###=     +###      =########=    ##########-      *##########:     *##**###+    *##*     :##########*    *###       ####      #####*  
    +### ###*    ###=-###=     ###+    -####+.   .    ####   :####    *###*:   =####-    ###.:####.  .###:   .####+.  .*####   =###-     ###*     .#######  
   :###: *###  .###= =###-    =###:   +###*           ###*   -###+   ####       -###=   *###  =####. *###   -###+       *###:  .###+    ####     :###--###: 
   ###+  =###- ###-  =###-    +###   .###*           :##########:   =###:       =###=   ###*   *###* ###*   ####        *###.   *###  .###*     :###:  #### 
  +###.  :###+*##=   +###:    ###=   -###+           *###*###.      ####        *###   :###:    ####+###    ###+       :###*    -###:.###+     -###:   ####.
 :###-    ######=    +###.   +###    -####.         .###= *###:     *###=     -####.   *###     :######*    ####.     +###*     .###*###+     +############:
 ####     #####=     *###.   ###*     *#########:   =###:  ####.    .############=     ###=      -#####=    =############.       *#####+     *###.     :###*
+**#.     =***=      ***#   .**#-       -*#####+    ****   .****.     .+#####*-       =***.       ****#       -*#####+:          -#***-     +***        ***#

</pre>

# Hackathon Template

Instructions:
1. This repository must be used as a template to create your teams' submission repository.
2. The Check-In section must remain intact, and you must edit it to include your details. Please indicate agreement to the terms by makring the checklist with an `[x]`.
3. The final demo video can be included as a file in the submission repository, or as a publicly accessible video on any website (e.g., Youtube).
4. All other sections, including this, can be edited as you see fit - including removing these instructions for your submission.


# Check-In

- Title of your submission: **[EpilepsyMRI: Machine Learning for Epilepsy Analysis]**
- Team Members: [Tobias Haar](mailto:tobias.haar@micronova.de), [Vignesh Gogulavasan](mailto:vignesh.gogulavasan@micronova.de), [Vojtech Brenik](mailto:vojtech.brenik@micronova.de), [Carolin Rickert](mailto:carolin.rickert@micronova.de)
- [x] All team members agree to abide by the [Hackathon Rules](https://aaai.org/conference/aaai/aaai-25/hackathon/)
- [x] This AAAI 2025 hackathon entry was created by the team during the period of the hackathon, February 17 – February 24, 2025
- [x] The entry includes a 2-minute maximum length demo video here: [Link](https://your-link.com)
- [x] The entry clearly identifies the selected theme in the README and the video.


# Project Description
This project applies machine learning to analyze MRI scans and clinical data from the IDEAS dataset (doi:10.18112/openneuro.ds005602.v1.0.0), aiming to uncover patterns in brain structure related to drug-resistant focal epilepsy. By leveraging imaging and demographic data, we seek to improve lesion detection, identify biomarkers, and explore factors influencing surgical outcomes. Our approach combines deep learning and statistical modeling to enhance the understanding of epilepsy and support clinical decision-making.

# Repository structure
```
dataset/                   # Dataset files for training and testing
demo_data/                 # Demo data for showcasing the application
epilepsydetection/         # Epilepsy detection application
├── resources/             # Static resources (images, icons)
├── create_empty_masks.py  # Script for creating empty masks
├── dict_model.py          # Custom model for dictionary data
├── epilepsydetection.py   # UI main window definition 
├── epilepsydetection.ui   # UI layout file
├── main.py                # Main application window and logic
└── model.py               # ML model functions for loading and inference
notebooks/                 # Jupyter notebooks for data analysis and model training pipelines
```

# Data downloading

In this project we use the IDEAS (The Imaging Database for Epilepsy And Surgery) obtained from https://openneuro.org/datasets/ds005602/versions/1.0.0.

You can download the dataset by executing the ds005602-1.0.0.sh script from OpenNeuro git bash or any other tool for executing bash scripts:

When using VSCode you can open a new Terminal and select the arrow next to the "+" sign on the bottom right corner of the terminal UI in VSCode and select "Git bash" where you can just type the following command to download the dataset.

```
sh ds005602-1.0.0.sh
```

# Tech stack

### Frontend:
- PySide6: Qt for Python framework for creating the UI
- QtAwesome: Icons from fontawesome
- pyvistaqt: PyVista integration with Qt for 3D plotting

### Backend:
- nnunetv2: 3D medical image segmentation framework based on the nnUNet architecture
- Numpy: Fundamental package for scientific computing with Python
- Pandas: Data manipulation and analysis tool
- scikit-learn: Machine learning library for Python

# Main features
1) Brain MRI Visualization: View MRI scans with rotation and scroll through different planes (axial, sagittal, coronal) to explore the brain structure.
       -> all preliminary analysis of the dataset can be found in the notebooks/data_analysis.ipynb
2) Epilepsy Prediction: Based on specific parameters extracted from MRI scans, the model predicts whether a person has epilepsy or is healthy.
       -> For this purpose, 5 models were trained and tested: Gaussian Naive Bayes, Random Forest, Linear Regression,K Nearest Neighbors, and a simple Neural Network.
       -> Random Forest model was chosen as the best performing model.
       -> All models and their evaluation can be found in the notebooks/featurebased_prediction.ipynb
3) Resection Mask Prediction: For epileptic patients, the model predicts the resection mask (area affected in the brain), indicating the area of the brain that may require surgical intervention.
       -> For this purpose, a U-Net model was trained.
       -> The model and its results can be found in the notebooks/model_training.ipynb


# Demo use case
important: ideally, this should be run using the GPU, using the CPU is also possible but the inference time will be longer.

1) create a new virtual environment using python 3.10 and install the dependencies in requirements.txt
2) Run the main.py file to start the application.
3) click on "load MRI" and from demo_data, select one MRI scan 
       - e.g. control_4012_mri.nii.gz for a healthy person or
       - e.g. patient_1_mri.nii.gz for a patient with epilepsy
4) you can then scroll through the MRI using the slider or rotate it by dragging the mouse on the image
5) To predict whether the person has epilepsy or not, click "load patient data" and select the corresponding csv file from the demo_data folder
       - e.g. control_4012_markers.csv for a healthy person or
       - e.g. patient_1_markers.csv for a patient with epilepsy
6) click on "predict epilepsy" and the model will make a prediction and display it in the UI
7) To show the resection mask (affected area of the brain) created by physicians, click "load mask" and select the corresponding file from the demo_data folder
       - e.g. mask.nii.gz for a patient with epilepsy
       - for healthy patients this does not exist
8) To predict the resection mask based on the MRI scan, click "generate mask" and the model will make a prediction and display it in the 3D image viewer







