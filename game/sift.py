# SIFT algorithm for image detection, ultimately unused

import cv2
import numpy

# calculate points of trained images
trainedDes = []
trainedKp = []
trainedImg = []
sift = cv2.SIFT_create()

for i in range(1, 14):
    img = cv2.imread('assets/clearTrained/%s.jpg' %i, 0)
    #img = img[0:1200, 500:1600]
    #img = img[300:1500, 1100:1900]
    kp, des = sift.detectAndCompute(img, None)
    #imgkp = cv2.drawKeypoints(img, kp, None, None, flags = cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    #cv2.imshow('%s' %i, imgkp)
    trainedImg.append(img)
    trainedDes.append(des)
    trainedKp.append(kp)
    #imgKp = cv2.drawKeypoints(img, kp, None, None, flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv2.imshow('%s' %i, imgKp)


for i in range(0, 52):
    print(i)
    img = cv2.imread('assets/hiResPhoto/%s.jpg' %str(i), 0)
    #img = img[65:230, 150:320]
    #img = img[300:1500, 1100:1900]
    img = img[0:1200, 500:1600]
    kp, des = sift.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList = []
    max = 0
    maxInd = -1
    for j in range(13):
        tDes = trainedDes[j]
        matches = bf.knnMatch(tDes, des, k = 2)
        good = []
        cnt = 0
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])
                cnt += 1
        if(cnt > max):
            max = cnt
            maxInd = j
        matchList.append(good)
    if(maxInd == -1):
        print("NONE FOUND")
    else:
        imgRes = cv2.drawMatchesKnn(img, kp, trainedImg[maxInd], trainedKp[maxInd], matchList[maxInd], None, flags = cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow('%s' %i, imgRes)


cv2.waitKey(0)
cv2.destroyAllWindows()
