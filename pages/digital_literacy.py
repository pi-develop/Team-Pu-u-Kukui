import streamlit as st

import pdfplumber

from style_helper import apply_custom_style

def main():
    apply_custom_style()
            
    st.header("Digital Literacy")

    with pdfplumber.open("data/WDC Digital Literacy Report FINAL Post Client Input R111021 (003) Inc Appendices.pdf") as pdf:
        # Select page 20 (index 19 since it's zero-indexed)
        page = pdf.pages[19]  # Page numbers start from 0
        
        # Extract the table
        table = page.extract_table()
        
        if table:
            # Convert the table into a DataFrame
            table_df = pd.DataFrame(table[1:], columns=table[0])
            st.write("Table extracted successfully:")
            print(table_df)
        else:
            st.write("No table found on page 20.")

if __name__ == "__main__":
    main()
