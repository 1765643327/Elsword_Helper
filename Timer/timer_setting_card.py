from qfluentwidgets.components.widgets import CardWidget, BodyLabel ,LineEdit,SwitchButton,ToolButton
from qfluentwidgets.components import IndicatorPosition
from qfluentwidgets.common import FluentIcon
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from .MyIcon import MyIcon
from .timericon import TimerWidget

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.files_processer import DataProcess as dp

class TimerSettingCard(CardWidget):
    FONT_STYLE = """
               QLabel {
                font-family: '微软雅黑';
                font-weight: bold;
                color: black;
                font-size: 14px;           
            }
        """
    def __init__(self, parent, basedir,id,config=None):
        super().__init__(parent)
        self.basedir = basedir
        self.interface = parent
        if config!=None:
            self.config = config
        else:
            self.config = {
                'id':id,
                'cooldown':'',
                'activate':'',
                'icon':''
            }
        self.setObjectName(id)
        self.iconWidget = MyIcon(self,None, basedir)
        self.cooldownLabel = BodyLabel('⌈冷却时间⌋',self)
        self.cooldownedit = LineEdit(self)
        self.cooldownLabel.setStyleSheet(self.FONT_STYLE)
        self.cooldownedit.setFixedWidth(75)
        self.cooldownedit.setPlaceholderText('单位/秒')
        self.activateLabel = BodyLabel('⌈触发方式⌋',self)
        self.activateedit = LineEdit(self)
        self.activateLabel.setStyleSheet(self.FONT_STYLE)
        self.activateedit.setFixedWidth(300)
        self.activateedit.setPlaceholderText('记录触发按键序列')

        if config!=None:
            self.cooldownedit.setText(str(self.config['cooldown']))
            self.activateedit.setText(str(self.config['activate']))
            self.iconWidget.setIcon(self.config['icon'])

        self.cooldown_layoout = QVBoxLayout()
        self.active_layout = QVBoxLayout()


        self.cooldown_layoout.setStretch(0,1)
        self.cooldown_layoout.setStretch(1,1)
    

        self.active_layout.setStretch(0,1)
        self.active_layout.setStretch(0,1)

        self.cooldown_layoout.addWidget(self.cooldownLabel)
        self.cooldown_layoout.addWidget(self.cooldownedit)
        self.active_layout.addWidget(self.activateLabel)
        self.active_layout.addWidget(self.activateedit)
       
        self.activeButton = SwitchButton('OFF',self,IndicatorPosition.RIGHT)
        self.activeButton.onText = 'ON'

        self.deleteButton = ToolButton(FluentIcon.DELETE,self)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.hBoxLayout = QHBoxLayout(self)

        self.iconWidget.setFixedSize(64, 64)
        self.hBoxLayout.addWidget(self.iconWidget,0,Qt.AlignLeft)
        self.hBoxLayout.addSpacing(20)
        self.hBoxLayout.addLayout(self.cooldown_layoout)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addLayout(self.active_layout)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.activeButton,0,Qt.AlignRight)
        self.hBoxLayout.addWidget(self.deleteButton,0,Qt.AlignRight)
      
        self.setContentsMargins(0,5,0,5)

        self.cooldownedit.editingFinished.connect(self.resetConfig)
        self.activateedit.editingFinished.connect(self.resetConfig)
        self.activeButton.checkedChanged.connect(self.add_or_delete_for_monitor)

        self.timer_widget = TimerWidget(self,self.config)
        
    def deleteButtonClicked(self):
        dp.delete_json_content(os.path.join(self.basedir,r'Userdata\\timersetting.json'),self.config['id'])
        self.interface.deleteTimer(self.objectName())

    def resetConfig(self):
        self.config['cooldown'] = str(self.cooldownedit.text())
        self.config['activate'] = str(self.activateedit.text())
        self.config['icon'] = self.iconWidget._icon
        self.timer_widget.resetConfig(self.config)
        dp.set_json_content(os.path.join(self.basedir,r'Userdata\\timersetting.json'),self.config)


    def add_or_delete_for_monitor(self):
        if self.activeButton.isChecked():
            self.interface.timer_monitor.addWidget(self.timer_widget)
        else:
            self.interface.timer_monitor.removeWidget(self.timer_widget)