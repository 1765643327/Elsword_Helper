# coding:utf-8
from PyQt5.QtWidgets import (
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QLabel,
    QWidget,
    QLabel,
)
from qfluentwidgets import (
    setTheme,
    SegmentedWidget,
)
from .equ_settting import EquSetting
from .timer_setting import TimerSetting


class Setting_interface(QWidget):

    _instance = None

    # 重写__new__方法保证该组件只被实例化一次
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Setting_interface, cls).__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setObjectName("settings")
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
        self.settings = args[0]
        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.characterInterface = TimerSetting(self, path=kwargs["path"])
        self.equipmentInterface = EquSetting(self, path=kwargs["path"])

        # add items to pivot
        self.addSubInterface(self.equipmentInterface, "albumInterface", "换装")
        self.addSubInterface(self.characterInterface, "timer", "计时器")

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.setCurrentWidget(self.equipmentInterface)
        self.pivot.setCurrentItem(self.equipmentInterface.objectName())
        self.pivot.currentItemChanged.connect(
            lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k))
        )

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)
