import streamlit as st
import pandas as pd

from streamlit_extras.add_vertical_space import add_vertical_space

from style_helper import apply_custom_style

@st.cache_data
def fetch_usage_data():
    conn = st.connection('mysql', type='sql')
    df = conn.query('SELECT Use_pc_internet, County, Estimate, Estimate_Perccent, Margin_Error, Margin_Error_Percent FROM use_pc_internet_by_county', ttl=6)
    return df

def main():
    apply_custom_style()
            
    st.header("Device Access")

    df = fetch_usage_data()

    # Filter out rows where County is 'Total households'
    filtered_data = df[df['Use_pc_internet'] != 'Total households']

    st.dataframe(filtered_data, use_container_width=True)
    
if __name__ == "__main__":
    main()
