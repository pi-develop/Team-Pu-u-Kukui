import streamlit as st
import streamlit.components.v1 as components

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Open Data")

    components.iframe("https://opendata.hawaii.gov/organization/hbdeo", height=500)

if __name__ == "__main__":
    main()
