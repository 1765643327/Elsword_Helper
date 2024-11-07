from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from qfluentwidgets.components import ListWidget, CommandBar, ComboBox
from qfluentwidgets.common import Action, FluentIcon
import sys, os
import random

sys.path.append("..")
sys.path.append(os.path.dirname(__file__))
from Characters.characters_list import CharactersList
from equipment_container import EquipmentContainer
from equipment_card import EquipmentCard


class EquipmentInterface(QWidget):
    character_msg = ["CET"]

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("EquipmentInterface")
        # 创建界面不同部分的布局
        self.characters = CharactersList(self)
        self.container_layout = QHBoxLayout()
        self.container_layout.setContentsMargins(0, 2, 2, 2)
        self.selcet_container = QHBoxLayout()
        # 创建命令栏
        self.commands = CommandBar()
        self.commands.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commands.addActions([Action(FluentIcon.ADD, "新建设置", triggered=self.add_equipment)])

        # 创建配置选择框
        self.comboxBox = ComboBox()
        self.comboxBox.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 255, 255, 100); /* 半透明白色背景 */
                color: rgba(0, 0, 0, 255); /* 文字颜色 */
                padding-right: 30px; /* 内边距 */
                border: none; /* 无边框 */
                border-radius: 10px; /* 圆角 */
                font-size: 13px; /* 字体大小 */
            }
            # QPushButton:hover {
            #     background-color: rgba(255, 255, 255, 200); /* 鼠标悬停时更亮 */
            #     color:  rgba(0, 0, 0, 255); /* 按下时更暗 */
            # }
            """
        )
        # self.comboxBox.setPlaceholderText("选择配置")
        # self.comboxBox.addItems(["设置1", "设置2", "设置3"])
        self.comboxBox.currentIndexChanged.connect(
            lambda index: print(self.comboxBox.currentText())
        )
        self.selcet_container.addWidget(self.commands, 0, Qt.AlignLeft)
        self.selcet_container.addWidget(self.comboxBox, 0, Qt.AlignRight)
        # self.commands.setEnabled(False)
        # self.comboxBox.setEnabled(False)
        # 创建换装配置
        self.equipments = EquipmentContainer(self)
        self.equipments.setStyleSheet("QWidget{background-color: #F0F0F0;}")

        self.equipment_layout = QVBoxLayout()
        self.container_layout.addWidget(self.characters, Qt.AlignLeft)
        self.container_layout.addLayout(self.equipment_layout, Qt.AlignRight)
        self.equipment_layout.addLayout(self.selcet_container, Qt.AlignTop)
        self.equipment_layout.addWidget(self.equipments, Qt.AlignBottom)

        self.setLayout(self.container_layout)
        # self.hide_equipments(True)
        # 创建装备列表
        pass

    def hide_equipments(self, flag):
        if flag:
            for i in range(self.equipment_layout.layout().count()):
                self.equipment_layout.itemAt(i).widget().hide()
        else:
            for i in range(self.equipment_layout.layout().count()):
                self.equipment_layout.itemAt(i).widget().show()

    def add_equipment(self, equipment):
        init_data = {
            'id': self.generate_random_sequence(10),
            "name": "换装测试",
            'equ_key':'f1',
            'activate_key':'f1',
            'save_sequence':'f1',
        }
        card = EquipmentCard(equipment,init_data)
        self.equipments.add_item(card,init_data['id'])

    def generate_random_sequence(self, length=10, range_start=0, range_end=9):
        return ''.join(str(i) for i in [random.randint(range_start, range_end) for _ in range(length)])