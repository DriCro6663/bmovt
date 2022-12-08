# https://qiita.com/derodero24/items/f22c22b22451609908ee

import numpy as np
import cv2
from PIL import Image

def pil2cv(image):
    """
    PIL 型 -> OpenCV 型
    
    Parameters
    ----------
    image: 
        PIL 型の画像
    
    Returns
    -------
    new_image: np.array
        OpenCV 型の画像
    """
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def cv2pil(image):
    """
    OpenCV 型 -> PIL 型
    
    Parameters
    ----------
    image: np.array
        OpenCV 型の画像
    
    Returns
    -------
    new_image: np.array
        PIL 型の画像
    """
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image