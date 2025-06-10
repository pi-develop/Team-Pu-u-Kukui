import streamlit as st
import pandas as pd
import altair as alt

from streamlit_extras.add_vertical_space import add_vertical_space

from style_helper import apply_custom_style

@st.cache_data
def load_and_clean_data(csv_path="Tbl_RegAttend.csv"):
  df = pd.read_csv(csv_path)
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
  
  st.markdown("### Regression Inputs")
  col1, col2 = st.columns(2)
  with col1:
      x_axis = st.selectbox("X-axis", df_total.columns, index=df_total.columns.get_loc("Marketing_and_Outreach"))
  with col2:
      y_axis = st.selectbox("Y-axis", df_total.columns, index=df_total.columns.get_loc("Attend_Rate"))
  
  st.subheader(f"Scatter plot of {y_axis.replace('_', ' ')} vs {x_axis.replace('_', ' ')}")
  
  # Create chart
  chart = alt.Chart(df_total).mark_circle(size=60).encode(
      x=alt.X(x_axis, title=x_axis.replace('_', ' ')),
      y=alt.Y(y_axis, title=y_axis.replace('_', ' ')),
      tooltip=["textDate", "Total"]
  ).properties(
      width=700,
      height=400,
      title="Attendance Rate vs Budget Used"
  ).interactive()
  
  # Add regression line
  reg_line = chart.transform_regression(
      x_axis, y_axis, method="loess"
  ).mark_line(color="orange")
  
  # Display chart
  st.altair_chart(chart + reg_line, use_container_width=True)
  
  # Optional raw data view
  with st.expander("Show raw data"):
      st.dataframe(df_total)

if __name__ == "__main__":
  main()
