import keyboard
import threading
import pygetwindow as gw
import time
import queue
from PyQt5.QtCore import pyqtSignal,QObject

class TimerManager(QObject):
    start_timer_signal = pyqtSignal()
    stop_timer_signal = pyqtSignal()
    def __init__(self, parent, config):
        super().__init__(parent)
        self.game_window_title = None
        self.config = config
        self.get_game_title()
        self.setObjectName("TimerManager"+config['id'])
        self.tm_parent = parent
        self.input_operations = config['activate']
        self.activate_key_list = []
        if ';' in self.input_operations:
            self.input_operations_list = self.input_operations.split(';')
            self.key_sequence_list = list(dict.fromkeys([item2 for item in self.input_operations_list for item2 in item.split('+')]))
            self.activate_key_list = [item.split('+')[-1] for item in self.input_operations_list]
        else:
            self.key_sequence_list = config['activate'].split('+')
            self.activate_key_list= [self.key_sequence_list[-1]]
        for key in self.activate_key_list:
            keyboard.add_hotkey(f"alt+{key}",self.reset_timer)
        self.input_sequence = self.key_sequence_list.copy()
        self.start_timer_signal.connect(self.tm_parent.start_timer)
        self.stop_timer_signal.connect(self.tm_parent.stop_timer)
        self.start_timer()

    def get_game_title(self):
        windows = gw.getAllWindows()
        for window in windows:
            if "Elsword -" in window.title:
                self.game_window_title = window.title
        pass

    def press_key(self, key):
        if gw.getActiveWindowTitle() != self.game_window_title or self.tm_parent.timer_working:
            return
        # if gw.getActiveWindowTitle() != self.game_window_title:
        #     return
        # print(f"{id(self)}==={key.name}==={self.input_sequence}")
        if key.name == self.input_sequence[0] or self.input_sequence == self.activate_key_list:
            if self.input_sequence != self.activate_key_list:
                self.input_sequence.pop(0)
            if self.input_sequence == [] or key.name in self.activate_key_list:
                self.start_timer_signal.emit()
                self.input_sequence = self.key_sequence_list.copy()
        else:
            return

    def check_repeat_key(self, key, key_list):
        print(key_list,key)
        temp_list = key_list.copy()
        temp_list.append(key)
        if len(temp_list) != len(set(temp_list)):
            return True

    def match_input_sequence(self, input_sequence):
        for k,v in self.key_sequence.items():
            if v == input_sequence:
                return True
                       
    def start_timer(self):
        # 启动一个新的线程来监听键盘事件
        listener_thread = threading.Thread(target=self.listen_keyboard,daemon=True)
        listener_thread.start()
    
    def reset_timer(self):
        self.tm_parent.resetConfig(self.config)
        self.stop_timer_signal.emit()

    def listen_keyboard(self):
        # 使用 keyboard 库来监听键盘事件
        keyboard.on_press(self.press_key)

    def reset_input_sequence(self,config):
        self.activate_key_list = []
        if ';' in config['activate']:
            self.input_operations_list = config['activate'].split(';')
            self.key_sequence_list = list(dict.fromkeys([item2 for item in self.input_operations_list for item2 in item.split('+')]))
            self.activate_key_list = [item.split('+')[-1] for item in self.input_operations_list]
        else:
            self.key_sequence_list = config['activate'].split('+')
        self.input_sequence = self.key_sequence_list.copy()


