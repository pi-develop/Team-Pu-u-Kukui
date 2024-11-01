import streamlit as st
import pandas as pd

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Device Access")

    df = pd.read_excel("data/acs2022_5yr_counties_hi.xlsx")

    
if __name__ == "__main__":
    main()
