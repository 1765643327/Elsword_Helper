from qfluentwidgets.components import (
    CardWidget,
    IconWidget,
    LineEdit,
    SwitchButton,
    ToolButton,
    IndicatorPosition
)
from qfluentwidgets.common import FluentIcon
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt,QSize

LABEL_STYLE = """
    QLabel {
        font-size: 13px;
        font-weight: bold;
        font-family: "微软雅黑";
    }
"""
LABEL_SIZE = QSize(100,30)
EDIT_SIZE = QSize(150,30)
DELETE_BUTTON_STYLE = """
    QToolButton:hover {
        background-color: rgba(255, 0, 0, 0.65);
        border-radius: 5px;
    }
"""
class EquipmentCard(CardWidget):
    def __init__(self, parent, equ_data):
        super().__init__()
        self.equ_data = equ_data
        self.setFixedHeight(150)
        self.message_layout = QHBoxLayout() 
        self.message_layout.setContentsMargins(10, 10, 5, 10)

        self.setting_layout = QVBoxLayout()
        self.activate_key_layout = QHBoxLayout()
        self.equ_key_layout = QHBoxLayout()
        self.save_sequence_layout = QHBoxLayout()
        self.name_label = QLabel(equ_data["name"], parent=self)
        self.name_label.setFixedSize(200, 30)
        self.name_label.setStyleSheet("font-size: 16px; font-weight: bold;font-family: '微软雅黑';")

        self.activate_key_label = QLabel("⌈启动换装按键⌋", parent=self)
        self.activate_key_label.setStyleSheet(LABEL_STYLE)
        self.activate_key_label.setFixedSize(LABEL_SIZE)
        self.activate_key_edit = LineEdit()
        self.activate_key_edit.setFixedSize(EDIT_SIZE)

        self.equ_key_label = QLabel("⌈装备栏按键⌋", parent=self)
        self.equ_key_label.setStyleSheet(LABEL_STYLE)
        self.equ_key_label.setFixedSize(LABEL_SIZE)
        self.equ_key_edit = LineEdit()
        self.equ_key_edit.setFixedSize(EDIT_SIZE)

        self.save_sequence_label = QLabel("⌈保存序列按键⌋", parent=self)
        self.save_sequence_label.setStyleSheet(LABEL_STYLE)
        self.save_sequence_label.setFixedSize(LABEL_SIZE)
        self.save_sequence_edit = LineEdit()
        self.save_sequence_edit.setFixedSize(EDIT_SIZE)

        self.speed_layout = QVBoxLayout()
        self.click_speed_layout = QHBoxLayout()
        self.move_speed_layout = QHBoxLayout()
        self.click_speed_layout.setContentsMargins(5, 0, 0, 0)
        self.move_speed_layout.setContentsMargins(5, 0, 0, 0)
        self.mouseclikcSpeed_label = QLabel("⌈鼠标点击速度⌋", parent=self)
        self.mouseclikcSpeed_label.setStyleSheet(LABEL_STYLE)
        self.mouseclikcSpeed_label.setFixedSize(LABEL_SIZE)
        self.mouseclikcSpeed_edit = LineEdit()
        self.mouseclikcSpeed_edit.setFixedSize(EDIT_SIZE)

        self.mousemoveSpeed_label = QLabel("⌈鼠标移动速度⌋", parent=self)
        self.mousemoveSpeed_label.setStyleSheet(LABEL_STYLE)
        self.mousemoveSpeed_label.setFixedSize(LABEL_SIZE)
        self.mousemoveSpeed_edit = LineEdit()
        self.mousemoveSpeed_edit.setFixedSize(EDIT_SIZE)

        self.click_speed_layout.addWidget(self.mouseclikcSpeed_label,Qt.AlignmentFlag.AlignLeft)
        self.click_speed_layout.addWidget(self.mouseclikcSpeed_edit,Qt.AlignmentFlag.AlignLeft)
        self.move_speed_layout.addWidget(self.mousemoveSpeed_label,Qt.AlignmentFlag.AlignLeft)
        self.move_speed_layout.addWidget(self.mousemoveSpeed_edit,Qt.AlignmentFlag.AlignLeft)
        self.speed_layout.addStretch(1)
        self.speed_layout.addLayout(self.click_speed_layout,Qt.AlignmentFlag.AlignBottom)
        self.speed_layout.addLayout(self.move_speed_layout,Qt.AlignmentFlag.AlignBottom)
        
        

        self.activate_key_layout.addWidget(self.activate_key_label,Qt.AlignmentFlag.AlignRight)
        self.activate_key_layout.addWidget(self.activate_key_edit,Qt.AlignmentFlag.AlignLeft)

        self.equ_key_layout.addWidget(self.equ_key_label,Qt.AlignmentFlag.AlignRight)
        self.equ_key_layout.addWidget(self.equ_key_edit,Qt.AlignmentFlag.AlignLeft)

        self.save_sequence_layout.addWidget(self.save_sequence_label,Qt.AlignmentFlag.AlignRight)
        self.save_sequence_layout.addWidget(self.save_sequence_edit,Qt.AlignmentFlag.AlignLeft)

        self.setting_layout.addWidget(self.name_label,Qt.AlignmentFlag.AlignLeft)
        self.setting_layout.addLayout(self.activate_key_layout,Qt.AlignmentFlag.AlignLeft)
        self.setting_layout.addLayout(self.equ_key_layout,Qt.AlignmentFlag.AlignLeft)
        self.setting_layout.addLayout(self.save_sequence_layout,Qt.AlignmentFlag.AlignLeft)

        self.load_setting_button = SwitchButton(indicatorPos=IndicatorPosition.RIGHT)
        self.delete_button = ToolButton(FluentIcon.DELETE, parent=self)
        self.delete_button.setFixedSize(80, 30)
        self.delete_button.setStyleSheet(DELETE_BUTTON_STYLE)
        self.button_layout = QVBoxLayout()
        
        self.button_layout.addWidget(self.load_setting_button,Qt.AlignmentFlag.AlignTop)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.delete_button,Qt.AlignmentFlag.AlignBottom)

        self.message_layout.addLayout(self.setting_layout,Qt.AlignmentFlag.AlignLeft)
        self.message_layout.addLayout(self.speed_layout,Qt.AlignmentFlag.AlignLeft)
        self.message_layout.addStretch(1)
        self.message_layout.addLayout(self.button_layout,Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.message_layout)
