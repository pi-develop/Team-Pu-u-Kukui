import streamlit as st
import pandas as pd
import plotly.express as px

from style_helper import apply_custom_style

@st.cache_data
def fetch_feedback_data():
    conn = st.connection('mysql', type='sql')
    df = conn.query("""
        SELECT
            SUM(Satisfied) AS Satisfied,
            SUM(Unsatisfied) AS Unsatisfied
        FROM user_feedback;
        """, ttl=6)
    return df

def main():
    apply_custom_style()

    st.header("User Feedback")

    df = fetch_feedback_data()
    satisfied_count = df['Satisfied'][0]
    unsatisfied_count = df['Unsatisfied'][0]
    
    # Prepare data for pie chart
    feedback_data = pd.DataFrame({
        "Feedback": ["Satisfied", "Unsatisfied"],
        "Count": [satisfied_count, unsatisfied_count]
    })

    # Plot pie chart
    fig = px.pie(
        feedback_data,
        names="Feedback",
        values="Count",
        color="Feedback",
        color_discrete_map={"Satisfied": "#0778DF", "Unsatisfied": "#FF3583"}
    )
    fig.update_traces(textinfo='percent+label')
    
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
