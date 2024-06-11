import json
from datetime import datetime
import pandas as pd
import plotly.express as px


class Person:
    
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        
        file = open("data/person_db.json")
        person_data = json.load(file)
        '''
        with open("data/person_db.json") as file:
            person_data = [json.loads(line) for line in file]
        '''
        return person_data

    @staticmethod
    def get_person_list(person_data):
        """A Function that takes the persons-dictionary and returns a list auf all person names"""
        list_of_names = []

        for eintrag in person_data:
            list_of_names.append(eintrag["lastname"] + ", " +  eintrag["firstname"])
        return list_of_names
    
    @staticmethod
    def find_person_data_by_name(suchstring):
        """ Eine Funktion der Nachname, Vorname als ein String übergeben wird
        und die die Person als Dictionary zurück gibt"""

        person_data = Person.load_person_data()
        #print(suchstring)
        if suchstring == "None":
            return {}

        two_names = suchstring.split(", ")
        vorname = two_names[1]
        nachname = two_names[0]

        for eintrag in person_data:
            print(eintrag)
            if (eintrag["lastname"] == nachname and eintrag["firstname"] == vorname):
                print()

                return eintrag
        else:
            return {}
        
    @staticmethod
    def find_person_data_by_id(person_id):
        """A Function that takes an ID and returns the person as a dictionary"""
        person_data = Person.load_person_data()
        for eintrag in person_data:
            if eintrag["id"] == person_id:
                return eintrag
        return {}
    
    @classmethod
    def load_by_id(self, person_id):
        person_dict = self.find_person_data_by_id(person_id)
        if person_dict:
            return self(person_dict)
        else:
            return None
       
        
    def __init__(self, person_dict):
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        self.ekg_tests = person_dict.get("ekg_tests", [])  # Initialize ekg_tests with an empty list if not present
        if "date_of_birth" in person_dict:
            try:
                self.date_of_birth = int(person_dict["date_of_birth"])
            except ValueError:
                raise ValueError(f"Invalid date_of_birth value: {person_dict['date_of_birth']}")
        else:
            raise KeyError("Missing key 'date_of_birth' in person data")

    def calc_age(self):
        today = datetime.now().date()
        age = today.year - self.date_of_birth
        self.age = age
        return age
    

    def calc_max_heart_rate(self):
        max_hr_bpm =  223 - 0.9 * self.calc_age()
        self.max_hr_bpm = max_hr_bpm
        return int(max_hr_bpm)


    def get_new_id():
        person_data = Person.load_person_data()
        if person_data:
            return person_data[-1]["id"] + 1
        else:
            return 1
        
    def save_person(self):
        """Saves the Person object's data to the JSON file."""
        person_data = Person.load_person_data()
        new_person_data = self.__dict__.copy()
        new_person_data["date_of_birth"] = str(self.date_of_birth)  # Convert date to string
        person_data.append(new_person_data)

        with open("data/person_db.json", "w", encoding='utf-8') as file:
            json.dump(person_data, file, indent=4)

