from enum import Enum

# Setting Name Enum for clarity
class FSettingName(Enum):
    ExcludeSelfSends = 0
    Column = 1

# Settings Class
class FocusSettings:
    def __init__(self):
        self.excludeSelfSends = True
        self.column = "Sender"
        pass

    def UpdateSettings(self, settingName, newVal):
        if settingName == FSettingName.ExcludeSelfSends and type(newVal) == type(True):
            self.excludeSelfSends = newVal
        elif settingName == FSettingName.Column and type(newVal) == type("Oof"):
            self.column = newVal
        else:
            print("Improper Settings Update")
        

