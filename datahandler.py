import pandas as pd
import numpy as np
from statMachComponents import EventType
# Anything dealing with dataframes I intend to put here.


class DataHandler:
    def ToDataframe(eventList):
        return pd.DataFrame(eventList)
