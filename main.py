import re

small_file = "C:/Users/tibor/Desktop/FREEBASE/freebase-head-1000000"
huge_file = "C:/Users/tibor/Desktop/FREEBASE/freebase-rdf-latest"

open_this_file = small_file

auto_assign_person = True

def get_persons():
    if auto_assign_person:
        return 'Kathrin Marchand', 'Vaino Haapalainen'

    else:
        print("write first name:")
        person_1 = input()
        print("write second name:")
        person_2 = input()

    return str(person_1), str(person_2)


def is_person(temp_object_data):
    for rows in temp_object_data:
        return re.search('<http:\/\/rdf.freebase.com\/ns\/type.object.type>.*<http:\/\/rdf.freebase.com/ns/people.person>', rows)


def has_name(temp_object_data):
    name = None
    for rows in temp_object_data:
        try:
            name = re.search('<http:\/\/rdf.freebase.com\/ns\/type.object.name>\t\"(.*?)\".*\t.', rows).group(1)
            return name
        except:
            pass

def check_temp_object(temp_object_data):

    if is_person(temp_object_data):
        # print(*temp_object_data, sep='\n')
        # print('-------------')
        name = has_name(temp_object_data)
        if name != None:
            print('name = ' + name)



def search(person_1_name, person_2_name):

    person_1_data = []
    person_2_data = []
    temp_object_data = []

    prev_object_id = ''
    current_object_id = ''

    with open(open_this_file, encoding="utf-8") as fileobject:
        for line in fileobject:

            fetched_object_id = re.search('^<http:\/\/rdf\.freebase\.com\/ns\/(.*?)>.*$', line).group(1)

            if fetched_object_id != prev_object_id:
                # print('printing whole object', *temp_object_data, sep='\n')
                # print('------------')
                check_temp_object(temp_object_data)
                temp_object_data.clear()
                # print('new object found: ' + fetched_object_id)
                current_object_id = fetched_object_id

            if current_object_id == prev_object_id:
                temp_object_data.append(line)
                # print('adding data')



                current_object_id = fetched_object_id

            prev_object_id = fetched_object_id


            # TODO: Get the inital object id and get the rest of the lines with the same id.
            # TODO: Check the list of lines with same object if one of the names occurs, then get the birth date, ?death date?, city.
            # TODO: always check if the object is person
            # if current_object:
            #     print(line)

            # match_1 = re.search(person_1_name, line)
            # match_2 = re.search(person_2_name, line)
            # if match_1:
            #     result_1.append(line)
        print('end')

        # print('printing whole object', *temp_object_data, sep='\n')
        # print('------------')
        temp_object_data.clear()

if __name__ == '__main__':

    result_1 = []
    result_2 = []
    person_1_name, person_2_name = get_persons()

    search(person_1_name, person_2_name)

    print(*result_1, sep='\n')
    print(*result_2, sep='\n')
