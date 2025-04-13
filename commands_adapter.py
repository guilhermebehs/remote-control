import subprocess

class CommandsAdapter:
    
    def up(self):
        subprocess.run(["adb", "shell", "input", "keyevent", "19"])
    def down(self):
        subprocess.run(["adb", "shell", "input", "keyevent", "20"])
    def left(self):
        subprocess.run(["adb", "shell","input", "keyevent", "21"])
    def right(self):
        subprocess.run(["adb", "shell", "input", "keyevent", "22"])
    def enter(self):
        subprocess.run(["adb", "shell", "input", "keyevent", "66"])
    def back(self):
        subprocess.run(["adb", "shell", "input", "keyevent", "4"])
