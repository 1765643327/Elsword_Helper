# coding:utf-8
import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF
from utils.files_processer import DataProcess
from Settings.setting_interface import Setting_interface
from Timer.timer_interface import TimerInterface
from Equipment.equ_interface import Equipments_interface
from Tools.Tools_interface import ToolsInterface

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text)


class Window(FluentWindow):
    """主界面"""

    def __init__(self):
        super().__init__()
        self.settings = DataProcess.get_json_content(
            os.path.join(BASE_DIR, r"Userdata\settings.json")
        )
        self.setupInterfaces()
        self.initWindow()

    def setupInterfaces(self):
        """初始化所有子界面"""
        try:
            self.homeInterface = Widget("主页开发中", self)
            self.utilsInterface = ToolsInterface(self,BASE_DIR)
            self.timerInterface = TimerInterface(None)
            self.equipmentInterface = Equipments_interface(BASE_DIR)
            self.settingInterface = Setting_interface(
                self.settings,
                path=os.path.join(BASE_DIR, r"Userdata\settings.json"),
            )
            self.initNavigation()
        except Exception as e:
            print(f"初始化子界面失败: {e}")

    def initNavigation(self):
        """初始化导航"""
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")
        self.addSubInterface(self.timerInterface, FIF.STOP_WATCH, "计时器")
        self.addSubInterface(self.equipmentInterface, FIF.UPDATE, "换装")
        self.addSubInterface(self.utilsInterface, FIF.QRCODE, "工具箱")
        self.navigationInterface.addSeparator()
        self.addSubInterface(
            self.settingInterface,
            FIF.SETTING,
            "设置", 
            NavigationItemPosition.BOTTOM,
        )

    def initWindow(self): 
        """初始化窗口设置"""
        self.setFixedSize(900, 700)
        icon_path = os.path.join(BASE_DIR, r"images\Icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"图标文件不存在: {icon_path}")
        self.setWindowTitle("Elsword Helper")


if __name__ == "__main__":
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling) 
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        app = QApplication(sys.argv)
        window = Window()
        window.show()
        app.exec()
    except Exception as e:
        print(f"程序启动失败: {e}")

