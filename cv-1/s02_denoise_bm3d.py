import cv2
import bm3d
import skimage
from skimage import io, img_as_float


FN0 = 's/gray.tiff'

img = img_as_float(io.imread(FN0, as_gray=True))
bm3d = bm3d.bm3d(img, sigma_psd=0.2,
    stage_arg=bm3d.BM3DStages.HARD_THRESHOLDING)
bm3di = skimage.img_as_ubyte(bm3d)
io.imsave('s/bm3d.tiff', bm3di)
# cv2.imshow("bm3d", bm3di)
# cv2.waitKey(0)
# cv2.destroyAllWindows()