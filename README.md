# 1 隐写与提取 运行指南


1. 在线体验网址 http://120.27.143.171:19191/ 由于云服务器配置有限，可能会一定卡顿
2. 由于当前隐写算法决定，隐写后的载体如果被压缩或修改，则无法提取被隐写信息


## 1.1 实现功能
- [x]  图像文件隐写
- [x]  LSB隐写
- [x]  gradio服务中消息隐写与提取
- [x]  隐写算法批量写入
- [ ]  隐写算法批量读取
- [ ]  gradio服务中文件隐写与提取
- [ ]  更多的隐写算法支持
- [ ]  更多的隐写载体支持



## 1.2 环境安装
```
pip install -r requirements.txt
```

## 1.3 运行gradio服务
```
python service_gradio.py
```

## 1.4 python代码调用隐写消息
```
    # 隐写信息
    import PIL.Image
    import os
    from gstego import Steganography
    
    # 初始化隐写器
    stego_opt = Steganography()
    # 读取载体信息
    carrier_path = r"**.png"
    image_file = PIL.Image.open(carrier_path)
    # 设置隐写消息
    hide_info = "我好像曾经见过你"
    # 隐写
    carrier_data = stego_opt.hide_message(image_file, hide_info)
    # 保存隐写的载体
    carrier_data.save("output.png", optimize=True)
    
    # 读取载体
    img_in = PIL.Image.open(r"output.png")
    # 提取隐写信息
    extract_info = stego_opt.extract(img_in)
    # 展示隐写消息
    print(extract_info["message"])
```

## 1.5 python代码调用隐写文件
```
    # 隐写文件
    import PIL.Image
    import os
    from gstego import Steganography
    
    # 初始化隐写器
    stego_opt = Steganography()
    # 读取载体信息
    carrier_path = r"**.png"
    image_file = PIL.Image.open(carrier_path)
    # 读取隐写文件
    hide_file_path = r"**.txt"
    hide_buffer = open(hide_file_path, "rb")
    # 隐写
    carrier_data = stego_opt.hide_file(image_file, hide_buffer)
    carrier_data.save("output.png", optimize=True)

    # 读取载体
    img_in = PIL.Image.open(r"output.png")
    extract_info = stego_opt.extract(img_in)
    # 保存提取出的文件
    with open("out." + extract_info["file"]["suffix"], "wb") as fw:
        fw.write(extract_info["file"]["bytes_data"])
```

