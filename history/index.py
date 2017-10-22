# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html
import numpy as np
import cv2

img = cv2.imread('example.jpg')
# gray = cv2.imread('example.jpg',0)

blurred = cv2.medianBlur(img,9)

gray = cv2.cvtColor( blurred, cv2.COLOR_BGR2GRAY )

gray = cv2.bilateralFilter( gray, 1, 10, 120 )

# ret,thresh = cv2.threshold(gray,127,255,0) # 0 or 1 ?

# _,contours,h = cv2.findContours(thresh,1,2)

edges = cv2.Canny(gray,10,20,3)
# edges = cv2.dilate(gray, gray); # anchor? Point(-1,-1)

# kernel = cv2.getStructuringElement( cv2.MORPH_RECT, ( 7, 7 ) )
#
# closed = cv2.morphologyEx( edges, cv2.MORPH_CLOSE, kernel )

_, contours, h = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

print(len(contours))
for cont in contours:
    cv2.drawContours( img, [cont], -1, ( 255, 0, 0 ), 2 )

cv2.imwrite('test.png', img)
