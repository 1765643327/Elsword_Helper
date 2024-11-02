# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy,QLabel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from qfluentwidgets.components import CommandBar
from qfluentwidgets.common import FluentIcon, Action
from .timer_setting_card import TimerSettingCard
from .timermonitor import TimerMonitor
import random,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.files_processer import DataProcess as dp
class BuffTimerInterface(QWidget):

    _instance = None

    # 重写__new__方法保证该组件只被实例化一次
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BuffTimerInterface, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent, objname, basedir):
        super().__init__()
        self.setObjectName(objname)
        self.base_dir = basedir
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
        self.command = CommandBar(self)
        self.command.addActions([
    Action(FluentIcon.ADD, '新建', triggered=self.add_timer_card),
    Action(FluentIcon.PLAY, '启动', checkable=True,triggered=self.showTimerMonitor),
])
        self.mylayout.addWidget(self.command)
        self.mylayout.addWidget(self.scroller)
        self.existed_config = dp.get_json_content(os.path.join(self.base_dir, r'Userdata\timersetting.json'))
        if self.existed_config!=[]:
            for item in self.existed_config:
                self.templayout.addWidget(TimerSettingCard(self, self.base_dir, item['id'],config=item))

        self.setLayout(self.mylayout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.timer_car_dict = {}

        self.timer_monitor = TimerMonitor(self)


    def add_timer_card(self):
        card_object_name = self.generate_random_sequence()
        new_card = TimerSettingCard(self, self.base_dir, card_object_name)
        self.timer_car_dict[card_object_name] = new_card
        self.templayout.addWidget(new_card)
        self.container.setLayout(self.templayout)
        self.scroller.update()
    
    def deleteTimer(self, card_object_name):
        del_widget = self.findChild(TimerSettingCard, card_object_name)
        self.templayout.removeWidget(del_widget)
        del_widget.deleteLater()
        self.container.setLayout(self.templayout)
        self.scroller.update()
    
    def showTimerMonitor(self):
        if self.command.actions()[1].isChecked():
            self.timer_monitor.show()
        else:
            self.timer_monitor.hide()

    def generate_random_sequence(self, length=10, range_start=0, range_end=9):
        return ''.join(str(i) for i in [random.randint(range_start, range_end) for _ in range(length)])
    
