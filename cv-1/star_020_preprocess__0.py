import pathlib
from pathlib import Path
import rawpy
import cv2
import ray

import star_common as SC


@ray.remote
def process(img_id):
    fn = f'star/{img_id}.ARW'
    print(f"process {img_id} ...")
    base_dir = pathlib.Path(SC.CACHE_DIR, "origin")
    with rawpy.imread(fn) as raw:
        rgb = raw.postprocess(use_camera_wb=True)
        #rgb = raw.postprocess(use_auto_wb=True)
        fout = base_dir / f"{img_id}.png"
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        bgr = bgr[12:-12,12:-12,:]
        print(bgr.shape)
        cv2.imwrite(str(fout), bgr)


def main():
    ray.init(address='auto')
    img_ids = SC.star_source_img_ids()
    base_dir = pathlib.Path(SC.CACHE_DIR, "origin")
    base_dir.mkdir(exist_ok=True, parents=True)
    future = [ process.remote(img_id) for img_id in img_ids ]
    ray.get(future)


if __name__ == '__main__':
    main()
