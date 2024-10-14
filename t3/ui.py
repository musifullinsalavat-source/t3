import gradio as gr
from pathlib import Path

def upload_file(file):
    filename = Path(file).name
    if file is not None:
        with open(file) as f:
            text = f.read()
            
        return text
        
def download_file():
    

# with gr.Blocks(title="T3") as demo:
#     with gr.Row():
#         with gr.Column(scale=1):
#             file_dropzone = gr.File(label="Upload Lecture")
#             # upload_btn = gr.UploadButton(label="Choose Lecture File")
#         with gr.Column(scale=2):
#             output = gr.Textbox(label="Output Box")
# 
demo = gr.Interface(
    fn = upload_file,
    inputs = ["file"],
    outputs = ["textbox", gr.DownloadButton(label = "Download File")]
)

demo.launch()