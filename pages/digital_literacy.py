import streamlit as st

import pdfplumber
import pandas as pd

from streamlit_extras.dataframe_explorer import dataframe_explorer

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Digital Literacy")

    with pdfplumber.open("data/WDC Digital Literacy Report FINAL Post Client Input R111021 (003) Inc Appendices.pdf") as pdf:
        # Select page 20
        page = pdf.pages[20]
        
        # Extract the table
        table = page.extract_table()
        
        if table:
            # Convert the table into a DataFrame
            demographic_df = pd.DataFrame(table[1:], columns=table[0])
            demographic_df.columns = ["Category", "Unprepared", "Old Guard", "Social Users", "Technical DIYers", "Digital Learners"]

            filtered_df = dataframe_explorer(demographic_df, case=False)
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.write("No table found on page 20.")

        # Select page 21
        page = pdf.pages[21]
        
        # Extract the table
        table = page.extract_table()
        
        if table:
            # Convert the table into a DataFrame
            occupation_df = pd.DataFrame(table[1:], columns=table[0])
            occupation_df.columns = ["Category", "Unprepared", "Old Guard", "Social Users", "Technical DIYers", "Digital Learners"]

            filtered_df = dataframe_explorer(occupation_df, case=False)
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.write("No table found on page 21.")

if __name__ == "__main__":
    main()
