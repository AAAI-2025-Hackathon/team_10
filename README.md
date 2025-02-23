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
2) Epilepsy Prediction: Based on specific parameters extracted from MRI scans, the model predicts whether a person has epilepsy or is healthy.
3) Resection Mask Prediction: For epileptic patients, the model predicts the resection mask, indicating the area of the brain that may require surgical intervention.


# Demo use case