import streamlit as st 
from auth_db import csr, conn
import pandas as pd

st.title("My web app")

query = "select * from signup_user;"

# df = pd.read_sql(query, conn)

# st.dataframe(df)

my_file = st.file_uploader("upload your file to view data", type = ["csv"])

if my_file != None:
    data = pd.read_csv(my_file, encoding = "latin-1")

    st.dataframe(data)
