from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF
from PySide6.QtWidgets import QHBoxLayout, QApplication, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from qfluentwidgets.common import qconfig
from Configs.application_config import MyConfig
import sys

from Equipments.equipment_interface import EquipmentInterface


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(" ", "-"))


class Window(FluentWindow):
    """主界面"""

    # cfg = MyConfig()
    # qconfig.load('config/config.json')
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.mainPageInterface = Widget("Main Page", self)
        self.equipmentInterface = EquipmentInterface(self)
        self.gameTimerInterface = Widget("gameTimerInterface", self)
        self.toolsInterface = Widget("toolsInterface", self)
        self.settingInterface = Widget("settingInterface", self)
        # 子界面添加到导航栏
        self.initNavigation()
        # 初始化主界面
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.mainPageInterface, FIF.HOME, "主页")
        self.addSubInterface(self.equipmentInterface, FIF.UPDATE, "换装")
        self.addSubInterface(self.gameTimerInterface, FIF.STOP_WATCH, "计时器")
        self.addSubInterface(self.toolsInterface, FIF.QRCODE, "工具")
        self.navigationInterface.addSeparator()
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, "设置", NavigationItemPosition.BOTTOM
        )

    def initWindow(self):

        self.setFixedSize(900, 700)
        self.setWindowIcon(QIcon(":/qfluentwidgets/images/logo.png"))
        self.setWindowTitle("Elsword Helper")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
