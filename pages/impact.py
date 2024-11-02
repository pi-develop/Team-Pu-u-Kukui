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
    
    # Create new columns for latitude and longitude if they don’t exist
    if 'Latitude' not in df.columns:
        df['Latitude'] = None
    if 'Longitude' not in df.columns:
        df['Longitude'] = None

    # Counter to limit the number of geocoding attempts
    max_attempts = 5
    attempt_count = 0    
    
    # Geocode each address
    for index, row in df.iterrows():
        # Stop if max geocoding attempts have been reached
        if attempt_count >= max_attempts:
            st.write("Reached maximum geocoding attempts. Stopping geocoding.")
            break
        
        if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
            continue  # Skip if coordinates already exist
        
        try:
            # location = geocode(row['Street Address'])
            attempt_count += 1  # Increment attempt count regardless of success

            # if location:
            #    df.at[index, 'Latitude'] = location.latitude
            #    df.at[index, 'Longitude'] = location.longitude
        except Exception as e:
            st.error(f"Error geocoding address at index {index}: {e}")

    filtered_df = dataframe_explorer(df, case=False)
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()
