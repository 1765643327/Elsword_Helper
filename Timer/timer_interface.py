# coding:utf-8
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel
from qfluentwidgets import SegmentedWidget
from .buff_timer_interface import BuffTimerInterface


class TimerInterface(QWidget):
    _instance = None

    # 重写__new__方法保证该组件只被实例化一次
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TimerInterface, cls).__new__(cls)
        return cls._instance

    def __init__(self,parent,basedir,*args, **kwargs):
        super().__init__()
        self.setObjectName("timer_interface")
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

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.machineInterface = QLabel(self)
        self.buffInterface = BuffTimerInterface(self,'bufftimerinterface',basedir)

        # 添加子界面
        self.addSubInterface(self.machineInterface, "machine", "副本机制")
        self.addSubInterface(self.buffInterface, "buff", "BUFF")

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.setCurrentWidget(self.machineInterface)
        self.pivot.setCurrentItem(self.machineInterface.objectName())
        self.pivot.currentItemChanged.connect(
            lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k))
        )

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)

