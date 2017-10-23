import cv2, numpy as np
import sys
import imutils
import os

retr_type = cv2.RETR_LIST
contour_algorithm = cv2.CHAIN_APPROX_TC89_KCOS

input_dir = 'img'
output_dir = 'output'

def find_contours (img, a, color):
    _, contours, _ = cv2.findContours(a.copy(), retr_type, contour_algorithm)
    contours = filter(lambda cont: cv2.contourArea(cont) > 400000, contours) # 20.000 to get more infor

    rects = []
    for cont in contours:
        rect = cv2.approxPolyDP(cont, 40, True).copy().reshape(-1, 2)
        rect = cv2.convexHull(rect)
        if (len(rect) > 15): continue # possibly not needed when comparing the areas
        area = cv2.contourArea(rect)
        x,y,width,height = cv2.boundingRect(rect)
        rect_area = width * height
        area_diff = abs(rect_area - area)
        if (area_diff > 60000): continue
        rects.append(rect)

    cv2.drawContours(img, rects,-1,color,10)

def process_image(file_name):
    original = cv2.imread(input_dir + '/' + file_name)
    img = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    cv2.GaussianBlur(img, (7,7), 0, img)

    thresh = 175
    maxValue = 255

    _, binary = cv2.threshold(img, thresh, maxValue, cv2.THRESH_BINARY)

    smallkernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(binary,smallkernel,iterations = 1)
    kernel = np.ones((11,11),np.uint8)
    erosion = cv2.erode(dilation,kernel,iterations = 1)


    rough_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(40,40))
    rough_dilation = cv2.dilate(binary, rough_kernel)
    rough_erosion = cv2.erode(rough_dilation,kernel,iterations = 1)

    edges = cv2.Canny(rough_erosion, 0, 85, apertureSize=3)

    find_contours(original, erosion, (0,255,0))
    find_contours(original, edges, (0,0,255))

    cv2.imwrite(output_dir + '/' + file_name, original)

files = os.listdir(input_dir)

for file_name in files:
    print('processing', file_name)
    process_image(file_name)
