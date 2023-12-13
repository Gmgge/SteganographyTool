from hide_algorithm.base_algorithm import BaseAlgorithm


class DataTooBig(Exception):
    pass


class LSB(BaseAlgorithm):
    """
    无损压缩位图像隐写，2位LSB， 适用于png，tiff等
    """

    def __init__(self):
        self.mask = 3
        self.carrier_mode = "RGBA"

    def check_carrier(self, carrier_data):
        """
        有效隐写载体检查
        :param carrier_data: 隐写载体数据
        :return: bool
        """
        sign = False
        if carrier_data.mode == self.carrier_mode:
            sign = True
        return sign

    def read(self, carrier_data):
        """
        按照指针依次读取数据
        :carrier_data: 载体图像数据 PIL ImageFile
        :return: 成功返回数据，未成功读取返回None
        """
        read_ptr = 0
        max_len = carrier_data.height * carrier_data.width
        pixels = list(carrier_data.getdata())
        while read_ptr < max_len:
            r, g, b, a = pixels[read_ptr]
            read_info = (r & self.mask) | ((g & self.mask) << 2) | ((b & self.mask) << 4) | ((a & self.mask) << 6)
            yield read_info
            read_ptr += 1

    def hide(self, carrier_data, hide_data):
        """
        在位图像中隐写数据，图像会被转换成四通道，每个像素写入1bits信息
        :param carrier_data: 载体图像数据 PIL ImageFile
        :param hide_data: 待隐写的二进制数据
        :return:
        """
        max_len = carrier_data.height * carrier_data.width
        carrier_data = carrier_data.convert("RGBA")
        pixels = list(carrier_data.getdata())
        if len(hide_data) > max_len:
            raise DataTooBig()
        for i, byte in enumerate(hide_data):
            r, g, b, a = pixels[i]
            r = (r & ~self.mask) | (byte & self.mask)
            g = (g & ~self.mask) | ((byte >> 2) & self.mask)
            b = (b & ~self.mask) | ((byte >> 4) & self.mask)
            a = (a & ~self.mask) | ((byte >> 6) & self.mask)
            pixels[i] = (r, g, b, a)
        carrier_data.putdata(pixels)
        return carrier_data


if __name__ == "__main__":
    import PIL.Image

    img_in = PIL.Image.open(r"D:\py_project\steganography_extraction\data\0.png")
    sto_opt = LSB()
    # 写入
    hide_info = b"a"
    test_data = sto_opt.hide(img_in, hide_info)

    # 读取
    test_read = next(sto_opt.read(test_data))
    print(test_read)
