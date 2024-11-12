import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

from streamlit_extras.add_vertical_space import add_vertical_space
from pygwalker.api.streamlit import StreamlitRenderer

from style_helper import apply_custom_style

@st.cache_data
def fetch_broadband_data():
    conn = st.connection('mysql', type='sql')
    df = conn.query('SELECT City, County, Providers, BroadbandCoverage, Latitude, Longitude FROM broadbcover_by_city', ttl=6)
    return df

def main():
    apply_custom_style()
            
    st.header("Broadband Connectivity Heatmap")
    
    # Drop rows where coordinates couldn't be found
    data = fetch_broadband_data()
    data.dropna(subset=['Latitude', 'Longitude'], inplace=True)

    # Create Leafmap map
    m = leafmap.Map(center=[20.5, -157.5], zoom=7)  # Center on Hawaii

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

    add_vertical_space(2)

    renderer = StreamlitRenderer(data, spec="./gw_config.json")
    renderer.explorer()

if __name__ == "__main__":
    main()
