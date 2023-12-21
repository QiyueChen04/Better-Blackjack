# Contour-comparison algorithm for image detection

import cv2 as cv

ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
# [631, 412, 165, 597, 596, 711], thresh 127
# detContoursIndex = [667, 815, 737, 497, 605, 929]

# These numbers were discovered and hard coded from template images
detContoursIndex = [21, 55, 50, 18, 19, 40]

detContours = []

for i in range(6):
    card = cv.imread(f'train/{i}-sm.png')
    
    card = cv.resize(card, None, fx=0.5, fy=0.5, interpolation = cv.INTER_LINEAR)

    gray = cv.cvtColor(card, cv.COLOR_BGR2GRAY);
    ret, thresh = cv.threshold(gray, 140, 255, 0)

    # Noise reduction
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 4))
    thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)


    contours, heirarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


    # This is the discovery process for finding the largest contour, is not necessary in final algorithm


    # height, width, channels = card.shape
    # scale = cv.resize(card, None, fx=0.25, fy=0.25, interpolation= cv.INTER_LINEAR)
    # cv.imwrite(f'train/{i}-sm.png', scale)

    # cv.imshow(f'{i}', thresh);

    # for j in range(len(contours)):
    #     area = cv.contourArea(contours[j])
    #     if (area < 200):
    #         continue
    #     print(j, area)
    #     img = card.copy()
    #     cv.drawContours(img, contours, j, (0, 255, 0), 3)
    #     cv.imshow(f'rank{i} contour{j}', img);

    img = card.copy()
    cv.drawContours(img, contours, detContoursIndex[i], (0, 255, 0), 1)
    cv.imshow(f'rank{i}', img);
    detContours.append(contours[detContoursIndex[i]])


# Reading and determining a single card
test0 = cv.imread('test/test-5.png')
test0 = cv.flip(test0, 1);
height, width, channels = test0.shape
testArea = height * width
gray0 = cv.cvtColor(test0, cv.COLOR_BGR2GRAY);
ret0, thresh0 = cv.threshold(gray0, 140, 255, 0)

kernel = cv.getStructuringElement(cv.MORPH_RECT, (4, 4))
thresh0 = cv.morphologyEx(thresh0, cv.MORPH_OPEN, kernel)

contours0, heirarchy0 = cv.findContours(thresh0, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

cv.imshow("gray", gray0)
cv.imshow("thresh", thresh0)

for i in range(len(contours0)):
    area = cv.contourArea(contours0[i])
    if (area < 100 or area > testArea/2):
        continue
    img = test0.copy()
    cv.drawContours(img, contours0, i, (0, 255, 0), 1)
    cv.imshow(f'test0 contour {i}', img);

    print(i, end=": ")
    for j in range(6):
        ret = cv.matchShapes(detContours[j], contours0[i], 1, 0.0)
        print(round(ret, 2), end=" ")
    print()

cv.waitKey(0);
cv.destroyAllWindows();