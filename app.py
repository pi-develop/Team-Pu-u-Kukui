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

    regions = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson"
    m.add_geojson(regions, layer_name="US Regions")
    m.add_points_from_xy(
        data,
        x="Latitude",
        y="Longitude",
        color_column="County",
        spin=False,
        add_legend=False,
    )

    # Add heatmap layer
    m.add_heatmap(data=data,
                  latitude="Latitude",
                  longitude="Longitude",
                  value="BroadbandCoverage",
                  name="Heat map",
                  radius=15,
                  blur=10, 
                  max_val=100)
    
    m.to_streamlit(height=500)

if __name__ == "__main__":
    main()
