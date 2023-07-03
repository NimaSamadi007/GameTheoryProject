from enum import Enum

class LogType(Enum):
    DEBUG = 1
    INFO = 2

class Logger:
    def __init__(self, log_level=LogType.DEBUG):
        self.log_level = log_level

    def log(self, in_str, end="\n", log_type: LogType = LogType.DEBUG):
        if log_type.value >= self.log_level.value:
            print(in_str, end=end)
