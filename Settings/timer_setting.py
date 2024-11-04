from qfluentwidgets import (
    SettingCardGroup,
    RangeConfigItem,
    FluentIcon,
    RangeSettingCard,
    RangeValidator,
)
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Timer.timericon import TimerWidget
from utils.files_processer import DataProcess
import gc


class TimerSetting(SettingCardGroup):
    def __init__(self, parent=None, **kwargs):
        super().__init__(title=None, parent=parent)
        self.setting_file_path = kwargs["path"]
        self.cfg = RangeConfigItem(None, None, 1, RangeValidator(36, 64))
        self.iconsize = RangeSettingCard(
            self.cfg,
            icon=FluentIcon.ZOOM,
            title="面板图标大小",
            content="36px-->64px",
        )
        self.iconsize.slider.setValue(self.window().settings["iconsize"])
        self.modify_iconsize()
        self.iconsize.slider.valueChanged.connect(self.modify_iconsize)
        self.titleLabel.hide()
        self.addSettingCard(self.iconsize)

    def modify_iconsize(self):
        DataProcess.write_json_content(
            self.setting_file_path, {"iconsize": self.iconsize.slider.value()}
        )
        isinstance_list = [
            item for item in gc.get_objects() if isinstance(item, TimerWidget)
        ]
        if isinstance_list != []:
            for item in isinstance_list:
                item.setIcon_Size(self.iconsize.slider.value())
                item.resetIcon(item.config['icon'])
        pass
