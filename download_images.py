import mwclient
import os.path

category_name = 'Rail_tickets_from_the_collection_of_the_Deutsches_Technikmuseum'
total_number = 2558

site = mwclient.Site('commons.wikimedia.org')
category = site.Categories[category_name]
images = category.members(namespace=6)
counter = 0

for image in images:
    counter = counter + 1
    title = image.page_title
    file_name = 'img/' + title
    file_exists = os.path.isfile(file_name)
    percentage = round(float(counter) / float(total_number) * 100)
    current_count = str(counter) + '/' + str(total_number) + ' ' + str(percentage) + '%'
    if file_exists:
        print(current_count + ' ' + title + ' - skip')
        continue

    print(current_count + ' ' + title + ' - download')
    with open(file_name, 'wb') as fd:
        image.download(fd)
