import math
import cv2
import numpy as np

fn = 'star-cache/gray__x4/s_00.png'

def main():
    gray = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
    gray0 = gray
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    mean = np.mean(gray)
    std = np.std(gray)
    print(f"mean:{mean}, std:{std}")
    gray2 = np.abs(gray - int(mean))
    ret0, mask0 = cv2.threshold(gray, mean + int(std * 1.5), 255, cv2.THRESH_BINARY)
    ret1, mask1 = cv2.threshold(gray, mean - int(std * 2), 255, cv2.THRESH_BINARY_INV)
    mask2 = mask0 + mask1
    cv2.imwrite("s/02__mask_src.png", gray0)
    cv2.imwrite("s/02__mask_blur.png", gray)
    cv2.imwrite("s/02__mask_0.png", mask0)
    cv2.imwrite("s/02__mask_1.png", mask1)
    cv2.imwrite("s/02__mask_2.png", mask2)


if __name__ == '__main__':
    main()