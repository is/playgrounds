"""
https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/
"""
import json
from pathlib import Path
import argparse

import numpy as np
import cv2


S0 = 'star-cache/x1/s_00.png'
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",
    default=S0, help="path to the image file")
args = vars(ap.parse_args())

from star_common import imsave

S0 = 'star-cache/x1/s_00.png'
OUT_DIR = Path('o/015')

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = cv2.imread(args['image'])
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imsave(OUT_DIR, "001_gray.png", gray)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    imsave(OUT_DIR, "011_blur.png", blur)

    _, mask = cv2.threshold(blur, 190, 255, cv2.THRESH_BINARY)
    imsave(OUT_DIR, "021_mask.png", mask)

    mask = cv2.erode(mask, None, iterations=2)
    imsave(OUT_DIR, "031_erode.png", mask)
    mask = cv2.dilate(mask, None, iterations=4)
    imsave(OUT_DIR, "033_dilate.png", mask)

    #labels = measure.label(mask, background=0)
    #imsave(OUT_DIR, "041_labels.png", labels)
    #print(np.unique(labels))
    contours, _hierarchy = cv2.findContours(mask, 
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    cimg = cv2.drawContours(mask.copy(), contours, 3, (0,255,0), 3)
    imsave(OUT_DIR, "040_contour.png", cimg)

    ds = []
    for contour in contours:
        ci = {}
        m = cv2.moments(contour)
        ci['M'] = m
        ci['area'] = cv2.contourArea(contour)
        ci['cx'] = m['m10'] / m['m00']
        ci['cy'] = m['m01'] / m['m00']
        ci['diameter'] = np.sqrt(4*ci['area']/np.pi)
        ds.append(ci)
    print(json.dumps(ds, indent=True))


if __name__ == '__main__':
    main()