from dotenv import load_dotenv
import os
import streamlit as st
import supabase
from supabase import create_client, Client
from streamlit_supabase_auth import login_form, logout_button

load_dotenv()

key: str = os.getenv('SUPABASE_KEY')
url: str = os.getenv('SUPABASE_URL')
supabase: Client = create_client(url, key)

def main():
    session = login_form(
        url,
        key,
        providers=["apple", "google", "email"],
    )
    
    if not session:
        return
        
    st.query_params(page=["success"])
    with st.sidebar:
        st.write(f"Welcome {session['user']['email']}")
        logout_button()
        
if __name__ == "__main__":
    main()