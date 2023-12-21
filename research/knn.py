# KNN feature detection algorithm for image detection

import cv2

ranks = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
suits = ["clubs", "diamonds", "hearts", "spades"]

# read all images in gray scale
rankImages = []
suitImages = []

for i in range(13):
    card = f"ranks/{ranks[i]}-0.png"
    img = cv2.imread(card, 0)

    # black and white binary
    ret, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    #scale the image?
    scale = cv2.resize(img, None, fx=3, fy=3, interpolation= cv2.INTER_LINEAR)

    rankImages.append(scale)


orb = cv2.ORB_create()

# compare rank
rankKp = []
rankDes = []

for i in range(13):
    kp, des = orb.detectAndCompute(rankImages[i], None)
    img1 = cv2.drawKeypoints(rankImages[i], kp, None)
    # cv2.imshow(f'{ranks[i]}', img1)
    rankKp.append(kp)
    rankDes.append(des)


# test images
# test1 = cv2.imread("archive/test/test/5600c2f88cf8106a5d53b5ba5f6f0ca1.png", 0)
# test1 = cv2.imread("archive/test/test/98787091-king-hearts-card-suit-icon-vector-playing-cards-symbols-vector.jpg", 0)
test1 = cv2.imread("PNG-cards-1.3/2_of_clubs.png", 0)
scale1 = cv2.resize(test1, None, fx=3, fy=3, interpolation= cv2.INTER_LINEAR)


kp1, des1 = orb.detectAndCompute(scale1, None)



bf = cv2.BFMatcher()
for i in range(13):
    matches = bf.knnMatch(rankDes[i], des1, k=2)
    good = []
    for m, n in matches:
        if (m.distance < 0.75 * n.distance):
            good.append([m])

    cv2.imshow(f'{ranks[i]}', cv2.drawMatchesKnn(test1, kp1, rankImages[i], rankKp[i], good, None, flags=2))

rankCmp = []
suitCmp = []

cv2.waitKey(0)
cv2.destroyAllWindows()
