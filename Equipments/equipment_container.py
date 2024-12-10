from qfluentwidgets.components import SmoothScrollArea
from PySide6.QtWidgets import QVBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Qt


class EquipmentContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setScrollAnimation(Qt.Vertical)
        self.item_dir = {}
        self.scroller = SmoothScrollArea(self)
        self.scroller.setWidgetResizable(True)
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setStyleSheet("background: transparent")
        self.scroller.setWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setAlignment(Qt.AlignTop)
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
        self.mylayout.addWidget(self.scroller)
        self.container.setContentsMargins(0, 0, 15, 0)
        self.setLayout(self.mylayout)

    def add_item(self, item, name):
        self.item_dir[name] = item
        self.container_layout.addWidget(item)

    def remove_item(self, name):
        item = self.item_dir.pop(name)
        self.container_layout.removeWidget(item)
        item.deleteLater()
