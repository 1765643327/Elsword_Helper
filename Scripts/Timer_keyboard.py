import keyboard
import threading
import time
from PyQt5.QtCore import pyqtSignal,QObject

class TimerManager(QObject):
    start_timer_signal = pyqtSignal()
    def __init__(self, parent, config):
        super().__init__(parent)
        self.setObjectName("TimerManager"+config['id'])
        self.tm_parent = parent
        self.input_operations = config['activate']
        self.input_operations_list = config['activate'].split(';')
        self.input_sequence_dir = {item:[] for item in self.input_operations_list}
        self.start_key = self.input_operations_list[0].split('+')[0]
        self.key_sequence = {item:item.split('+') for item in self.input_operations_list}
        self.keyname_list = list(set(([item for k,v in self.key_sequence.items() for item in v])))
        self.input_sequence = []
        self.start_timer_signal.connect(self.tm_parent.start_timer)
        self.start_timer()

    def press_key(self, key):
        print(key.name)
        if key.name == self.start_key and self.input_sequence == []:
            self.input_sequence.append(key.name)
            print(self.input_sequence)
            return
        if key.name in self.keyname_list and self.input_sequence!= []:
            if self.check_repeat_key(key.name, self.input_sequence):
                return
            self.input_sequence.append(key.name)
            print(self.input_sequence)
            if self.match_input_sequence(self.input_sequence):
                # 添加重置时间的逻辑
                self.start_timer_signal.emit()
                self.input_sequence.clear()
                time.sleep(5)
                return
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
        

    def listen_keyboard(self):
        # 使用 keyboard 库来监听键盘事件
        keyboard.on_press(self.press_key)

    def reset_input_sequence(self,config):
         self.input_operations = config['activate']
         self.input_operations_list = config['activate'].split(';')
         self.input_sequence_dir = {item:[] for item in self.input_operations_list}
         self.start_key = self.input_operations_list[0].split('+')[0]
         self.key_sequence = {item:item.split('+') for item in self.input_operations_list}
         self.keyname_list = list(set(([item for k,v in self.key_sequence.items() for item in v])))