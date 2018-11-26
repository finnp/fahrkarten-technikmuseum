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


def process_image(file_name):
    original = cv2.imread(input_dir + '/' + file_name)

    tickets = find_tickets(original)

    print(len(tickets), 'tickets found')
    for index, ticket in enumerate(tickets):
        cropped = original[y - border: y + h + border, x - border: x + w + border]
        ticket['tableau'] = file_name
        ticket['created_at'] = datetime.datetime.now().isoformat()

        file_without_ending = file_name[:-len('.' + image_type)]

        output_filename = output_dir + '/' + file_without_ending + '-' + str(index)

        with open(output_filename + '.json', 'w') as fp:
            json.dump(ticket, fp)
        cv2.imwrite(output_filename  + '.jpg', cropped)

files = os.listdir(input_dir)
files = list(filter(lambda f: f[-len(image_type):] == 'jpg', files))
total = len(files)

for index, file_name in enumerate(files):
    print('processing ' + str(index + 1) + '/' + str(total), file_name)
    process_image(file_name)
