import keyboard
import threading
import pygetwindow as gw
import time
from collections import deque
from PyQt5.QtCore import pyqtSignal,QObject
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = {}
        self.parent = None
        self.is_end_of_sequence = False

class MultiTree:
    def __init__(self):
        self.root = TreeNode('root')

    def add_sequence(self, sequence):
        current = self.root
        for key in sequence.split('+'):
            temp_key_node = TreeNode(key)
            if key not in current.children:
                current.children[key] = temp_key_node
                temp_key_node.parent = current
            current = current.children[key]
        current.is_end_of_sequence = True

    def query_whether_end(self, current_node):
        for k,v in current_node.children.items():
            if v.is_end_of_sequence:
                return True
        return False
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

        self.operations_tree = MultiTree()
        # self.activate_key_list = []
        if ';' in self.input_operations:
            self.input_operations_list = self.input_operations.split(';')
            for item in self.input_operations_list:
                self.operations_tree.add_sequence(item)
            self.key_sequence_list = list(dict.fromkeys([item2 for item in self.input_operations_list for item2 in item.split('+')]))
            # self.activate_key_list = [item.split('+')[-1] for item in self.input_operations_list]
        else:
            self.operations_tree.add_sequence(self.input_operations)
            self.key_sequence_list = config['activate'].split('+')
            # self.activate_key_list= [self.key_sequence_list[-1]]

        if len(self.key_sequence_list)>1:
            keyboard.add_hotkey(f'tab+{self.key_sequence_list[0]}+{self.key_sequence_list[1]}', self.reset_timer)
        else:
            keyboard.add_hotkey(f'{self.key_sequence_list[0]}', self.reset_timer)
        
        # self.input_sequence = self.key_sequence_list.copy()
        self.input_queue = deque()
        self.current_node = self.operations_tree.root

        self.start_timer_signal.connect(self.tm_parent.start_timer)
        self.stop_timer_signal.connect(self.tm_parent.stop_timer)
        self.start_timer()

    def get_game_title(self):
        windows = gw.getAllWindows()
        for window in windows:
            if "Elsword -" in window.title:
                self.game_window_title = window.title
        pass

    def on_key_event(self, event):
        if self.current_node.value == event.name and self.current_node.is_end_of_sequence:  # 如果当前输入与当前节点相同且到达终点
            self.start_timer_signal.emit()  # 启动计时器
            self.input_queue.clear()  # 清空队列
            self.current_node = self.operations_tree.root  # 回到根节点
            return
        if event.name in self.current_node.children:  # 如果当前输入在子节点中
            self.input_queue.append(event.name)  # 将按键压入队列
            print(f"当前输入序列:{self.input_queue}")
            self.current_node = self.current_node.children[event.name]  # 切换到子节点
            print(f"当前节点:{self.current_node.value}")
            if self.current_node.is_end_of_sequence:  # 如果到达终点
                self.start_timer_signal.emit()  # 启动计时器
                self.input_queue.clear()  # 清空队列
                self.current_node = self.operations_tree.root  # 回到根节点
                return
            else:
                return
        else: 
            if self.operations_tree.query_whether_end(self.current_node):  # 如果当前节点有子节点的终点
                    self.input_queue.clear()  # 清空队列
                    self.current_node = self.operations_tree.root  # 回到根节点
            if self.current_node.parent == None:  # 如果当前节点不是根节点
                return
            else:
                self.current_node = self.current_node.parent  # 回退到父节点
                self.input_queue.pop()  # 弹出最后一个按键
                print(f"当前输入序列:{self.input_queue}")
                return


    # def press_key(self, key):
    #     # print(f"{id(self)}==={key.name}==={self.input_sequence}")
    #     if gw.getActiveWindowTitle() != self.game_window_title or self.tm_parent.timer_working:
    #         return
    #     if key.name == self.key_sequence_list[0]:
    #         self.input_sequence.pop(0)
    #     if key.name in self.activate_key_list and self.input_sequence == self.activate_key_list:
    #         self.input_sequence = self.key_sequence_list.copy()
    #         self.start_timer_signal.emit()
    #     if key.name in ['left','right','up','down']:
    #         if self.input_sequence == self.activate_key_list:
    #             return
    #         if key.name == self.input_sequence[0]:
    #             self.input_sequence.pop(0)
    #         else:
    #             if self.input_sequence[0] != self.key_sequence_list[0]:
    #                 self.input_sequence.insert(0,self.key_sequence_list[0])
    #             else:
    #                 return
    #     if self.input_sequence == []:
    #         self.input_sequence = self.key_sequence_list.copy()
    #         self.start_timer_signal.emit()
    #     else:
    #         return


                       
    def start_timer(self):
        # 启动一个新的线程来监听键盘事件
        listener_thread = threading.Thread(target=self.listen_keyboard,daemon=True)
        listener_thread.start()
    
    def reset_timer(self):
        # print(f"{id(self)}-->{self.activate_key_list}-->reset_timer")
        self.stop_timer_signal.emit()
       

    def listen_keyboard(self):
        # 使用 keyboard 库来监听键盘事件
        keyboard.on_press(self.on_key_event)

    def reset_input_sequence(self,config):
        if len(self.key_sequence_list)>1:
            keyboard.remove_hotkey(f'tab+{self.key_sequence_list[0]}+{self.key_sequence_list[1]}')
        else:
            keyboard.remove_hotkey(f'{self.key_sequence_list[0]}')

        self.operations_tree = MultiTree()
        # self.activate_key_list = []
        if ';' in self.input_operations:
            self.input_operations_list = self.input_operations.split(';')
            for item in self.input_operations_list:
                self.operations_tree.add_sequence(item)
            self.key_sequence_list = list(dict.fromkeys([item2 for item in self.input_operations_list for item2 in item.split('+')]))
            # self.activate_key_list = [item.split('+')[-1] for item in self.input_operations_list]
        else:
            self.operations_tree.add_sequence(self.input_operations)
            self.key_sequence_list = config['activate'].split('+')
            # self.activate_key_list= [self.key_sequence_list[-1]]

        if len(self.key_sequence_list)>1:
            keyboard.add_hotkey(f'tab+{self.key_sequence_list[0]}+{self.key_sequence_list[1]}', self.reset_timer)
        else:
            keyboard.add_hotkey(f'{self.key_sequence_list[0]}', self.reset_timer)
