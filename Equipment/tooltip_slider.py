# coding:utf-8
from PyQt5.QtCore import Qt
from qfluentwidgets import Slider, LineEdit, BodyLabel
from PyQt5.QtWidgets import QWidget, QHBoxLayout

# from PyQt5.QtGui import QDoubleValidator


class Tooltip_Slider(QWidget):
    def __init__(self, parent, time_gap, setting_msg):
        super().__init__(parent)

        self.slider = Slider(Qt.Horizontal)
        self.setting_msg = setting_msg

        self.slider.setValue(1)  # 默认值
        self.slider.setMinimum(1)  # 最小值
        self.slider.setMaximum(100)  # 最大值
        self.slider.setSingleStep(2)  # 步长
        self.slider_button = LineEdit()
        # self.slider_button.setValidator(QDoubleValidator(self.slider_button))
        self.slider_button.setAlignment(Qt.AlignCenter)
        self.slider_button.setText(str(time_gap))
        self.slider.setValue(int(time_gap * 100))
        self.slider_button.setMinimumWidth(80)
        self.slider_button.setFixedWidth(80)
        self.slider_label = BodyLabel("操作间隔")

        self.slider.setFixedWidth(200)

        self.w1 = QWidget()
        self.w2 = QWidget()
        self.w1.setFixedHeight(60)
        self.layout1 = QHBoxLayout(self.w1)
        self.layout2 = QHBoxLayout(self.w2)
        self.layout2.addWidget(self.slider_label)
        self.layout2.addWidget(self.slider)
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.layout1.setContentsMargins(48, 12, 48, 12)
        self.layout1.addWidget(self.w2)
        self.layout1.addStretch(1)
        self.layout1.addWidget(self.slider_button)

        self.slider.valueChanged.connect(lambda: self.update_button_text(parent))
        self.slider_button.editingFinished.connect(lambda: self.update_slider(parent))
        self.slider_button.returnPressed.connect(lambda: self.update_slider(parent))

        parent.auto_equ._set_time_gap(self.setting_msg["time_gap"])
        pass

    def update_button_text(self, parent):
        # self.switch.setChecked(False)
        # print(self.slider.value, type(self.slider.value))
        self.slider_button.setText("{:.2f}".format((self.slider.value() * 0.01)))
        self.setting_msg["time_gap"] = self.slider.value() * 0.01
        parent.auto_equ._set_time_gap(self.setting_msg["time_gap"])

    def update_slider(self, parent):
        # self.switch.setChecked(False)
        value = float(self.slider_button.text())
        if float(self.slider_button.text()) < 0.01:
            self.slider_button.setText("0.01")
            value = 0.01
            self.slider.setValue(int(value) * 100)
        elif float(self.slider_button.text()) > 1.00:
            self.slider_button.setText("1.00")
            value = 1.00
            self.slider.setValue(int(value) * 100)
        else:
            self.slider.setValue(int(value) * 100)
        self.setting_msg["time_gap"] = self.slider.value() * 0.01
        parent.auto_equ._set_time_gap(self.setting_msg["time_gap"])
        pass
