
import streamlit as st
from ekgdata2 import EKGdata
from person import Person
from datetime import date
from oploadfile import upload
import gpxpy
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
from Garmin import (
    calculate_distance_and_speed,
    folium_plot,
    parse_tcx,
    calculate_minutes_since_start,
    plot_hr_over_time_interactive,
)

if __name__ == "__main__":
    #Passwort = 1234 und Nutzername = Nutzername
    #Anmeldeseite
    def creds_entered():
        if st.session_state["user"].strip() == "Nutzername" and st.session_state["password"].strip() == "1234":
            st.session_state["logged_in"] = True
        else:
            st.session_state["logged_in"] = False # Wenn Benutzername oder Passwort falsch ist, wird der Benutzer nicht angemeldet
            if not st.session_state["user"]:
                st.warning("Bitte geben Sie einen Benutzernamen ein.") # Warnung, wenn kein Benutzername eingegeben wurde
            elif not st.session_state["password"]:
                st.warning("Bitte geben Sie ein Passwort ein.") # Warnung, wenn kein Passwort eingegeben wurde
            else:
                st.error("Passwort oder Benutzername ist falsch!") # Fehlermeldung, wenn Benutzername oder Passwort falsch ist

    def authenticate_user(): # Funktion zur Authentifizierung des Benutzers
        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = False
            st.session_state["user"] = ""
            st.session_state["password"] = ""

        if st.session_state["logged_in"]: 
            return True
        else:
            st.markdown("<h1 style='text-align: center;'>EKG Analyse Tool</h1>", unsafe_allow_html=True) #Überschrift
            with st.columns(3)[1]:
                st.image("data/pictures/logo.jpg", width=200) #Logo
            st.text_input(label="Benutzername", value=st.session_state.get("user", ""), key="user") #Benutzername
            st.text_input(label="Passwort", value=st.session_state.get("password", ""), key="password", type="password") #Passwort
            with st.columns(5)[2]:
                if st.button("Anmelden"):
                    creds_entered()
                return False
    
    if authenticate_user(): # Wenn der Benutzer angemeldet ist, wird die Seite angezeigt
        # Seitenleiste für Navigation
        with st.sidebar: # Seitenleiste
            st.title("Navigation")
            selected_page = st.selectbox("Seite auswählen", ["Start", "Personen", "Neuen Datensatz anlegen", "GPX und TCX Dateien einlesen","Einstellungen"])

            # Abmelde-Button am unteren Rand der Seitenleiste
            st.markdown("---")
            logout_placeholder = st.empty()

            if logout_placeholder.button("Abmelden"): # Abmelde-Button
                st.session_state["logged_in"] = False
                st.session_state["user"] = ""
                st.session_state["password"] = ""
   
        if selected_page == "Start": # Startseite
            st.title("EKG Data Analysis Tool")
            st.write("Willkommen im EKG Data Analysis Tool.")


        
        elif selected_page == "Personen": # Personen-Seite
            st.title("EKG Data Analysis Tool")
            # Load person data and populate all_ekg_data class variable
            person_data = Person.load_person_data() # Personendaten laden
            for person in person_data:
                EKGdata.all_ekg_daten.extend(person.get("ekg_tests", []))  # Use get method to avoid KeyError
            tab1, tab2 = st.tabs(["Personenangabe", "EKG-Tests"])
            with tab1: # Personenangabe
                person_names = Person.get_person_list(person_data)
                selected_person_name = st.selectbox("Wählen Sie eine Person", ["Auswählen"] + person_names) 
                if selected_person_name != "Auswählen": 
                    person_dict = Person.find_person_data_by_name(selected_person_name)
                    if person_dict:
                        person_objekt = Person(person_dict)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.image(person_objekt.picture_path) # Profilbild
                        with col2: # Personenangaben
                            st.write(f"Name: {person_objekt.firstname} {person_objekt.lastname}")
                            st.write(f"Geburtsdatum: {person_objekt.date_of_birth}")
                            st.write("Alter:", person_objekt.calc_age())
                            st.write("Die maximale Herzfrequenz beträgt:", person_objekt.calc_max_heart_rate(), "bpm")
                        st.divider() # Trennlinie
                        with st.columns(3)[1]:
                            with st.popover("Personenangaben ändern"): # Popover für Änderung der Personenangaben
                                st.session_state["change_profile"] = True

                                if st.session_state.get("change_profile", False):
                                    new_firstname = st.text_input("Vorname", value=person_objekt.firstname, key="new_firstname") # Eingabefeld für Vorname
                                    new_lastname = st.text_input("Nachname", value=person_objekt.lastname, key="new_lastname") # Eingabefeld für Nachname
                                    new_dob = st.text_input("Geburtsjahr", value=str(person_objekt.date_of_birth), key="new_dob") # Eingabefeld für Geburtsjahr
                                    file_path1 = upload()  
                                    if file_path1: # Wenn ein Bild hochgeladen wird, wird der Pfad gespeichert
                                        person_objekt.picture_path = file_path1
                                    else:
                                        person_objekt.picture_path = "data/pictures/none.jpg" # Standardbild
                                    if st.button("Speichern"): # Speichern-Button
                                        try:
                                            person_objekt.firstname = new_firstname
                                            person_objekt.lastname = new_lastname
                                            person_objekt.date_of_birth = int(new_dob)
                                            person_objekt.update_person()  # Call update_person to overwrite the existing data
                                            st.success("Profil erfolgreich aktualisiert.")
                                            st.session_state["change_profile"] = False 
                                            st.experimental_rerun() 
                                        except ValueError:
                                            st.error("Geburtsjahr muss eine Zahl sein.")

                
            with tab2: # EKG-Tests
                if selected_person_name != "Auswählen":
                    selected_ekg_id = st.selectbox("Wählen Sie eine EKG-ID", [ekg["id"] for ekg in person_dict.get("ekg_tests", [])]) # EKG-ID auswählen
                    if selected_ekg_id:
                        ekg_by_id = EKGdata.load_by_id(selected_ekg_id) # EKG-Daten laden
                        if ekg_by_id:
                            st.write("Die Herzfrequenz lautet:")
                            ekg_by_id.find_peaks(threshold=320, distance=150) 
                            st.write(ekg_by_id.estimate_hr())
                            ekg_by_id.display_test_date_and_plot()  
                        else:
                            st.write("Keine EKG-Daten mit der gegebenen ID gefunden.")
                    else:
                        st.write("Keine Person mit diesem Namen gefunden.")

        elif selected_page == "Neuen Datensatz anlegen": # Neue Person anlegen
            st.title("Neuen Datensatz anlegen")
        # Create a new person
            st.write("Bitte geben Sie die Daten der neuen Person ein.")
            new_person = {} # Dictionary für neue Person
            new_person["firstname"] = st.text_input("Vorname")
            new_person["lastname"] = st.text_input("Nachname")
            min_date = date(1900, 1, 1)
            max_date = date.today()
            ndate = st.text_input("Geburtsjahr") # Eingabefeld für Geburtsjahr
            try:
                if ndate.isdigit(): # Überprüfen, ob das eingegebene Geburtsjahr eine Zahl ist
                    new_person["date_of_birth"] = int(ndate)
            except ValueError:
                st.error("Geburtsjahr muss eine Zahl sein.")
            new_person["ekg_tests"] = [] 
            # neue ID erstellen
            new_person["id"] = Person.get_new_id()
            file_path = upload()  
            if file_path: # Wenn ein Bild hochgeladen wird, wird der Pfad gespeichert
                new_person["picture_path"] = file_path
            else:
                new_person["picture_path"] = "data/pictures/none.jpg"
            
            with st.columns(5)[2]:

                if st.button("Person anlegen"): # Person anlegen-Button
                    try:
                        st.success("Person erfolgreich angelegt.")
                        new_person_obj = Person(new_person)
                        new_person_obj.save_person()
                        st.experimental_rerun()
                    except KeyError as e:
                        st.error(f"Fehlender Schlüssel in Personendaten: {e}") # Fehlermeldung, wenn ein Schlüssel fehlt
                    except ValueError as e:
                        st.error(f"Ungültiger Wert in Personendaten: {e}")


        elif selected_page == "GPX und TCX Dateien einlesen":
            st.title("GPX und TCX Datenanalyse")

            # GPX Datei hochladen
            uploaded_gpx_file = st.file_uploader("GPX Datei hochladen", type='gpx')
        
            if uploaded_gpx_file is not None:
                # GPX Datei lesen
                gpx = gpxpy.parse(uploaded_gpx_file)

                # Datum, Distanz, Geschwindigkeit und Dauer
                total_distance, average_speed, total_duration = calculate_distance_and_speed(gpx)
                activity_date = gpx.tracks[0].segments[0].points[0].time.strftime("%d-%m-%Y")
                st.write(f"**Streckenanalyse**")
                st.write(f"Datum: {activity_date}")
                st.write(f"Distanz: {total_distance:.2f} km")
                st.write(f"Durchschnitsgeschwindigkeit: {average_speed:.2f} km/h")
                st.write(f"Gesamtdauer: {total_duration}")

                # Karte mit zusätzlichen Optionen plotten
                m = folium_plot(gpx, tiles="OpenStreetMap", color="blue", start_stop_colors=("green", "red"),
                                way_points_color="blue", minimap=True, coord_popup=False,
                                zoom=8)

                # Karte in Streamlit anzeigen
                st.subheader("Karte")
                st_folium(m, width=700, height=500)

            st.markdown("---")

            # TCX Datei hochladen
            uploaded_tcx_file = st.file_uploader('TCX Datei hochladen', type='tcx')

            if uploaded_tcx_file is not None:
                timestamps, heart_rates = parse_tcx(uploaded_tcx_file)
                minutes_since_start = calculate_minutes_since_start(timestamps)

                # Datum der Aktivität anzeigen
                activity_date = timestamps[0].strftime("%d-%m-%Y")
                st.write(f"Datum: {activity_date}")

                min_time = min(minutes_since_start)
                max_time = max(minutes_since_start)

                # Zeitbereich auswählen mit einem Slider
                start_time, end_time = st.slider('Wählen Sie den Zeitbereich:', min_value=min_time, max_value=max_time, value=(min_time, max_time))

                # Interaktive Herzfrequenz über Zeit anzeigen
                fig = plot_hr_over_time_interactive(minutes_since_start, heart_rates, start_time, end_time)
                st.plotly_chart(fig)

        elif selected_page == "Einstellungen":
            st.title("Einstellungen")
            st.write("Einstellungen ändern.")
            st.write("Benutzername ändern.")
            st.text_input("Neuer Benutzername")
            st.write("Passwort ändern.")
            st.text_input("Neues Passwort", type="password")
