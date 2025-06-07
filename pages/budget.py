import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from streamlit_extras.add_vertical_space import add_vertical_space

from style_helper import apply_custom_style

@st.cache_data
def fetch_budget_data():
  data = pd.read_csv("data/budget.csv")

  # Clean column names
  data.columns = data.columns.str.strip().str.replace('/', '_')
    
  # Filter out Total rows for per-category breakdown
  category_data = data[data['Category'] != 'Total']
  total_data = data[data['Category'] == 'Total']
  return category_data, total_data

def monthly_overview(total_data):
  fig, ax = plt.subplots()
  ax.bar(total_data['Date'], total_data['Budgeted'], label='Budgeted', alpha=0.6)
  ax.bar(total_data['Date'], total_data['Used'], label='Used')
  ax.set_ylabel("Amount ($)")
  ax.set_title("Total Budget vs Used")
  ax.legend()
  st.pyplot(fig)

def main():
  apply_custom_style()
            
  st.header("Budget Data Visualization")

  category_data, total_data = fetch_budget_data()
  monthly_overview(total_data)

if __name__ == "__main__":
  main()
