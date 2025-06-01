import subprocess
from dotenv import load_dotenv
import speech_recognition as sr
import os

load_dotenv()

class CommandsAdapter:
    isDebugging = os.getenv("DEBUG")
    def show_only_print(self):
        return self.isDebugging is not None and self.isDebugging.lower() == "true"
    def up(self):
        if  self.show_only_print():
            print("up")
            return
        subprocess.run(["adb", "shell", "input", "keyevent", "19"])
    def down(self):
        if  self.show_only_print():
            print("down")
            return
        subprocess.run(["adb", "shell", "input", "keyevent", "20"])
    def left(self):
        if  self.show_only_print():
            print("left")
            return
        subprocess.run(["adb", "shell","input", "keyevent", "21"])
    def right(self):
        if  self.show_only_print():
            print("right")
            return
        subprocess.run(["adb", "shell", "input", "keyevent", "22"])
    def enter(self):
        if  self.show_only_print():
            print("enter")
            return
        subprocess.run(["adb", "shell", "input", "keyevent", "66"])
    def back(self):
        if  self.show_only_print():
            print("back")
            return
        subprocess.run(["adb", "shell", "input", "keyevent", "4"])
