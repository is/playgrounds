import os
import glob
from pathlib import Path
from typing import List, Any, NoReturn

import cv2


__all__ = [
    "img_id",
    "imsave",
    "star_source_img_ids",
    "mkdir"]

RAW_DIR = 'S0'
SOURCE_DIR = 'star'
CACHE_DIR = 'star-cache'
REVISION = '0.0.1'

def img_id(path:str) -> str:
    return os.path.basename(path).partition('.')[0]


def star_source_img_ids() -> List[str]:
    imgs = glob.glob('star/*.ARW')
    imgs.sort()
    return [ img_id(x) for x in imgs]


def imsave(base:Path, name:str, img:Any, **kwargs) -> None:
    cv2.imwrite(str(base / name), img, **kwargs)

def mkdir(base:Path) -> None:
    base.mkdir(parents=True, exist_ok=True)