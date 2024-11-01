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


    # Extract relevant rows and columns for each county
    locations = {
        "Hawaii Total": internet_df.iloc[0, 2],  # Column 2 for "Total households", row 2 for Hawaii Total
        "Hawaii County": internet_df.iloc[0, 6], # Column 6 for "Total households" of Hawaii County, row 2
        "Honolulu County": internet_df.iloc[0, 10], # Column 10 for "Total households" of Honolulu, row 2
        "Kalawao County": internet_df.iloc[0, 14], # Column 14 for "Total households" of Kalawao, row 2
        "Kauai County": internet_df.iloc[0, 18], # Column 18 for "Total households" of Kauai, row 2
        "Maui County": internet_df.iloc[0, 22] # Column 22 for "Total households" of Maui, row 2
    }
    
    # "With a computer" values for each county
    computer_users = {
        "Hawaii Total": internet_df.iloc[1, 2], 
        "Hawaii County": internet_df.iloc[1, 6],
        "Honolulu County": internet_df.iloc[1, 10],
        "Kalawao County": internet_df.iloc[1, 14],
        "Kauai County": internet_df.iloc[1, 18],
        "Maui County": internet_df.iloc[1, 22]
    }
    
    # Create progress bars
    st.title("Computer Usage in Hawaii Counties")
    
    for county, total_households in locations.items():
        with_computer = computer_users[county]
        
        # Calculate percentage of households with a computer
        percentage = with_computer / total_households
        
        # Display progress bar with the computed percentage
        st.subheader(f"{county}")
        st.progress(percentage)
    
    st.dataframe(internet_df, use_container_width=True)
    
if __name__ == "__main__":
    main()
