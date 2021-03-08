import os
import rawpy
import cv2
import pathlib

FIN = 'S0/DSC01912.ARW'

def main():
    pathlib.Path('s').mkdir(parents=True, exist_ok=True)
    raw = rawpy.imread(FIN)
    rgb = raw.postprocess(use_camera_wb=True)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite('s/default.tiff', bgr)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('s/gray.tiff', gray)

    for i in [750, 500, 300, 250, 125, 50]:
        fn = f's/gray_resize_{i:04d}.tiff'
        img = cv2.resize(gray, None,
            fx=i/1000.0, fy=i/1000.0,
            interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(fn, img)


if __name__ == '__main__':
    main()
