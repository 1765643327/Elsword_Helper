
from qfluentwidgets import FlowLayout
from Scripts.Music_character import MusicService
from PyQt5.QtWidgets import (
    QWidget,
    QWidget,

)
from .toolcard import ToolCard
from functools import partial
import os
import threading

class ToolsInterface(QWidget):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ToolsInterface, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.base_dir = args[0]
        self.toolmanager = {}
        self.setObjectName("ToolsInterface")
        self.setStyleSheet(
            """
            Demo{background: white}
            QLabel{
                font: 20px 'Segoe UI';
                background: rgb(242,242,242);
            }
        """
        )
        self.toollayout = FlowLayout()
        self.setLayout(self.toollayout)
        self.add_tool(os.path.join(self.base_dir, r"images\game_icons\205-2.png"),
                      "钢琴演奏", "请确保正确设置完字符图片")

    def add_tool(self, icon, title, content):
        toolcard = ToolCard(icon=icon, title=title, content=content)
        if title == "钢琴演奏":
            toolcard.switchButton.checkedChanged.connect(partial(self.music_service))
        self.toolmanager[title] = toolcard
        self.toollayout.addWidget(toolcard)

    def music_service(self):
        if self.toolmanager["钢琴演奏"].switchButton.isChecked():
            threading.Thread(target=MusicService().start_task, args=(True,), daemon=True).start()
        else:
            MusicService().start_task(False)
        

