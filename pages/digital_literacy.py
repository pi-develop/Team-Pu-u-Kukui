import streamlit as st

import pandas as pd

from streamlit_extras.add_vertical_space import add_vertical_space

from style_helper import apply_custom_style

@st.cache_data
def fetch_readiness_data():
    conn = st.connection('mysql', type='sql')
    df = conn.query('SELECT Dimension, Details, Unprepared, Old_Guard, Social_Users, Technical, Digital FROM readiness_by_dimensions', ttl=6)
    return df

def main():            
    st.header("Digital Literacy")

    st.subheader("First-of-its-kind study assessing Hawaii residents' digital literacy and preparedness for the digital economy.")
    
    st.markdown(
      """
      The Digital Literacy and Readiness Study (DLRS) evaluates Hawaii residents' digital preparedness across seven key areas,
      including **device confidence, tech adaptation, digital productivity, online information litereacy, and educational technology usage**.
      """
    )

    st.subheader("Users in Hawaii were Divided in 5 Categories.")
        
if __name__ == "__main__":
    main()
