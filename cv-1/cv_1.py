import cv2


FI = 'use_camera_wb_4color.png'

def main():
    img = cv2.imread(FI)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(gray.shape)
    cv2.imwrite('gray.png', gray)
    th3 = cv2.adaptiveThreshold(gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    print(th3.shape)
    cv2.imwrite('gaussian.png', th3)

if __name__ == '__main__':
    main()