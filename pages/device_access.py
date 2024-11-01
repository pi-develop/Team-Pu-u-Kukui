import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_extras.dataframe_explorer import dataframe_explorer

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Device Access")

    df = pd.read_excel("data/acs2022_5yr_counties_hi.xlsx")

    # Plot percentage of households with a computer by location
    st.subheader("Households with a Computer (%) by Location")
    fig_computer = px.bar(
        df, x='Location', y='With a Computer Percent',
        error_y='With a Computer Percent Margin of Error',
        title="Households with a Computer by Location",
        labels={'With a Computer Percent': 'Percentage with Computer (%)'}
    )
    st.plotly_chart(fig_computer)
    
    filtered_df = dataframe_explorer(df, case=False)
    st.dataframe(filtered_df, use_container_width=True)
    
if __name__ == "__main__":
    main()
