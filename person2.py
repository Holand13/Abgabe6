import json
from datetime import datetime
import pandas as pd
import plotly.express as px


class Person2:
    
    @staticmethod
    def load_person_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        person_data = json.load(file)
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

        person_data = Person2.load_person_data()
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
        person_data = Person2.load_person_data()
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
        self.date_of_birth = person_dict["date_of_birth"]
        self.firstname = person_dict["firstname"]
        self.lastname = person_dict["lastname"]
        self.picture_path = person_dict["picture_path"]
        self.id = person_dict["id"]
        

    def calc_age(self):
        today = datetime.now()
        age = today.year - self.date_of_birth
        self.age = age
        return age
    

    def calc_max_heart_rate(self):
        max_hr_bpm =  223 - 0.9 * self.calc_age()
        self.max_hr_bpm = max_hr_bpm
        return int(max_hr_bpm)
    
    '''
    def get_new_id():
        person_data = Person.load_person_data()
        max_id = 0
        for eintrag in person_data:
            if eintrag["id"] > max_id:
                max_id = eintrag["id"]
        return max_id + 1
    

    #datensatz in json file hinzufügen
'''