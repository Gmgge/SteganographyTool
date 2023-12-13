import os
from hide_algorithm import init_hide_opt
from tool.log_init import logger


class Steganography(object):
    def __init__(self, hide_algorithm="LSB"):
        self.hide_opt = init_hide_opt(hide_algorithm)
        self.magic_number = b"41433130"
        self.attribute_map = {"message": b"0", "file": b"1"}
        self.head_info_len = {"magic_number": 8,
                              "attribute": 1,
                              "data_len": 3,
                              "data_suffix": 4}

    def check_magic(self, read_iterator):
        """
        读取并检查头部信息中的隐写信息魔法数
        :param read_iterator: 隐写信息读取迭代器
        :return: 匹配 True，不匹配 False
        """
        check_status = True
        for i in range(self.head_info_len["magic_number"]):
            if next(read_iterator) != self.magic_number[i]:
                check_status = False
                logger.info("隐写头校验失败")
                break
        return check_status

    @staticmethod
    def read_len(read_iterator):
        """
        读取头部信息中的数据长度
        :param read_iterator: 隐写信息读取迭代器
        :return:
        """
        data_len = next(read_iterator) | (next(read_iterator) << 8) | (next(read_iterator) << 16)
        return data_len

    def read_suffix(self, read_iterator):
        """
        读取头部信息中的后缀信息，如果隐写的属性为message，则忽略该属性
        :param read_iterator: 隐写信息读取迭代器
        :return:
        """
        suffix = b""
        for i in range(self.head_info_len["data_suffix"]):
            suffix += next(read_iterator).to_bytes(length=1, byteorder='big')
        suffix = suffix.replace(b".", b"").decode("ascii")
        return suffix

    def read_head(self, read_iterator):
        """
        读取隐写信息头文件
        :param read_iterator: 隐写信息读取迭代器
        :return: 解码后的文件信息，未成功返回None
        """
        data_info = {}
        if self.check_magic(read_iterator):
            data_info["attribute"] = next(read_iterator).to_bytes(length=1, byteorder='big')
            data_info["data_len"] = self.read_len(read_iterator)
            data_info["data_suffix"] = self.read_suffix(read_iterator)
        return data_info

    def extract(self, carrier_data):
        res_info = {"message": None, "file": None}
        # 隐写载体检查
        if not self.hide_opt.check_carrier(carrier_data):
            logger.info("隐写载体校验失败")
            return res_info
        # 隐写信息读取
        read_iterator = self.hide_opt.read(carrier_data)
        # 隐写信息头读取
        head_info = self.read_head(read_iterator)
        # 成功提取信息
        if len(head_info) > 0:
            data_info = bytearray(head_info["data_len"])
            # bytes形式隐写信息提取
            for i in range(head_info["data_len"]):
                pre_info = next(read_iterator)
                data_info[i] = pre_info
            # message隐写解码
            if head_info["attribute"] == self.attribute_map["message"]:
                res_info["message"] = data_info.decode("utf-8")
            # file隐写解码
            elif head_info["attribute"] == self.attribute_map["file"]:
                res_info["file"] = {"bytes_data": data_info, "suffix": head_info["data_suffix"]}
        return res_info

    def encode_info(self, hide_data, attribute, file_suffix=""):
        # 构建隐写信息头
        magic_number_b = self.magic_number
        attribute_b = self.attribute_map[attribute]
        data_len = len(hide_data)
        data_len_b = bytes([data_len & 255, (data_len >> 8) & 255, (data_len >> 16) & 255])
        data_suffix_b = file_suffix.encode("ascii")
        # 填充后缀
        data_suffix_b = (self.head_info_len["data_suffix"]-len(data_suffix_b)) * b"." + data_suffix_b
        # 组装信息
        hide_data_b = magic_number_b+attribute_b+data_len_b+data_suffix_b+hide_data
        return hide_data_b

    def hide_message(self, carrier_data, message):
        bytes_data = message.encode("utf-8")
        carrier_data = self.hide(carrier_data, bytes_data, "message")
        return carrier_data

    def hide_file(self, carrier_data, file_buffer):
        file_suffix = os.path.splitext(file_buffer.name)[1][1:]
        carrier_data = self.hide(carrier_data, file_buffer.read(), "file", file_suffix)
        return carrier_data

    def hide(self, carrier_data, hide_info, attribute, file_suffix=""):
        assert type(hide_info) is bytes
        hide_data = self.encode_info(hide_info, attribute, file_suffix)
        carrier_data = self.hide_opt.hide(carrier_data, hide_data)
        return carrier_data



