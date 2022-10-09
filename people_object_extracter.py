import re

from parsers import is_person, get_name, get_birth_date, get_death_date
from settings import open_this_file, debug

output_file_path = 'C:/Users/tibor/Desktop/FREEBASE/people_person'


def process_temp_object_for_get_people_objects(temp_object_data):
    if is_person(temp_object_data):
        name = get_name(temp_object_data)
        if name is not None:
            birth_date = get_birth_date(temp_object_data)
            if birth_date is not None:
                with open(output_file_path, 'a', encoding="utf-8") as fileobject:
                    fileobject.write('\n'.join(temp_object_data))
                fileobject.close()
                return True
    return False


def get_people_objects():
    temp_object_data = []

    prev_object_id = ''
    current_object_id = ''

    line_counter = 0
    object_counter = 0
    person_counter = 0

    with open(open_this_file, encoding="utf-8") as fileobject:
        for line in fileobject:

            if line_counter % 1000000 == 0:
                print('line = ' + str(line_counter))

            line_counter += 1

            fetched_object_id = re.search('^<http:\/\/rdf\.freebase\.com\/.+?\/(.*?)>.*$', line).group(1)

            if debug: print(f'fetched: {fetched_object_id}, prev: {prev_object_id}')

            if fetched_object_id != prev_object_id:
                if process_temp_object_for_get_people_objects(temp_object_data):  # if it is person & is written to file
                    person_counter += 1
                    print('person = ' + str(person_counter))

                temp_object_data.clear()
                current_object_id = fetched_object_id  # new object
                object_counter += 1

                if object_counter % 100000 == 0:
                    print('object = ' + str(object_counter))

            if current_object_id == prev_object_id:  # adding data
                temp_object_data.append(line)
                current_object_id = fetched_object_id

            prev_object_id = fetched_object_id

        process_temp_object_for_get_people_objects(temp_object_data)
    fileobject.close()
