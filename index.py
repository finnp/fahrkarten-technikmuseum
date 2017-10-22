import cv2, numpy as np
import sys
import imutils

# finding contours
def contorize (img, a):
    _, contours, _ = cv2.findContours(a.copy(), cv2.RETR_LIST,
                               cv2.CHAIN_APPROX_SIMPLE)

    contours = filter(lambda cont: cv2.contourArea(cont) > 400000, contours)

    rects = []
    for cont in contours:
        rect = cv2.approxPolyDP(cont, 40, True).copy().reshape(-1, 2)
        rect = cv2.convexHull(rect)
        if (len(rect) > 15): continue
        area = cv2.contourArea(rect)
        x,y,width,height = cv2.boundingRect(rect)
        rect_area = width * height
        area_diff = abs(rect_area - area)
        if (area_diff > 60000): continue
        rects.append(rect)

    cv2.drawContours(img, rects,-1,(0,255,0),10)



original = cv2.imread('img/test.jpg')

# resize?

img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
cv2.GaussianBlur(img, (7,7), 0, img)

thresh = 175 # 172
maxValue = 255

_, binary = cv2.threshold(img, thresh, maxValue, cv2.THRESH_BINARY)

smallkernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(binary,smallkernel,iterations = 1)
kernel = np.ones((11,11),np.uint8)
erosion = cv2.erode(dilation,kernel,iterations = 1)

# HoughLines?

# is this the right tool?
# edges = cv2.Canny(binary, 0, 100) # this produces the wrong output
contorize(original, erosion)

cv2.imwrite('output/test.png', original)
