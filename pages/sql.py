import streamlit as st
import socket

def print_server_info():
  hostname = socket.gethostname()
  server_ip = socket.gethostbyname(hostname)
  st.write("Server Host:", hostname)
  st.write("Server IP:", server_ip)

print_server_info()

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Perform query.
df = conn.query('SELECT * from broadbcover_by_city;', ttl=600)

# Print results.
for row in df.itertuples():
  st.write(f"{row.City} has a :{row.BroadbandCoverage}:")
