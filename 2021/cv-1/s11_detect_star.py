import numpy as np
import cv2 as cv
from pathlib import Path

from star_common import imsave

S0 = 'star-cache/x2/s_00.png'
OUT_DIR = Path('o/011')

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    img = cv.imread(S0)
    gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    sift = cv.SIFT_create()
    kp, desc = sift.detectAndCompute(gray, None)

    oimg = cv.drawKeypoints(gray, kp, img,
        flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    imsave(OUT_DIR, '01_kp.png', oimg)
    print(desc.shape)

if __name__ == '__main__':
    main()