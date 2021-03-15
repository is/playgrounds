import glob
import pathlib
from star_000_common import *
import star_000_common as SC

IN_DIR = 'S0'
OUT_DIR = 'star'


def main():
    # print(SC.star_source_img_ids())
    infns = glob.glob(IN_DIR + "/*")
    infns.sort()
    # pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    for i in range(len(infns)):
        p1 = pathlib.Path(f'{OUT_DIR}/s_{i:02d}.ARW')
        if p1.is_symlink():
            p1.unlink()
        p1.symlink_to("../" + infns[i])
        # print(img_id(p1.name))
    print("{} images".format(len(SC.star_source_img_ids())))

if __name__ == '__main__':
    main()

