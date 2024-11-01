import streamlit as st

import pdfplumber
import pandas as pd

from streamlit_extras.dataframe_explorer import dataframe_explorer

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Digital Literacy")

    with pdfplumber.open("data/WDC Digital Literacy Report FINAL Post Client Input R111021 (003) Inc Appendices.pdf") as pdf:
        # Select page 20 (index 19 since it's zero-indexed)
        page = pdf.pages[20]  # Page numbers start from 0
        
        # Extract the table
        table = page.extract_table()
        
        if table:
            # Convert the table into a DataFrame
            table_df = pd.DataFrame(table[1:], columns=table[0])
            table_df.columns = ["Category", "Unprepared", "Old Guard", "Social Users", "Technical DIYers", "Digital Learners"]

            filtered_df = dataframe_explorer(table_df, case=False)
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.write("No table found on page 20.")

if __name__ == "__main__":
    main()
