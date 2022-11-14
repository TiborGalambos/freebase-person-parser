import re
from datetime import datetime

from settings import person_1_data, person_2_data


def is_person(temp_object_data):

    for rows in temp_object_data:
        if rows in ['\n', '\r\n']:
            continue
        if re.search(
            '<http:\/\/rdf.freebase.com\/ns\/people.person>', rows):
            return True
    return False


def get_name(temp_object_data):
    name = None
    for rows in temp_object_data:
        if rows in ['\n', '\r\n']:
            continue
        try:
            name = re.search('<http:\/\/rdf.freebase.com\/ns\/type.object.name>\t\"(.*?)\"@(en|de|sk|cz).*\t.', rows).group(1)
            return name
        except:
            pass
    return name


def get_birth_date(temp_object_data):
    birth_date = None
    for rows in temp_object_data:
        if rows in ['\n', '\r\n']:
            continue
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
        if rows in ['\n', '\r\n']:
            continue
        try:
            death_date = re.search('<http:\/\/rdf.freebase.com\/ns\/people.deceased_person.date_of_death>\t\"(.*?)\"',
                                   rows).group(1)
            return death_date
        except:
            pass
    return death_date


def parse_dates():
    try:
        person_1_birth = datetime.strptime(person_1_data.get('birth_date'), '%Y-%m-%d')
    except:
        try:
            person_1_birth = datetime.strptime(person_1_data.get('birth_date'), '%Y-%m')
        except:
            person_1_birth = datetime.strptime(person_1_data.get('birth_date'), '%Y')
    try:
        person_1_death = datetime.strptime(person_1_data.get('death_date'), '%Y-%m-%d')
    except:
        try:
            person_1_death = datetime.strptime(person_1_data.get('death_date'), '%Y-%m')
        except:
            person_1_death = datetime.strptime(person_1_data.get('death_date'), '%Y')
            try:
                person_1_death = datetime.today()
            except:
                pass
    try:
        person_2_birth = datetime.strptime(person_2_data.get('birth_date'), '%Y-%m-%d')
    except:
        try:
            person_2_birth = datetime.strptime(person_2_data.get('birth_date'), '%Y-%m')
        except:
            person_2_birth = datetime.strptime(person_2_data.get('birth_date'), '%Y')
    try:
        person_2_death = datetime.strptime(person_2_data.get('death_date'), '%Y-%m-%d')
    except:
        try:
            person_2_death = datetime.strptime(person_2_data.get('death_date'), '%Y-%m')
        except:
            person_2_death = datetime.strptime(person_2_data.get('death_date'), '%Y')
            try:
                person_2_death = datetime.today()
            except:
                pass
    return person_1_birth, person_1_death, person_2_birth, person_2_death
