from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidgetItem,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from qfluentwidgets.components import ListWidget, CommandBar
from qfluentwidgets.common import Action, FluentIcon


class EquipmentInterface(QWidget):
    character_msg = ["CET"]

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("EquipmentInterface")
        # 创建界面不同部分的布局
        self.container_layout = QHBoxLayout()
        self.commands = CommandBar()
        self.commands.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commands.addActions(
            [
                Action(
                    FluentIcon.EDIT,
                    "编辑",
                    checkable=True,
                    triggered=lambda: print("编辑"),
                ),
                Action(FluentIcon.COPY, "复制"),
                Action(FluentIcon.SHARE, "分享"),
            ]
        )
        self.commands.setEnabled(False)
        self.equipments = QWidget(self)
        self.character_select_layout = QVBoxLayout()
        self.equipment_layout = QVBoxLayout()
        self.container_layout.addLayout(self.character_select_layout, Qt.AlignLeft)
        self.container_layout.addLayout(self.equipment_layout, Qt.AlignRight)
        self.equipment_layout.addWidget(self.commands, Qt.AlignTop)
        self.equipment_layout.addWidget(self.equipments, Qt.AlignBottom)

        self.setLayout(self.container_layout)
        # 创建角色列表
        self.list_commands = CommandBar()
        self.list_commands.addActions(
            [
                Action(FluentIcon.EDIT, "选择角色"),
                Action(FluentIcon.COPY, "删除角色"),
            ]
        )

        self.character_list = ListWidget()
        self.list_commands.setFixedWidth(100)
        self.character_list.setFixedWidth(100)
        self.character_list.setIconSize(QSize(24, 24))

        self.character_select_layout.addWidget(self.list_commands)
        self.character_select_layout.addWidget(self.character_list)
        for character in self.character_msg:
            item = QListWidgetItem(character)
            item.setIcon(
                QIcon(
                    "/home/zk/Vscode_WorkSpace/Elsword_Helper/Icon_-_Knight_Emperor.png"
                )
            )
            item.setTextAlignment(Qt.AlignCenter)
            self.character_list.addItem(item)
        self.hide_equipments(True)
        # 创建装备列表

        pass

    def hide_equipments(self, flag):
        if flag:
            for i in range(self.equipment_layout.layout().count()):
                self.equipment_layout.itemAt(i).widget().hide()
        else:
            for i in range(self.equipment_layout.layout().count()):
                self.equipment_layout.itemAt(i).widget().show()
