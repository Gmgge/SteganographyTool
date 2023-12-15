import cv2
import numpy as np
from hide_algorithm.base_algorithm import BaseAlgorithm


class SteganographyException(Exception):
    pass


class LSB(BaseAlgorithm):
    def __init__(self):
        self.maskONEValues = [1, 2, 4, 8, 16, 32, 64, 128]
        self.maskZEROValues = [254, 253, 251, 247, 239, 223, 191, 127]
        self.max_use_bit = 3  # 最多使用3位用于写入数据

    def check_carrier(self, carrier_data):
        sign = False
        if carrier_data is not None and isinstance(carrier_data, np.ndarray):
            sign = True
        return sign

    def read(self, carrier_data, ):
        carrier_flat = carrier_data.flatten()
        for use_bit_ptr in range(self.max_use_bit):
            mask_one = self.maskONEValues[use_bit_ptr]
            for i in range(len(carrier_flat))[::8]:
                pre_pixel = (carrier_flat[i:i + 8] & mask_one).astype(str)
                byte_data = ''.join(pre_pixel)
                byte_data = int(byte_data, 2)
                yield byte_data

    def hide(self, carrier_data, hide_data):
        """
        将bytes数据隐写到矩阵数据中
        :param carrier_data: numpy.array 载体矩阵
        :param hide_data: bytes 待隐写消息
        :return: numpy.array 隐写后的载体矩阵
        """
        # 备份载体信息
        bak_shape = carrier_data.shape
        carrier_flat = carrier_data.flatten()
        # 检查载体容量
        pixel_size = carrier_flat.size
        binary_hide_str = "".join(format(byte, "08b") for byte in hide_data)
        hide_len = len(binary_hide_str)
        if pixel_size * self.max_use_bit < hide_len:
            raise SteganographyException("Carrier image not big enough to hold all the data to steganography")

        # 隐写信息分批
        hide_list = [binary_hide_str[i:i + pixel_size] for i in range(0, hide_len, pixel_size)]
        for i, hide_data in enumerate(hide_list):
            hide_data = np.array(list(hide_data))
            mask_one = self.maskONEValues[i]
            mask_zero = self.maskZEROValues[i]
            hide_carrier_flat = carrier_flat[:hide_data.size]
            hide_carrier_flat[hide_data == "1"] = hide_carrier_flat[hide_data == "1"] | mask_one
            hide_carrier_flat[hide_data == "0"] = hide_carrier_flat[hide_data == "0"] & mask_zero
        hide_carrier = carrier_flat.reshape(bak_shape)
        return hide_carrier


if __name__ == "__main__":
    steg = LSB()
    hide_info = b"a"
    test_carrier = cv2.imread("../data/0.png")
    img_encoded = steg.hide(test_carrier, hide_info)
    cv2.imwrite("0_new.png", img_encoded)

    # decoding
    test_carrier = cv2.imread("0_new.png")
    # 读取
    read_opt = steg.read(test_carrier)
    print(next(read_opt))
