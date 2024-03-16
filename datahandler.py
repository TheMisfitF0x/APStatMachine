import pandas as pd
import numpy as np
from statMachComponents import EventType
# Anything dealing with dataframes I intend to put here.


class DataHandler:
    def ToDataframe(self, eventList):
        return pd.DataFrame(eventList, columns=[
            "Date/Time (UTC)", "Sender", "Sender Game", "Receiver", "Receiver Game", "Item"])
