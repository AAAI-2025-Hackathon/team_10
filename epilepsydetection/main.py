import nibabel as nib
import numpy as np
import pyvista as pv
from vtk import vtkCommand
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
        self.setWindowIcon(qta.icon(WINDOW_ICON_NAME, color="#164194"))
        self.ui.setupUi(self)  # Set up the UI from the generated file
        self.setWindowTitle(WINDOW_TITLE)
        self.array_3d = None

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

        # Link upload button to upload_file method
        self.ui.uploadButton.clicked.connect(self.upload_file)

        # Link mask upload button to upload_file method
        self.ui.uploadMaskButton.clicked.connect(self.upload_mask)

        # Slider setup
        self.ui.slice_slider.setMinimum(0)
        self.ui.slice_slider.setMaximum(0)
        self.ui.slice_slider.setValue(0)
        self.ui.slice_slider.valueChanged.connect(self.update_2d_slice)
        self.ui.slice_slider.valueChanged.connect(self.update_3d_slice)

        # Set icons for buttons
        setButtonsIcon("uploadButton", "mdi.brain", {"color": "#164194"})
        setButtonsIcon("uploadMaskButton", "mdi.selection-ellipse", {"color": "#164194"})
        setButtonsIcon("inferMaskButton", "mdi.head-cog", {"color": "#164194"})


    def layer_changed(self, caller, ev):
        self.ui.slice_slider.setValue(int(caller.GetOrigin()[2]))


    def load_array(self, array):
        """Load a new 3D array and update slider range."""
        self.array_3d = array
        self.mask_3d = None
        if array is not None:
            self.ui.slice_slider.setMaximum(array.shape[2] - 1)  # Assuming we slice along last axis
            self.update_2d_slice(0)  # Show initial slice
            self.update_3d_model()
            self.update_3d_slice(0)


    def load_mask(self, array: np.ndarray):
        self.mask_3d = array
        if array is None or self.array_3d is None or not self.array_3d.shape == array.shape:
            return
        self.update_2d_slice(self.ui.slice_slider.value())
        self.update_3d_model()
        self.update_3d_slice(self.ui.slice_slider.value())

    def update_2d_slice(self, value):
        """Update display with the selected slice."""
        if self.array_3d is not None:
            current_slice = self.array_3d[:, :, value]
            current_mask_slice = self.mask_3d[:, :, value] if self.mask_3d is not None else None
            # Update your display here with current_slice
            self.ui.image_label.setPixmap(self.array_to_pixmap(current_slice, current_mask_slice))
            print(f"Showing slice {value} with shape {current_slice.shape}")

    def update_3d_model(self):
        self.ui.three_D_plotter.clear_plane_widgets()
        if self.array_3d is not None:
            model_data = self.array_3d
            self.ui.three_D_plotter.clear()
            self.ui.three_D_plotter.add_volume(model_data, cmap="gray", opacity=np.linspace(0,30,256)) # opaque whole model
            volume = self.ui.three_D_plotter.add_volume(model_data, cmap="viridis") # colored model with slicing
            self.slicing_plane = self.ui.three_D_plotter.add_volume_clip_plane(volume, normal = "-z", normal_rotation=False, outline_opacity=0, value=0)
            self.slicing_plane.SetEnabled(0)
        if self.mask_3d is not None:
            self.ui.three_D_plotter.add_volume(self.mask_3d * self.array_3d, cmap = "cool", opacity=np.linspace(0,30,256), show_scalar_bar = False) # opaque whole mask
            mask_volume = self.ui.three_D_plotter.add_volume(self.mask_3d * self.array_3d, cmap = "cool", opacity=np.linspace(0,60,256), show_scalar_bar = False)
            mask_volume.mapper.SetClippingPlanes(volume.mapper.GetClippingPlanes())


    def update_3d_slice(self, value):
        plane_origin = list(self.slicing_plane.GetOrigin())
        plane_origin[2] = value
        # print(plane_origin)
        self.ui.three_D_plotter.plane_widgets[0].SetOrigin(plane_origin)
        self.slicing_plane.InvokeEvent(vtkCommand.EndInteractionEvent)


    def overlay_mask(self, grayscale_image, binary_mask):
        rgb_image = np.stack((grayscale_image,) * 3, axis=-1)

        colored_mask = np.zeros_like(rgb_image)
        colored_mask[binary_mask == 1] = [255, 0, 0]  # Red color for mask

        # Blend the images
        alpha = 0.3  # Adjust this value to change the overlay intensity
        blended_image = (1 - alpha) * rgb_image + alpha * colored_mask

        # Ensure the values are within 0-255 range and convert to uint8
        blended_image = np.clip(blended_image, 0, 255).astype(np.uint8)

        return blended_image

    def array_to_pixmap(self, array_slice, mask_slice = None):
        """Convert a 2D numpy array to QPixmap."""
        array_slice = np.ascontiguousarray(array_slice)
        normalized = ((array_slice - array_slice.min()) * 255 / 
                     (array_slice.max() - array_slice.min())).astype(np.uint8)
        
        height, width = normalized.shape
        if mask_slice is not None:
            mask_slice = np.ascontiguousarray(mask_slice)
            bytes_per_line = width * 3
            normalized_with_mask = self.overlay_mask(normalized, mask_slice)
            image = QImage(normalized_with_mask.data, width, height, bytes_per_line, QImage.Format_RGB888)
        else:
            bytes_per_line = width
            image = QImage(normalized.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        
        # Convert to QPixmap and scale to a reasonable size
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(512, 512, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        return scaled_pixmap


    def upload_file(self, model_type = "mri"): # gets passed False when used as a slot unfortunately, leaving this for now
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
                if model_type=="mask":
                    self.load_mask(nifti_img)
                else:
                    self.load_array(nifti_img)
            except Exception as e:
                print(f"Error loading file: {e}")


    def upload_mask(self):
        self.upload_file(model_type="mask")


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    main_window = MainWindow()    # Instantiate the main window
    main_window.show()            # Show the main window
    sys.exit(app.exec())          # Execute the application