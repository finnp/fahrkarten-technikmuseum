import cv2, numpy as np
import sys
import imutils

# remove borders


MORPH = 2
CANNY = 84
HOUGH = 25

orig = cv2.imread('img/test.jpg')

orig = imutils.resize(orig, height = 2000)


img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
cv2.GaussianBlur(img, (13,13), 0, img) # whoot? 7 is nice


# # this is to recognize white on white
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(MORPH,MORPH))
dilated = cv2.dilate(img, kernel)

edges = cv2.Canny(dilated, 0, CANNY, apertureSize=3)

# finding contours
_, contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_TC89_KCOS)

# look for bigest contour
contours = sorted(contours, key=lambda cont: -cv2.contourArea(cont))

# reshape
# rect = cv2.approxPolyDP(contours[0], 40, True).copy().reshape(-1, 2)

# contours
x, y, w, h = cv2.boundingRect(contours[0])

smaller = orig[y:y+h, x:x+w]


# width = rect[0][0] - rect[1][0]
# height = rect[2][1] - rect[1][1]
#
#
# x = rect[3][0]
# y = rect[3][1]
# print(x, y, width, height)
#
# crop_img = orig[1:1, 100:100] # Crop from x, y, w, h -> 100, 200, 300, 400
# # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
# print(crop_img)

# [[2548   33]
#  [  32   31]
#  [  32 1968]
#  [2547 1968]]
#
# cv2.drawContours(orig, [rect],-1,(0,255,0),2)

cv2.imwrite('output/output.png', smaller)
