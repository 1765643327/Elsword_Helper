# coding:utf-8
from qfluentwidgets import (
    MessageBoxBase,
    SubtitleLabel,
    LineEdit,
    setTheme,
)


class CustomMessageBox(MessageBoxBase):
    """Custom message box"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.nameLabel = SubtitleLabel("名字", self)
        self.description = SubtitleLabel("描述", self)
        self.name_LineEdit = LineEdit(self)
        self.descript1_LineEdit = LineEdit(self)

        self.name_LineEdit.setPlaceholderText("为设置命名(不可留空)")
        self.descript1_LineEdit.setPlaceholderText("添加设置描述信息(可以留空)")
        self.name_LineEdit.setClearButtonEnabled(True)
        self.descript1_LineEdit.setClearButtonEnabled(True)

        # add widget to view layout
        self.viewLayout.addWidget(self.nameLabel)
        self.viewLayout.addWidget(self.name_LineEdit)

        self.viewLayout.addWidget(self.description)
        self.viewLayout.addWidget(self.descript1_LineEdit)

        # change the text of button
        self.yesButton.setText("打开")
        self.cancelButton.setText("取消")

        self.widget.setMinimumWidth(350)
        self.yesButton.setDisabled(True)
        self.name_LineEdit.textChanged.connect(self._validateText)

    def _validateText(self, text):
        self.yesButton.setEnabled(len(self.name_LineEdit.text()) != 0)
