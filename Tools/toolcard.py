from qfluentwidgets import CardWidget, IconWidget, BodyLabel, CaptionLabel, PushButton, SwitchButton, IndicatorPosition
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt


class ToolCard(CardWidget):

    def __init__(self, icon, title, content, parent=None,**kwargs):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.switchButton = SwitchButton(self, IndicatorPosition.LEFT)
        # self.iconWidget.setStyleSheet("IconWidget { background-color: rgba(255, 255, 255, 0); }")
        self.titleLabel.setStyleSheet(
            "BodyLabel { background-color: rgba(255, 255, 255, 0);font-size: 16px;font-family: 黑体; }")
        self.contentLabel.setStyleSheet(
            "CaptionLabel { background-color: rgba(255, 255, 255, 0);font-size: 12px; font-family: 黑体}")
        self.contentLabel.setMinimumWidth(75)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(70)
        self.iconWidget.setFixedSize(48, 48)
        
        self.hBoxLayout.setContentsMargins(20, 5, 10, 11)
        self.hBoxLayout.setSpacing(10)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)

        self.hBoxLayout.addWidget(self.switchButton, 0, Qt.AlignRight)

    

