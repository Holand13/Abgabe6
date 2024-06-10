import json
import pandas as pd
import scipy.signal
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st


class EKGdata:
    # Klassenvariable zur Speicherung aller EKG-Daten
    all_ekg_daten = []

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
        self.df['Time in s'] = self.df['Time in ms'] / 1000  # Konvertieren der Zeit von Millisekunden in Sekunden
        self.peaks = None
        self.herzfrequenz = None

    @staticmethod
    def find_ekg_data_by_id(ekg_id):
        """Eine Funktion, die eine ID nimmt und die EKG-Daten als Dictionary zurückgibt"""
        for ekg_dict in EKGdata.all_ekg_daten:
            if ekg_dict["id"] == ekg_id:
                return ekg_dict
        return None

    @classmethod
    def load_by_id(cls, ekg_id_input):
        ekg_dict = cls.find_ekg_data_by_id(ekg_id_input)
        if ekg_dict:
            return cls(ekg_dict)
        else:
            return None

    def find_peaks(self, threshold, distance):
        #Peaks finden
        serie = self.df['EKG in mV']
        peaks, _ = scipy.signal.find_peaks(serie, height=threshold, distance=distance)
        self.peaks = peaks
        return peaks

    def estimate_hr(self):
        if self.peaks is not None:
            num_peaks = len(self.peaks)
            duration = self.df['Time in ms'].iloc[-1] - self.df['Time in ms'].iloc[0]
            herzfrequenz = (num_peaks / duration) * 60000  # Umrechnen in Schläge pro Minute
            print(f"Heart Rate: {herzfrequenz:.2f} bpm")
        else:
            print("Keine Peaks gefunden. Herzfrequenz kann nicht berechnet werden.")
        self.herzfrequenz = herzfrequenz
        return herzfrequenz

    def plot_time_series(self, startzeit=None, endzeit=None):
        fig = go.Figure()

        # Daten basierend auf dem ausgewählten Zeitbereich filtern
        if startzeit is not None and endzeit is not None:
            df_gefiltert = self.df[(self.df['Time in s'] >= startzeit) & (self.df['Time in s'] <= endzeit)]
        else:
            df_gefiltert = self.df

        # EKG-Zeitreihendaten hinzufügen
        fig.add_trace(go.Scatter(x=df_gefiltert['Time in s'], y=df_gefiltert['EKG in mV'],  
                                 mode='lines', name='EKG in mV'))

        # Peaks hinzufügen
        if self.peaks is not None:
            gefilterte_peaks = [peak for peak in self.peaks if startzeit <= self.df['Time in s'].iloc[peak] <= endzeit]
            fig.add_trace(go.Scatter(x=self.df['Time in s'].iloc[gefilterte_peaks],  
                                     y=self.df['EKG in mV'].iloc[gefilterte_peaks],
                                     mode='markers', name='Peaks',
                                     marker=dict(color='red', size=10, symbol='x')))

        fig.update_layout(title='EKG Zeitreihe with Peaks',
                          xaxis_title='Time in s',  
                          yaxis_title='EKG in mV')

        return fig

    def display_test_date_and_plot(self):
        # Schieberegler zur Auswahl des Zeitbereichs
        min_zeit = float(self.df['Time in s'].min())
        max_zeit = float(self.df['Time in s'].max())
        startzeit, endzeit = st.slider('Wählen Sie den Zeitbereich:', min_value=min_zeit, max_value=max_zeit,
                                       value=(min_zeit, max_zeit), step=0.1)

        st.plotly_chart(self.plot_time_series(startzeit, endzeit))  
        st.write(f"Testdatum: {self.date}")  # Anzeigen des Testdatums