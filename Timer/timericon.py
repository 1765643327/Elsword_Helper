
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import QTimer, Qt
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Scripts.Timer_keyboard import TimerManager

class TimerWidget(QWidget):
    icon_size = 56
    def __init__(self,parent,config):
        super().__init__()
        self.timer_card = parent
        self.timer_working = False
        # 设置初始时间
        if config['cooldown'] == '':
            self.initial_time = 0
        else:
            self.initial_time = int(config['cooldown'])
        self.time_left = self.initial_time
        # 创建标签用于显示图像
        self.image_label = QLabel(self)
        self.original_pixmap = QPixmap(config['icon']).scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio)  # 替换为你的图像路径
        # 设置布局
        self.image_label.setMargin(0)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        # 添加事件
        self.keyboard_listener = TimerManager(self,config)
        self.image_label.setPixmap(self.original_pixmap)

       
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.update_image()
        else:
            self.timer_working = False
            self.timer.stop()

    def update_image(self):
        pixmap = self.original_pixmap.copy()
        painter = QPainter(pixmap)
        if self.time_left > 0:
            # 增加黑色半透明遮罩
            painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 150))

            # 显示时间数字
            painter.setPen(Qt.green)
            painter.setFont(QFont("Arial", 16, QFont.Bold))
            painter.drawText(pixmap.rect(), Qt.AlignCenter,
                             str(self.time_left))
        painter.end()
        self.image_label.setPixmap(pixmap)

    def start_timer(self):
        if self.timer_working == False:
            self.timer_working = True
            self.time_left = self.initial_time
            self.timer.start(1000)
    
    def resetConfig(self,config):
        self.initial_time = int(config['cooldown'])
        self.time_left = self.initial_time
        self.keyboard_listener.reset_input_sequence(config)
        self.original_pixmap = QPixmap(config['icon']).scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio)  # 替换为你的图像路径
        self.image_label.setPixmap(self.original_pixmap)