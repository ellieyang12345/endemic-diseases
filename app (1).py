import streamlit as st
import pandas as pd

# Assuming the functions collect_patient_data, collect_symptom_data,
# collect_contact_history, and calculate_risk_level are defined in the environment

def calculate_risk_level(symptom_binary_data, contact_history_binary_data):
    """Calculates the risk level based on binary symptom and contact history data."""
    all_binary_data = list(symptom_binary_data.values()) + [contact_history_binary_data]
    total_yes_count = sum(all_binary_data)
    total_questions = len(all_binary_data)
    frequency = total_yes_count / total_questions if total_questions > 0 else 0

    if frequency < 0.33:
        risk_level = "Low Risk"
    elif frequency < 0.66:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    return risk_level, frequency


st.set_page_config(layout="wide") # Use wide layout for better appearance

st.title("Pediatric Patient Susceptibility Assessment")

st.header("Patient Information")
col1, col2 = st.columns(2) # Use columns to organize input fields
with col1:
    patient_name = st.text_input("Enter patient's name:")
    patient_region = st.text_input("Enter patient's region:")
with col2:
    patient_age = st.number_input("Enter patient's age:", min_value=0, max_value=18, step=1)
    patient_temperature = st.number_input("Enter patient's temperature:", format="%0.2f")


st.header("Symptom Data")
symptoms_list = [
    "coughing", "chest pain", "breathing problems", "papule appearance",
    "skin pain", "diarrhea", "abdominal pain", "conjunctival congestion",
    "burning eyes", "itchy eyes", "eye secretions", "blisters/ulcers in hand/foot/mouth"
]
symptoms_input = {}
# Use columns for symptoms as well
num_cols = 3
cols = st.columns(num_cols)
for i, symptom in enumerate(symptoms_list):
    with cols[i % num_cols]:
        symptoms_input[symptom] = st.radio(f"{symptom.replace('_', ' ').capitalize()} (yes/no):", ('no', 'yes'), index=None) # Set index to None for no default selection

st.header("Contact History")
contact_history_input = st.radio("Contact/consumption of infected/sick/dead animals/remains (yes/no):", ('no', 'yes'), index=None) # Set index to None for no default selection

# Convert 'yes'/'no' to 1/0
symptom_binary_streamlit = {symptom: 1 if response == 'yes' else 0 for symptom, response in symptoms_input.items() if response is not None} # Filter out None values
contact_history_binary_streamlit = 1 if contact_history_input == 'yes' else 0

if st.button("Assess Risk"):
    # Assuming calculate_risk_level function is available
    risk_level, frequency = calculate_risk_level(symptom_binary_streamlit, contact_history_binary_streamlit)

    st.subheader("Assessment Results")
    st.write(f"Patient Name: {patient_name}")
    st.write(f"Patient Age: {patient_age}")
    st.write(f"Patient Region: {patient_region}")
    st.write(f"Patient Temperature: {patient_temperature}")
    st.write(f"Frequency of 'yes' responses: {frequency:.2f}")
    st.write(f"Calculated Risk Level: {risk_level}")

    # Add descriptions based on risk level
    if risk_level == "Low Risk":
        st.success("Low Risk indicates a low risk of being infected by endemic diseases.")
    elif risk_level == "Medium Risk":
        st.warning("Medium Risk indicates that you are moderately susceptible to being infected by endemic diseases. Please notify a healthcare professional if more symptoms start presenting themselves.")
    else:
        st.error("High Risk indicates a high risk of being infected by endemic diseases. If not already, please inform a healthcare professional in your local area.")

    st.write("Thank you for using the Pediatric Patient Susceptibility Assessment tool.")
