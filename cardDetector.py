#########################################
# USAGE
# 
# from PIL import Image
# from cardDetector import CardDetector
# 
# cd = CardDetector()
#
# img = Image.open("Your image here.png");
# print(cd.determineRank(img)) # Will give the indice [0, 12] of the card
#########################################


from PIL import Image, ImageEnhance, ImageOps, ImageChops
import numpy as np
from collections import deque




# Module global variables
CROP = (140, 30, 350, 250) # Preliminary Crop to get approximate location of rank
TEMPLATE_SIZE = (150, 240) # Dimension of template arrays/images
vis = np.zeros([220, 210]) # (CROP[3] - CROP[1], CROP[2] - CROP[0])

class CardDetector:

    NUM_CARDS = 13

    # These need to be adjusted based on where the images are
    TEMPLATE_PATHS = [f'contours/{i}.png' for i in range(NUM_CARDS)]
    BLANK_PATH = 'newPhoto/blank.jpg'

    TEMPLATES = [] # Array of Numpy Arrays
    BLANK = None # Grayscale image of empty card

    # Read templates
    def __init__(self):
        if (len(CardDetector.TEMPLATES) == 0):
            for path in CardDetector.TEMPLATE_PATHS:
                img = Image.open(path);
                img_np = np.array(img)
                CardDetector.TEMPLATES.append(img_np)

        if (CardDetector.BLANK == None):
            CardDetector.BLANK = Image.open(CardDetector.BLANK_PATH)
            CardDetector.BLANK = ImageOps.grayscale(CardDetector.BLANK)

    def getBestXORMatch(self, img_np):
        cmp = 1e9
        best = 0

        for j in range(len(CardDetector.TEMPLATES)):
            white = countWhiteXOR(CardDetector.TEMPLATES[j], img_np)
            if (white < cmp):
                cmp = white
                best = j

        return best

    # Accepts a pillow image of the card, returns it's rank
    def determineRank(self, img):
        gray = ImageOps.grayscale(img);
        sub = ImageChops.subtract(CardDetector.BLANK, gray, 1, 0)
        crop = sub.crop(CROP)

        threshold = 6;
        thresh_np = np.array(crop)
        thresh_np = np.where(thresh_np > threshold, 255, 0)

        crop.putdata(thresh_np.flatten())

        arr_np = outlineContours(thresh_np)
        boundingRect = maxContour(arr_np)

        fixed = crop.crop((boundingRect[0], boundingRect[1], boundingRect[2], boundingRect[3]))
        fixed = fixed.transpose(Image.FLIP_TOP_BOTTOM)
        fixed = fixed.transpose(Image.FLIP_LEFT_RIGHT)
        fixed = fixed.resize(TEMPLATE_SIZE)
        fixed_np = np.array(fixed)

        best = self.getBestXORMatch(fixed_np)

        return best



# Takes a black and white image img_np
# Returns an array with all the contour edges as white 
def outlineContours(img_np):
    height = len(img_np)
    width = round(img_np.size / height)

    arr = np.zeros([height, width])

    for i in range(height):
        for j in range(width):
            cur = img_np[i][j]
            edge = False
            if (i > 0 and img_np[i-1][j] != cur): edge = True
            if (j > 0 and img_np[i][j-1] != cur): edge = True
            if (i < height - 1 and img_np[i+1][j] != cur): edge = True
            if (j < width - 1 and img_np[i][j+1] != cur): edge = True
            
            if (edge): arr[i][j] = 255
            else: arr[i][j] = 0
    
    return arr;


# Returns area of a rectangle
def getArea(minX, minY, maxX, maxY):
    return (maxX - minX) * (maxY - minY)


# Assumes cnt_np is black and white
# Depth first search to find bounding box of contour starting at (startX, startY)
def dfs(cnt_np, startY, startX):

    height = len(cnt_np)
    width = round(cnt_np.size / height)

    minX = width + 1
    minY = height + 1
    maxX = -1
    maxY = -1

    dq = deque()
    dq.append((startY, startX))
    while(len(dq) > 0):
        cy, cx = dq.popleft()

        minX = min(minX, cx)
        minY = min(minY, cy)
        maxX = max(maxX, cx)
        maxY = max(maxY, cy)

        for d in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            dy, dx = d
            ny = cy + dy
            nx = cx + dx

            if (nx < 0 or ny < 0 or nx >= width or ny >= height):
                continue
            if (vis[ny][nx] == 1):
                continue
            if (cnt_np[ny][nx] != cnt_np[startY][startX]):
                continue
            
            dq.append((ny, nx))
            vis[ny][nx] = 1

    return (minX, minY, maxX, maxY)


# Assumes cnt_np is black and white
# Depth first search on all contours to get bounding box, returns bounding box of largest contour 
def maxContour(cnt_np):
    height = len(cnt_np)
    width = round(cnt_np.size / height)

    # reset visited array
    for i in range(height):
        for j in range(width):
            vis[i][j] = 0;


    bestArea = 0
    boundingRect = (-1, -1, -1, -1) # sx, ex, sy, ey

    for i in range(height):
        for j in range(width):
            if (vis[i][j] == 1): 
                continue
            
            if (cnt_np[i][j] == 0):
                continue

            vis[i][j] = 1
            minX, minY, maxX, maxY = dfs(cnt_np, i, j)

            # Ignore contours that touch the edge of the photo
            if (minX == 0 or minY == 0 or maxX == width - 1 or maxY == height - 1):
                continue

            area = getArea(minX, minY, maxX, maxY)
            if (area > bestArea):
                bestArea = area
                boundingRect = (minX, minY, maxX, maxY)

    return boundingRect



# Assume images are black and white (0 or 255)
# assume images are the same size
# returns # white pixels and xor'ed image
def countWhiteXOR(img1_np, img2_np):
    height = len(img1_np)
    width = round(img1_np.size / height)
    xor = np.bitwise_xor(img1_np, img2_np)
    white  = np.count_nonzero(xor)
    return white