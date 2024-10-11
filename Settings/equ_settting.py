from qfluentwidgets import (
    SettingCardGroup,
    RangeConfigItem,
    FluentIcon,
    RangeSettingCard,
    RangeValidator,
)
from Scripts.Automatic import AutoEquipment
from utils.files_processer import DataProcess
import gc


class EquSetting(SettingCardGroup):
    def __init__(self, parent=None, **kwargs):
        super().__init__(title=None, parent=parent)
        self.setting_file_path = kwargs["path"]
        self.cfg = RangeConfigItem(None, None, 10, RangeValidator(1, 1000))
        self.frequency = RangeSettingCard(
            self.cfg,
            icon=FluentIcon.SPEED_OFF,
            title="鼠标点击间隔",
            content="指按下和松开的间隔 | 单位毫秒",
        )
        self.frequency.slider.setValue(self.window().settings["frequency"])
        self.frequency.slider.valueChanged.connect(self.modify_frequency)
        self.titleLabel.hide()
        self.addSettingCard(self.frequency)

    def modify_frequency(self):
        DataProcess.write_json_content(
            self.setting_file_path, {"frequency": self.frequency.slider.value()}
        )
        isinstance_list = [
            item for item in gc.get_objects() if isinstance(item, AutoEquipment)
        ]
        if isinstance_list != []:
            for item in isinstance_list:
                item.set_pyautogui_pause(self.frequency.slider.value() * 0.001)
        pass
