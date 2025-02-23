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


# Check-In

- Title of your submission: **[EpilepsyMRI: Machine Learning for Epilepsy Analysis]**
- Team Members: [Tobias Haar](mailto:tobias.haar@micronova.de), [Vignesh Gogulavasan](mailto:vignesh.gogulavasan@micronova.de), [Vojtěch Breník](mailto:vojtech.brenik@micronova.de), [Carolin Rickert](mailto:carolin.rickert@micronova.de)
- [x] All team members agree to abide by the [Hackathon Rules](https://aaai.org/conference/aaai/aaai-25/hackathon/)
- [x] This AAAI 2025 hackathon entry was created by the team during the period of the hackathon, February 17 – February 24, 2025
- [x] The entry includes a 2-minute maximum length demo video here: [Link](https://your-link.com)
- [x] The entry clearly identifies the selected theme in the README and the video.


# Project Description
This project applies machine learning to analyze MRI scans and clinical data from the IDEAS dataset (doi:10.18112/openneuro.ds005602.v1.0.0). The application provides an interactive visualization of MRI data, enables epilepsy diagnosis based on key parameters, and predicts resection masks for epileptic patients.


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


# Tech stack

### Frontend:
- [PySide6](https://pypi.org/project/PySide6/): Qt for Python framework for creating the UI
- [QtAwesome](https://pypi.org/project/QtAwesome/): Icons from fontawesome
- [pyvistaqt](https://pypi.org/project/pyvistaqt/): PyVista integration with Qt for 3D plotting

### Backend:
- [nnunetv2](https://github.com/MIC-DKFZ/nnUNet/tree/master): 3D medical image segmentation framework based on the nnUNet architecture
- [Numpy](https://pypi.org/project/numpy/): Fundamental package for scientific computing with Python
- [Pandas](https://pandas.pydata.org/docs/index.html): Data manipulation and analysis tool
- [scikit-learn](https://scikit-learn.org/stable/): Machine learning library for Python

# Main features
1) **Brain MRI Visualization**: View MRI scans with rotation and scroll through different planes (axial, sagittal, coronal) to explore the brain structure.
       -> all preliminary analysis of the dataset can be found in the notebooks/data_analysis.ipynb
2) **Epilepsy Prediction**: Based on specific parameters extracted from MRI scans, the model predicts whether a person has epilepsy or is healthy.
       -> For this purpose, 5 models were trained and tested: Gaussian Naive Bayes, Random Forest, Linear Regression,K Nearest Neighbors, and a simple Neural Network.
       -> Random Forest model was chosen as the best performing model.
       -> All models and their evaluation can be found in the notebooks/featurebased_prediction.ipynb
3) **Resection Mask Prediction**: For epileptic patients, the model predicts the resection mask (area affected in the brain), indicating the area of the brain that may require surgical intervention.
       -> For this purpose, a U-Net model was trained.
       -> The model and its results can be found in the notebooks/model_training.ipynb


# Demo use case
important: ideally, this should be run using the GPU, using the CPU is also possible but the inference time will be longer.

1) create a new virtual environment using python 3.12 and install the dependencies in requirements.txt
2) Run the main.py file to start the application.
3) click on "load brain MRI" and from demo_data, select one MRI scan 
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
8) To predict the resection mask based on the MRI scan, click "AI generate mask" and the model will make a prediction and display it in the 3D image viewer







