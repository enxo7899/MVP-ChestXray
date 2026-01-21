"""
Chest X-Ray Pathology Classification Engine

Uses torchxrayvision DenseNet model with specific preprocessing pipeline.
CRITICAL: XRV models require normalization to [-1024, +1024] range,
NOT standard ImageNet normalization. This represents radiographic density values.
"""

import numpy as np
import torch
import torchvision.transforms as transforms
import torchxrayvision as xrv


# Global model instance (lazy loaded)
_model = None


def _get_model() -> xrv.models.DenseNet:
    """Lazy load and cache the DenseNet model."""
    global _model
    if _model is None:
        _model = xrv.models.DenseNet(weights="densenet121-res224-all")
        _model.eval()
    return _model


def _preprocess_image(image_array: np.ndarray) -> np.ndarray:
    """
    Preprocess input image array to XRV-compatible format.
    
    Args:
        image_array: Input numpy array of shape (H, W), (H, W, 3), or (3, H, W)
        
    Returns:
        Preprocessed array of shape (1, H, W) normalized to [-1024, 1024]
        Note: Returns 3D array (C, H, W) for transforms; batch dim added later
    """
    img = image_array.copy()
    
    # Handle different input shapes -> convert to (1, H, W) grayscale
    if img.ndim == 2:
        # Grayscale (H, W) -> add channel dim only
        img = img[np.newaxis, :, :]
    elif img.ndim == 3:
        if img.shape[2] == 3:
            # RGB (H, W, 3) -> convert to grayscale by mean
            img = img.mean(axis=2)
            img = img[np.newaxis, :, :]
        elif img.shape[0] == 3:
            # RGB (3, H, W) -> convert to grayscale by mean
            img = img.mean(axis=0)
            img = img[np.newaxis, :, :]
        elif img.shape[0] == 1:
            # Already (1, H, W) -> keep as is
            pass
        else:
            raise ValueError(f"Unexpected 3D shape: {image_array.shape}")
    elif img.ndim == 4:
        # (B, C, H, W) -> take first sample and convert to grayscale
        img = img[0]
        if img.shape[0] == 3:
            img = img.mean(axis=0)
            img = img[np.newaxis, :, :]
        elif img.shape[0] != 1:
            raise ValueError(f"Unexpected channel count: {img.shape[0]}")
    else:
        raise ValueError(f"Unsupported array dimensions: {img.ndim}")
    
    # Ensure float type for normalization
    img = img.astype(np.float32)
    
    # CRITICAL: Use XRV-specific normalization
    # This scales from [0, 255] to approximately [-1024, 1024]
    # Representing radiographic density values (like Hounsfield units)
    # DO NOT use ImageNet normalization!
    img = xrv.datasets.normalize(img, 255)
    
    return img


def _build_transforms() -> transforms.Compose:
    """
    Build XRV-specific transformation pipeline.
    
    CRITICAL: Must use xrv.datasets transformations, not standard torchvision.
    """
    return transforms.Compose([
        xrv.datasets.XRayCenterCrop(),
        xrv.datasets.XRayResizer(224),
    ])


def predict_chest(image_array: np.ndarray) -> dict[str, float]:
    """
    Predict pathologies from a chest X-ray image.
    
    Args:
        image_array: Numpy array of chest X-ray image.
                     Supported shapes: (H, W), (H, W, 3), (3, H, W)
                     Expected dtype: uint8 [0-255] or float [0-1] or [0-255]
                     
    Returns:
        Dictionary mapping pathology names to probability scores.
        
    Example:
        >>> img = load_xray("chest.png")  # (1024, 1024) uint8
        >>> results = predict_chest(img)
        >>> print(results["Pneumonia"])
        0.234
    """
    # Get model
    model = _get_model()
    
    # Preprocess image
    img = _preprocess_image(image_array)
    
    # Apply XRV transformations (expects 3D: C, H, W)
    transform = _build_transforms()
    img = transform(img)
    
    # Convert to tensor and add batch dimension
    img_tensor = torch.from_numpy(img).unsqueeze(0)  # (1, 1, 224, 224)
    
    # Run inference
    with torch.no_grad():
        outputs = model(img_tensor)
    
    # Convert to dictionary
    probs = outputs[0].cpu().numpy()
    pathologies = model.pathologies
    
    results = {
        pathology: float(prob)
        for pathology, prob in zip(pathologies, probs)
    }
    
    return results
