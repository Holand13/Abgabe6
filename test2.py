import streamlit as st
from ekgdata2 import EKGdata
from person2 import Person
from datetime import datetime

if __name__ == "__main__":
    st.set_page_config(page_title="EKG Data Analysis Tool", page_icon=":heart:")
    
    def creds_entered():
        if st.session_state["user"].strip() == "Julian" and st.session_state["password"].strip() == "Passwort":
            st.session_state["logged_in"] = True
        else:
            st.session_state["logged_in"] = False
            if not st.session_state["user"]:
                st.warning("Bitte geben Sie einen Benutzernamen ein.")
            elif not st.session_state["password"]:
                st.warning("Bitte geben Sie ein Passwort ein.")
            else:
                st.error("Passwort oder Benutzername ist falsch. :face_with_symbols_over_mouth:")
    
    def authenticate_user():
        st.title("Anmeldung")
        if "logged_in" not in st.session_state:
            st.text_input(label="Benutzername", value="", key="user", on_change=creds_entered)
            st.text_input(label="Passwort", value="", key="password", type="password", on_change=creds_entered)
            return False
        else:
            if st.session_state["logged_in"]:
                return True
            else:
                st.text_input(label="Benutzername", value="", key="user", on_change=creds_entered)
                st.text_input(label="Passwort", value="", key="password", type="password", on_change=creds_entered)
                return False
            
    if authenticate_user():
        st.title("EKG Data Analysis Tool")

        # Laden der Personendaten und Auffüllen der Klassenvariable alle_
        # Laden der Personendaten und Auffüllen der Klassenvariable alle_ekg_daten
        person_data = Person.load_person_data()
        for person in person_data:
            EKGdata.all_ekg_daten.extend(person["ekg_tests"])
    
        person_names = Person.get_person_list(person_data)
        selected_person_name = st.selectbox("Wählen Sie eine Person", ["Auswählen"] + person_names)
        if selected_person_name != "Auswählen":
            person_dict = Person.find_person_data_by_name(selected_person_name)
            if person_dict:
                person_objekt = Person(person_dict)
                st.write(f"Name: {person_objekt.firstname} {person_objekt.lastname}")
                st.write(f"Geburtsdatum: {person_objekt.date_of_birth}")
                st.image(person_objekt.picture_path)
                st.write("Alter:", person_objekt.calc_age())
                st.write("Die maximale Herzfrequenz beträgt:", person_objekt.calc_max_heart_rate(), "bpm")
        
                selected_ekg_id = st.selectbox("Wählen Sie eine EKG-ID", [ekg["id"] for ekg in person_dict["ekg_tests"]])
                if selected_ekg_id:
                    ekg_by_id = EKGdata.load_by_id(selected_ekg_id)
                    if ekg_by_id:
                        st.write("Die Herzfrequenz lautet:")
                        ekg_by_id.find_peaks(threshold=320, distance=150)
                        st.write(ekg_by_id.estimate_hr())
                        ekg_by_id.display_test_date_and_plot()  
                    else:
                        st.write("Keine EKG-Daten mit der gegebenen ID gefunden.")
            else:
                st.write("Keine Person mit diesem Namen gefunden.")
