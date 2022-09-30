import re

small_file = "C:/Users/tibor/Desktop/FREEBASE/freebase-head-1000000"
huge_file = "C:/Users/tibor/Desktop/FREEBASE/freebase-rdf-latest"
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

def search(person_1_name, person_2_name):
    with open(small_file, encoding="utf-8") as fileobject:
        for line in fileobject:

            current_object_id = re.search('^<http:\/\/rdf\.freebase\.com\/ns\/(.*?)>.*$', line).group(1)
            print(current_object_id)

            # TODO: Get the inital object id and get the rest of the lines with the same id.
            # TODO: Check the list of lines with same object if one of the names occurs, then get the birth date, ?death date?, city.
            # TODO: always check if the object is person
            # if current_object:
            #     print(line)

            # match_1 = re.search(person_1_name, line)
            # match_2 = re.search(person_2_name, line)
            # if match_1:
            #     result_1.append(line)


if __name__ == '__main__':

    result_1 = []
    result_2 = []
    person_1_name, person_2_name = get_persons()

    search(person_1_name, person_2_name)

    print(*result_1, sep='\n')
    print(*result_2, sep='\n')
