import nibabel as nib
import numpy as np
import pandas as pd
from vtk import vtkCommand
import sys
from epilepsydetection import Ui_MainWindow
from model import generate_mask
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QSize, Qt, QThread, Signal
from PySide6.QtGui import QPainter, QPixmap, QImage
from PySide6.QtSvg import QSvgRenderer
import qtawesome as qta
import nibabel as nib
from dict_model import DictionaryModel
from model import classify_patient

SAMPLE_NUMBER = 1
DEFAULT_ICON_SIZE = QSize(35, 35)
TOP_RIGHT_BUTTONS_X_OFFSET = -60
WINDOW_ICON_NAME = "mdi.brain"
WINDOW_TITLE = "MicroNova Epilepsie Detection"
PLANES_NORMALS_DIRECTIONS_NAMES = [["Inferior (bottom)", "Superior (top)"], ["Anterior (front)", "Posterior (back)"], ["Right", "Left"]]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.setWindowIcon(qta.icon(WINDOW_ICON_NAME, color="#164194"))
        self.ui.setupUi(self)  # Set up the UI from the generated file
        self.setWindowTitle(WINDOW_TITLE)
        self.array_3d = None
        self.mask_3d = None
        self.patient_data = None
        self.volumes = DictionaryModel()
        self.PLANES = [1,2,0]

        self.customUiSetup()
        self.slicing_axis = self.PLANES[self.ui.planeComboBox.currentIndex()]
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

        # Link buttons to methods
        self.ui.uploadButton.clicked.connect(self.upload_file)
        self.ui.uploadMaskButton.clicked.connect(self.upload_mask)
        self.ui.inferMaskButton.clicked.connect(self.generate_mask)
        self.ui.loadPatientDataButton.clicked.connect(self.load_patient_data)
        self.ui.classifyPatientButton.clicked.connect(self.extract_features)

        # Slider setup
        self.ui.slice_slider.setMinimum(0)
        self.ui.slice_slider.setMaximum(255)
        self.ui.slice_slider.setValue(128)
        self.ui.slice_slider.setEnabled(False)
        self.ui.slice_slider.valueChanged.connect(self.update_2d_slice)
        self.ui.slice_slider.valueChanged.connect(self.update_3d_slice)

        # Set icons for buttons
        setButtonsIcon("uploadButton", "mdi.brain", {"color": "#164194"})
        setButtonsIcon("uploadMaskButton", "mdi.selection-ellipse", {"color": "#164194"})
        setButtonsIcon("inferMaskButton", "mdi.head-cog", {"color": "#164194"})
        setButtonsIcon("loadPatientDataButton", "mdi.file-document-outline", {"color": "#164194"})
        setButtonsIcon("classifyPatientButton", "fa.caret-square-o-right", {"color": "#164194"})

        self.ui.volumeListView.setModel(self.volumes)
        self.ui.volumeListView.setStyleSheet("QListView::indicator { width: 20px; height: 20px; }")
        self.volumes.dataChanged.connect(self.on_volume_check)

        # Link comboBoxes signals to slots
        self.ui.planeComboBox.currentIndexChanged.connect(self.planeChanged)
        self.ui.directionComboBox.currentIndexChanged.connect(self.planeNormalDirectionChanged)


    def update_combobox(self, combobox, new_items):
        combobox.clear()
        combobox.addItems(new_items)


    def planeChanged(self):
        index = self.ui.planeComboBox.currentIndex()
        self.slicing_axis = self.PLANES[index]
        self.update_combobox(self.ui.directionComboBox, PLANES_NORMALS_DIRECTIONS_NAMES[index])


    def planeNormalDirectionChanged(self):
        normal = [0,0,0]
        normal[self.slicing_axis] = self.ui.directionComboBox.currentIndex()*2-1
        self.slicing_plane.SetNormal(normal)
        self.slicing_plane.InvokeEvent(vtkCommand.EndInteractionEvent)
        current_slice = self.ui.slice_slider.value()
        self.update_2d_slice(current_slice)
        self.update_3d_slice(current_slice)


    def load_array(self, array):
        """Load a new 3D array and update slider range."""
        self.array_3d = array
        self.mask_3d = None
        self.volumes.resetInternalData()
        if array is not None:
            self.ui.slice_slider.setMaximum(array.shape[2] - 1)  # Assuming we slice along last axis
            self.ui.slice_slider.setValue(int(array.shape[2]/2))
            self.ui.slice_slider.setEnabled(True)
            self.update_3d_model()
            self.planeChanged()
            self.planeNormalDirectionChanged()


    def load_mask(self, array: np.ndarray):
        self.mask_3d = array
        if array is None or self.array_3d is None or not self.array_3d.shape == array.shape:
            return
        self.update_3d_model()
        self.planeChanged()
        self.planeNormalDirectionChanged()

    def update_2d_slice(self, value):
        """Update display with the selected slice."""
        if self.array_3d is not None:
            if self.slicing_axis == 0:
                current_slice = self.array_3d[value, :, :]
                current_mask_slice = self.mask_3d[value, :, :] if self.mask_3d is not None else None
            elif self.slicing_axis == 1:
                current_slice = self.array_3d[:, value, :]
                current_mask_slice = self.mask_3d[:, value, :] if self.mask_3d is not None else None
            else:
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
            opaque_scan = self.ui.three_D_plotter.add_volume(model_data, cmap="gray", opacity=np.logspace(0,1.8,256)-1, show_scalar_bar=False) # opaque whole model
            slicing_scan = self.ui.three_D_plotter.add_volume(model_data, cmap="viridis", show_scalar_bar=False) # colored model with slicing
            self.slicing_plane = self.ui.three_D_plotter.add_volume_clip_plane(slicing_scan, normal = "-z", normal_rotation=False, outline_opacity=0, value=0)
            self.slicing_plane.SetEnabled(0)
            self.volumes.set_value("Opaque scan (whole)", opaque_scan)
            self.volumes.set_value("Sliced scan", slicing_scan)
        if self.mask_3d is not None:
            opaque_mask_volume = self.ui.three_D_plotter.add_volume(self.mask_3d * self.array_3d, cmap = "Wistia", opacity=np.logspace(0,1.8,256)-1, show_scalar_bar=False) # opaque whole mask
            mask_volume = self.ui.three_D_plotter.add_volume(self.mask_3d * self.array_3d, cmap = "cool", opacity=np.linspace(0,45,256), show_scalar_bar=False)
            mask_volume.mapper.SetClippingPlanes(slicing_scan.mapper.GetClippingPlanes())
            self.volumes.set_value("Opaque mask (whole)", opaque_mask_volume)
            self.volumes.set_value("Sliced mask", mask_volume)


    def on_volume_check(self, top_left, bottom_right, roles):
        if Qt.CheckStateRole in roles:
            index = top_left  # Assuming single item selection
            if self.volumes.data(index, Qt.CheckStateRole) == Qt.Checked:
                volume = self.volumes.get_value(self.volumes.data(index, Qt.DisplayRole))
                self.restore_volume_order()
            else:
                volume = self.volumes.get_value(self.volumes.data(index, Qt.DisplayRole))
                self.ui.three_D_plotter.remove_actor(volume)


    def restore_volume_order(self):
        index = 0
        checked = self.volumes.data(self.volumes.index(index), Qt.CheckStateRole)
        while checked is not None:
            if checked == Qt.Checked:
                volume = self.volumes.get_value(self.volumes.data(self.volumes.index(index), Qt.DisplayRole))
                self.ui.three_D_plotter.remove_actor(volume)
                self.ui.three_D_plotter.add_actor(volume)
            index += 1
            checked = self.volumes.data(self.volumes.index(index), Qt.CheckStateRole)


    def update_3d_slice(self, value):
        plane_origin = list(self.slicing_plane.GetOrigin())
        plane_origin[self.slicing_axis] = value
        self.slicing_plane.SetOrigin(plane_origin)
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

    
    def generate_mask(self):
        if self.array_3d is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Mask generation failed")
            msg.setInformativeText("No MRI data is currently loaded. Please load MRI data first.")
            msg.setWindowTitle("No MRI data loaded")
            msg.setWindowIcon(qta.icon(WINDOW_ICON_NAME, color="#164194"))
            msg.exec()
            return

        # Create and start the worker thread
        self.mask_thread = MaskGeneratorThread(self.array_3d)
        self.mask_thread.finished.connect(self.handle_mask_generation_complete)
        self.mask_thread.error.connect(self.handle_mask_generation_error)
        self.mask_thread.start()

    def handle_mask_generation_complete(self, mask):
        if mask is not None:
            self.load_mask(mask)

    def handle_mask_generation_error(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Mask generation failed")
        msg.setInformativeText(str(error))
        msg.setWindowTitle("Error")
        msg.exec()


    def load_patient_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Patient Data File",
            "",
            "CSV Files (*.csv);;All Files (*)"  # Adjust file types as needed
        )
        
        if file_path:
            try:
                self.patient_data = pd.read_csv(file_path, sep=",")
                print(f"Patient data loaded:\n{self.patient_data}")
            except Exception as e:
                print(f"Error loading file: {e}")


    def extract_features(self):
        if self.patient_data is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Classification failed")
            msg.setInformativeText("No patient data is currently loaded. Please load patient data first.")
            msg.setWindowTitle("No patient data loaded")
            msg.setWindowIcon(qta.icon(WINDOW_ICON_NAME, color="#164194"))
            msg.exec()
            return
        
        print("Extracting features...")
        result = classify_patient(self.patient_data)
        probability = result['probability'][0]*100 if result['probability'][0] > result['probability'][1] else result['probability'][1]*100
        self.update_prediction_label(result['prediction'], probability)            

    
    def update_prediction_label(self, prediction, probability):
        self.ui.patientPredictionLabel.setText(f"Diagnosis: {prediction} ({probability}%)")


class MaskGeneratorThread(QThread):
    finished = Signal(object)  # Signal to emit the result
    error = Signal(str)        # Signal to emit errors

    def __init__(self, array_3d):
        super().__init__()
        self.array_3d = array_3d

    def run(self):
        try:
            mask = generate_mask(self.array_3d)
            self.finished.emit(mask)
        except Exception as e:
            self.error.emit(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application
    main_window = MainWindow()    # Instantiate the main window
    main_window.show()            # Show the main window
    sys.exit(app.exec())          # Execute the application