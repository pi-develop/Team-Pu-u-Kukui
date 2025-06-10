import streamlit as st
import pandas as pd
from style_helper import apply_custom_style

apply_custom_style()
st.header("Business Intelligence: Filings Overview")

st.markdown("""
This page provides a detailed breakdown of recent filings and business intelligence data. Use the filters below to explore the data.
""")

df = pd.read_json("data/sample.json")
df["Filed Date"] = pd.to_datetime(df["Filed Date"], errors="coerce")

# Sidebar filters
st.sidebar.header("Filter Filings")
category_options = ["All"] + sorted(df["Document Category"].dropna().unique())
type_options = ["All"] + sorted(df["Document Type"].dropna().unique())

selected_category = st.sidebar.selectbox("Document Category", category_options)
selected_type = st.sidebar.selectbox("Document Type", type_options)
min_date, max_date = df["Filed Date"].min(), df["Filed Date"].max()
selected_dates = st.sidebar.date_input("Filed Date Range", (min_date, max_date), min_value=min_date, max_value=max_date)

# Filter logic
filtered_df = df.copy()
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Document Category"] == selected_category]
if selected_type != "All":
    filtered_df = filtered_df[filtered_df["Document Type"] == selected_type]
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    # Make sure both sides of the comparison are timezone-naive
    filed_date_naive = filtered_df["Filed Date"].dt.tz_localize(None)
    start_date = pd.to_datetime(selected_dates[0])
    end_date = pd.to_datetime(selected_dates[1])
    filtered_df = filtered_df[(filed_date_naive >= start_date) & (filed_date_naive <= end_date)]

# Summary statistics
st.subheader("Summary Statistics")
st.write(f"**Total Filings:** {len(filtered_df)}")
st.write(f"**Unique Categories:** {filtered_df['Document Category'].nunique()}")
st.write(f"**Unique Types:** {filtered_df['Document Type'].nunique()}")
if not filtered_df.empty:
    st.write(f"**Date Range:** {filtered_df['Filed Date'].min().date()} to {filtered_df['Filed Date'].max().date()}")
else:
    st.write("**Date Range:** No data in selected range.")

# Show filtered table
st.subheader("Filtered Filings Table")
st.dataframe(filtered_df.sort_values("Filed Date", ascending=False), use_container_width=True) 