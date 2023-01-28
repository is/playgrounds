import numpy as np
import cv2

img = cv2.imread('IMG_8649.JPG')
print(img.shape)

cv2.namedWindow('IMG-8649', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
