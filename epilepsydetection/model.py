import torch
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
import numpy as np
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
MODEL_DIR = CURRENT_DIR / 'models' / 'nnUnet_results' / 'Dataset001_BrainEpilepsy' / 'nnUNetTrainer__nnUNetPlans__3d_fullres'

def generate_mask(input_array):
    """Generate mask for input array using nnUNet model."""
    try:
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
            model_training_output_dir=MODEL_DIR,
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

