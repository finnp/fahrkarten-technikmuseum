import cv2
import numpy as np
import sys
from functools import reduce

# options
min_ticket_size = 450000
retr_type = cv2.RETR_LIST
contour_algorithm = cv2.CHAIN_APPROX_SIMPLE
erode_kernel = np.ones((11,11),np.uint8)
dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(40,40))

def grey(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def blur(img):
    return cv2.GaussianBlur(img, (7,7), 0)

def threshold(img):
    _, binary = cv2.threshold(img, 174, 255, cv2.THRESH_BINARY)
    return binary

def dilate(img):
    return cv2.dilate(img, dilate_kernel)

def erode(img):
    return cv2.erode(img,erode_kernel,iterations = 1)

def canny(img):
    return cv2.Canny(img, 0, 85, apertureSize=3)

def find_contours (img):
    _, contours, _ = cv2.findContours(img.copy(), retr_type, contour_algorithm)
    contours = list(filter(lambda cont: cv2.contourArea(cont) > min_ticket_size, contours))
    rects = []
    polygons = []
    for cont in contours:
        polygon = cv2.approxPolyDP(cont, 40, True).copy().reshape(-1, 2)
        polygon = cv2.convexHull(polygon)
        if (len(polygon) > 15): continue # possibly not needed when comparing the areas
        area = cv2.contourArea(polygon)
        rect = cv2.boundingRect(polygon)
        x,y,width,height = rect
        if (width > 2.3*height or height > 2.3*width): continue # unusual shape
        rect_area = width * height
        area_diff = abs(rect_area - area)
        if (area_diff > 60000): continue
        rects.append(rect)
        polygons.append(polygon)

    return (rects, polygons)

steps = [
    grey,
    blur,
    threshold,
    dilate,
    erode,
    canny
]

def calculate_distance(x1, y1, x2, y2):
    return (x2 - x1)**2 + (y2 - y1)**2

def find_tickets(img):
    for step in steps:
        img = step(img)

    (rects, contours) = find_contours(img)

    for ticket_a in rects:
        x1, y1, w1, h1 = ticket_a
        for ticket_b in rects:
            x2, y2, w2, h2 = ticket_b
            distance = calculate_distance(x1, y1, x2, y2)
            if (distance < 10000):
                rects.remove(ticket_b)

    tickets = []
    for ticket in rects:
        x,y,w,h = ticket
        tickets.append({
            'x': x,
            'y': y,
            'width': w,
            'height': h,
        })
    return tickets


def debug_tickets(original, img):
    for index, step in enumerate(steps):
        img = step(img)
        cv2.imwrite(str(index) + '-' + step.__name__ + '.jpg', img)

    (rects, contours) = find_contours(img)
    print(len(rects))
    cv2.drawContours(original,contours,-1,(0,255,0),3)
    cv2.imwrite('final.jpg', original)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        file_name = sys.argv[1]
    else:
        file_name = 'img/III.5.01-01.jpg'
    print('reading', file_name)
    original = cv2.imread(file_name)
    debug_tickets(original, original.copy())
