import re
import os.path
import statMachComponents as ac
from statMachComponents import EventType


class LogParser:
    eventPatterns = {
        "sent": re.compile(
            r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: \(Team #\d\) (\w+) sent (.+?) to (\w+)"),
        "hint": re.compile(
            r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: Notice \(Team #1\): \[Hint\]: (\w+)'s (.+?) is at (.+?) in (\w+)'s World\.")
    }

    def __init__(self, logFilePath):
        self.logFilePath = logFilePath
        self.ParseEvents(logFilePath)
        print("Sent Events: " + str(len(self.sentEvents)))
        print("Hint Events: " + str(len(self.hintEvents)))
        print("Completed Events: " + str(len(self.completeEvents)))

    def GetEvents(self, eventType):
        if eventType == EventType.Sent:
            return self.sentEvents
        elif eventType == EventType.Hint:
            return self.hintEvents
        elif eventType == EventType.Complete:
            return self.completeEvents

    def ParseEvents(self, logFilePath):
        # Open the text file for reading and CSV file for writing (create if not exists)
        with open(logFilePath, 'r') as infile:

            # To become a 2D Array, convertable into a dataframe.
            self.sentEvents = []
            self.hintEvents = []
            self.completeEvents = []

            # Iterates over every line
            for line in infile:
                # Identify Sent event
                match = self.eventPatterns["sent"].search(line)
                if match:  # If event is Sent Event

                    newRow = []

                    # Date and Time
                    date = match.group(1)
                    time = match.group(2)
                    dateTime = date + " " + time  # Combine for ease.
                    newRow.append(dateTime)

                    # Sender
                    senderComp = match.group(3)
                    # Get the name from the complete Sender
                    sender = senderComp[:-2]
                    try:
                        # Get the game from the complete Sender
                        senderGame = ac.gameCodes[senderComp[-2:]]
                    except:
                        # If the game doesn't exist or isn't found, use the complete sender with the last two digits removed.
                        senderGame = senderComp[-2:]
                    newRow.append(sender)
                    newRow.append(senderGame)

                    # Receiver (same process as sender)
                    receiverComp = match.group(5)
                    receiver = receiverComp[:-2]
                    try:
                        receiverGame = ac.gameCodes[receiverComp[-2:]]
                    except:
                        receiverGame = receiverComp[-2:]
                    newRow.append(receiver)
                    newRow.append(receiverGame)

                    # Item
                    item = match.group(4)
                    # if item.startswith("+"):
                    #    item = "\'" + item
                    #    print("Weird starting character found")
                    newRow.append(item)

                    # Add the completed event array to the larger 2D array
                    self.sentEvents.append(newRow)
