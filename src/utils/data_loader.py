from os import PathLike
import cv2
import numpy as np
from typing import Union


def load_image(path: PathLike, contrast: float = 1.0, resolution: float = 1.0) -> Union[cv2.Mat, None]:
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    img = np.clip(img * contrast, 0, 255).astype(np.uint8)

    if resolution != 1.0:
        new_size = (int(img.shape[1] * resolution), int(img.shape[0] * resolution))
        img = cv2.resize(img, new_size)

    return img
