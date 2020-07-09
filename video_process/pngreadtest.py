import cv2
import skimage
import numpy as np

import PIL.Image as pil

p = "data/0007.png"


im_cv2 = cv2.imread(p,cv2.IMREAD_GRAYSCALE)
im_pil = np.array(pil.open(p)).astype(np.float32)
print('ok')
