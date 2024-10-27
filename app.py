import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.set_page_config(layout="wide")
    
    # Customize the sidebar
    markdown = """
    Team Puʻu Kukui HBDEO project for HACC 2024
    """
    
    st.sidebar.title("About")
    st.sidebar.info(markdown)
    logo = "https://i.imgur.com/UbOXYAU.png"
    st.sidebar.image(logo)
    
    # Customize page title
    st.title("Hawaii Digital Equity Dashboard")
    
    st.markdown(
        """
        This page displays a heatmap of broadband coverage in Hawaii. 
        It visualizes the percentage of broadband coverage across different cities, allowing users to easily identify areas with varying levels of access.
        """
    )
    
    st.header("Heatmap")

    # Load data
    data_file = "data/BroadBandCover_by_City.csv"
    data = pd.read_csv(data_file)
    
    # Drop rows where coordinates couldn't be found
    data.dropna(subset=['Latitude', 'Longitude'], inplace=True)

    # Create Leafmap map
    m = leafmap.Map(center=[20.5, -157.5], zoom=7)  # Center on Hawaii

    # Prepare data for heatmap
    data['BroadbandCoverage'] = data['BroadbandCoverage'].str.replace('%', '').astype(float)
    
    # Add heatmap layer
    m.add_heatmap(data=data,
                  latitude="Latitude",
                  longitude="Longitude",
                  value="BroadbandCoverage",
                  name="Heat map",
                  radius=15,
                  blur=10, 
                  max_val=100)

    # Add clickable markers for each city
    for _, row in data.iterrows():
        city = row["City"]
        coverage = row["BroadbandCoverage"]
        providers = row["Providers"]
        latitude = row["Latitude"]
        longitude = row["Longitude"]
    
        # Add a small point (marker) with a popup
        m.add_marker(location=[latitude, longitude],
                     popup=f"{city}<br>Coverage: {coverage}<br>Providers: {providers}",
                     icon=leafmap.MarkerIcon(color="blue", icon="info-sign", prefix="glyphicon"))

    m.to_streamlit(height=500)

if __name__ == "__main__":
    main()
