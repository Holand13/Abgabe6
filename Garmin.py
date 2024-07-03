
import streamlit as st
import gpxpy
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic

import xml.etree.ElementTree as ET
import plotly.graph_objects as go
from datetime import datetime, timedelta

def calculate_distance_and_speed(gpx):
    total_distance = 0.0 
    total_time = 0.0 

    for track in gpx.tracks:
        for segment in track.segments:
            segment_distance = 0.0
            segment_time = 0.0
            for i in range(1, len(segment.points)):
                point1 = segment.points[i - 1]
                point2 = segment.points[i]
                segment_distance += geodesic((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).km
                segment_time += (point2.time - point1.time).total_seconds()

            total_distance += segment_distance
            total_time += segment_time

    # In Stunden:Minuten:Sekunden umschreiben
    total_time_hours = total_time / 3600
    hours = int(total_time_hours)
    minutes = int((total_time_hours * 60) % 60)
    seconds = int(total_time_hours * 3600 % 60)

    average_speed = total_distance / total_time_hours if total_time_hours > 0 else 0.0  # in km/h

    return total_distance, average_speed, f"{hours:02}:{minutes:02}:{seconds:02}"

def folium_plot(gpx, tiles="OpenStreetMap", color="blue", start_stop_colors=("green", "red"),
                way_points_color="blue", minimap=True, coord_popup=False,
                zoom=8, file_path=None, open_in_browser=False):
    """
    Plot the GPX data on a Folium map.

    Args:
        gpx: Parsed GPX data.
        tiles (str): Map tiles.
        color (str): Line color for the route.
        start_stop_colors (tuple): Colors for the start and stop markers.
        way_points_color (str): Color for the waypoints.
        minimap (bool): Show a minimap.
        coord_popup (bool): Show a popup with coordinates when clicking on the map.
        title (str): Title of the map.
        zoom (int): Initial zoom level.
        file_path (str): Path to save the map as an HTML file.
        open_in_browser (bool): Open the map in a new browser tab.
    """
    start_coords = [gpx.tracks[0].segments[0].points[0].latitude, gpx.tracks[0].segments[0].points[0].longitude]
    m = folium.Map(location=start_coords, zoom_start=zoom, tiles=tiles)

    for track in gpx.tracks:
        for segment in track.segments:
            points = [(point.latitude, point.longitude) for point in segment.points]
            folium.PolyLine(points, color=color, weight=2.5, opacity=1).add_to(m)

            # Start und Stop markieren
            folium.Marker(points[0], icon=folium.Icon(color=start_stop_colors[0]), popup="Start").add_to(m)
            folium.Marker(points[-1], icon=folium.Icon(color=start_stop_colors[1]), popup="End").add_to(m)

    if minimap:
        minimap = folium.plugins.MiniMap(toggle_display=True)
        m.add_child(minimap)

    if coord_popup:
        m.add_child(folium.LatLngPopup())

    if file_path:
        m.save(file_path)

    if open_in_browser:
        import webbrowser
        webbrowser.open(file_path)

    return m

def parse_tcx(tcx_file):
    tree = ET.parse(tcx_file)
    root = tree.getroot()

    namespaces = {'tcx': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}
    trackpoints = root.findall('.//tcx:Trackpoint', namespaces)

    timestamps = []
    heart_rates = []

    for trackpoint in trackpoints:
        time_element = trackpoint.find('tcx:Time', namespaces)
        heart_rate_element = trackpoint.find('.//tcx:HeartRateBpm/tcx:Value', namespaces)

        if time_element is not None and heart_rate_element is not None:
            timestamp = datetime.strptime(time_element.text, '%Y-%m-%dT%H:%M:%S.%fZ')
            heart_rate = int(heart_rate_element.text)
            timestamps.append(timestamp)
            heart_rates.append(heart_rate)

    return timestamps, heart_rates

def calculate_minutes_since_start(timestamps):
    start_time = timestamps[0]
    minutes_since_start = [(timestamp - start_time).total_seconds() / 60 for timestamp in timestamps]
    return minutes_since_start

def filter_data_by_time_range(timestamps, heart_rates, start_time_minutes, end_time_minutes):
    start_time = timestamps[0] + timedelta(minutes=start_time_minutes)
    end_time = timestamps[0] + timedelta(minutes=end_time_minutes)

    filtered_timestamps = []
    filtered_heart_rates = []

    for ts, hr in zip(timestamps, heart_rates):
        if start_time <= ts <= end_time:
            filtered_timestamps.append(ts)
            filtered_heart_rates.append(hr)

    return filtered_timestamps, filtered_heart_rates

def plot_hr_over_time_interactive(minutes_since_start, heart_rates, start_time_minutes, end_time_minutes):
    filtered_minutes = []
    filtered_heart_rates = []

    for minute, hr in zip(minutes_since_start, heart_rates):
        if start_time_minutes <= minute <= end_time_minutes:
            filtered_minutes.append(minute)
            filtered_heart_rates.append(hr)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=filtered_minutes, y=filtered_heart_rates, mode='lines+markers', name='Heart Rate'))
    
    fig.update_layout(
        title='Herzfrequenz über die Zeit',
        xaxis_title='Zeit (Minuten)',
        yaxis_title='Herzfrequenz (bpm)',
    )

    return fig

def main():
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

if __name__ == "__main__":
    main()
