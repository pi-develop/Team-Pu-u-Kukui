import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from streamlit_extras.add_vertical_space import add_vertical_space

from style_helper import apply_custom_style

@st.cache_data
def load_and_clean_data():
  df = pd.read_csv("data/Tbl_RegAttend.csv")
  df = df[df["Island"] == "Total"].copy()
  df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('/', '_')
  for col in ['Marketing_and_Outreach', 'Attend_Rate']:
      if col in df.columns:
          df[col] = pd.to_numeric(df[col], errors='coerce')
  return df

def main():
  apply_custom_style()
  
  st.header("Attendance Rate vs. Budget")
  df_total = load_and_clean_data()
  
  x_axis = st.selectbox("X-axis", df_total.columns, index=df_total.columns.get_loc("Marketing_and_Outreach"))
  y_axis = st.selectbox("Y-axis", df_total.columns, index=df_total.columns.get_loc("Attend_Rate"))

  fig, ax = plt.subplots()
  sns.regplot(x=df_total[x_axis], y=df_total[y_axis], ax=ax, scatter_kws={"s": 40})
  ax.set_title(f"{y_axis} vs {x_axis}")
  ax.set_xlabel(x_axis)
  ax.set_ylabel(y_axis)
  st.pyplot(fig)

if __name__ == "__main__":
  main()
