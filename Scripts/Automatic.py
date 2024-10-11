
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import keyboard as kb
import pyautogui
import time
import pygetwindow as gw
import threading
from .Listener import Listener

pyautogui.PAUSE = 0.05
    

class AutoEquipment(QObject):
    single = pyqtSignal(str)
    def __init__(self, parent,ACTIVE_SIGNAL_KEY='f1',SAVE_SIGNAL_KEY='space',EQU_KEY='i'):
        super().__init__()
        self.temp_parent = parent
        ########
        self.record = []
        self.temp_list = []
        ########
        self.time_gap = 0.05
        self.SAVE_SIGNAL_KEY = SAVE_SIGNAL_KEY
        self.ACTIVE_SIGNAL_KEY = ACTIVE_SIGNAL_KEY
        self.EQU_KEY = EQU_KEY
        self.SAVE_SIGNAL = False
        self.FLAG = 1
        ##############
        self.game_window_title = None
        self.get_game_title()
        ###############
        self.single.connect(parent.createSuccessInfoBar)
        self.stopevent = threading.Event()
        self.terminate_flag = True
        self.listener = Listener(mouse_Linsten_func=self.on_click)
        self.activate_signal=kb.add_hotkey(self.ACTIVE_SIGNAL_KEY, self.excute_click)
        self.save_signal =kb.add_hotkey(self.SAVE_SIGNAL_KEY, self.excute_save)
        ################
        pass

    def get_game_title(self):
        windows = gw.getAllWindows()
        for window in windows:
            if "Elsword -" in window.title:
                self.game_window_title = window.title
        pass

    def excute_save(self):
        if self.FLAG != 0:
            print(f"{self.time_stamp()}: 录制鼠标轨迹中...")
            self.FLAG = self.FLAG - 1
            self.SAVE_SIGNAL = True
            return
        if self.SAVE_SIGNAL == True:
            print(
                f"{self.time_stamp()}: 鼠标轨迹录制完毕,随时按下 {self.ACTIVE_SIGNAL_KEY.title()} 以启动换装"
            )
            self.listener.mouse_listener.stop()
            self.SAVE_SIGNAL = False
            self.temp_list = self.record
            return
        else:
            return

    def on_click(self, x, y, button, pressed):
        if gw.getActiveWindowTitle() != self.game_window_title:
            return
        if len(self.temp_list) != 0:
            self.SAVE_SIGNAL = False
            return
        else:
            if pressed and self.SAVE_SIGNAL:
                print(f"{self.time_stamp()}: {button}")
                self.record.append((button.name, (x, y)))

    def excute_click(self):

        if gw.getActiveWindowTitle() != self.game_window_title or self.terminate_flag:
            return
        print(f"{self.time_stamp()}: 执行换装")
        kb.press(self.EQU_KEY)
        time.sleep(0.03)
        kb.release(self.EQU_KEY)
     
        for item in self.temp_list:
            position = (item[1][0], item[1][1])
            if item[0] == "left":
                pyautogui.moveTo(position, duration=self.time_gap)
                pyautogui.doubleClick(position,button='left')
            elif item[0] == "right":
                pyautogui.moveTo(position, duration=self.time_gap)
                pyautogui.rightClick(position)

    def run_script(self):
        if len(self.temp_list) != 0:
            self.terminate_flag = False
            self.SAVE_SIGNAL = False
            self.FLAG = 0
            print(
                f"{self.time_stamp()}: 已使用预设坐标,随时按下 {self.ACTIVE_SIGNAL_KEY.title()} 以启动换装,如需重新设置请新建配置文件"
            )
            self.single.emit(
                f"已使用预设坐标,随时按下 {self.ACTIVE_SIGNAL_KEY.title()} 以启动换装,如需重新设置请新建配置文件"
            )
        else:
            print(
                f"{self.time_stamp()}: 请按下 {self.SAVE_SIGNAL_KEY.title()} 开始录制鼠标"
            )
            self.single.emit(f"请按下 {self.SAVE_SIGNAL_KEY.title()} 开始录制鼠标")
        self.stopevent.wait()  # 等待事件发生
        self.terminate_flag = True
        

    def _set_time_gap(self, time):
        self.time_gap = time

    def _set_terminate(self):
        self.stopevent.set()

    def _set_key(self, SAVE_SIGNAL_KEY, ACTIVE_SIGNAL_KEY, EQU_KEY):
        kb.remove_hotkey(self.save_signal)
        kb.remove_hotkey(self.activate_signal)
        self.save_signal = kb.add_hotkey(SAVE_SIGNAL_KEY,self.excute_save)
        self.activate_signal = kb.add_hotkey(ACTIVE_SIGNAL_KEY,self.excute_click)
        self.EQU_KEY = EQU_KEY
        pass

    def set_cor_list(self, cor_list):
        self.temp_list = cor_list

    def get_cor_list(self):
        return self.temp_list

    def time_stamp(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    def set_pyautogui_pause(self, time):
        pyautogui.PAUSE = time
