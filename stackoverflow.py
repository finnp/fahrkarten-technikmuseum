import cv2, numpy as np
import sys
import imutils

def get_new(old):
    new = np.ones(old.shape, np.uint8)
    cv2.bitwise_not(new,new)
    return new

orig = cv2.imread('example.jpg')

orig = imutils.resize(orig, height = 2000)

# these constants are carefully picked
MORPH = 2
CANNY = 84
HOUGH = 25


img = orig
# img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
cv2.GaussianBlur(img, (13,13), 0, img) # whoot? 7 is nice


# # this is to recognize white on white
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(MORPH,MORPH))
dilated = cv2.dilate(img, kernel)

edges = cv2.Canny(dilated, 0, CANNY, apertureSize=3)

# finding contours
_, contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_TC89_KCOS)
# contours = filter(lambda cont: cv2.arcLength(cont, False) > 100, contours)
contours = filter(lambda cont: cv2.contourArea(cont) > 400000, contours)

# simplify contours down to polygons
rects = []
for cont in contours:
    rect = cv2.approxPolyDP(cont, 40, True).copy().reshape(-1, 2)
    rects.append(rect)

# that's basically it
cv2.drawContours(orig, rects,-1,(0,255,0),-1)

# show only contours
new = get_new(img)
cv2.drawContours(new, rects,-1,(0,255,0),1)
cv2.GaussianBlur(new, (9,9), 0, new)
new = cv2.Canny(new, 0, CANNY, apertureSize=3)


cv2.imwrite('dilated.png', dilated)
cv2.imwrite('edges.png', edges)
cv2.imwrite('test.png', orig)
