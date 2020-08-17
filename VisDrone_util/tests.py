from tqdm import tqdm
import torch
from time import  time
import numpy as np

a = np.array([2,3,4,5,6])
ones =  - np.ones(4)
b = np.concatenate([a,ones])
print(b)