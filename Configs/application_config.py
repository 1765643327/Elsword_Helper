from enum import Enum
from qfluentwidgets import QConfig, ConfigItem,qconfig


class MyConfig(QConfig):
    """ 
    Config of application 
    """
    equ_settins1 = ConfigItem(
        group="equ_settins",
        name='mouse_move_time',
        default=0,
        validator=None
    )
    equ_settins2 = ConfigItem(
        group="equ_settins",
        name='time',
        default=10,
        validator=None
    )


pass

# cfg = MyConfig()
# qconfig.load('/home/zk/Vscode_WorkSpace/Elsword_Helper/config/config.json',cfg)

# cfg.set(cfg.equ_settins1, 100)
# cfg.set(cfg.equ_settins2, 20)
# print(cfg.equ_settins1.value)
# print(cfg.equ_settins2.value)
  

