import mwclient
import os
import hashlib

"""
Check the integrity of the downloaded images, delete corrupted images
"""

path = 'img'
category_name = 'Rail_tickets_from_the_collection_of_the_Deutsches_Technikmuseum'

site = mwclient.Site('commons.wikimedia.org')
category = site.Categories[category_name]
images = category.members(namespace=6)

missing_count = 0
corrupt_count = 0

existing_files = os.listdir(path)

for image in images:
    title = image.page_title
    if title in existing_files: existing_files.remove(title)
    image_path = path + '/' + title
    try:
        openedFile = open(image_path, 'rb')
        readFile = openedFile.read()
        sha = hashlib.sha1(readFile).hexdigest()
        if (sha != image.imageinfo['sha1']):
            print(image_path, 'is corrupt, deleting file')
            os.remove(image_path)
            corrupt_count += 1
    except FileNotFoundError:
        missing_count += 1

print(str(missing_count), ' are missing')
print(str(corrupt_count), 'corrupted files deleted')
print('additional files:', existing_files)
