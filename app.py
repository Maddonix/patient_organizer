import streamlit as st
import pandas as pd
from classes import Organizer, Patient
from utils import attributes as attribute_list
import json

st.set_page_config(page_title="Organizer", layout="wide")


st.subheader("Patienten")

organizer = Organizer()
table_space = st.empty()
table_space.write(organizer.df)

# st.write(organizer.patients["DANIEL"].data)

with st.sidebar:

    new_patient = st.text_input("New Patient")
    if st.button("Add"):
        Patient(name = new_patient)
        organizer.patients, organizer.df = organizer.load_patients()
        table_space.write(organizer.df)

    patients_bar, attributes_bar = st.columns((1,1))
    with patients_bar:
        current_patient_space = st.empty()
        current_patient = current_patient_space.radio("Patients", organizer.patients.keys())

        if st.button("Delete Selected"):
            organizer.delete_patient(current_patient)
            organizer.patients, organizer.df = organizer.load_patients()
            table_space.write(organizer.df)
            current_patient = current_patient_space.radio("Patients", organizer.patients.keys())

    with attributes_bar:
        # st.radio("Select Attribute", attribute_list)
        # if st.button("Toggle")
        attribute_checkboxes = {
            attribute_name: st.checkbox(attribute_name, attribute_state)
            for attribute_name, attribute_state in organizer.get_patient_attribute_states(current_patient)
            }
        
        organizer.set_patient_attribute_states(current_patient, attribute_checkboxes)
        table_space.write(organizer.df)

    if st.button("Reset All"):
        organizer.reset()
        table_space.write(organizer.df)
