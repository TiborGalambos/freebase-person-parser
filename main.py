import json

from debug_tests import date_test
import people_object_extracter
from parsers import *
from parsers import parse_dates
from settings import open_this_file, auto_assign_person, just_extract_person_objects, person_1_data, person_2_data


# --------------------------------------------------------------------- #


def get_persons():
    if auto_assign_person:
        return 'Dursley McLinden', 'Robert Brattain'

    else:
        print("write first name:")
        person_1 = input()
        print("write second name:")
        person_2 = input()

    return str(person_1), str(person_2)


def process_temp_object(temp_object_data, person_1_name, person_2_name):
    if is_person(temp_object_data):

        name = get_name(temp_object_data)
        if name != None and (name == person_1_name or name == person_2_name):
            birth_date = get_birth_date(temp_object_data)
            death_date = get_death_date(temp_object_data)

            if not person_1_data:  # if empty
                person_1_data['name'] = name
                person_1_data.update({'name': name, 'birth_date': birth_date, 'death_date': death_date})

                print('found: \n', json.dumps(person_1_data, indent=4))
            else:
                person_2_data.update({'name': name, 'birth_date': birth_date, 'death_date': death_date})
                print('found: \n', json.dumps(person_2_data, indent=4))
                return True


def could_they_meet():

    # TODO: expect date for every date format that can occur
    # TODO: could they meet by date -> place
    person_1_birth, person_1_death, person_2_birth, person_2_death = parse_dates()

    if (person_1_birth < person_2_birth < person_1_death or person_2_birth < person_1_birth < person_2_death):
        print('\nYES, they could have met')
    else:
        print('\nNO, they could not have met')
    exit(0)


def search(person_1_name, person_2_name):
    temp_object_data = []

    prev_object_id = ''
    current_object_id = ''

    with open(open_this_file, encoding="utf-8") as fileobject:
        for line in fileobject:

            fetched_object_id = re.search('^<http:\/\/rdf\.freebase\.com\/.+?\/(.*?)>.*$', line).group(1)

            if fetched_object_id != prev_object_id:
                if (process_temp_object(temp_object_data, person_1_name, person_2_name)):  # check prev object data
                    could_they_meet()
                temp_object_data.clear()
                current_object_id = fetched_object_id  # new object

            if current_object_id == prev_object_id:  # adding data
                temp_object_data.append(line)
                current_object_id = fetched_object_id

            prev_object_id = fetched_object_id

        if (process_temp_object(temp_object_data, person_1_name, person_2_name)):  # check prev object data
            could_they_meet()
        temp_object_data.clear()

    fileobject.close()


if __name__ == '__main__':

    if date_test():
        could_they_meet()

    if not just_extract_person_objects:
        person_1_name, person_2_name = get_persons()
        print('searching names: {}, {} ...'.format(person_1_name, person_2_name))
        search(person_1_name, person_2_name)
    else:
        people_object_extracter.get_people_objects()
