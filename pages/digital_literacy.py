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

    df = fetch_readiness_data()
    # Select the first row where Dimension is 'Overall' and specific columns
    overall_row = df.loc[df['Dimension'] == 'Overall', ['Unprepared', 'Old_Guard', 'Social_Users', 'Technical', 'Digital']]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="The Unprepared", value=overall_row['Unprepared'].values[0])

        st.markdown("""
        * Limited tech adoption
        * Resistant to learning (online & traditional)
        * Low computer confidence
        """)

    with col2:
        st.subheader("Old Guard")
        st.write(overall_row['Old_Guard'].values[0])

        st.markdown("""
        * Traditional learners with lowest tech adoption/ownership
        * Low confidence in computer skills and new device setup
        * Middle-aged (45-65), blue-collar/self-employed workers
        """)

    with col3:
        st.subheader("Social Users")
        st.write(overall_row['Social_Users'].values[0])

        st.markdown("""
        * Digitally adept but not focused on online learning/development
        * Strong at social networking and sharing content
        * Young professionals (18-35), middle income, sales-oriented
        """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Technical DIYers")
        st.write(overall_row['Technical'].values[0])

        st.markdown("""
        * Confident with tech and digital info
        * Engages in informal online learning
        * Single, educated professionals on O'ahu skilled in job-search tech
        """)

    with col2:
        st.subheader("Digital Learners")
        st.write(overall_row['Digital'].values[0])

        st.markdown("""
        * Eager online learners; tech-confident and productive
        * Mostly on O'ahu; educated, high-income professionals
        * Skilled in digital creativity
        """)
        
if __name__ == "__main__":
    main()
