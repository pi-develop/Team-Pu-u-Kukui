import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from streamlit_extras.dataframe_explorer import dataframe_explorer

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Initiatives Impact")

    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="geoapiExercises")
    
    # Set up rate limiter to avoid overloading the API
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    # Load CSV file into a DataFrame
    input_csv = 'data/entities.csv'  # Path to your CSV file
    df = pd.read_csv(input_csv)
    
    # Ensure there is a 'Street Address' column in your CSV
    if 'Street Address' not in df.columns:
        raise ValueError("The CSV file must have a 'Street Address' column")
    
    # Create new columns for latitude and longitude
    df['Latitude'] = None
    df['Longitude'] = None

    filtered_df = dataframe_explorer(df, case=False)
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
