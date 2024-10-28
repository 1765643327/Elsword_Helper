from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class CustomFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint)  # 设置无边框
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(400, 300)  # 设置窗口初始大小
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton("这是一个无边框窗口"))
        self.old_pos = None
        self.resizing = False  # 记录是否正在调整大小
        self.mouseIn = False  # 记录鼠标是否在窗口内

    def paintEvent(self, event):
        if not self.mouseIn:
            return
        # 在窗口范围绘制边框
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置边框颜色和宽度
        border_color = QColor(0, 120, 215, 200)  # 带透明度的蓝色边框
        painter.setPen(border_color)
        painter.setBrush(QColor(0, 0, 0, 0))  # 背景透明

        # 绘制矩形边框
        painter.drawRect(self.rect())  # 绘制整个窗口的边框

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主窗口")
        self.setGeometry(100, 100, 600, 400)

        button = QPushButton("打开无边框框架", self)
        button.clicked.connect(self.open_custom_frame)
        self.setCentralWidget(button)

    def open_custom_frame(self):
        self.custom_frame = CustomFrame()
        self.custom_frame.show()


if __name__ == "__main__":
    app = QApplication([])

    main_window = MainWindow()
    main_window.show()

    app.exec_()
