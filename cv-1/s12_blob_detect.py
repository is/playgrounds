import numpy as np
import cv2 as cv
from pathlib import Path

S0 = 'star-cache/x2/s_00.png'

def main():
    Path('o/008').mkdir(parents=True, exist_ok=True)

    img = cv.imread(S0)
    gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    sift = cv.SIFT_create()
    kp, desc = sift.detectAndCompute(gray, None)

    oimg = cv.drawKeypoints(gray, kp, img,
        flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imwrite('o/008/kp.png', oimg)
    print(desc.shape)

if __name__ == '__main__':
    main()