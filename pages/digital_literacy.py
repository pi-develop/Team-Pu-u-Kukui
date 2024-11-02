import streamlit as st

import pdfplumber
import pandas as pd

from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.dataframe_explorer import dataframe_explorer

from style_helper import apply_custom_style

def extract_table(pdf, page_number, columns):
    # Select page number
    page = pdf.pages[page_number]
    
    # Extract the table
    table = page.extract_table()
    
    if table:
        # Convert the table into a DataFrame
        table_df = pd.DataFrame(table[1:], columns=table[0])
        table_df.columns = columns

        filtered_df = dataframe_explorer(table_df, case=False)
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.write(f"No table found on page {page_number}.")

def main():
    apply_custom_style()
            
    st.header("Digital Literacy")

    with pdfplumber.open("data/WDC Digital Literacy Report FINAL Post Client Input R111021 (003) Inc Appendices.pdf") as pdf:
        columns = ["Category", "Unprepared", "Old Guard", "Social Users", "Technical DIYers", "Digital Learners"]
        st.subheader("Demographic Characteristics Of Digital Readiness Groups (Statewide)")
        extract_table(pdf, 20, columns)

        add_vertical_space(2)
        st.subheader("Employment Characteristics Of Digital Readiness Groups (Statewide)")
        extract_table(pdf, 21, columns)
        
if __name__ == "__main__":
    main()
