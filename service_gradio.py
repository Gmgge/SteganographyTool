import os
import gradio as gr
from tool.log_init import logger
from gstego import Steganography


data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


# 构建分析模块
logger.info("初始隐写模块")
stego_opt = Steganography()
logger.info("隐写模块初始化成功")


def call_hide(image_file, message_input_):
    image_file = stego_opt.hide_message(image_file, message_input_)
    return image_file


def call_extract(image_file):
    extract_info = stego_opt.extract(image_file)
    return extract_info["message"]


if __name__ == "__main__":
    with gr.Blocks() as gradio_demo:
        with gr.Tab("图像隐写"):
            with gr.Row():
                image = gr.Image(source="upload", label="图像文件", type="pil", image_mode="RGBA")
                message_input = gr.Textbox(label="隐写消息输入")
                output = gr.Image(label="隐写后图像", type="pil", image_mode="RGBA")
            btn = gr.Button("隐写")
            btn.click(fn=call_hide, inputs=[image, message_input], outputs=output)
            gr.Examples(
                examples=data_dir,
                inputs=[image],
                outputs=output,
                fn=call_hide

            )
        with gr.Tab("隐写提取"):
            with gr.Row():
                image = gr.Image(source="upload", label="图像文件", type="pil", image_mode="RGBA")
                output = gr.Text(label="提取结果")
            btn = gr.Button("提取")
            btn.click(fn=call_extract, inputs=[image], outputs=output)
            gr.Examples(
                examples=data_dir,
                inputs=[image],
                outputs=output,
                fn=call_extract

            )
    gradio_demo.launch(show_error=True, show_tips=True, server_name="localhost", server_port=8081, share=True)
