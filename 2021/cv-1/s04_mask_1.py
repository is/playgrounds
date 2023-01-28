import math
import cv2
import numpy as np

fn = 'star-cache/gray__x4/s_00.png'

def main():
    src = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
    cv2.imwrite("s/03/010__mask_src.png", src)

    th1 = cv2.adaptiveThreshold(
        src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite("s/03/020__gaussian_01.png", th1)

    th2 = cv2.adaptiveThreshold(
        src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 5)
    cv2.imwrite("s/03/021__gaussian_02.png", th2)

    th3 = cv2.GaussianBlur(src, (5, 5), 1)
    th3 = cv2.adaptiveThreshold(
        th3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite("s/03/022__gaussian_03.png", th3)


    th4 = cv2.medianBlur(src, 5)
    th4 = cv2.adaptiveThreshold(
        th4, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite("s/03/022__gaussian_04.png", th4)

if __name__ == '__main__':
    main()