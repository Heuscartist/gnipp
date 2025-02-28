import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    schools_df = pd.read_csv("./data/school_geolocations_with-connnectivity.csv")
    connectivity_df = pd.read_csv("./data/measurements.csv")
    return schools_df, connectivity_df