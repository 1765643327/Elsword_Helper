# import keyboard as kb

# def on_press(key):
#     print(key.name)
#     print(kb.key_to_scan_codes(key.name))

# kb.on_press(on_press)
# kb.wait('esc')
import keyboard as kb
# kb.key_to_scan_codes('ctrl+shift+a')
kb.press((2,79))
kb.release((2,79))