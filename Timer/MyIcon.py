from qfluentwidgets.components.widgets import IconWidget
from PyQt5.QtWidgets import QFileDialog
from PIL import Image
import os

class MyIcon(IconWidget):
    def __init__(self, parent, icon_path, basedir):
        super().__init__()
        self.basedir = basedir
        if icon_path!=None:
            self.icon = icon_path  # 设置图标路径
        else:
            self.icon = os.path.join(basedir, r"images\\bufficon\\default.png")  # 设置默认图标

    def resize_image_with_transparency(self,input_path, output_path, size=(64, 64)):
        # 打开原始图像
        original_image = Image.open(input_path)

        # 计算原图的纵横比
        original_ratio = original_image.width / original_image.height
        target_ratio = size[0] / size[1]

        # 计算新的图像尺寸
        if original_ratio > target_ratio:
            new_width = size[0]  # 目标宽度
            new_height = int(size[0] / original_ratio)  # 根据纵横比计算高度
        else:
            new_height = size[1]  # 目标高度
            new_width = int(size[1] * original_ratio)  # 根据纵横比计算宽度

        # 调整图像大小
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

        # 创建一个透明背景的图像
        new_image = Image.new("RGBA", size, (0, 0, 0, 0))

        # 计算放置调整后图像的位置
        x_offset = (size[0] - new_width) // 2
        y_offset = (size[1] - new_height) // 2

        # 将调整后的图像粘贴到透明图像上
        new_image.paste(resized_image, (x_offset, y_offset))

        # 保存新图像
        new_image.save(output_path)
 
    def mousePressEvent(self, event):
        super().mousePressEvent(event)  # 调用父类的鼠标按下事件
        # 打开文件选择对话框
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "*.png;*.jpg;*.jpeg", options=options)
        if fileName:
            filename = os.path.basename(fileName)  # 获取文件名
            save_path = os.path.join(self.basedir, r"images\\bufficon\\"+filename)  # 保存路径
            self.resize_image_with_transparency(fileName, save_path)  # 调用自定义的图像处理函数
            self.setIcon(save_path)  # 设置新的图标
            self.parent().resetConfig()

    