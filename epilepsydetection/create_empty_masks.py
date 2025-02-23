import nibabel as nib
import numpy as np
from pathlib import Path

DATA_PATH = Path("dataset/freesurfer_orig/freesurfer_orig")
MASK_PATH = Path("dataset/masks/masks")

def create_empty_masks(file_path: Path):
    """Create empty mask for a given MRI file."""
    try:
        img = nib.load(file_path)
        data = img.get_fdata()
        affine = img.affine  # Get the affine transformation matrix
        header = img.header  # Get the header information
        mask = np.zeros_like(data)
        mask_img = nib.Nifti1Image(mask, affine, header)
        
        patient_id = file_path.stem[:4]
        patient_mask_dir = MASK_PATH / patient_id
        patient_mask_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = patient_mask_dir / f"{patient_id}_MaskInOrig.nii.gz"
        nib.save(mask_img, output_path)
        print(f"Created mask for patient {patient_id} in {output_path}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_all_patients():
    """Process all patient files starting with 4000."""
    patient_files = list(DATA_PATH.glob("4[0-9][0-9][0-9]_freesurfer_orig.nii.gz"))

    if not patient_files:
        print("No matching files found")
        return
    
    print(f"Found {len(patient_files)} files to process")
    
    for file_path in patient_files:
        if file_path.stem.startswith('4'):
            create_empty_masks(file_path)

if __name__ == "__main__":
    process_all_patients()