from pathlib import Path

import cv2
import numpy as np

import star_common as sc

INPUT = "x1"
IN_DIR = Path(sc.CACHE_DIR, INPUT)
OUT_DIR = Path("o/017")
IDS = sc.star_source_img_ids()

def im_save(name, img):
    cv2.imwrite(str(OUT_DIR / name), img)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img0 = cv2.imread(str(IN_DIR / f"{IDS[0]}.png"))
    gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 3)
    
    th = cv2.adaptiveThreshold(blur, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 125, -8)
    th = cv2.GaussianBlur(th, (3, 3), 1)
    im_save("b0.png", th)


if __name__ == '__main__':
    main()
