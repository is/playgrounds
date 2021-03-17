import numpy as np
import cv2 as cv
from pathlib import Path

S0 = 'star-cache/x2/s_00.png'
OUT_DIR = 'o/009'

def main():
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    img = cv.imread(S0)
    gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    surf = cv.xfeatures2d.SURF_create(400)
    surf.setExtended(True)
    kp, desc = surf.detectAndCompute(gray, None)

    oimg = cv.drawKeypoints(gray, kp, img,
        flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imwrite(OUT_DIR + '/kp.png', oimg)
    print(desc.shape)
    print(desc)

if __name__ == '__main__':
    main()