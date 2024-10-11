
import keyboard
import time

def a(b):
    print(b)

keyboard.add_hotkey('ctrl+shift+a', a, args=('hello',))

keyboard.wait('esc')
