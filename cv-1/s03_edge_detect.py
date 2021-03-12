import cv2
import numpy as np

FI0 = 's/02__source.jpg'
FI1 = 's/bm3d_color_0.tiff'
src = cv2.imread(FI1)
e0 = cv2.Canny(src, 100, 200)
cv2.imwrite('s/02__edge_detect_0.png', e0)
e1 = 255 - e0
cv2.imwrite('s/02__edge_detect_0_1.png', e1)
e2 = cv2.GaussianBlur(e1, (3, 3), 0)
cv2.imwrite('s/02__edge_detect_0_2.png', e2)
