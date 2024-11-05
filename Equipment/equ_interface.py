# coding:utf-8
from PyQt5.QtWidgets import (
    QWidget,
    QStackedWidget,
    QVBoxLayout,

    QWidget,

)
from qfluentwidgets import (
    setTheme,

)
from .equipment import Equipments
import os


class Equipments_interface(QWidget):

    _instance = None

    # 重写__new__方法保证该组件只被实例化一次
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Equipments_interface, cls).__new__(cls)
        return cls._instance

    def __init__(self, root):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet(
            """
            Demo{background: white}
            QLabel{
                font: 20px 'Segoe UI';
                background: rgb(242,242,242);
            }
        """
        )
        self.setObjectName("equInterface")
        self.config_path = os.path.join(root, "Userdata\equipment.json")

        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.equipmentInterface = Equipments("Equipments", self.config_path)
        self.equipmentInterface.setObjectName("equInterface")
        self.stackedWidget.addWidget(self.equipmentInterface)
        self.stackedWidget.setCurrentWidget(self.equipmentInterface)
