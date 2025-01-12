from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.adb_device import AdbDeviceTcp
import os

class CommandsAdapter:
    
    def __init__(self):
        adb_private_key = os.getenv("ADB_PRIVATE_KEY_FILE")
        if adb_private_key is None:
           raise Exception("ADB private key missing")
        adb_public_key = os.getenv("ADB_PUBLIC_KEY_FILE")
        if adb_public_key is None:
           raise Exception("ADB public key missing")
        with open(adb_private_key) as f:
         priv = f.read()
        with open(adb_public_key) as f:
         pub = f.read()
        signer = PythonRSASigner(pub, priv)
        self.device = AdbDeviceTcp('192.168.1.10', 5555)
        self.device.connect(rsa_keys=[signer],auth_timeout_s=2) 
    def up(self):
        self.device.shell('input keyevent 19')
    def down(self):
        self.device.shell('input keyevent 20')
    def left(self):
        self.device.shell('input keyevent 21')
    def right(self):
        self.device.shell('input keyevent 22')
    def enter(self):
        self.device.shell('input keyevent 66')
    def back(self):
        self.device.shell('input keyevent 4')