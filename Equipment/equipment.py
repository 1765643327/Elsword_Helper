# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from qfluentwidgets import (
    Action,
    MenuAnimationType,
    RoundMenu,
)
import time, random
from qfluentwidgets import FluentIcon as FIF
import sys

sys.path.append("..")
from .setting_dialog import CustomMessageBox
from .setting_card import PowerSettingCard
from utils.files_processer import DataProcess


class Equipments(QWidget):
    def __init__(self, objname, config_path):
        super().__init__()
        self.setObjectName(objname)
        self.config_path = config_path
        self.temp_data = {
            "id": None,
            "setting_name": "None",
            "description": "None",
            "active_key": "f1",
            "save_cor_key": "space",
            "time_gap": 0.05,
            "item_key": "i",
            "cor_list": [],
        }

        self.scroller = QScrollArea(self)
        self.scroller.setAlignment(Qt.AlignTop)
        self.scroller.setWidgetResizable(True)
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setStyleSheet("background: transparent")
        self.scroller.setWidget(self.container)
        self.templayout = QVBoxLayout(self.container)
        self.templayout.setContentsMargins(0, 0, 0, 0)
        self.templayout.setAlignment(Qt.AlignTop)
        self.scroller.setStyleSheet(
            """
            QScrollArea { border: none; background: transparent; border-radius: 5px;}
            QScrollBar:vertical { border: none; background: transparent; width: 10px; }
            QScrollBar:horizontal { border: none; background: transparent; height: 10px; }
            QScrollBar::handle { background: gray; border-radius: 5px; }
            QScrollBar::add-line, QScrollBar::sub-line { background: none; }
            """
        )

        self.mylayout = QVBoxLayout(self)
        self.config_list = DataProcess.get_json_content(self.config_path)
        self.instance_dict = {}
        for item in self.config_list:
            name = item["id"]
            temp = PowerSettingCard(self, name, item)
            self.instance_dict[name] = temp
            self.templayout.addWidget(temp)

        self.mylayout.addWidget(self.scroller)
        self.setLayout(self.mylayout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def contextMenuEvent(self, e):
        menu = RoundMenu(parent=self)
        new = Action(FIF.ADD, "新建设置")
        help = Action(FIF.HELP, "帮助")
        new.triggered.connect(self.showDialog)
        menu.addAction(new)
        menu.addAction(help)
        menu.exec(e.globalPos(), aniType=MenuAnimationType.DROP_DOWN)
        pass

    def showDialog(self):
        w = CustomMessageBox(self)
        w.yesButton.clicked.connect(lambda: self.create_setting_card(w))
        w.exec()
        pass

    def create_setting_card(self, w):
        seed = int(time.time())
        random.seed(seed)
        self.temp_data["id"] = str(random.randint(1, 1000000))
        self.temp_data["setting_name"] = w.name_LineEdit.text()
        self.temp_data["description"] = w.descript1_LineEdit.text()
        temp = PowerSettingCard(self, self.temp_data["id"], self.temp_data)
        self.instance_dict[self.temp_data["id"]] = temp
        self.templayout.addWidget(temp)
        pass

    def delete_settingcard(self, deleted_id):
        del_widget = self.findChild(PowerSettingCard, deleted_id)
        self.mylayout.removeWidget(del_widget)
        del_widget.deleteLater()

        pass
