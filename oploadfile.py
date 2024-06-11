import os
import streamlit as st
from PIL import Image
import io

def save_uploaded_file(uploaded_file, directory="data\pictures"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    
    return file_path

def upload():
    uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)

        if uploaded_file.type == "image/jpeg":
            file_path = save_uploaded_file(uploaded_file)
            st.write("Bild wurde erfolgreich hochgeladen")
        else:
            image = Image.open(io.BytesIO(uploaded_file.read()))
            file_path = os.path.join("data/pictures", uploaded_file.name.split('.')[0] + ".jpg")
            image.save(file_path, "JPEG")
            st.write("Bild wurde erfolgreich gespeichert")
        
        return file_path
    return None


