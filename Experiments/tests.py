
import matplotlib.pyplot as plt

import torch
import cv2
from PIL import Image

def pil_loader(path):
    # open path as file to avoid ResourceWarning
    # (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('RGB')


img = torch.ones([96,128])
img = img.numpy()
cv2.imwrite('img.png',img)

img2= cv2.imread('img.png')
img2 = cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)

print('ok')