from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QColor,QPen
from PyQt5.QtCore import Qt,QEvent
from PyQt5.QtGui import QCursor
from qfluentwidgets.components.layout import FlowLayout
from .timericon import TimerWidget

class TimerMonitor(QFrame): 
    def __init__(self, parent):
        super().__init__()
        self.timer_interface = parent
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint| Qt.Tool)  # 设置无边框
        self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.resize(300, 100)  # 设置窗口初始大小
        self.setContentsMargins(0,0,0,0)  # 设置窗口内边距为0
        self.mylayout = FlowLayout(self,isTight=True)
        self.mylayout.setHorizontalSpacing(5)
        self.mylayout.setVerticalSpacing(5)
        self.mylayout.setContentsMargins(5,5,5,5)
        self.old_pos = None
        self.resizing = False  # 记录是否正在调整大小
        self.mouseIn = False  # 记录鼠标是否在窗口内
        self.update()

    def paintEvent(self, event):
       
        # 在窗口范围绘制边框
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255,255,255,1))
        if not self.mouseIn:
            return
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置边框颜色和宽度
        
        border_color = QColor(0, 0, 255, 100)  # 带透明度的蓝色边框
        border_pen = QPen(border_color, 10)
        painter.setPen(border_pen)
        painter.setBrush(QColor(0, 0, 0, 0))  # 背景透明

        # 绘制矩形边框
        painter.drawRect(self.rect())  # 绘制整个窗口的边框
        #   # 绘制背景色

    def enterEvent(self, event):
        # 鼠标进入窗口时设置光标为默认样式
        self.mouseIn = True
        self.update()
        self.setCursor(QCursor(Qt.ArrowCursor))

    def leaveEvent(self, event):
        # 鼠标离开窗口时设置光标为默认样式
        self.mouseIn = False
        self.update()
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            mouseX = event.x()
            mouseY = event.y()
            # 判断是否在右下角进行调整
            if mouseX > self.width() - 10 and mouseY > self.height() - 10:
                self.resizing = True
            else:
                self.old_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        mouseX = event.x()
        mouseY = event.y()
        # print("mouseMoveEvent: ", mouseX, mouseY)

        # 设置光标样式
        if mouseX > self.width() - 10 and mouseY > self.height() - 10:
            self.setCursor(QCursor(Qt.SizeFDiagCursor))  # 右下角调整
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))  # 默认光标样式

        # 处理窗口拖动或调整大小
        if self.resizing and event.buttons() == Qt.LeftButton:
            # 更新窗口大小
            self.resize(event.globalX() - self.x(), event.globalY() - self.y())
            event.accept()
        elif event.buttons() == Qt.LeftButton and self.old_pos:
            self.move(event.globalPos() - self.old_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.resizing = False  # 结束调整大小状态
        self.setCursor(QCursor(Qt.ArrowCursor))  # 恢复默认光标样式


    def addWidget(self, widget):
        if isinstance(widget, TimerWidget):
            self.mylayout.addWidget(widget)
            widget.show()
            self.update()
        else:
            self.mylayout.addWidget(widget)
            self.update()

    def removeWidget(self, widget):
        widget.hide()
        self.mylayout.removeWidget(widget)
        self.update()

    
   