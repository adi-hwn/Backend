import numpy as np

def distance(a,b):
    return np.sqrt(np.square(a[0]-b[0]) + np.square(a[1]-b[1]))