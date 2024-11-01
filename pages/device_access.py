import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from streamlit_extras.dataframe_explorer import dataframe_explorer

from style_helper import apply_custom_style

# Function to plot pie chart
def plot_pie_chart(data, title):
    fig, ax = plt.subplots()
    ax.pie(data['Values'], labels=data['County'], autopct='%1.1f%%', startangle=90)
    ax.set_title(title)
    st.pyplot(fig)

def main():
    apply_custom_style()
            
    st.header("Device Access")

    df = pd.read_excel("data/acs2022_5yr_counties_hi.xlsx")

    internet_df = df.iloc[170:174]

    # Rename columns for clarity (based on your provided data)
    internet_df.columns = ['Computers and Internet Use', 'Hawaii_Total', 'Hawaii_MOE', 'Hawaii_Percent', 'Hawaii_Percent_MOE',
              'Hawaii_County_Total', 'Hawaii_County_MOE', 'Hawaii_County_Percent', 'Hawaii_County_Percent_MOE',
              'Honolulu_County_Total', 'Honolulu_County_MOE', 'Honolulu_County_Percent', 'Honolulu_County_Percent_MOE',
              'Kalawao_County_Total', 'Kalawao_County_MOE', 'Kalawao_County_Percent', 'Kalawao_County_Percent_MOE',
              'Kauai_County_Total', 'Kauai_County_MOE', 'Kauai_County_Percent', 'Kauai_County_Percent_MOE',
              'Maui_County_Total', 'Maui_County_MOE', 'Maui_County_Percent', 'Maui_County_Percent_MOE']


    # Extract rows for each metric
    total_households_df = internet_df[internet_df['Computers and Internet Use'] == 'Total households']
    with_computer_df = internet_df[internet_df['Computers and Internet Use'] == 'With a computer']
    with_broadband_df = internet_df[internet_df['Computers and Internet Use'] == 'With a broadband Internet subscription']
    
    # Data for Total Households pie chart
    total_households = {
        'County': ['Hawaii County', 'Honolulu County', 'Kalawao County', 'Kauai County', 'Maui County'],
        'Values': [
            total_households_df['Hawaii_County_Total'].values[0],
            total_households_df['Honolulu_County_Total'].values[0],
            total_households_df['Kalawao_County_Total'].values[0],
            total_households_df['Kauai_County_Total'].values[0],
            total_households_df['Maui_County_Total'].values[0]
        ]
    }

    # Data for With a Computer pie chart
    with_computer = {
        'County': ['Hawaii County', 'Honolulu County', 'Kalawao County', 'Kauai County', 'Maui County'],
        'Values': [
            with_computer_df['Hawaii_County_Total'].values[0],
            with_computer_df['Honolulu_County_Total'].values[0],
            with_computer_df['Kalawao_County_Total'].values[0],
            with_computer_df['Kauai_County_Total'].values[0],
            with_computer_df['Maui_County_Total'].values[0]
        ]
    }
    
    # Data for With Broadband Subscription pie chart
    with_broadband = {
        'County': ['Hawaii County', 'Honolulu County', 'Kalawao County', 'Kauai County', 'Maui County'],
        'Values': [
            with_broadband_df['Hawaii_County_Total'].values[0],
            with_broadband_df['Honolulu_County_Total'].values[0],
            with_broadband_df['Kalawao_County_Total'].values[0],
            with_broadband_df['Kauai_County_Total'].values[0],
            with_broadband_df['Maui_County_Total'].values[0]
        ]
}

    # Create three columns for the pie charts
    col1, col2, col3 = st.columns(3)
    
    # Plot each pie chart in its respective column
    with col1:
        fig1 = plot_pie_chart(total_households, "Total Households")
        st.pyplot(fig1)
    
    with col2:
        fig2 = plot_pie_chart(with_computer, "Households with a Computer")
        st.pyplot(fig2)
    
    with col3:
        fig3 = plot_pie_chart(with_broadband, "Households with Broadband Internet")
        st.pyplot(fig3)
    
    filtered_df = dataframe_explorer(internet_df, case=False)
    st.dataframe(filtered_df, use_container_width=True)
    
if __name__ == "__main__":
    main()
