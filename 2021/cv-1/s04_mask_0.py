import math
import cv2
import numpy as np

fn = 'star-cache/gray__x4/s_00.png'

def main():
    src = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
    gray = src
    
    gaussian = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imwrite("o/002/mask_blur_gaussian.png", gaussian)
    print(f"gaussian mean:{np.mean(gaussian)}, std:{np.std(gaussian)}")

    bilateral = cv2.bilateralFilter(src, 7, 42, 70)
    cv2.imwrite("o/002/mask_bulr_bilateral.png", bilateral)
    print(f"bilateral mean:{np.mean(bilateral)}, std:{np.std(bilateral)}")

    median = cv2.medianBlur(src,5)
    cv2.imwrite("o/002/mask_blur_median.png", median)
    print(f"median mean:{np.mean(median)}, std:{np.std(median)}")
    gray = gaussian

    mean = np.mean(gray)
    std = np.std(gray)
    print(f"mean:{mean}, std:{std}")

    ret0, mask0 = cv2.threshold(gray, mean + int(std * 2.15), 255, cv2.THRESH_BINARY)
    ret1, mask1 = cv2.threshold(gray, mean - int(std * 2), 255, cv2.THRESH_BINARY_INV)
    mask2 = mask0 + mask1
    mask2 = cv2.medianBlur(mask2, 3)

    cv2.imwrite("o/002/mask_src.png", src)
    cv2.imwrite("o/002/mask_0.png", cv2.GaussianBlur(255 - mask0, (5, 5), 0))
    cv2.imwrite("o/002/mask_1.png", mask1)
    cv2.imwrite("o/002/mask_2.png", mask2)

if __name__ == '__main__':
    main()