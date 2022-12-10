from whoosh import index
from whoosh.qparser import QueryParser, FuzzyTermPlugin
from datetime import datetime
from settings import debug, INDEX_PATH


def check_if_found(result, entry):
    if result is None:
        print(entry, 'not found. Exiting program.')
        exit(1)


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
        person_death = datetime.today()
    return person_death


def compare_dates(person_1_birth, person_1_death, person_2_birth, person_2_death):
    if debug:
        print('p1 bd: ', person_1_birth)
        print('p1 dd: ', person_1_death)
        print('p2 bd: ', person_2_birth)
        print('p2 dd: ', person_2_death)

    if person_1_birth <= person_2_birth <= person_1_death or person_2_birth <= person_1_birth <= person_2_death:
        print('\nYES, they could have met')
    else:
        print('\nNO, they could not have met')


if __name__ == '__main__':
    ix = index.open_dir(INDEX_PATH)
    searcher = ix.searcher()

    result1_name = None
    result2_name = None

    entry1 = input('search for first name:')
    entry2 = input('search for second name:')

    print('\n')

    parser = QueryParser("name", ix.schema)
    parser.add_plugin(FuzzyTermPlugin)

    # first search
    query1 = parser.parse(entry1)
    results = searcher.search(query1, terms=True, limit=1)

    for r in results:
        print(r.get('name'))
        result1_name = r.get('name')

        print('born:', r.get('birthdate'))
        result1_bd = r.get('birthdate')

        print('death:', r.get('deathdate'))
        result1_dd = r.get('deathdate')

    print('\n')

    # second search
    query2 = parser.parse(entry2)
    results = searcher.search(query2, terms=True, limit=1)

    for r in results:
        print(r.get('name'))
        result2_name = r.get('name')

        print('born:', r.get('birthdate'))
        result2_bd = r.get('birthdate')

        print('death:', r.get('deathdate'))
        result2_dd = r.get('deathdate')

    check_if_found(result1_name, entry1)
    check_if_found(result2_name, entry2)

    person_1_birth = birth_to_date(result1_bd)
    person_1_death = death_to_date(result1_dd)

    person_2_birth = birth_to_date(result2_bd)
    person_2_death = death_to_date(result2_dd)

    compare_dates(person_1_birth, person_1_death, person_2_birth, person_2_death)

    exit(0)
