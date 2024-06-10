'''
import ezgpx

# Parse GPX file
gpx = ezgpx.GPX("Activity.gpx")

# Plot with Folium
gpx.folium_plot(tiles="OpenStreetMap",
                color="orange",
                start_stop_colors=("green", "red"),
                way_points_color="blue",
                minimap=True,
                coord_popup=False,
                title="Innsbruck-Runde",
                zoom=8,
                file_path="Map.Activity.html",
                open=True)

'''
'''

from xml.dom import minidom
from datetime import *

xmldoc = minidom.parse("Activity.tcx")
print(xmldoc)


tcd = xmldoc.getElementsByTagName("TrainingCenterDatabase")[0]

activitiesElement = tcd.getElementsByTagName("Activities")[0]

activities = activitiesElement.getElementsByTagName("Activity")

for activity in activities:
    sport = activity.attributes["Sport"]
    sportName = sport.value

    idElement = activity.getElementsByTagName("Id")[0]
    timeOfDay = idElement.firstChild.data
    year = int(timeOfDay[0:4])
    month = int(timeOfDay[5:7])
    day = int(timeOfDay[8:10])
    date = datetime(year,month,day)
    #print(sportName, month, day, year)
    print(sportName, date)


trackPoints = tcd.getElementsByTagName("Time")
heartRate = tcd.getElementsByTagName("Value")


print(type(trackPoints))
print(type(heartRate))

i=0

while i <= 10:
    print(trackPoints[i], heartRate[i])
    i += 1

'''
'''
from xml.dom import minidom
from datetime import datetime
import matplotlib.pyplot as plt

# Parse TCX file
xmldoc = minidom.parse("Activity.tcx")

# Extract TrainingCenterDatabase
tcd = xmldoc.getElementsByTagName("TrainingCenterDatabase")[0]

# Extract Activities
activitiesElement = tcd.getElementsByTagName("Activities")[0]
activities = activitiesElement.getElementsByTagName("Activity")

# Lists to store data
timestamps = []
heart_rates = []

# Loop through each activity
for activity in activities:
    sport = activity.attributes["Sport"].value

    idElement = activity.getElementsByTagName("Id")[0]
    timeOfDay = idElement.firstChild.data
    year = int(timeOfDay[0:4])
    month = int(timeOfDay[5:7])
    day = int(timeOfDay[8:10])
    date = datetime(year, month, day)

    # Extract TrackPoints and HeartRate values
    trackpoints = activity.getElementsByTagName("Trackpoint")
    for trackpoint in trackpoints:
        timeElement = trackpoint.getElementsByTagName("Time")[0]
        time = timeElement.firstChild.data
        timestamp = datetime.fromisoformat(time.replace("Z", ""))

        # Ensure all timestamps are datetime objects
        if isinstance(timestamp, datetime):
            timestamps.append(timestamp)

        hr_elements = trackpoint.getElementsByTagName("HeartRateBpm")
        if hr_elements:
            hr_value = hr_elements[0].getElementsByTagName("Value")[0].firstChild.data
            heart_rates.append(int(hr_value))
        else:
            heart_rates.append(None)

# Print extracted data for verification
print(timestamps[:5], heart_rates[:5])

# Plotting the data
plt.figure(figsize=(10, 6))
# Convert timestamps to minutes
timestamps_minutes = [(t - timestamps[0]).total_seconds() / 60 for t in timestamps]
plt.plot(timestamps_minutes, heart_rates, color='orange', linestyle='-', marker='o', markersize=2)

# Formatting the plot
plt.title("Heart Rate Over Time")
plt.xlabel("Time (minutes)")
plt.ylabel("Heart Rate (bpm)")
plt.grid(True)
plt.ylim(0)  # Set y-axis minimum to 0 bpm
plt.tight_layout()

# Display the plot
plt.show()
'''
'''
import matplotlib.pyplot as plt
from xml.dom import minidom
from datetime import datetime
import scipy.signal
import plotly.graph_objs as go
import streamlit as st


class TCXData:
    def __init__(self, tcx_file):
        self.tcx_file = tcx_file
        self.timestamps = []
        self.heart_rates = []
        self.load_data()

    def load_data(self):
        xmldoc = minidom.parse(self.tcx_file)
        tcd = xmldoc.getElementsByTagName("TrainingCenterDatabase")[0]
        activitiesElement = tcd.getElementsByTagName("Activities")[0]
        activities = activitiesElement.getElementsByTagName("Activity")

        for activity in activities:
            trackpoints = activity.getElementsByTagName("Trackpoint")
            for trackpoint in trackpoints:
                timeElement = trackpoint.getElementsByTagName("Time")[0]
                time = timeElement.firstChild.data
                timestamp = datetime.fromisoformat(time.replace("Z", ""))
                self.timestamps.append(timestamp)

                hr_elements = trackpoint.getElementsByTagName("HeartRateBpm")
                if hr_elements:
                    hr_value = hr_elements[0].getElementsByTagName("Value")[0].firstChild.data
                    self.heart_rates.append(int(hr_value))
                else:
                    self.heart_rates.append(None)

    def find_peaks(self, threshold, distance):
        serie = self.heart_rates
        peaks, _ = scipy.signal.find_peaks(serie, height=threshold, distance=distance)
        return peaks

    def estimate_hr(self):
        peaks = self.find_peaks(threshold=100, distance=100)
        num_peaks = len(peaks)
        duration = (self.timestamps[-1] - self.timestamps[0]).total_seconds()
        herzfrequenz = (num_peaks / duration) * 60  # Umrechnen in Schläge pro Minute
        return herzfrequenz

    def plot_time_series(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.timestamps, y=self.heart_rates, mode='lines', name='Herzfrequenz'))
        fig.update_layout(title='Herzfrequenz über die Zeit', xaxis_title='Zeit', yaxis_title='Herzfrequenz (bpm)')
        return fig


# Streamlit-Anwendung
def main():
    st.title("Herzfrequenzanalyse aus TCX-Datei")

    tcx_file = st.file_uploader("Wählen Sie eine TCX-Datei:", type=["tcx"])
    if tcx_file is not None:
        tcx_data = TCXData(tcx_file)

        # Berechne Herzfrequenz
        herzfrequenz = tcx_data.estimate_hr()

        # Plot
        st.plotly_chart(tcx_data.plot_time_series())

        # Anzeige der Herzfrequenz
        st.write(f"Geschätzte Herzfrequenz: {herzfrequenz:.2f} bpm")


if __name__ == "__main__":
    main()

'''
import matplotlib.pyplot as plt
from xml.dom import minidom
from datetime import datetime
import plotly.graph_objs as go
import plotly.io as pio

