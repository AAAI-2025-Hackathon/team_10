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
- Team Members: [Tobias Haar](mailto:tobias.haar@micronova.de), [Vignesh Gogulavasan](mailto:vignesh.gogulavasan@micronova.de), [Vojtěch Breník](mailto:vojtech.brenik@micronova.cz), [Carolin Rickert](mailto:carolin.rickert@micronova.de)
- [x] All team members agree to abide by the [Hackathon Rules](https://aaai.org/conference/aaai/aaai-25/hackathon/)
- [x] This AAAI 2025 hackathon entry was created by the team during the period of the hackathon, February 17 – February 24, 2025
- [x] The entry includes a 2-minute maximum length demo video here: [Link](https://micronovaag-my.sharepoint.com/:v:/g/personal/carolin_rickert_micronova_de/EbOjnd7z1gZNkPgmEGuSwUoBnhlTDtBGebT8_qnwVrEPMA?e=coMH91&nav=eyJwbGF5YmFja09wdGlvbnMiOnt9LCJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJUZWFtcyIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJ2aWRlb2FjdGlvbnMtc2hhcmUiLCJyZWZlcnJhbFBsYXliYWNrU2Vzc2lvbklkIjoiOTQ5YTVlZmMtYTJmZC00MTM0LWE0ZDUtNzRkODNlZDRlMTFlIn19)
- [x] The entry clearly identifies the selected theme in the README and the video.


# Project Description
This project applies machine learning to analyze MRI scans and clinical data from the [IDEAS dataset](https://doi.org/10.18112/openneuro.ds005602.v1.0.0). The application provides an interactive visualization of MRI data, enables epilepsy diagnosis based on key parameters, and predicts resection masks for epileptic patients.


# Repository structure
```
dataset/                   # Dataset files for training and testing
demo_data/                 # Demo data for showcasing the application (id<4000: epileptic, id>4000: healthy)
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
> :warning: important: ideally, this should be run using the GPU, using the CPU is also possible but the inference time will be longer. You can use conda to install some of the dependencies with GPU support, just use the alternative first step [here](#alternative-dependency-installation-step-with-gpu-support).

1) Create a new virtual environment using python 3.12 and install the dependencies in `requirements.txt`.
    ```cmd
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
2) Run the main.py file to start the application.
    ```cmd
    python epilepsydetection/main.py
    ```
3) Click on "load brain MRI" and from demo_data, select one MRI scan
    - e.g. control_4012_mri.nii.gz for a healthy person or
    - e.g. patient_1_mri.nii.gz for a patient with epilepsy
4) You can then scroll through the MRI using the slider or rotate it by dragging the mouse on the image.
5) To predict whether the person has epilepsy or not, click "load patient data" and select the corresponding csv file from the demo_data folder
    - e.g. control_4012_markers.csv for a healthy person or
    - e.g. patient_1_markers.csv for a patient with epilepsy
6) Click on "predict epilepsy" and the model will make a prediction and display it in the UI.
7) To show the resection mask (affected area of the brain) created by physicians, click "load mask" and select the corresponding file from the demo_data folder
    - e.g. mask.nii.gz for a patient with epilepsy
    - for healthy patients this does not exist
8) To predict the resection mask based on the MRI scan, click "AI generate mask" and the model will make a prediction and display it in the 3D image viewer.

## Alternative dependency installation step with GPU support
1. Create a new conda environment with python 3.12, install torch with GPU support and install the dependencies in `requirements.txt`.
```cmd
conda create -n gpu_environment python=3.12
conda activate gpu_environment
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
pip install -r requirements.txt
```
Continue with step 2. [above](#demo-use-case).

# Data downloading

In this project we use the IDEAS (The Imaging Database for Epilepsy And Surgery) obtained from https://openneuro.org/datasets/ds005602/versions/1.0.0.

You can download the dataset by executing the ds005602-1.0.0.sh script from OpenNeuro in git bash or any other tool for executing bash scripts where you can just run the following commands to download the dataset and move it to the `dataset` directory.

```bash
sh ds005602-1.0.0.sh
mv ds005602-1.0.0 dataset/
```

This is only a part of the available dataset, we use some other parts as well, but those have to be obtained using a web browser. Please refer to the following links to download the other parts of the dataset:

1. [freesurfer-orig](https://figshare.com/s/f13391a4161b807ce6b0?file=48485917) - MRI data normalized in dimensions and intensities. Downloads as a ZIP archive, you need to unzip it. You should unzip it into the dataset directory, so that it has this structure:
    - `dataset/freesurfer_orig/freesurfer_orig/`
        - `1_freesurfer_orig.nii.gz`,
        - `2_freesurfer_orig.nii.gz`,
        - ...
1. [masks](https://figshare.com/s/31ab43d1829b12ac13e8?file=46130973) - Binary resection masks in two versions - for the freesurfer normalized scans (`orig` and `brain` sets) and for the raw data (`ds005602-1.0.0` T1 set). Downloads as a ZIP archive, you need to unzip it. You should unzip it into the dataset directory, so that it has this structure:
    - `dataset/masks/masks/`
        - `1/`
            - `1_MaskInOrig.nii.gz`,
            - `1_MaskInRawData.nii.gz`
        - `2/`
            - `2_MaskInOrig.nii.gz`,
            - `2_MaskInRawData.nii.gz`
        - ...




