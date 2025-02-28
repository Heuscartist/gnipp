import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

# Import modularized functions
from data_loader import load_data
from network_data import fetch_network_towers, summarize_tower_data
from ai_expert import generate_ai_recommendation_gemini

st.title("gNIPP - Geonetwork Infrastructure Planning and Procurement")

# Load data
schools_df, connectivity_df = load_data()

# Sidebar for school selection with country filtering
st.sidebar.header("🏫 Select Location")

# Get unique country names
countries = schools_df["country"].dropna().unique()
selected_country = st.sidebar.selectbox("Select a country", countries)

# Filter schools based on selected country
filtered_schools = schools_df[schools_df["country"] == selected_country]
school_names = filtered_schools["school_name"].dropna().unique()

selected_school = st.sidebar.selectbox("Choose a school", school_names)

# Button to update information
if st.sidebar.button("🔄 Update Information"):
    school_info = filtered_schools.query("school_name == @selected_school")
    school_info = pd.merge(school_info, connectivity_df, on="school_id_giga", how="left")

    if not school_info.empty:
        school_info = school_info.iloc[0]  # Extract first matching row
        lat, lon = school_info["latitude"], school_info["longitude"]
        has_connectivity = school_info["connectivity"]
        connectivity_info = school_info[['download_speed', 'upload_speed', 'latency']]

        # Fetch network tower data
        tower_data = fetch_network_towers(lat, lon)
        summary = summarize_tower_data(tower_data)

        # First row: Map
        st.subheader("📍 School Location")
        m = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup=selected_school).add_to(m)
        folium_static(m)

        # Second row: Summary
        st.subheader("📊 Network Tower Summary")
        st.markdown(
            f"<div style='background-color: rgba(50, 50, 50, 0.8); padding: 10px; border-radius: 10px; color: white;'>"
            f"{summary}"
            f"</div>",
            unsafe_allow_html=True,
        )

        st.subheader("📈 AI Analysis and Recommendation")
        ai_analysis = generate_ai_recommendation_gemini(selected_school, has_connectivity, connectivity_info, summary)
        st.markdown(
            f"<div style='background-color: rgba(50, 50, 50, 0.8); padding: 10px; border-radius: 10px; color: white;'>"
            f"{ai_analysis}"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.error("No data available for this school.")
