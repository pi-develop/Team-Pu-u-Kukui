import streamlit as st

#Tiger testing mysql connection11/2 
conn = st.connection('mysql', type='sql') 

# Perform query. 
df = conn.query('select * from broadbcover_by_city limit 5', ttl=6) 

st.write(df)
