import json
import pandas as pd
import scipy.signal
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st


class EKGdata:
    # Class variable to hold all EKG data
    all_ekg_data = []

    def __init__(self, ekg_dict):
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['EKG in mV', 'Time in ms'])
        self.df['Time in s'] = self.df['Time in ms'] / 1000  # Konvertieren der Zeit von Millisekunden in Sekunden

    @staticmethod
    def find_ekg_data_by_id(ekg_id):
        """A Function that takes an ID and returns the EKG data as a dictionary"""
        for ekg_dict in EKGdata.all_ekg_data:
            if ekg_dict["id"] == ekg_id:
                return ekg_dict
        return None

    @classmethod
    def load_by_id(self, ekg_id_input):
        ekg_dict = self.find_ekg_data_by_id(ekg_id_input)
        if ekg_dict:
            return self(ekg_dict)
        else:
            return None

    def find_peaks(self, threshold, distance):
        series = self.df['EKG in mV']
        peaks, _ = scipy.signal.find_peaks(series, height=threshold, distance=distance)
        self.peaks = peaks
        return peaks

    def estimate_hr(self):
        if self.peaks is not None:
            num_peaks = len(self.peaks)
            duration = self.df['Time in ms'].iloc[-1] - self.df['Time in ms'].iloc[0]
            heart_rate = (num_peaks / duration) * 60000  # Convert to beats per minute
            print(f"Heart Rate: {heart_rate:.2f} bpm")
        else:
            print("No peaks found. Heart rate cannot be calculated.")
        self.heart_rate = heart_rate
        return heart_rate

    def plot_time_series(self):
        fig = go.Figure()

        # Add EKG time series data
        fig.add_trace(go.Scatter(x=self.df['Time in s'], y=self.df['EKG in mV'],  
                                 mode='lines', name='EKG in mV'))

        # Add peaks
        if self.peaks is not None:
            fig.add_trace(go.Scatter(x=self.df['Time in s'].iloc[self.peaks],  
                                     y=self.df['EKG in mV'].iloc[self.peaks],
                                     mode='markers', name='Peaks',
                                     marker=dict(color='red', size=10, symbol='x')))

        fig.update_layout(title='EKG Time Series with Peaks',
                          xaxis_title='Time in s',  
                          yaxis_title='EKG in mV')

        return fig

    def display_test_date_and_plot(self):
        st.plotly_chart(self.plot_time_series())  
        st.write(f"Test Datum: {self.date}")  # Anzeigen des Testdatums
         


'''
    def display(self):
        print(f"ID: {self.id}")
        print(f"Date: {self.date}")
        print(f"Data File: {self.data}")
        print(f"EKG Data (first 5 rows):\n{self.df.head()}")
'''
    
'''
if __name__ == "__main__":
    print("Welcome to the EKG Data Analysis Tool!")
    

    # Load person data and populate all_ekg_data class variable
    with open("data/person_db.json") as file:
        person_data = json.load(file)
    
    for person in person_data:
        EKGdata.all_ekg_data.extend(person["ekg_tests"])

   
    try:
        ekg_id_input = int(input("Bitte geben Sie die ID der Person ein: "))
        ekg_by_id = EKGdata.load_by_id(ekg_id_input)
        if ekg_by_id:
            print("EKG Data loaded by ID:")
            ekg_by_id.display()
            ekg_by_id.find_peaks(threshold=320,distance=150)  
            ekg_by_id.estimate_hr()
            ekg_by_id.plot_time_series()
        else:
            print("Keine EKG-Daten mit der gegebenen ID gefunden.")
    except ValueError:
        print("Bitte geben Sie eine gültige numerische ID ein.")
'''