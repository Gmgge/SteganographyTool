import cv2
import os
from gstego import Steganography


def test_stego_message():
    # 隐写信息
    stego_opt = Steganography()
    test_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/0.png")
    image_file = cv2.imread(test_image_path)
    hide_info = "我好像曾经见过你"
    test_data = stego_opt.hide_message(image_file, hide_info)
    cv2.imwrite("output.png", test_data)
    # 提取
    img_in = cv2.imread(r"output.png")
    extract_info = stego_opt.extract(img_in)
    os.remove(r"output.png")
    assert extract_info["message"] == hide_info


def test_stego_file():
    stego_opt = Steganography()
    # 隐写文件
    test_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/0.png")
    hide_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/in_0.png")
    image_file = cv2.imread(test_image_path)
    hide_buffer = open(hide_file_path, "rb")
    test_data = stego_opt.hide_file(image_file, hide_buffer)
    cv2.imwrite("output.png", test_data)

    # 提取文件
    img_in = cv2.imread(r"output.png")
    extract_info = stego_opt.extract(img_in)
    hide_buffer.seek(0)
    hide_data = hide_buffer.read()
    os.remove(r"output.png")
    assert hide_data == extract_info["file"]["bytes_data"]
