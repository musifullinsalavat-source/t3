import gradio as gr

def upload_file(file):
    if file is not None:
        with open(file.name) as f:
            text = f.read()
            
        return text, gr.DownloadButton(label = "Download File", value = file)

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
    inputs = ["files"],
    outputs = ["textbox", "downloadbutton"]
)

demo.launch()