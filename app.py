import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import pandas as pd

# Import modularized functions
from data_loader import load_data
from network_data import fetch_network_towers, summarize_tower_data
from ai_expert import build_agentic_graph, stream_tool_responses, generate_ai_recommendation_gemini, ask_rag_llm

# Load data
schools_df, connectivity_df, gppd_data= load_data()
merged_df = pd.merge(schools_df, connectivity_df, on="school_id_giga", how="left")

# Sidebar Navigation
graph = build_agentic_graph()
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Internet Speed Heatmap", "Agentic Wikipedia Query & RAG Procurement Policies"])

if page == "Home":
    st.title("gNIPP - Geonetwork Infrastructure Planning and Procurement")
    
    # Sidebar for school selection
    st.sidebar.header("🏫 Select Location")
    countries = schools_df["country"].dropna().unique()
    selected_country = st.sidebar.selectbox("Select a country", countries)
    
    filtered_schools = schools_df[schools_df["country"] == selected_country]
    school_names = filtered_schools["school_name"].dropna().unique()
    selected_school = st.sidebar.selectbox("Choose a school", school_names)
    
    if st.sidebar.button("🔄 Update Information"):
        school_info = filtered_schools.query("school_name == @selected_school")
        school_info = pd.merge(school_info, connectivity_df, on="school_id_giga", how="left")
        
        if not school_info.empty:
            school_info = school_info.iloc[0]
            lat, lon = school_info["latitude"], school_info["longitude"]
            has_connectivity = school_info["connectivity"]
            connectivity_info = school_info[['download_speed', 'upload_speed', 'latency']]
            
            # Fetch network tower data
            tower_data = fetch_network_towers(lat, lon)
            summary = summarize_tower_data(tower_data)
            
            # Display map
            st.subheader("📍 School Location")
            m = folium.Map(location=[lat, lon], zoom_start=12)
            folium.Marker([lat, lon], popup=selected_school).add_to(m)
            folium_static(m)
            
            # Display tower summary
            st.subheader("📊 Network Tower Summary")
            st.markdown(f"<div style='background-color: rgba(50, 50, 50, 0.8); padding: 10px; border-radius: 10px; color: white;'>{summary}</div>", unsafe_allow_html=True)
            
            # AI Analysis and Recommendation
            st.subheader("📈 AI Analysis and Recommendation")
            ai_analysis = generate_ai_recommendation_gemini(selected_school, has_connectivity, connectivity_info, summary)
            st.markdown(f"<div style='background-color: rgba(50, 50, 50, 0.8); padding: 10px; border-radius: 10px; color: white;'>{ai_analysis}</div>", unsafe_allow_html=True)
        else:
            st.error("No data available for this school.")

elif page == "Internet Speed Heatmap":
    st.title("🌍 Internet Speed Heatmap")
    
    # Sidebar metric selection
    st.sidebar.header("📊 Select Heatmap Metric")
    metric = st.sidebar.selectbox("Metric:", ["download_speed", "upload_speed", "latency"])
    
    # Heatmap interpretation guide
    st.markdown("""
    **How to Interpret the Heatmap:**
    - **Red Areas:** Poor connectivity, slow speeds, or high latency.
    - **Yellow Areas:** Moderate connectivity and speeds.
    - **Green Areas:** Good connectivity and high speeds.
    
    Higher intensity indicates better performance for download/upload speeds but worse performance for latency.
    """)
    
    # Filter out missing values
    df_filtered = merged_df[merged_df[metric] > 0]
    
    # Create map
    m = folium.Map(location=[merged_df["latitude"].mean(), merged_df["longitude"].mean()], zoom_start=3)
    
    heat_data = df_filtered[['latitude', 'longitude', metric]].values.tolist()
    HeatMap(heat_data, radius=15).add_to(m)
    
    folium_static(m)

    
elif page == "Agentic Wikipedia Query & RAG Procurement Policies":
    st.title("📝 Agentic Wikipedia Query & RAG Procurement Policies")
    user_text = st.text_input("Search the Wiki: eg. Describe LTE Towers:")
    
    if st.button("Submit"):
        st.success("Fetching Response using Agent")
        agentic_response = stream_tool_responses(graph, user_text)
        st.markdown(f"<div style='background-color: rgba(50, 50, 50, 0.8); padding: 10px; border-radius: 10px; color: white;'>{agentic_response}</div>", unsafe_allow_html=True)
    
    rag_query = st.text_input("Procurement Policy Details:")
    if st.button("Query RAG LLM"):
        if rag_query:
            with st.spinner("Fetching answer from RAG model..."):
                rag_response = ask_rag_llm(rag_query)
            st.markdown(f"<div style='background-color: rgba(50, 50, 50, 0.8); padding: 10px; border-radius: 10px; color: white;'>{rag_response}</div>", unsafe_allow_html=True)
        else:
            st.error("Please enter a query for the RAG model.")