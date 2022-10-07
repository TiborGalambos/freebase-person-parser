import re
from datetime import datetime

small_file = "C:/Users/tibor/Desktop/FREEBASE/freebase-head-1000000"
huge_file = "C:/Users/tibor/Desktop/FREEBASE/freebase-rdf-latest"

open_this_file = huge_file
auto_assign_person = True

person_1_data = []
person_2_data = []

debug = False
just_get_person_objects = True


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


def is_person(temp_object_data):
    for rows in temp_object_data:
        return re.search(
            '<http:\/\/rdf.freebase.com\/ns\/type.object.type>.*<http:\/\/rdf.freebase.com/ns/people.person>', rows)


def get_name(temp_object_data):
    name = None
    for rows in temp_object_data:
        try:
            name = re.search('<http:\/\/rdf.freebase.com\/ns\/type.object.name>\t\"(.*?)\".*\t.', rows).group(1)
            return name
        except:
            pass
    return name


def get_birth_date(temp_object_data):
    birth_date = None
    for rows in temp_object_data:
        try:
            birth_date = re.search('<http:\/\/rdf.freebase.com\/ns\/people.person.date_of_birth>\t\"(.*?)\"',
                                   rows).group(1)
            return birth_date
        except:
            pass
    return birth_date


def get_death_date(temp_object_data):
    death_date = None
    for rows in temp_object_data:
        try:
            death_date = re.search('<http:\/\/rdf.freebase.com\/ns\/people.deceased_person.date_of_death>\t\"(.*?)\"',
                                   rows).group(1)
            return death_date
        except:
            pass
    return death_date


def process_temp_object(temp_object_data, person_1_name, person_2_name):
    if is_person(temp_object_data):

        name = get_name(temp_object_data)
        if name != None and (name == person_1_name or name == person_2_name):
            birth_date = get_birth_date(temp_object_data)
            death_date = get_death_date(temp_object_data)

            if not person_1_data:  # if empty
                person_1_data.extend([name, birth_date, death_date])
                print('found: \n', *person_1_data, sep='\n')
            else:
                person_2_data.extend([name, birth_date, death_date])
                print('\nfound: \n', *person_2_data, sep='\n')
                return True


def could_they_meet():
    person_1_birth = datetime.strptime(person_1_data[1], '%Y-%m-%d')
    person_1_death = datetime.strptime(person_1_data[2], '%Y-%m-%d')

    person_2_birth = datetime.strptime(person_2_data[1], '%Y-%m-%d')
    person_2_death = datetime.strptime(person_2_data[2], '%Y-%m-%d')

    if (person_1_birth < person_2_birth < person_1_death or person_2_birth < person_1_birth < person_2_death):
        print('\nthey could meet')
    else:
        print('\nthey could not meet')
    exit(0)


def search(person_1_name, person_2_name):
    temp_object_data = []

    prev_object_id = ''
    current_object_id = ''

    with open(open_this_file, encoding="utf-8") as fileobject:
        for line in fileobject:

            fetched_object_id = re.search('^<http:\/\/rdf\.freebase\.com\/ns\/(.*?)>.*$', line).group(1)

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


def process_temp_object_for_get_people_objects(temp_object_data):
    if is_person(temp_object_data):
        name = get_name(temp_object_data)
        if name is not None:
            birth_date = get_birth_date(temp_object_data)
            death_date = get_death_date(temp_object_data)
            if birth_date is not None and death_date is not None:
                with open('C:/Users/tibor/Desktop/FREEBASE/people_person', 'a', encoding="utf-8") as fileobject:
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

            fetched_object_id = re.search('^<http:\/\/rdf\.freebase\.com\/ns\/(.*?)>.*$', line).group(1)

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


if __name__ == '__main__':

    if not just_get_person_objects:
        person_1_name, person_2_name = get_persons()
        print('searching names: {}, {} ...'.format(person_1_name, person_2_name))
        search(person_1_name, person_2_name)
    else:
        get_people_objects()
