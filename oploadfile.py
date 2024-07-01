import os
import streamlit as st
from PIL import Image
import io

def save_uploaded_file(uploaded_file, directory="data\pictures"): #Das hochgeladene Bild wird gespeichert
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, uploaded_file.name) #Der Pfad wird erstellt
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    
    return file_path

def upload():
    uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"]) #Bild hochladen

    if uploaded_file is not None:     #Wenn ein Bild hochgeladen wird
        if st.button("Überprüfen"):
            image = Image.open(io.BytesIO(uploaded_file.read()))
            st.image(image, caption = "Hochgeladenes Profilbild", use_column_width=True) #Das hochgeladene Bild wird angezeigt

        if uploaded_file.type == "image/jpeg": 
            file_path = save_uploaded_file(uploaded_file)
            st.write("Bild wurde erfolgreich hochgeladen")
        else:
            image = Image.open(io.BytesIO(uploaded_file.read())) #Das Bild wird geöffnet
            st.image(image, caption = "Hochgeladenes Profilbild", use_column_width=True)
            file_path = os.path.join("data/pictures", uploaded_file.name.split('.')[0] + ".jpg") #Der Pfad wird erstellt
            image.save(file_path, "JPEG")
            st.write("Bild wurde erfolgreich gespeichert")
       

        return file_path
    return None


