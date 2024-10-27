import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import leafmap.foliumap as leafmap
from geopy.geocoders import Nominatim

# Cache the geocoding results for each city
@st.cache_data
def get_coordinates(city, state="Hawaii"):
    location = geolocator.geocode(f"{city}, {state}")
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def main():
    st.set_page_config(layout="wide")
    
    # Customize the sidebar
    markdown = """
    A Streamlit map template
    <https://github.com/opengeos/streamlit-map-template>
    """
    
    st.sidebar.title("About")
    st.sidebar.info(markdown)
    logo = "https://i.imgur.com/UbOXYAU.png"
    st.sidebar.image(logo)
    
    # Customize page title
    st.title("Digital Equity Dashboard")
    
    st.markdown(
        """
        This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/opengeos/streamlit-map-template).
        """
    )
    
    st.header("Instructions")
    
    markdown = """
    1. For the [GitHub repository](https://github.com/opengeos/streamlit-map-template) or [use it as a template](https://github.com/opengeos/streamlit-map-template/generate) for your own project.
    2. Customize the sidebar by changing the sidebar text and logo in each Python files.
    3. Find your favorite emoji from https://emojipedia.org.
    4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.
    
    """
    
    st.markdown(markdown)

    # Load data
    data_file = "data/BroadBandCover_by_City.csv"
    data = pd.read_csv(data_file)
    
    # Initialize geolocator
    geolocator = Nominatim(user_agent="hawaii_map_app")
    
    m = leafmap.Map(minimap_control=True)
    m.add_basemap("OpenTopoMap")
    m.to_streamlit(height=500)

if __name__ == "__main__":
    main()
