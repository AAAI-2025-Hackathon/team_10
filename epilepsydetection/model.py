import torch
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
import numpy as np
from pathlib import Path
from huggingface_hub import snapshot_download, hf_hub_download
import joblib

CURRENT_DIR = Path(__file__).parent
MODEL_DIR = CURRENT_DIR / 'models'

def download_checkpoint():
    """Download checkpoint file from Hugging Face if not present."""
    try:
        # Create model directory if it doesn't exist
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        
        checkpoint_path = MODEL_DIR / "nnUNetTrainer__nnUNetPlans__3d_fullres" / "fold_1" / "checkpoint_latest.pth"
        
        # Only download if file doesn't exist
        if not checkpoint_path.exists():
            print("Downloading checkpoint from Hugging Face...")
            snapshot_download(
                repo_id="THaar50/epilepsyresection",
                local_dir=MODEL_DIR,
                ignore_patterns=[".gitattributes", "README.md"]
            )
            print("Checkpoint downloaded successfully!")
        return True
    except Exception as e:
        print(f"Error downloading checkpoint: {e}")
        return False

def generate_mask(input_array):
    """Generate mask for input array using nnUNet model."""
    try:
        if not download_checkpoint():
            raise Exception("Failed to download checkpoint")
        
        if len(input_array.shape) == 3:
            input_array = input_array[np.newaxis]  # Add channel dimension as first dimension

        input_array = input_array.astype(np.float32)
        
        predictor = nnUNetPredictor(
            tile_step_size=0.5,
            use_gaussian=True,
            use_mirroring=True,
            device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
            verbose=False,
            verbose_preprocessing=False,
            allow_tqdm=True
        )

        predictor.initialize_from_trained_model_folder(
            model_training_output_dir=MODEL_DIR / "nnUNetTrainer__nnUNetPlans__3d_fullres",
            use_folds=(1,),
            checkpoint_name='checkpoint_latest.pth'
        )

        properties = {
            'spacing': (1.0, 1.0, 1.0),  # Default spacing if not known
            'original_size_of_raw_data': input_array.shape[1:],  # Size without channel dimension
            'original_spacing': (1.0, 1.0, 1.0),  # Default original spacing
            'resampling_transpose': None,
            'current_spacing': (1.0, 1.0, 1.0)
        }
        
        prediction = predictor.predict_single_npy_array(
            input_array,
            properties,
            None,  # segmentation_previous_stage
            None,  # output_file_truncated
            False  # save_probabilities
        )
        
        return prediction

    except Exception as e:
        print(f"Error in generate_mask: {e}")
        return None


def load_classifier():
    """Load Random Forest classifier and scaler from joblib file."""
    try:
        rf_path = MODEL_DIR / "rf_epilepsy" / "rf_model_final.joblib"
        scaler_path = MODEL_DIR / "rf_epilepsy" / "scaler_final.joblib"
        if not rf_path.exists():
            print("Downloading RF model from Hugging Face...")
            hf_hub_download(
                repo_id="THaar50/epilepsyresection",
                local_dir=MODEL_DIR,
                subfolder="rf_epilepsy",
                filename="rf_model_final.joblib"
            )
            print("RF model downloaded successfully!")

        if not scaler_path.exists():
            print("Downloading scaler from Hugging Face...")
            hf_hub_download(
                repo_id="THaar50/epilepsyresection",
                local_dir=MODEL_DIR,
                subfolder="rf_epilepsy",
                filename="scaler_final.joblib"
            )
            print("Scaler downloaded successfully!")

        classifier = joblib.load(rf_path)
        scaler = joblib.load(scaler_path)
        print("Random Forest classifier loaded successfully!")
        return classifier, scaler

    except Exception as e:
        print(f"Error loading Random Forest classifier: {e}")
        return None


def classify_patient(input_array):
    """Classify patient using RF model."""
    try:
        classifier, scaler = load_classifier()
        if classifier is None:
            raise Exception("Failed to load classifier")

        input_array = scaler.transform(input_array)

        prediction = classifier.predict(input_array)
        probability = classifier.predict_proba(input_array)

        return {
            'prediction': prediction[0],
            'probability': probability[0]
        }

    except Exception as e:
        print(f"Error in classify_patient: {e}")
        return None