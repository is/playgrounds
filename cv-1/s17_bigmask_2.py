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
    accu = np.zeros_like(img0, dtype=np.int32)
    for id in IDS:
        img = cv2.imread(str(IN_DIR / f"{id}.png"))
        accu += img
    
    accu = accu / len(IDS)
    accu = np.minimum(accu, 255).astype(np.uint8)

    im_save("0__base.png", accu)
    for i in range(8):
        accu = cv2.medianBlur(accu, 3)
        im_save(f"{i}__blur.png", accu)

    print(np.max(accu))
    print(np.min(accu))
    accu = accu - np.min(accu)
    im_save(f"0__bigmask.png", accu)


if __name__ == '__main__':
    main()
