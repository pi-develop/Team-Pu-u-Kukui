import streamlit as st
import pandas as pd

from streamlit_extras.dataframe_explorer import dataframe_explorer

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Device Access")

    df = pd.read_excel("data/acs2022_5yr_counties_hi.xlsx")

    filtered_df = dataframe_explorer(df, case=False)
    st.dataframe(filtered_df, use_container_width=True)
    
if __name__ == "__main__":
    main()
