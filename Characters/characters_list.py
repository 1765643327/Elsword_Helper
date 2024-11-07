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


class CharactersList(ListWidget):
    character_dict = {
        "CET": "/home/zk/Vscode_WorkSpace/Elsword_Helper/Icon_-_Knight_Emperor.png"
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.container_layout = QVBoxLayout()
        self.container_layout.setContentsMargins(0, 2, 2, 2)
        self.container_layout.setSpacing(2)
        self.setFixedWidth(100)
        self.setLayout(self.container_layout)
        # 创建角色列表
        self.list_commands = CommandBar()
        self.list_commands.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.list_commands.addAction(Action(FluentIcon.ADD, "添加角色"))
        self.list_commands.setFixedWidth(self.width())
        self.character_list = ListWidget()
        self.character_list.setFixedWidth(self.width())
        self.character_list.setIconSize(QSize(24, 24))
        self.container_layout.addWidget(self.list_commands, Qt.AlignLeft)
        self.container_layout.addWidget(self.character_list, Qt.AlignLeft)
        for k, v in self.character_dict.items():
            item = QListWidgetItem(k)
            item.setSizeHint(QSize(self.width() - 10, 30))
            item.setIcon(QIcon(v))
            item.setTextAlignment(Qt.AlignCenter)
            self.character_list.addItem(item)

        self.character_object_dict = {}
