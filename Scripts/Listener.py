import keyboard as kb
from pynput import mouse


class Listener:
    _instance = None

    # 重写__new__方法保证该组件只被实例化一次
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Listener, cls).__new__(cls)
        return cls._instance

    def __init__(self,kb_Linsten_func=None, mouse_Linsten_func=None):
        self.kb_Linsten_func = kb_Linsten_func
        self.mouse_Linsten_func = mouse_Linsten_func
        self.mouse_listener = mouse.Listener(on_click=self.mouse_Linsten_func)        
        # self.kb_listener = kb.on_press(self.kb_Linsten_func)
        self.mouse_listener.start()
