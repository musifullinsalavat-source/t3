# from pandas.core.frame import StringIO
from io import StringIO
import streamlit as st
from pathlib import Path
import os
from supabase import create_client, Client

# def upload_file(file):
#     filename = Path(file).name
#     if file is not None:
#         with open(filename) as f:
#             text = f.read()
            
#         return text

with st.sidebar:
    st.button("login")
        
file = st.file_uploader("Upload file")
if file is not None:
    filename = Path(file.name).name
    bytes_data = file.getvalue()
    stringio = StringIO(file.getvalue().decode("utf-8"))
    string_data = stringio.read()
    text = file.read().decode("utf-8")
    st.write(filename)
    st.text_area("Output", value = text, disabled=True)
    st.download_button("Download file", data = text, file_name=filename)
    st.feedback()
    # st.write("Reading file line by line")
    # for line in text.splitlines():
    #     st.write(line)