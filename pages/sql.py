import streamlit as st
import socket

def get_server_ip():
  hostname = socket.gethostname()
  server_ip = socket.gethostbyname(hostname)
  return server_ip

st.write("Server IP Address:", get_server_ip())

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from broadbcover_by_city;', ttl=600)

# Print results.
for row in df.itertuples():
  st.write(f"{row.City} has a :{row.BroadbandCoverage}:")
