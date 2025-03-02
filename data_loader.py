import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

@st.cache_data
def load_data():
    try:
        schools_df = pd.read_csv("./data/school_geolocations_with-connnectivity.csv")
        connectivity_df = pd.read_csv("./data/measurements.csv")
        gppd_data = pd.read_csv("./data/gppd_data.csv")
    except:
        print("Data not found locally")
    try:
        url = "https://docs.google.com/spreadsheets/d/14Ui9DSqPahAxKadDjvuBHlzfERyHdQyfrZljixWIPl0/edit?usp=sharing"
        conn = st.connection("gsheets", type=GSheetsConnection) 
        data = conn.read(spreadsheet=url)  
        schools_df = pd.DataFrame(data)

        url = "https://docs.google.com/spreadsheets/d/1GpLMY2JHK3bA88IpZnoU-jtmd_ojIKnrh7UkDcJTwdQ/edit?usp=sharing"
        conn = st.connection("gsheets", type=GSheetsConnection) 
        data = conn.read(spreadsheet=url)  
        connectivity_df = pd.DataFrame(data)

        url = "https://docs.google.com/spreadsheets/d/1ZVTNq8nb_5WHq9x-zGCUI8FUNtAfhjqkzXKdvwrez48/edit?usp=sharing"
        conn = st.connection("gsheets", type=GSheetsConnection) 
        data = conn.read(spreadsheet=url)  
        gppd_data = pd.DataFrame(data)
    except:
        print("Cannot Fetch Data")
    return schools_df, connectivity_df, gppd_data
