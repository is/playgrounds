from pathlib import Path

import numpy as np
import cv2

from star_common import imsave

S0 = 'star-cache/x1/s_00.png'
# S0 = 'blob_detection.jpeg'
OUT_DIR = Path('o/013')

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    img = cv2.imread(S0)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(
        gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
    imsave(OUT_DIR, "01_contour_0.png", img)
    print(len(contours))
    print(contours[0].shape)
    print(contours)
    M = cv2.moments(contours[0])
    print(M)
    cnt = contours[0]
    print(cv2.contourArea(cnt))


if __name__ == '__main__':
    main()