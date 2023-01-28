import numpy as np
import cv2 as cv
from pathlib import Path

S0 = 'star-cache/x2/s_00.png'
S1 = 'star-cache/x2/s_03.png'
OUT_DIR = 'o/010'

def main():
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    img1 = cv.imread(S0, cv.IMREAD_GRAYSCALE)
    img2 = cv.imread(S1, cv.IMREAD_GRAYSCALE)

    orb = cv.ORB_create()
    #orb = cv.SIFT_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key = lambda x:x.distance)
    img3 = cv.drawMatches(img1,kp1,img2,kp2,matches,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv.imwrite(OUT_DIR + "/match.png", img3)

    img4 = cv.drawKeypoints(img1, kp1, img1,
        flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imwrite(OUT_DIR + "/kp1.png", img4)
    print (des1.shape)
    
    
    # bf = cv.BFMatcher()
    # matches = bf.knnMatch(des1, des2, k=2)
    # # Apply ratio test
    # good = []
    # for m,n in matches:
    #     if m.distance < 0.75*n.distance:
    #         good.append([m])
    # img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    


if __name__ == '__main__':
    main()