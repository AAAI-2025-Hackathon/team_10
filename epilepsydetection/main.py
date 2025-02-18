import nibabel as nib
import numpy as np
import pyvista as pv
# from app.main import create_app
from scipy.ndimage import zoom
import os

# app = create_app()

SAMPLE_NUMBER = 1

def get_3d_nifti_data(sample_number: int, type: str) -> np.ndarray:
    if type == "mask":
        mask_file_path = rf"C:\Users\haar\Documents\AI_Consulting\Hackathon\team_10\masks\{sample_number}\{sample_number}_MaskInRawData.nii.gz"
        nifti_img = nib.load(mask_file_path)
        return nifti_img.get_fdata() # get the data as a 3D numpy array
    elif type == "raw":
        raw_file_path = rf"C:\Users\haar\Documents\AI_Consulting\Hackathon\team_10\ds005602-1.0.0\sub-{sample_number}\anat\sub-{sample_number}_T1w.nii.gz"
        nifti_img = nib.load(raw_file_path)
        return nifti_img.get_fdata() # get the data as a 3D numpy array

raw_data = get_3d_nifti_data(SAMPLE_NUMBER, "raw")
mask_data = get_3d_nifti_data(SAMPLE_NUMBER, "mask")

print(f"Shape of the raw data: {raw_data.shape}")
print(f"Shape of the mask data: {mask_data.shape}")
# raw_data[:, :, 133:] = 0 # adjust slice to be plotted
nifti_data = raw_data + mask_data*4000
print(f"Shape of the 3D numpy array: {nifti_data.shape}")

grid = pv.ImageData()
grid.dimensions = np.array(nifti_data.shape) + 1
grid.origin = (0, 0, 0)  # The bottom left corner of the data set
grid.spacing = (0.9, 0.9, 0.9)  # Cell sizes along each axis
grid.cell_data["values"] = nifti_data.flatten(order="F") # Assign the data to the cell data

# Create a plot
plotter = pv.Plotter()
plotter.add_volume(grid, cmap="viridis")
plotter.show()

# if __name__ == '__main__':
#     app.run(debug=True)