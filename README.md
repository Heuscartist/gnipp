# gNIPP - Geonetwork Infrastructure Planning and Procurement
## 💡 About

gNIPP is an AI-powered network infrastructure analysis tool designed to provide insights into network tower distribution, coverage, and signal strength. The platform allows users to visualize network tower data on an interactive map while summarizing key statistics for better decision-making. It leverages AI capabilities to analyze current network infrastructure and create strategies to develop underserved regions. It utilizes RAG and Agentic AI capbabilities to provide reliable data regarding definitions of different keywords and procurement policies.

## 🔎 How it Works

gNIPP processes network tower data and uses geographical information about schools to analyze the wireless network infrastructure available to these regions.

- Curated Dataset for School geographical information and details regarding their network performance made available through Giga School Mapping Data
  
- Using OpenCellID API to fetch Network Tower Data around a specific bounding box of latitude and longitude
    
- Utilize Gemini API to analyze the network performance and availablity

- Provide Heatmap of underserved reagions based on key network performance metrics allowing users to quickly identify key regions of interest

- Use AI Agent to access wikipedia allowing users to get access to correct information regarding keywords and jargon

- Use RAG to access gppd data and extract procurement information of various countries.
    

## 💻 Usage

1. Create a virtual environment and install the dependencies using the requirements.txt file
2. Download the Dataset from [here](https://drive.google.com/drive/folders/1gliQCbbAX8s4cyq0gpQKvZjnMpbnEPiI) and paste them into **data** folder in the root directory
3. If Rag DB not created yet first download the data from [here](https://drive.google.com/file/d/1l13gzPOywjLYtO1XQek-EZcB9Awy2Teq/view?usp=sharing) and place in data directory. Then run`
    ```
    python create_rag_db.py file
    ```
5. **Run the application**: Ensure all dependencies are installed, then execute the script.
    
    ```
    streamlit run app.py
    ```
    
6. **Select a country and school**: Use the sidebar dropdown to choose a school location.
7. **Update information**: Click the update button after selecting a school to refresh data. 
8. **View the network insights**:
    
    - The map displays network tower locations.
        
    - The summary section provides details about the network infrastructure.
9. **Visualize Metrics**: Using the heatmap page allowing quick and easy visualization of key metrics
10. **Understand Keywords**: By utilizing agentic AI and fetching information from wikipedia
11. **Query Procurement Policies**: Using RAG to get access to the GDDP Data and procurement policies of country of interest by querying using natural language
    

## 🧰 Tech Stack

- **Frontend**: Streamlit for UI components and interactivity.
    
- **Backend**: Python for data fetching processing.
    
- **Data Processing**: Pandas and NumPy for handling and summarizing network data.

- **Gemini**: LLM used for this project.
  
- **Langchain**: Creating AI Agents and RAG implementation.
