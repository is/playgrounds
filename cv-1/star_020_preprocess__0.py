import rawpy
import cv2
import pathlib

import star_000_common as SC


def main():
    img_ids = SC.star_source_img_ids()
    base_dir = pathlib.Path(SC.CACHE_DIR, "origin")
    base_dir.mkdir(exist_ok=True, parents=True)
    for img_id in img_ids:
        fn = f'star/{img_id}.ARW'
        print(f"process {img_id} ...")
        with rawpy.imread(fn) as raw:
            rgb = raw.postprocess(use_camera_wb=True)
            fout = base_dir / f"{img_id}.png"
            bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            bgr = bgr[12:-12,12:-12,:]
            print(bgr.shape)
            cv2.imwrite(str(fout), bgr)

if __name__ == '__main__':
    main()

