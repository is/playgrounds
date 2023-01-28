"""

"""
import json
from pathlib import Path
import argparse

import numpy as np
import cv2
from star_common import imsave

S0 = 'star-cache/x1/s_00.png'
OUT_DIR = Path('o/016')

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",
    default=S0, help="path to the image file")
args = vars(ap.parse_args())


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = cv2.imread(args['image'])
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imsave(OUT_DIR, "000_gray.png", gray)

    # blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # imsave(OUT_DIR, "001_blur.png", blur)
    blur = gray
    for i in range(1, 16):
        blur = cv2.medianBlur(blur, 9)
        imsave(OUT_DIR, f"001_{i:02d}_blur.png", blur)
        for C in range(2, 20, 2):
            img = cv2.adaptiveThreshold(blur, 255,
                cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, C)
            imsave(OUT_DIR, f"002_{i:02d}_{C:02d}.png", img)
            print(f"002_{i:02d}_{C:02d}.png")

if __name__ == '__main__':
    main()