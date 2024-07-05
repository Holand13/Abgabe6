# EKG Data Analysis Tool

Diese APP implementiert ein EKG-Datenanalysetool in Python, das mithilfe von Streamlit als Benutzeroberfläche entwickelt wurde.

## Funktionalitäten
- **Personenauswahl und EKG Auswertung**
  - Ermöglicht die Visualisierung von personenbezogenen EKGs
  - Möglichkeit neue Personendaten anzulegen und zu bearbeiten
- **Routen- und Herzfrequenzvisualisierung (GPX und TCX)**
  - Ermöglicht das Hochladen und Analysieren von GPX- und TCX-Dateien für Aktivitätsdaten.
  - Zeigt Distanz, Geschwindigkeit und interaktive Herzfrequenzplots über die Zeit an.

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

Verwenden Sie die Seitenleiste, um zwischen den verschiedenen Funktionen der APP zu navigieren (Personen, Neue Person anlegen, GPX und TCX Datenanalyse, Einstellungen).

3. Personen verwalten

Auf der "Personen"-Seite können Sie Informationen zu Personen anzeigen, bearbeiten und EKG-Tests analysieren.
Wählen Sie eine Person und einen EKG-Test aus, um Details wie die Herzfrequenz und die Zeitreihe der EKG-Daten anzuzeigen. Außerdem besteht die Möglichkeit die Person zu löschen.

4. Neu Person anlegen

Auf dieser Seite können neue Personendaten angelegt werden.

5. GPX und TCX Datenanalyse

Laden Sie GPX- und TCX-Dateien hoch, um Aktivitätsdaten zu analysieren und Karten sowie interaktive Herzfrequenzplots anzuzeigen.

