import re
from tqdm import tqdm
from parsers import is_person, get_name, get_birth_date, get_death_date, get_place_of_birth, get_place_lived
from settings import debug


def process_temp_object_for_get_people_objects(temp_object_data, writer):
    if is_person(temp_object_data):
        name = get_name(temp_object_data)

        if name is not None:
            birth_date = get_birth_date(temp_object_data)
            if debug:
                print(birth_date)
            if birth_date is not None:
                if debug:
                    print(name)
                    print(str(get_place_of_birth(temp_object_data)))
                    print(str(get_place_lived(temp_object_data)))
                writer \
                    .add_document(name=str(name),
                                  birthdate=str(birth_date),
                                  deathdate=str(get_death_date(temp_object_data)),
                                  birthplace=str(get_place_of_birth(temp_object_data)),
                                  placelived=str(get_place_lived(temp_object_data)))
                return True
    return False


def get_people_objects(writer, dataframe):
    temp_object_data = []

    prev_object_id = ''
    current_object_id = ''

    person_counter = 0
    fetched_object_id = 0

    for index, row in tqdm(dataframe.iterrows(), total=dataframe.shape[0]):
        line = (row['object_id'], row['type'], row['context'])
        line = "\t".join(line)

        try:
            fetched_object_id = re \
                .search('^<http:\/\/rdf\.freebase\.com\/.+?\/(.*?)>.*$', line) \
                .group(1)
        except:
            pass

        if debug:
            print(f'fetched: {fetched_object_id}, prev: {prev_object_id}')

        if fetched_object_id != prev_object_id:
            if debug:
                print('checking if person')
            if process_temp_object_for_get_people_objects(temp_object_data, writer):  # if it is person make index
                person_counter += 1
                if debug:
                    print('person = ' + str(person_counter))
            else:
                if debug:
                    print('not person')

            temp_object_data.clear()
            current_object_id = fetched_object_id  # new id found
            temp_object_data.append(line)

            if debug:
                print('appending line to ', current_object_id, line)

        if current_object_id == prev_object_id:  # adding data
            temp_object_data.append(line)
            if debug:
                print('appending line to ', current_object_id, line)
            current_object_id = fetched_object_id

        prev_object_id = fetched_object_id

    process_temp_object_for_get_people_objects(temp_object_data, writer)
    print('persons sum = ' + str(person_counter))
