import cv2
import bm3d
from bm3d import bm3d_rgb, BM3DProfile
import skimage
from skimage import io, img_as_float, img_as_ubyte
import numpy as np


FN0 = 'color_0.jpg'
img = img_as_float(io.imread(FN0))
print(f'{img.shape} - {img.dtype}')
bm3d = bm3d_rgb(img, sigma_psd=[0.2, 0.2, 0.2])
bm3d = np.minimum(np.maximum(bm3d, 0), 1)
bm3di = img_as_ubyte(bm3d)
io.imsave('s/bm3d_color_0.tiff', bm3di)
