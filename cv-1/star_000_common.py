import os
import glob
from typing import List

__all__ = [
    "img_id"
]

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

