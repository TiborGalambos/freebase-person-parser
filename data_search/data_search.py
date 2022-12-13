from whoosh import index
from whoosh.qparser import QueryParser, FuzzyTermPlugin
from io import StringIO
import sys
from datetime import datetime

INDEX_PATH = '/usr/src/indexdir'
debug = False


# method for making sure that the index lookup found someone
def check_if_found(result, entry):
    if result is None:
        print(entry, 'not found. Exiting program.')
        return False
    else:
        return True


# convert the string date of birth to datetime
def birth_to_date(result_bd):
    try:
        person_birth = datetime.strptime(result_bd, '%Y-%m-%d')
    except:
        pass
        try:
            person_birth = datetime.strptime(result_bd, '%Y-%m')
        except:
            pass
            try:
                person_birth = datetime.strptime(result_bd, '%Y')
            except:
                pass
    return person_birth


# convert the string date of death to datetime
def death_to_date(result_dd):
    if result_dd is not None:
        try:
            person_death = datetime.strptime(result_dd, '%Y-%m-%d')
        except:
            pass
            try:
                person_death = datetime.strptime(result_dd, '%Y-%m')
            except:
                pass
                try:
                    person_death = datetime.strptime(result_dd, '%Y')
                except:
                    pass
                    try:
                        person_death = datetime.today()
                    except:
                        pass
    else:
        # if death is not available we assume that the person is alive
        person_death = datetime.today()
    return person_death


# method for comparing two persons lifetime line
def compare_dates(person_1_birth, person_1_death, person_2_birth, person_2_death):
    if debug:
        print('p1 bd: ', person_1_birth)
        print('p1 dd: ', person_1_death)
        print('p2 bd: ', person_2_birth)
        print('p2 dd: ', person_2_death)

    if person_1_birth <= person_2_birth <= person_1_death or person_2_birth <= person_1_birth <= person_2_death:
        print('\nYES, they could have met by fetched time')
        return True
    else:
        print('\nNO, they could not have met by fetched time')
        return False


# compare the birthplaces of persons
def compare_birthplace(result1_bp, result2_bp):
    if result1_bp != 'None' and result2_bp != 'None' and result1_bp == result2_bp:
        print('YES, they have the same birthplace')
        return True
    else:
        print('NO, I have no information about one or both persons birthplace')
        return False


# compare the place the persons live(d)
def compare_place_lived(result1_pl, result2_pl):
    if result1_pl != 'None' and result2_pl != 'None' and result1_pl == result2_pl:
        print('YES, they lived in same location')
        return True
    else:
        print('NO, I have no information about one or both persons place they lived')
        return False


def run_search():
    # opening indexing directory
    ix = index.open_dir(INDEX_PATH)
    searcher = ix.searcher()

    result1_name = None
    result2_name = None

    result1_bp = None
    result2_bp = None

    result1_pl = None
    result2_pl = None

    # user input of two names
    entry1 = input('search for first name:')
    entry2 = input('search for second name:')

    buffer = StringIO()
    sys.stdout = buffer

    print('\n')

    # we will get index by name
    parser = QueryParser("name", ix.schema)
    # we allow some mistakes in names or lower/upper case
    parser.add_plugin(FuzzyTermPlugin)

    # first search
    query1 = parser.parse(entry1)
    results = searcher.search(query1, terms=True, limit=1)

    for r in results:
        result1_name = r.get('name')
        print(result1_name)

        result1_bd = r.get('birthdate')
        print('born:', result1_bd)

        result1_dd = r.get('deathdate')
        print('death:', result1_dd)

        result1_bp = r.get('birthplace')
        print('birth place id:', result1_bp)

        result1_pl = r.get('placelived')
        print('place lived id:', result1_pl)

    print('\n')

    # second search
    query2 = parser.parse(entry2)
    results = searcher.search(query2, terms=True, limit=1)

    for r in results:
        result2_name = r.get('name')
        print(result2_name)

        result2_bd = r.get('birthdate')
        print('born:', result2_bd)

        result2_dd = r.get('deathdate')
        print('death:', result2_dd)

        result2_bp = r.get('birthplace')
        print('birth place id:', result2_bp)

        result2_pl = r.get('placelived')
        print('place lived id:', result2_pl)

    if not (check_if_found(result1_name, entry1) and check_if_found(result2_name, entry2)):
        return buffer.getvalue()

    person_1_birth = birth_to_date(result1_bd)
    person_1_death = death_to_date(result1_dd)

    person_2_birth = birth_to_date(result2_bd)
    person_2_death = death_to_date(result2_dd)

    # calling comparing methods: date, birthplace, place lived
    compare_dates(person_1_birth, person_1_death, person_2_birth, person_2_death)
    compare_birthplace(result1_bp, result2_bp)
    compare_place_lived(result1_pl, result2_pl)

    return buffer.getvalue()


if __name__ == '__main__':
    output = run_search()

    sys.stdout = sys.__stdout__
    print(output)

    exit(0)
