import nibabel as nib
import numpy as np
import pyvista as pv
import pyvistaqt as pvqt
import sys
from epilepsydetection import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QSlider, QFileDialog, QPushButton, QLabel
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QImage
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
        self.setWindowTitle(WINDOW_TITLE)
        self.array_3d = None
        
        # Link upload button to upload_file method
        self.ui.uploadButton.clicked.connect(self.upload_file)
        self.ui.tabWidget.widget(0).layout().addWidget(self.ui.uploadButton)

        self.ui.image_label = QLabel()
        self.ui.tabWidget.widget(0).layout().addWidget(self.ui.image_label)
        self.three_D_plotter = pvqt.QtInteractor(self)
        self.ui.horizontalLayout_1.addWidget(self.three_D_plotter.interactor)

        # Slider setup
        self.slice_slider = QSlider(Qt.Horizontal, self)
        self.slice_slider.setMinimum(0)
        self.slice_slider.setMaximum(0)
        self.slice_slider.setValue(0)
        self.slice_slider.valueChanged.connect(self.update_2d_slice)
        self.ui.tabWidget.widget(0).layout().addWidget(self.slice_slider)

        self.customUiSetup()

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
        QSvgRenderer("epilepsydetection/resources/MN_logo.svg").render(logoPainter)
        self.ui.logoMN.setPixmap(logoPixMap)
        logoPainter.end()


    def load_array(self, array):
        """Load a new 3D array and update slider range."""
        self.array_3d = array
        if array is not None:
            self.slice_slider.setMaximum(array.shape[2] - 1)  # Assuming we slice along last axis
            self.update_2d_slice(0)  # Show initial slice
            self.update_3d_model()

    def update_2d_slice(self, value):
        """Update display with the selected slice."""
        if self.array_3d is not None:
            current_slice = self.array_3d[:, :, value]
            # Update your display here with current_slice
            self.ui.image_label.setPixmap(self.array_to_pixmap(current_slice))
            print(f"Showing slice {value} with shape {current_slice.shape}")

    def update_3d_model(self):
        if self.array_3d is not None:
            model_data = self.array_3d
            self.three_D_plotter.clear()
            self.three_D_plotter.add_volume(model_data, cmap="viridis")

    def array_to_pixmap(self, array_slice):
        """Convert a 2D numpy array to QPixmap."""
        array_slice = np.ascontiguousarray(array_slice)
        normalized = ((array_slice - array_slice.min()) * 255 / 
                     (array_slice.max() - array_slice.min())).astype(np.uint8)
        
        height, width = normalized.shape
        bytes_per_line = width
        image = QImage(normalized.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        
        # Convert to QPixmap and scale to a reasonable size
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        return scaled_pixmap


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


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    main_window = MainWindow()    # Instantiate the main window
    main_window.show()            # Show the main window
    sys.exit(app.exec())          # Execute the application