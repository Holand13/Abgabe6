`python -m venv .venv`
`.venv\Scripts\Activate`
`pip install streamlit`
`pip freeze > requirements.txt`
`streamlit run main.py`

# EKG Data Analysis Tool

Diese APP implementiert ein EKG-Datenanalysetool in Python, das mithilfe von Streamlit als Benutzeroberfläche entwickelt wurde.

## Funktionalitäten
- **Personenauswahl und EKG Auswertung**
  - Ermöglicht die Visualisierung von personenbezogenen EKGs
  - Möglichkeit neue Personendaten anzulegen und zu bearbeiten
- **Routen- und Herzfrequenzvisualisierung (GPX und TCX)**
  - Ermöglicht das Hochladen und Analysieren von GPX- und TCX-Dateien für Aktivitätsdaten.
  - Zeigt Distanz, Geschwindigkeit und interaktive Herzfrequenzplots über Zeit an.

## Setup

1. Erstellen Sie eine virtuelle Umgebung:
    ```sh
    python -m venv .venv
    ```

2. Aktivieren Sie die virtuelle Umgebung:
    ```sh
    .venv\Scripts\Activate
    ```

3. Installieren Sie die benötigten Bibliotheken, wie zum Beispiel:
    ```sh
    pip install streamlit
    ```

4. Speichern Sie die installierten Bibliotheken in einer `requirements.txt` Datei:
    ```sh
    pip freeze > requirements.txt
    ```

5. Starten Sie die Streamlit-App:
    ```sh
    streamlit run main.py
    ```

## Benutzung
1. Anmelden

Geben Sie den Benutzernamen "Nutzername" und das Passwort "1234" ein, um sich anzumelden.

2. Navigation

Verwenden Sie die Seitenleiste, um zwischen den verschiedenen Funktionen der Anwendung zu navigieren (Personen, Neue Person anlegen, GPX und TCX Datenanalyse, Einstellungen).

3. Personen verwalten

Auf der "Personen"-Seite können Sie Informationen zu Personen anzeigen, bearbeiten und neue Personen hinzufügen.
EKG-Tests analysieren
Wählen Sie eine Person und einen EKG-Test aus, um Details wie die Herzfrequenz und die Zeitreihe der EKG-Daten anzuzeigen.

4. GPX und TCX Daten analysieren

Laden Sie GPX- und TCX-Dateien hoch, um Aktivitätsdaten zu analysieren und Karten sowie interaktive Herzfrequenzplots anzuzeigen.

5. Einstellungen

Ändern Sie Benutzername und Passwort in den Einstellungen der Anwendung.