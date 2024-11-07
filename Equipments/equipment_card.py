from qfluentwidgets.components import (
    CardWidget,
    IconWidget,
    LineEdit,
    SwitchButton,
    ToolButton,
)
from qfluentwidgets.common import FluentIcon
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel


class EquipmentCard(CardWidget):
    def __init__(self, parent, equ_data):
        super().__init__(parent)
        self.equ_data = equ_data
        self.icon_widget = IconWidget(FluentIcon.SETTINGS, parent=self)
        # self.icon_widget.mouseDoubleClickEvent =
        self.icon_widget.setFixedSize(28, 28)
        self.message_layout = QHBoxLayout()

        self.setting_layout = QVBoxLayout()
        self.activate_key_layout = QHBoxLayout()
        self.equ_key_layout = QHBoxLayout()
        self.save_sequence_layout = QHBoxLayout()
        self.name_label = QLabel(equ_data["name"], parent=self)
        self.name_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.activate_key_label = QLabel("启动换装: ", parent=self)
        self.activate_key_edit = LineEdit(equ_data["activate_key"], parent=self)

        self.equ_key_label = QLabel("装备栏: ", parent=self)
        self.equ_key_edit = LineEdit(equ_data["equ_key"], parent=self)

        self.save_sequence_label = QLabel("保存序列: ", parent=self)
        self.save_sequence_edit = LineEdit(equ_data["save_sequence"], parent=self)

        self.activate_key_layout.addWidget(self.activate_key_label)
        self.activate_key_layout.addWidget(self.activate_key_edit)

        self.equ_key_layout.addWidget(self.equ_key_label)
        self.equ_key_layout.addWidget(self.equ_key_edit)

        self.save_sequence_layout.addWidget(self.save_sequence_label)
        self.save_sequence_layout.addWidget(self.save_sequence_edit)

        self.setting_layout.addLayout(self.activate_key_layout)
        self.setting_layout.addLayout(self.equ_key_layout)
        self.setting_layout.addLayout(self.save_sequence_layout)

        self.load_setting_button = SwitchButton()
        self.delete_button = ToolButton(FluentIcon.DELETE, parent=self)
        self.message_layout.addWidget(self.icon_widget)
        self.message_layout.addLayout(self.setting_layout)
        self.message_layout.addWidget(self.load_setting_button)
        self.message_layout.addWidget(self.delete_button)
        self.setLayout(self.message_layout)
