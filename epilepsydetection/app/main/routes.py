from flask import render_template, jsonify, Blueprint
import nibabel as nib
import pyvista as pv
import numpy as np

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/get_data')
def get_mesh_data():
    nifti_file_path = "C:\\Users\\haar\\Documents\\AI_Consulting\\Hackathon\\team_10\\ds005602-1.0.0\\sub-1\\anat\\sub-1_FLAIR.nii.gz"
    nifti_img = nib.load(nifti_file_path)
    nifti_data = nifti_img.get_fdata()

    # Normalize the data to range [0, 1]
    nifti_data_normalized = (nifti_data - nifti_data.min()) / (nifti_data.max() - nifti_data.min())
    
    # Create a PyVista plot
    grid = pv.ImageData()
    grid.dimensions = nifti_data.shape
    grid.origin = (0, 0, 0)
    grid.spacing = (1, 1, 1)
    
    grid.point_data["values"] = nifti_data_normalized.flatten(order="F")

    # Create more contour levels with a wider range
    threshold_range = np.linspace(0.2, 0.9, 10)  # More levels (10 instead of 5) and wider range
    contours = grid.contour(threshold_range)
    
    # Increase smoothing iterations for better surface quality
    contours = contours.smooth(n_iter=200)
    
    # Get the data in a format suitable for JSON
    vertices = contours.points.tolist()
    faces = contours.faces.reshape(-1, 4)[:, 1:].tolist()

    print(f"Number of vertices: {len(vertices)}")
    print(f"Number of faces: {len(faces)}")

    return jsonify({
        'vertices': vertices,
        'faces': faces,
        'values': contours.point_data["values"].tolist() if "values" in contours.point_data else []
    })