# Parse TCX file
xmldoc = minidom.parse("Activity.tcx")

# Extract TrainingCenterDatabase
tcd = xmldoc.getElementsByTagName("TrainingCenterDatabase")[0]

# Extract Activities
activitiesElement = tcd.getElementsByTagName("Activities")[0]
activities = activitiesElement.getElementsByTagName("Activity")

# Lists to store data
timestamps = []
heart_rates = []

# Loop through each activity
for activity in activities:
    sport = activity.attributes["Sport"].value

    idElement = activity.getElementsByTagName("Id")[0]
    timeOfDay = idElement.firstChild.data
    year = int(timeOfDay[0:4])
    month = int(timeOfDay[5:7])
    day = int(timeOfDay[8:10])
    date = datetime(year, month, day)

    # Extract TrackPoints and HeartRate values
    trackpoints = activity.getElementsByTagName("Trackpoint")
    for trackpoint in trackpoints:
        timeElement = trackpoint.getElementsByTagName("Time")[0]
        time = timeElement.firstChild.data
        timestamp = datetime.fromisoformat(time.replace("Z", ""))

        # Ensure all timestamps are datetime objects
        if isinstance(timestamp, datetime):
            timestamps.append(timestamp)

        hr_elements = trackpoint.getElementsByTagName("HeartRateBpm")
        if hr_elements:
            hr_value = hr_elements[0].getElementsByTagName("Value")[0].firstChild.data
            heart_rates.append(int(hr_value))
        else:
            heart_rates.append(None)

# Convert timestamps to minutes
timestamps_minutes = [(t - timestamps[0]).total_seconds() / 60 for t in timestamps]

# Plotting the data with Matplotlib
plt.figure(figsize=(10, 6))
plt.plot(timestamps_minutes, heart_rates, color='blue', linestyle='-', marker='o', markersize=2)
plt.title("Heart Rate Over Time")
plt.xlabel("Time (minutes)")
plt.ylabel("Heart Rate (bpm)")
plt.grid(True)
plt.tight_layout()

# Display the plot
plt.show()

# Convert the plot to an interactive Plotly plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=timestamps_minutes, y=heart_rates, mode='markers', marker=dict(color='blue')))
fig.update_layout(title="Heart Rate Over Time (Plotly)",
                  xaxis_title="Time (minutes)",
                  yaxis_title="Heart Rate (bpm)",
                  hovermode="closest")
pio.show(fig)
