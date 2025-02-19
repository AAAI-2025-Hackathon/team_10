import nibabel as nib
import numpy as np
import pyvista as pv
import pyvistaqt as pvqt
import sys
from epilepsydetection import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QSlider, QFileDialog, QPushButton
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
import qtawesome as qta
import nibabel as nib

SAMPLE_NUMBER = 1
DEFAULT_ICON_SIZE = QSize(35, 35)
TOP_RIGHT_BUTTONS_X_OFFSET = -60
WINDOW_ICON_NAME = "mdi.brain"
WINDOW_TITLE = "MicroNova Epilepsie Detection"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.uploadButton = QPushButton("Upload File")
        self.setWindowIcon(qta.icon(WINDOW_ICON_NAME, color="#164194"))
        self.ui.setupUi(self)  # Set up the UI from the generated file
        self.customUiSetup()
        self.setWindowTitle(WINDOW_TITLE)
        
        # Initialize array attribute (replace with your actual array)
        self.array_3d = None
        
        # Add upload button
        self.ui.uploadButton.clicked.connect(self.upload_file)
        
        # Add slider setup
        self.slice_slider = QSlider(Qt.Horizontal, self)
        self.slice_slider.setMinimum(0)
        self.slice_slider.setMaximum(0)  # Will be updated when array is loaded
        self.slice_slider.setValue(0)
        self.slice_slider.valueChanged.connect(self.update_slice)
        
        # Add slider to the main window
        self.ui.tabWidget.widget(0).layout().addWidget(self.slice_slider)
        self.ui.tabWidget.widget(0).layout().addWidget(self.ui.uploadButton)

    def resizeEvent(self, event):
        self.resizeTabWidget()
        return super().resizeEvent(event)
    

    def resizeTabWidget(self):
        self.ui.tabWidget.resize(self.width(), self.height())
    

    def customUiSetup(self):
        def setButtonsIcon(buttonName, iconName, iconKwargs, **kwargs):
            button = self.ui.__getattribute__(buttonName)
            icon = qta.icon(iconName, **iconKwargs)
            button.setIcon(icon)

            iconSize = kwargs.get("iconSize", DEFAULT_ICON_SIZE)
            button.setIconSize(iconSize)

            styleSheet = kwargs.get("styleSheet", "")
            button.setStyleSheet(styleSheet)

        self.resizeTabWidget()

        logoPixMap = QPixmap(QSize(162, 44))
        logoPixMap.fill(Qt.transparent)
        logoPainter = QPainter(logoPixMap)
        QSvgRenderer("resources/MN_logo.svg").render(logoPainter)
        self.ui.logoMN.setPixmap(logoPixMap)
        logoPainter.end()
        self.get_plotter(SAMPLE_NUMBER)

    def load_array(self, array):
        """Load a new 3D array and update slider range."""
        self.array_3d = array
        if array is not None:
            self.slice_slider.setMaximum(array.shape[2] - 1)  # Assuming we slice along last axis
            self.update_slice(0)  # Show initial slice

    def update_slice(self, value):
        """Update display with the selected slice."""
        if self.array_3d is not None:
            current_slice = self.array_3d[:, :, value]
            # Update your display here with current_slice
            # Example: self.ui.image_label.setPixmap(array_to_pixmap(current_slice))
            print(f"Showing slice {value} with shape {current_slice.shape}")

    def upload_file(self):
        """Open file dialog and load the selected file as a 3D array."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Image Files (*.nii *.nii.gz *.dcm);;All Files (*)"  # Adjust file types as needed
        )
        
        if file_path:
            try:
                nifti_img = nib.load(file_path).get_fdata()
                print(f"Selected file: {file_path}")
                self.load_array(nifti_img)
            except Exception as e:
                print(f"Error loading file: {e}")

    def get_plotter(self, sample_number: int):
        brain_data = get_3d_nifti_data(sample_number, "raw")
        mask_data = get_3d_nifti_data(sample_number, "mask")

        brain_data[:, :, 133:] = 0 # adjust slice to be plotted
        nifti_data = brain_data + mask_data*200
        print(f"Shape of the 3D numpy array: {nifti_data.shape}")

        grid = pv.ImageData()
        grid.dimensions = np.array(nifti_data.shape) + 1
        grid.origin = (0, 0, 0)  # The bottom left corner of the data set
        grid.spacing = (0.9, 0.9, 0.9)  # Cell sizes along each axis
        grid.cell_data["values"] = nifti_data.flatten(order="F") # Assign the data to the cell data

        # Create a plot
        self.three_D_plotter = pvqt.QtInteractor(self)
        self.ui.horizontalLayout_1.addWidget(self.three_D_plotter.interactor)
        self.three_D_plotter.add_volume(grid, cmap="viridis")
        self.three_D_plotter.show()

sets_templates = {
    "ds005602": "../dataset/ds005602-1.0.0/sub-{0}/anat/sub-{0}_T1w.nii.gz",
    "flair": "../dataset/ds005602-1.0.0/sub-{0}/anat/sub-{0}_FLAIR.nii.gz",
    "masks_orig": "../dataset/masks/{0}/{0}_MaskInOrig.nii.gz",
    "masks_raw": "../dataset/masks/{0}/{0}_MaskInRawData.nii.gz",
    "orig": "../dataset/freesurfer_orig/{0}_freesurfer_orig.nii.gz"
}
def get_image_path(subject_id: int, set_name = "ds005602"):
    return sets_templates[set_name].format(subject_id)

def get_3d_nifti_data(sample_number: int, type: str) -> np.ndarray:
    if type == "mask":
        mask_file_path = rf"masks\{sample_number}\{sample_number}_MaskInOrig.nii.gz"
        mask_file_path = get_image_path(sample_number, "masks_orig")
        nifti_img = nib.load(mask_file_path)
        return nifti_img.get_fdata() # get the data as a 3D numpy array
    elif type == "raw":
        raw_file_path = rf"freesurfer_orig\{sample_number}_freesurfer_orig.nii.gz"
        raw_file_path = get_image_path(sample_number, "orig")
        nifti_img = nib.load(raw_file_path)
        return nifti_img.get_fdata() # get the data as a 3D numpy array

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    main_window = MainWindow()    # Instantiate the main window
    main_window.show()            # Show the main window
    sys.exit(app.exec())          # Execute the application