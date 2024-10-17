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