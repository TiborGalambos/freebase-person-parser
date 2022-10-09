from settings import run_date_test, person_1_data, person_2_data


def date_test():
    if run_date_test:
        person_1_data.update({'name': 'no one', 'birth_date': '2001-03-23', 'death_date': '2004-03-15'})
        person_2_data.update({'name': 'no two', 'birth_date': '2004-03-23', 'death_date': '2005-03-24'})
        return True
    return False
