import rawpy
import cv2
import glob
import os
import sys


FN = "s0/DSC01892.ARW"

def write_png(img, ext):
    fn = f"s1/{ext}.png"
    print(f"write {fn} ...")
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite(fn, img)

def C2(raw, ext, **kwargs):
    r0 = raw.postprocess(**kwargs)
    write_png(r0, ext)

def main():
    try:
        os.makedirs("s1")
    except FileExistsError:
        pass

    print(f'read {FN}')
    with rawpy.imread(FN) as raw:
        r0 = raw.postprocess(use_camera_wb=True)
        for i in [750, 500, 400, 250, 125, 100, 50]:
            r1 = cv2.resize(r0, None, fx=i/1000.0, fy=i/1000.0, 
                interpolation=cv2.INTER_LINEAR)
            write_png(r1, f"scale_{i:03d}")

        C2(raw, "default")
        C2(raw, "use_auto_wb", use_auto_wb=True)
        C2(raw, "use_camera_wb", use_camera_wb=True)
        C2(raw, "use_camera_wb_4color", use_camera_wb=True, four_color_rgb=True)


if __name__ == '__main__':
    main()