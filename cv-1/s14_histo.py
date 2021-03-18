from pathlib import Path

import numpy as np
import cv2

from star_common import imsave

S0 = 'star-cache/x1/s_00.png'
OUT_DIR = Path('o/014')

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    img = cv2.imread(S0)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)
    res = np.hstack((gray, equ))
    imsave(OUT_DIR, "01_equ.png", res)
    
if __name__ == '__main__':
    main()