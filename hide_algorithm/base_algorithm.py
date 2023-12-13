from abc import abstractmethod


class BaseAlgorithm(object):
    """
    隐写算法基类
    """

    @abstractmethod
    def check_carrier(self, carrier_data):
        """
        有效隐写载体检查
        :param carrier_data: 隐写载体数据
        :return: bool
        """
        pass

    @abstractmethod
    def read(self, carrier_data):
        """
        数据读取迭代器
        :carrier_data: 载体图像数据 PIL ImageFile
        :return: 成功数据读取迭代器，未成功读取返回None
        """

    @abstractmethod
    def hide(self, carrier_data, hide_data):
        """
        在位图像中隐写数据，图像会被转换成四通道，每个像素写入1bits信息
        :param carrier_data: 载体图像数据 PIL ImageFile
        :param hide_data: 待隐写的二进制数据
        :return:
        """
        pass
