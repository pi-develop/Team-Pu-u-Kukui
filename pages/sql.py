import streamlit as st

#Tiger testing mysql connection11/2 
conn = st.connection('mysql', type='sql') 

st.write("Testing connection ok") 

# Perform query. 
df = conn.query('SELECT * from BroadBandConnection_By_City limit 5;', ttl=6) 

st.write(df)
