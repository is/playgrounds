import cv2 as cv
import bm3d

FN0 = 'star-cache/origin/s_00.png'

gray = cv.imread(FN0, cv.IMREAD_GRAYSCALE)
denoise = cv.GaussianBlur(gray, (5, 5), 0)
denoise_2 = cv.fastNlMeansDenoising(gray, None, 10, 5, 21)
# cv.imshow("denoise", denoise_2)
# cv.waitKey(0)
cv.imwrite("s/blur_2.tiff", denoise)
cv.imwrite("s/nlmeans_2.tiff", denoise_2)