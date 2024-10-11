# coding:utf-8
import time
import threading
from utils.files_processer import DataProcess as DP
from Scripts.Automatic import AutoEquipment
from .tooltip_slider import Tooltip_Slider
from PyQt5.QtCore import Qt
from functools import partial
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import (
    TogglePushButton,
    MessageBox,
    PrimaryPushButton,
    InfoBar,
    InfoBarPosition,
)
from qfluentwidgets.components.settings import ExpandGroupSettingCard
from qfluentwidgets.components.widgets.label import BodyLabel
from qfluentwidgets.components.widgets import SwitchButton
from qfluentwidgets import FluentIcon
from qfluentwidgets.components import IndicatorPosition
import keyboard
from qfluentwidgets import FluentIcon as FIF

import sys

sys.path.append("..")


class PowerSettingCard(ExpandGroupSettingCard):
    def __init__(self, parent, _id, json_data):
        super().__init__(
            FluentIcon.SETTING,
            f"{json_data['setting_name']}",
            f"{json_data['description']}",
        )

        self.setObjectName(_id)
        self.temp_parent = parent
        self.setting_msg = json_data.copy()
        self.auto_equ = AutoEquipment(
            self, SAVE_SIGNAL_KEY=self.setting_msg["save_cor_key"], ACTIVE_SIGNAL_KEY=self.setting_msg["active_key"], EQU_KEY=self.setting_msg["item_key"])

        self.task = threading.Thread(
            target=self.auto_equ.run_script,
            daemon=True,
        )

        self.lable_list = []
        self.button_list = []
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # 第一组
        self.modeButton1 = TogglePushButton(
            self.setting_msg["active_key"].title())
        self.modeButton1.setObjectName(f"{self.objectName}_触发按键")
        self.modeLabel1 = BodyLabel("触发按键")
        self.lable_list.append(self.modeLabel1)
        self.button_list.append(self.modeButton1)

        # 第二组
        self.modeButton2 = TogglePushButton(
            self.setting_msg["save_cor_key"].title())
        self.modeButton2.setObjectName(f"{self.objectName}_保存坐标序列按键")
        self.modeLabel2 = BodyLabel("保存坐标序列按键")
        self.lable_list.append(self.modeLabel2)
        self.button_list.append(self.modeButton2)

        # 第三组
        self.modeButton3 = TogglePushButton(
            self.setting_msg["item_key"].title())
        self.modeButton3.setObjectName(f"{self.objectName}_物品栏按键")
        self.modeLabel3 = BodyLabel("物品栏按键")
        self.lable_list.append(self.modeLabel3)
        self.button_list.append(self.modeButton3)

        # 调整内部布局
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)

        # 启动关闭按钮
        self.switch = SwitchButton(self, IndicatorPosition.RIGHT)
        self.addWidget(self.switch)
        self.switch.checkedChanged.connect(self.start_service)

        # 添加各组到设置卡中
        for i in range(3):
            self.add(self.lable_list[i], self.button_list[i])
            self.button_list[i].clicked.connect(
                partial(
                    self.setbutton,
                    self.lable_list[i],
                    self.button_list[i],
                )
            )

        # 挑战操作间隔按钮
        self.tootip_slider = Tooltip_Slider(
            self, self.setting_msg["time_gap"], self.setting_msg
        )
        self.addGroupWidget(self.tootip_slider.w1)

        # 初始化删除按钮及其功能
        self.delteButton_area = QWidget()
        self.delteButton_area.setFixedHeight(60)
        self.delteButton_layout = QHBoxLayout(self.delteButton_area)
        self.delteButton_layout.setContentsMargins(48, 12, 48, 12)
        self.deleteButton = PrimaryPushButton(
            FIF.DELETE.icon(color="black"), "删除", self.delteButton_area
        )
        self.deleteButton.setStyleSheet("background-color: rgba(255,0,0,0.75)")
        self.delteButton_layout.addWidget(self.deleteButton)
        self.deleteButton.clicked.connect(partial(self.show_delte_dialog))
        self.addGroupWidget(self.delteButton_area)

    def add(self, label, widget):
        w = QWidget()
        w.setFixedHeight(60)
        layout = QHBoxLayout(w)
        layout.setContentsMargins(48, 12, 48, 12)
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(widget)
        self.addGroupWidget(w)

    def setbutton(self, label, button):
        self.switch.setChecked(False)
        key = keyboard.read_hotkey(suppress=False)
        if label.text() == "触发按键":
            self.setting_msg["active_key"] = key.replace(" ", "_")
            button.setText(key.title())
            button.setChecked(False)
            self.auto_equ._set_key(
                self.setting_msg["save_cor_key"],
                self.setting_msg["active_key"],
                self.setting_msg["item_key"],
            )
            return
        if label.text() == "保存坐标序列按键":
            self.setting_msg["save_cor_key"] = key.replace(" ", "_")
            button.setText(key.title())
            button.setChecked(False)
            self.auto_equ._set_key(
                self.setting_msg["save_cor_key"],
                self.setting_msg["active_key"],
                self.setting_msg["item_key"],
            )
            return
        if label.text() == "物品栏按键":
            self.setting_msg["item_key"] = key.replace(" ", "_")
            button.setText(key.title())
            button.setChecked(False)
            self.auto_equ._set_key(
                self.setting_msg["save_cor_key"],
                self.setting_msg["active_key"],
                self.setting_msg["item_key"],
            )
            return

    def start_service(self):

        if self.switch.checked:
            self.auto_equ.terminate_flag = False
            self.star_thread()
        else:
            self.terminate_thread()

    def show_delte_dialog(self):
        w = MessageBox("确认删除", "注意：该设置将被完全清除！", self)
        w.yesButton.clicked.connect(partial(self.delete_settings))
        w.exec()

    def delete_settings(self):
        self.terminate_thread()
        self.temp_parent.delete_settingcard(self.objectName())
        DP.delete_json_content(self.temp_parent.config_path, self.objectName())

    def terminate_thread(self):

        self.setting_msg["cor_list"] = self.auto_equ.get_cor_list()
        self.switch.setEnabled(False)
        self.auto_equ._set_terminate()

        while self.task.is_alive():
            continue
        self.task = threading.Thread(
            target=self.auto_equ.run_script,
            daemon=True,
        )
        self.auto_equ.stopevent = threading.Event()
        DP.set_json_content(self.temp_parent.config_path, self.setting_msg)
        self.switch.setEnabled(True)

    def star_thread(self):
        self.auto_equ.set_cor_list(self.setting_msg["cor_list"])
        self.task.start()

    def createSuccessInfoBar(self, content):
        InfoBar.success(
            title="提示",
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self.nativeParentWidget(),
        )
