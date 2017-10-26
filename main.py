import cv2, numpy as np
import sys
import imutils
import os
import json
import datetime
from find_tickets import find_tickets

retr_type = cv2.RETR_LIST
contour_algorithm = cv2.CHAIN_APPROX_SIMPLE

input_dir = 'img'
output_dir = 'output'
border = 30
image_type = 'jpg'

def calculate_distance(x1, y1, x2, y2):
    return (x2 - x1)**2 + (y2 - y1)**2

def process_image(file_name):
    original = cv2.imread(input_dir + '/' + file_name)

    tickets = find_tickets(original)

    # remove probable duplicates TODO: move to tickets.py
    for ticket_a in tickets:
        x1, y1, w1, h1 = ticket_a
        for ticket_b in tickets:
            x2, y2, w2, h2 = ticket_b
            distance = calculate_distance(x1, y1, x2, y2)
            if (distance < 10000):
                tickets.remove(ticket_b)

    print(len(tickets), 'tickets found')
    for index, ticket in enumerate(tickets):
        x,y,w,h = ticket
        cropped = original[y - border: y + h + border, x - border: x + w + border]
        metadata = {
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'tableau': file_name,
            'created_at': datetime.datetime.now().isoformat()
        }

        file_without_ending = file_name[:-len('.' + image_type)]

        output_filename = output_dir + '/' + file_without_ending + '-' + str(index)

        with open(output_filename + '.json', 'w') as fp:
            json.dump(metadata, fp)
        cv2.imwrite(output_filename  + '.jpg', cropped)

files = os.listdir(input_dir)
files = list(filter(lambda f: f[-len(image_type):] == 'jpg', files))
total = len(files)

for index, file_name in enumerate(files):
    print('processing ' + str(index + 1) + '/' + str(total), file_name)
    process_image(file_name)
