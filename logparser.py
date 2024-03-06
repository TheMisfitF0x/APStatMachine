import re
import os.path
import statMachComponents as appComps

def parseEvents(logFilePath, type="Sent"):
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

        for line in infile:
            # Iterate over the sent events
            match = sentPattern.search(line)
            if match:
                print("Match Found")
                newRow = []
                # Date and Time
                date = match.group(1)
                time = match.group(2)
                dateTime = date + " " + time
                newRow.append(dateTime)

                # Sender
                senderComp = match.group(3)
                sender = senderComp[:-2]
                try:
                    senderGame = appComps.gameCodes[senderComp[-2:]]
                except:
                    senderGame = senderComp[-2:]

                newRow.append(sender)
                newRow.append(senderGame)

                # Receiver
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
                print("Sent Match")
                if item.startswith("+"):
                    item = "\'" + item
                    print("Weird starting character found")
                newRow.append(item)
                sentEvents.append(newRow)
    return sentEvents