import re
import os.path
import statMachComponents as appComps
from enum import Enum

# Enum for clarity when defining the type of event to be found and filtered.
# May be discontinued in favor of a more complicated parser class
# Eventually I want to drop this in favor of evaluating the whole log in one go and just adding each event to it's own 2D array,
# And use a parser object to hold and manage those different 2D arrays.
# Maybe something like a DataParser class that requires a log file to be constructed,
# A dictionary or enum for all the patterns and has an updateData() function of the sort? 
# IDK but sounds like a blast.
class EventType(Enum):
    Sent = 1
    Hint = 2
    Complete = 3

def parseEvents(logFilePath, eventType = EventType.Sent):
    # Open the text file for reading and CSV file for writing (create if not exists)
    with open(logFilePath, 'r') as infile:
        # Event Patterns
        sentPattern = re.compile(
            r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: \(Team #\d\) (\w+) sent (.+?) to (\w+)")

        # Hint Pattern (not currently in use)
        hintPattern = re.compile(
            r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: Notice \(Team #1\): \[Hint\]: (\w+)'s (.+?) is at (.+?) in (\w+)'s World\.")

        # To become a 2D Array, convertable into a dataframe.
        sentEvents = []

        # Iterates over every line
        for line in infile:
            # Identify Sent event
            match = sentPattern.search(line)
            if match: # If event is Sent Event
                
                newRow = []

                # Date and Time
                date = match.group(1)
                time = match.group(2)
                dateTime = date + " " + time #Combine for ease.
                newRow.append(dateTime)

                # Sender
                senderComp = match.group(3)
                sender = senderComp[:-2] # Get the name from the complete Sender
                try:
                    senderGame = appComps.gameCodes[senderComp[-2:]] # Get the game from the complete Sender
                except:
                    senderGame = senderComp[-2:] # If the game doesn't exist or isn't found, use the complete sender with the last two digits removed.
                newRow.append(sender)
                newRow.append(senderGame)

                # Receiver (same process as sender)
                receiverComp = match.group(5)
                receiver = receiverComp[:-2]
                try:
                    receiverGame = appComps.gameCodes[receiverComp[-2:]]
                except:
                    receiverGame = receiverComp[-2:]
                newRow.append(receiver)
                newRow.append(receiverGame)

                # Item
                item = match.group(4)
                #if item.startswith("+"):
                #    item = "\'" + item
                #    print("Weird starting character found")
                newRow.append(item)

                # Add the completed event array to the larger 2D array
                sentEvents.append(newRow)
    return sentEvents # Return the completed 2D array


