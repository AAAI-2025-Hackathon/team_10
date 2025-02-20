import nibabel as nib
import numpy as np
from pathlib import Path

def create_empty_masks(file_path: Path):
    data = nib.load(file_path).get_fdata()
    affine = nib.load(file_path).affine
    mask = np.zeros_like(data)
    nifti_image = nib.Nifti1Image(mask, affine)
    nib.save(nifti_image, f"{file_path.stem[:4]}_MaskInOrig.nii.gz")

if __name__ == "__main__":
    create_empty_masks(Path(r"C:\Users\haar\Documents\AI_Consulting\Hackathon\team_10\freesurfer_orig\4001_freesurfer_orig.nii.gz"))