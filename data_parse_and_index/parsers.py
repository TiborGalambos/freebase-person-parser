import re

from settings import debug

# regex parsers for various parts of rows

def is_person(temp_object_data):

    for rows in temp_object_data:
        if debug: print(rows)
        if rows in ['\n', '\r\n']:
            continue
        if re.search('<http:\/\/rdf.freebase.com\/ns\/people.person>', rows):
            return True
    if debug: print('is person is False')
    return False


def get_name(temp_object_data):
    name = None
    for rows in temp_object_data:
        if rows in ['\n', '\r\n']:
            continue
        try:
            name = re\
                .search('<http:\/\/rdf.freebase.com\/ns\/type.object.name>\t\"(.*?)\"@.*', rows)\
                .group(1)
            return name
        except:
            pass
    return name


def get_birth_date(temp_object_data):
    birth_date = None
    for rows in temp_object_data:
        if debug: print(rows)
        if rows in ['\n', '\r\n']:
            if debug:
                print('this row is empty')
            continue
        try:
            birth_date = re\
                .search('<http:\/\/rdf.freebase.com\/ns\/people.person.date_of_birth>\t\"(.*?)\"', rows)\
                .group(1)
            if debug:
                print(birth_date)
            return birth_date
        except:
            pass
    if debug:
        print('returning none at the end')
    return birth_date


def get_death_date(temp_object_data):
    death_date = None
    for rows in temp_object_data:
        if rows in ['\n', '\r\n']:
            continue
        try:
            death_date = re\
                .search('<http:\/\/rdf.freebase.com\/ns\/people.deceased_person.date_of_death>\t\"(.*?)\"', rows)\
                .group(1)
            return death_date
        except:
            pass
    return death_date


def get_place_of_birth(temp_object_data):
    place_of_birth = None
    for rows in temp_object_data:
        if rows in ['\n', '\r\n']:
            continue
        try:
            place_of_birth = re\
                .search('^<http:\/\/rdf\.freebase\.com\/.+?\/.*?>\t<http:\/\/rdf.freebase.com\/ns\/people.person.place_of_birth>\t<http:\/\/rdf\.freebase\.com\/ns\/(.*?)>', rows)\
                .group(1)
            return place_of_birth
        except:
            pass
    return place_of_birth


def get_place_lived(temp_object_data):
    place_lived = None
    for rows in temp_object_data:
        if rows in ['\n', '\r\n']:
            continue
        try:
            place_lived = re\
                .search('^<http:\/\/rdf\.freebase\.com\/.+?\/.*?>\t<http:\/\/rdf.freebase.com\/ns\/people.person.places_lived>\t<http:\/\/rdf\.freebase\.com\/ns\/(.*?)>', rows)\
                .group(1)
            return place_lived
        except:
            pass
    return place_lived
