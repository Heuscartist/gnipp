# gNIPP - Geonetwork Infrastructure Planning and Procurement
## 💡 About

gNIPP is an AI-powered network infrastructure analysis tool designed to provide insights into network tower distribution, coverage, and signal strength. The platform allows users to visualize network tower data on an interactive map while summarizing key statistics for better decision-making. It leverages AI capabilities to analyze current network infrastructure and create strategies to develop underserved regions.

## 🔎 How it Works

gNIPP processes network tower data and uses geographical information about schools to analyze the wireless network infrastructure available to these regions.

- Curated Dataset for School geographical information and details regarding their network performance made available through Giga School Mapping Data
  
- Using OpenCellID API to fetch Network Tower Data around a specific bounding box of latitude and longitude
    
- Utilize OpenAI API to analyze the network performance and availablity.
    

## 💻 Usage

1. Create a virtual environment and install the dependencies using the requirements.txt file
2. Download the Dataset from [here](https://drive.google.com/drive/folders/1gliQCbbAX8s4cyq0gpQKvZjnMpbnEPiI) and paste them into **data** folder in the root directory
3. **Run the application**: Ensure all dependencies are installed, then execute the script.
    
    ```
    streamlit run app.py
    ```
    
4. **Select a country and school**: Use the sidebar dropdown to choose a school location.
5. **Update information**: Click the update button after selecting a school to refresh data. 
6. **View the network insights**:
    
    - The map displays network tower locations.
        
    - The summary section provides details about the network infrastructure.
        
    

## 🧰 Tech Stack

- **Frontend**: Streamlit for UI components and interactivity.
    
- **Backend**: Python for data fetching processing.
    
- **Data Processing**: Pandas and NumPy for handling and summarizing network data.

- **Gemini**: Utilize Network data to generate analysis and devise network planning strategies.
