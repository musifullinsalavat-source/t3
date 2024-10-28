# from pandas.core.frame import StringIO
from io import StringIO, BytesIO
import streamlit as st
from pathlib import Path
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import supabase
from pypdf import PdfReader
import textract # textract 1.6.5 requires six~=1.12.0, but you have six 1.16.0 which is incompatible.
from docx import Document
from st_supabase_connection import SupabaseConnection
import argon2

load_dotenv()

api_key: str = os.getenv('KEY')
url: str = os.getenv('URL')
supabase: Client = create_client(url, api_key)

if "text" not in st.session_state:
    st.session_state.text = ""
    
# def signup(user_email):
#     pass

def login_form(
    *,
    title: str = "Log In/Sign Up",
    user_tablename : str = "users",
    username_col: str = "username",
    email_col: str = "email",
    password_col: str = "password",
    signup_title: str = "Create new account",
    login_title: str = "Login to existing account",
    allow_signup: bool = True,
) -> Client:
    """Create a user login/signup form with email validation and password hashing which is then saved to supabase db."""
    
    client = st.connection(name = "supabase", type = SupabaseConnection)
    password_hasher = argon2.PasswordHasher()
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        
    if "username" not in st.session_state:
        st.session_state.username = None
        
    if not st.session_state["authenticated"]:
        with st.expander("Authentication", expanded = True):
            if allow_signup:
                signup_tab, login_tab = st.tabs(["New User? Sign Up", "Existing User? Log In"])
            else:
                login_tab = st.container()
            if allow_signup:
                with signup_tab:
                    with st.form(key = "signup"):
                        username = st.text_input(label = "Enter a username")
                        user_email = st.text_input(label = "Enter your email")
                        password = st.text_input(label = "Create password", help = "Password cannot be recovered if lost", type = "password")
                        confirmed_password = st.text_input(label = "Confirm Password", type = "password")
                        assert password == confirmed_password # todo: add more context
                        hashed_password = password_hasher.hash(password)
                        if st.form_submit_button(label="Sign Up", type = "primary"):
                            if "@" not in user_email: # todo: switch to more robust email validation library.
                                st.error("Invalid Email address")
                                st.stop()
                            try:
                                client.table(user_tablename).insert({username_col: username, email_col: user_email, password_col: hashed_password}).execute()
                            except Exception as e:
                                st.error(e.message)
                            else:
                                st.session_state["authenticated"] = True
                                st.session_state["username"] = username
                                st.success("Sign up successful")
                                st.rerun()
                                
            with login_tab:
                with st.form(key = "login"):
                    username = st.text_input(label = "Username:")
                    password = st.text_input(label = "Password", type = "password")
                    
                    if st.form_submit_button(label = "Log In", type = "primary"):
                        response = client.table(user_tablename).select(f"{username_col}, {password_col}").eq(username_col, username).execute()
                    
                        if len(response.data) > 0:
                            db_password = response.data[0]["password"]
                            if password_hasher.verify(db_password, password):
                                st.session_state["authenticated"] = True
                                st.session_state["username"] = username
                                st.success("Log in successful")
                                st.rerun()
                            else:
                                st.error("Incorrect Password")
                        else:
                            st.error("Username or Password incorrect")
                    
    return client
    
# login_form()

def signout():
    st.session_state["authenticated"] = False
    st.session_state["username"] = None

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
        # elif file_type == "application/msword":
            # st.session_state.text = textract.process(file) # might not work due to dependency incompatibility. waiting for textract to merge dependency update.
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            st.session_state.text = "\n".join([para.text for para in doc.paragraphs])
        else:
            st.error("Unsupported file type!")
            return
        
def download_file(text):
    pass

def main():
    client = login_form()
    
    if st.session_state["authenticated"]:
        st.title("T3 Assistant")
        
        file = st.file_uploader("Upload file", type=['txt', 'docx', 'pdf'])
        st.button("Upload file", on_click=upload_file, args=[file])
        # st.download_button("Download file", data = file)
        st.feedback()
        
        with st.sidebar:
            st.write(f"Signed in as {st.session_state.username}")
            st.button(label = "Sign out", on_click=signout, type = "primary", use_container_width=True)
        
        
if __name__ == "__main__":
    main()

# with st.sidebar:
#     st.session_state.user_email = None
#     if st.session_state["user_email"]:
#         st.write(f"Logged in as {st.session_state['user_email']}")
#     else:
#         st.write("Not logged in")
#     signin, signup, sso =  st.tabs(["Sign in", "Sign up", "SSO"])
#     with signin:
#         with st.form("Log In"):
#             user_email = st.text_input("Email")
#             signin_button = st.form_submit_button("Log In", on_click=login, args=[user_email])
#             # print(user_email)
#     with signup:
#         with st.form("signup"):
#             email_input = st.text_input("Email")
#             signup_button = st.form_submit_button("Sign up")
#     with sso:
#         with st.form("sso"):
#             sso_button = st.form_submit_button("SSO")
# idea: use login with link, that way a user will just get link via email and I won't need to deal with passwords or keys
# OTP login won't work since I need to set up a custom smtp server
        
# file = st.file_uploader("Upload file", type=['txt', 'docx', 'pdf']) #todo: add .doc later when textract is updated to latest version of six (1.16.0)
# st.button("Upload file", on_click=upload_file, args=[file])
# st.text_area("Output", value = st.session_state.text, disabled=True)
# # st.download_button("Download file", data = st.session_state.text, file_name=f"{filename}.txt", mime="text/plain")
# st.feedback()

