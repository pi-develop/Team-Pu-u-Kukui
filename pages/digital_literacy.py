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
    st.header("Digital Literacy")

    st.subheader("First-of-its-kind study assessing Hawaii residents' digital literacy and preparedness for the digital economy.")
    
    st.markdown(
      """
      The Digital Literacy and Readiness Study (DLRS) evaluates Hawaii residents' digital preparedness across seven key areas,
      including **device confidence, tech adaptation, digital productivity, online information litereacy, and educational technology usage**.
      """
    )
        
if __name__ == "__main__":
    main()
