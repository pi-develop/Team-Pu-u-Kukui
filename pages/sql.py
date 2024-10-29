import streamlit as st

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from broadbcover_by_city;', ttl=600)

# Print results.
for row in df.itertuples():
  st.write(f"{row.City} has a :{row.BroadbandCoverage}:")
