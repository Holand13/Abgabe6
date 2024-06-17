import streamlit as st
from ekgdata2 import EKGdata
from person2 import Person2
from datetime import date

if __name__ == "__main__":
    #Passwort = 1234 und Nutzername = Nutzername
    def creds_entered():
        if st.session_state["user"].strip() == "Nutzername" and st.session_state["password"].strip() == "1234":
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
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False
            st.session_state["user"] = ""
            st.session_state["password"] = ""

        if st.session_state["logged_in"]:
            return True
        else:
            st.title("Anmeldung")
            st.text_input(label="Benutzername", value=st.session_state.get("user", ""), key="user")
            st.text_input(label="Passwort", value=st.session_state.get("password", ""), key="password", type="password")
            if st.button("Anmelden"):
                creds_entered()
            return False

    if authenticate_user():
        # Seitenleiste für Navigation
        with st.sidebar:
            st.title("Navigation")
            selected_page = st.selectbox("Seite auswählen", ["Start", "Personen", "Neuen Datensatz anlegen", "Einstellungen"])

            # Abmelde-Button am unteren Rand der Seitenleiste
            st.markdown("---")
            logout_placeholder = st.empty()
            if logout_placeholder.button("Abmelden"):
                st.session_state["logged_in"] = False
                st.session_state["user"] = ""
                st.session_state["password"] = ""
                st.experimental_rerun()

        if selected_page == "Start":
            st.title("EKG Data Analysis Tool")
            st.write("Willkommen im EKG Data Analysis Tool.")
        
        elif selected_page == "Personen":
            st.title("EKG Data Analysis Tool")
            # Load person data and populate all_ekg_data class variable
            person_data = Person2.load_person_data()
            for person in person_data:
                EKGdata.all_ekg_daten.extend(person["ekg_tests"])
            tab1, tab2 = st.tabs(["Personenangabe", "EKG-Tests"])
            with tab1:
                person_names = Person2.get_person_list(person_data)
                selected_person_name = st.selectbox("Wählen Sie eine Person", ["Auswählen"] + person_names)
                if selected_person_name != "Auswählen":
                    person_dict = Person2.find_person_data_by_name(selected_person_name)
                    if person_dict:
                        person_objekt = Person2(person_dict)
                        st.write(f"Name: {person_objekt.firstname} {person_objekt.lastname}")
                        st.write(f"Geburtsdatum: {person_objekt.date_of_birth}")
                        st.image(person_objekt.picture_path)
                        st.write("Alter:", person_objekt.calc_age())
                        st.write("Die maximale Herzfrequenz beträgt:", person_objekt.calc_max_heart_rate(), "bpm")
            with tab2:
                if selected_person_name != "Auswählen":
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

        
        elif selected_page == "Neuen Datensatz anlegen":
            st.title("Neuen Datensatz anlegen")
    
    
        elif selected_page == "Einstellungen":
            st.title("Einstellungen")
            st.write("Einstellungen ändern.")
            st.write("Benutzername ändern.")
            st.text_input("Neuer Benutzername")
            st.write("Passwort ändern.")
            st.text_input("Neues Passwort", type="password")
