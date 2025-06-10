import streamlit as st
import pandas as pd
import plotly.express as px
from style_helper import apply_custom_style

apply_custom_style()
st.header("Survey Results: Digital Literacy Classes")

st.markdown("""
This page provides a detailed breakdown of survey results from two digital literacy classes:
- **Class 3: Email**
- **Class 4: Online Safety**
""")

# Load data
class3 = pd.read_excel("data/SurveyClass3.xlsx", engine="openpyxl")
class4 = pd.read_excel("data/SurveyClass4.xlsx", engine="openpyxl")

# Remove N row for display and plotting
class3_no_n = class3[class3[class3.columns[0]] != 'N']
class4_no_n = class4[class4[class4.columns[0]] != 'N']

# Transpose tables so dates are rows and questions are columns
def transpose_survey(df):
    df_t = df.set_index(df.columns[0]).T
    df_t.index.name = 'Date'
    df_t = df_t.reset_index()
    return df_t

class3_t = transpose_survey(class3_no_n)
class4_t = transpose_survey(class4_no_n)

# Show transposed tables
st.subheader("Class 3: Email - Survey Table (Dates as Rows)")
st.dataframe(class3_t, use_container_width=True)

st.subheader("Class 4: Online Safety - Survey Table (Dates as Rows)")
st.dataframe(class4_t, use_container_width=True)

# Plot: Each question as a line, x=Date, y=Score
def plot_survey(df_t, orig_df, title):
    df_long = df_t.melt(id_vars=['Date'], var_name='Question', value_name='Score')
    df_long['Date'] = pd.to_datetime(df_long['Date'], errors='coerce')
    df_long = df_long.sort_values('Date')
    fig = px.line(df_long, x='Date', y='Score', color='Question', markers=True, title=title)
    fig.update_layout(height=400, margin=dict(t=60, b=40), legend=dict(orientation='h', yanchor='bottom', y=-0.45, xanchor='center', x=0.5))
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Class 3: Email - Trends by Question")
plot_survey(class3_t, class3_no_n, "Class 3: Email - Survey Trends")

st.subheader("Class 4: Online Safety - Trends by Question")
plot_survey(class4_t, class4_no_n, "Class 4: Online Safety - Survey Trends")
