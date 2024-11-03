# print("Hello+World+a".split("+"))
# for i in range(10):
#     print("Hello+World+a".split("+"))
# list1 = set(["Hello", "World", "a"])
# list2 = set(["Hello", "a","World"])

# print(list1 == list2)k

import keyboard 

def key_pressed():
    print('1')

keyboard.add_hotkey('space+right ctrl+left',key_pressed)
keyboard.wait('esc ')                           