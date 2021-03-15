"""
准备灰度图以及图片金字塔.
"""
import rawpy
import cv2
import pathlib
from pathlib import Path

import star_000_common as SC

def imsave(fn:Path, data) -> None:
    fn.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(fn), data)

def convert(img_id:str) -> None:
    cache_dir = Path(SC.CACHE_DIR)
    indir = cache_dir / "origin"

    img = cv2.imread(str(indir / f"{img_id}.png"))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fn = f"{img_id}.png"
    imsave(cache_dir / "gray" / fn, gray)

    h = img.shape[0]
    w = img.shape[1]

    for i in (2, 4, 8):
        i2 = cv2.resize(img, None, fx=1.0/i, fy=1.0/i,
            interpolation=cv2.INTER_LANCZOS4)
        g2 = cv2.resize(gray, None, fx=1.0/i, fy=1.0/i,
            interpolation=cv2.INTER_LANCZOS4)
        print(f"{i2.shape}, {g2.shape}")
        imsave(cache_dir / f"gray__x{i}" / fn, g2)
        imsave(cache_dir / f"x{i}" / fn, i2)



def main():
    img_ids = SC.star_source_img_ids()
    for img_id in img_ids:
        print(img_id)
        convert(img_id)


if __name__ == '__main__':
    main()

