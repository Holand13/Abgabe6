import json

def get_person_data():
# Opening JSON file
    file = open("data/person_db.json")

# Loading the JSON File in a dictionary
    person_data = json.load(file)
    return person_data

def get_person_names(person_data):
    """gets all names from the person_data and returns them as a list"""

    #person_data = get_person_data()

    #print(person_data)
    list_with_person_names = []
    for person in person_data:
        list_with_person_names.append(person['lastname'] + ' , ' + person['firstname'])
    #print(list_with_person_names)

    return list_with_person_names

def find_person_data_by_name(suchstring):
   
    person_data = get_person_data()
    if suchstring == "None":
        return {}

    two_names = suchstring.split(" , ")
    vorname = two_names[1]
    nachname = two_names[0]

    for eintrag in person_data:
        if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
            #print(eintrag)
    
            return eintrag
    else:
        return {}

if __name__ == "__main__" :
    person_data = get_person_data()
    person_names_list = get_person_names(person_data)
    #print(person_names_list)
    suchstring ='Schmirander , Yunus'
    print(find_person_data_by_name(suchstring))
