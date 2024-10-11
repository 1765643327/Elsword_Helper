
import cv2
import numpy as np
import keyboard
import mss
import time
import os
import sys
from pyautogui import size

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
# BASE_DIR = 'E:\Vscode\WorkSpace\Auto_Music\Elsword_Helper'


class MusicService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.letters = {
            # "A": self.convert_img(os.path.join(BASE_DIR, "images\characters", "A.png")),
            "B": self.convert_img(os.path.join(BASE_DIR, "images\characters", "B.png")),
            "C": self.convert_img(os.path.join(BASE_DIR, "images\characters", "C.png")),
            "D": self.convert_img(os.path.join(BASE_DIR, "images\characters", "D.png")),
            "E": self.convert_img(os.path.join(BASE_DIR, "images\characters", "E.png")),
            "F": self.convert_img(os.path.join(BASE_DIR, "images\characters", "F.png")),
            "G": self.convert_img(os.path.join(BASE_DIR, "images\characters", "G.png")),
            "C!": self.convert_img(os.path.join(BASE_DIR, "images\characters", "C!.png")),
        }

        self.single = False

    def find_string(self, img, letters):
        result = []
        for letter in letters:
            result.append(
                (letter, cv2.matchTemplate(img, letters[letter], cv2.TM_CCOEFF_NORMED))
            )
        result = [
            (letter, pt)
            for letter, value in result
            for pt in zip(*np.where(value >= 0.9)[::-1])
        ]
        if result == []:
            return []
        re_result = []
        total_result = sorted(result, key=lambda x: x[1][0])
        for i in range(len(total_result) - 1):
            if total_result[i + 1][1][0] - total_result[i][1][0] < 3:
                continue
            else:
                re_result.append(total_result[i])
        re_result.append(total_result[-1])
        return [letter for letter, pt in re_result]

    def caputer_screen(self):
        with mss.mss() as sct:
            monitor = {"top": 0, "left": 0, "width": size().width, "height":int(size().height/3)}
            img = np.array(sct.grab(monitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
            _, binary_image = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY_INV)
            find_res = self.find_string(binary_image, self.letters)
            print(find_res)
            if find_res != []:
                res = self.format_string(find_res)
                time.sleep(0.5)
                keyboard.write(res)
        sct.close()

    def format_string(self, string_list):
        result = ""
        for i in range(len(string_list)):
            if i % 4 == 0:
                result += "|" + string_list[i]
            else:
                result += string_list[i]
        return result

    def convert_img(self, img_path,threshold=60):
        img = cv2.imread(img_path, 0)
        _, binary_image = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
        return binary_image

    def start_task(self,single):
        print(single)
        self.single = single
        while self.single:
            print("正在监听事件,按下Enter开始分析")
            keyboard.wait("enter")
            self.caputer_screen()



# if __name__ == "__main__":
#     music_service = MusicService()
#     music_service.start_task(True)
#     time.sleep(3)
#     music_service.single = False



