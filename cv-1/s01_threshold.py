import cv2
from matplotlib import pyplot as plt

def main():
    gray = cv2.imread('s/gray_resize_0500.tiff',
        cv2.IMREAD_GRAYSCALE)
    th2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 5)
    cv2.imwrite('s/gray_threshold_gaussion.tiff', th2)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    #ret3,th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret3, th3 = cv2.threshold(blur, 155, 255, cv2.THRESH_BINARY)
    cv2.imwrite('s/gray_threshold_gaussianblur.tiff', blur)
    cv2.imwrite('s/gray_threshold_otsu.tiff', th3)

    print(ret3)

if __name__ == '__main__':
    main()