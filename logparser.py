import csv
import re
import sys

print(sys.path)
gameCodeDict = {
    "CL": "Clique",
    "DS": "Dark Souls III",
    "DM": "Doom 1993",
    "FT": "Factorio",
    "HK": "Hollow Knight",
    "KH": "Kingdom Hearts 2",
    "LZ": "Legend of Zelda",
    "MM": "Megaman Battle Network 3",
    "MC": "Minecraft",
    "NA": "Noita",
    "OT": "Ocarina of Time",
    "PE": "Pokemon Emerald",
    "PB": "Pokemon Blue",
    "PR": "Pokemon Red",
    "RT": "Raft",
    "RR": "Risk of Rain 2",
    "SS": "Slay the Spire",
    "SC": "StarCraft 2",
    "SV": "Stardew Valley",
    "SB": "Subnautica",
    "TR": "Terraria",
    "WG": "Wargroove"
}


def parseSentEvents(logFilePath):
    # Open the text file for reading and CSV file for writing (create if not exists)
    sentEvents = []
    with open(logFilePath, 'r') as infile:
        # Event Patterns
        sentPattern = re.compile(
            r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: \(Team #\d\) (\w+) sent (.+?) to (\w+)")

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
                    senderGame = gameCodeDict[senderComp[-2:]]
                except:
                    senderGame = senderComp[-2:]

                newRow.append(sender)
                newRow.append(senderGame)

                # Receiver
                receiverComp = match.group(5)
                receiver = receiverComp[:-2]
                try:
                    receiverGame = gameCodeDict[receiverComp[-2:]]
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
