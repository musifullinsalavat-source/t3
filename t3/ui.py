# import gradio as gr
# from pathlib import Path

# def login():
#     return gr.LoginButton()

# def upload_file(file):
#     if file is not None:
#         with open(file.name) as f:
#             text = f.read()
            
#         return text, Path(file.name).name
        
# def download_file(text, filename):
#     return text, filename
        
# def generate_tests():
#     """
#     Takes in lecture(s) in text format as input, feeds them to the LLM
#     which then produces the tests as ouput based on the lecture(s) and
#     the number of tests specified by user
#     """
#     pass
    
# def save_inputs():
#     """
#     Saves inputs (lecture files and number of tests needed to the db and storage)
#     """
#     pass

# def main(file):
#     text = upload_file(file)
    

# # with gr.Blocks(title="T3") as demo:
# #     login_button = gr.LoginButton
# #     with gr.Row():
# #         with gr.Column(scale=1):
# #             file_dropzone = gr.File(label="Upload Lecture")
# #         with gr.Column(scale=2):
# #             output = gr.Textbox(label="Output Box")
# #             download_button = gr.DownloadButton(label = "Download file")
            
# #     file_dropzone.change(upload_file, inputs = file_dropzone, outputs = [output, download_button])
    
# #     # output.change(download_file, inputs = [output, file_dropzone], outputs = [download_button])
# #     output.change(lambda text: (text, Path(file_dropzone).name) if text else (None, None),
# #         inputs = output, outputs = [download_button])
# # 
# demo = gr.Interface(
#     fn = upload_file,
#     inputs = ["loginbutton", "files", gr.Slider(5, 50, value = 5, step = 5, interactive = True)],
#     outputs = ["textbox", "downloadbutton", "loginbutton"]
# )

# demo.launch(auth = ("username", "password"))
# 
# 
# STREAMLIT
# # with st.sidebar:
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