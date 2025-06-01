from commands_adapter import CommandsAdapter
from commands_enum import COMMANDS
import threading
import time

commandsAdapter = CommandsAdapter()

cooldown = {
    COMMANDS.LEFT: 0.5,
    COMMANDS.RIGHT: 0.5,
    COMMANDS.UP: 0.5,
    COMMANDS.DOWN: 0.5,
    COMMANDS.ENTER: 2.0,
    COMMANDS.BACK: 2.0,
}
last_trigger_times = {
    COMMANDS.LEFT: 0,
    COMMANDS.RIGHT: 0,
    COMMANDS.UP: 0,
    COMMANDS.DOWN: 0,
    COMMANDS.ENTER: 0,
    COMMANDS.BACK: 0,
}

def trigger_command(command):
    now = time.time()
    if now - last_trigger_times[command] >= cooldown[command]:
        last_trigger_times[command] = now
        func = getattr(commandsAdapter, command.value)
        threading.Thread(target=func).start()      
