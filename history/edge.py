import numpy as np
import cv2
import imutils

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread("example.jpg")
# ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 400)
#
# b,g,r = cv2.split(image)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 20, 30)


# loop over the contours
_, cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)

# show the original image and the edge detected image
cv2.imwrite('test.png', image)
# b seems good
# g hm
# r
