# from pandas.core.frame import StringIO
from io import StringIO
import streamlit as st
from pathlib import Path
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import supabase
from pypdf import PdfReader
import textract # textract 1.6.5 requires six~=1.12.0, but you have six 1.16.0 which is incompatible.
from docx import Document

load_dotenv()

api_key: str = os.getenv('KEY')
url: str = os.getenv('URL')
supabase: Client = create_client(url, api_key)

if "text" not in st.session_state:
    st.session_state.text = ""

def upload_file(file):
    if file is not None:
        file_type = file.type
        if file_type == "text/plain":
            st.session_state.text = file.read().decode('utf-8')
        elif file_type == "application/pdf":
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            st.session_state.text = text
        elif file_type == "application/msword":
            st.session_state.text = textract.process(file) # might not work due to dependency incompatibility.
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            st.session_state.text = "\n".join([para.text for para in doc.paragraphs])
        else:
            st.error("Unsupported file type!")
            return
        
def download_file():
    pass

with st.sidebar:
    signin, signup, sso =  st.tabs(["Sig in", "Sign up", "SSO"])
    with signin:
        with st.form("signin"):
            email_input = st.text_input("Email")
            signin_button = st.form_submit_button("Sign in")
    with signup:
        with st.form("signup"):
            email_input = st.text_input("Email")
            signup_button = st.form_submit_button("Sign up")
    with sso:
        with st.form("sso"):
            sso_button = st.form_submit_button("SSO")
# idea: use login with link, that way a user will just get link via email and I won't need to deal with passwords or keys
        
file = st.file_uploader("Upload file", type=['txt', 'doc', 'docx', 'pdf'])
st.button("Upload file", on_click=upload_file, args=[file])
# if file is not None:
    # upload_file(file)
# filename = Path(file.name).name
    # bytes_data = file.getvalue()
    # stringio = StringIO(file.getvalue().decode("utf-8"))
    # string_data = stringio.read()
    # text = file.read().decode("utf-8")
    # st.write(filename)
st.text_area("Output", value = st.session_state.text, disabled=True)
# st.download_button("Download file", data = st.session_state.text, file_name=f"{filename}.txt", mime="text/plain")
st.feedback()
    # st.write(url)
    # st.write("Reading file line by line")
    # for line in text.splitlines():
    #     st.write(line)

