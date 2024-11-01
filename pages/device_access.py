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


    total_households_df = df[df['Computers and Internet Use'] == 'Total households']
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

    # Plot each pie chart
    st.subheader("Total Households")
    # plot_pie_chart(total_households, "Total Households by County")
    
    filtered_df = dataframe_explorer(total_households_df, case=False)
    st.dataframe(filtered_df, use_container_width=True)
    
if __name__ == "__main__":
    main()
