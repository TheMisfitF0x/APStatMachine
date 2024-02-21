import csv
import re
input_file = r'C:\Users\logan\Documents\ArchipelaFox\WorkFriends\Log.txt'
output_csv = r'C:\Users\logan\Documents\ArchipelaFox\WorkFriends\Stats.csv'

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

# Open the text file for reading and CSV file for writing (create if not exists)
with open(input_file, 'r') as infile, open(output_csv, 'w+', newline='') as outfile:
    # Create CSV writer
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(["Date/Time (UTC)",
                        "Sender", "Sender Game", "Receiver", "Receiver Game", "Item"])
    ignoreHelpLines = 0

    # Event Patterns
    sentPattern = re.compile(
        r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: \(Team #\d\) (\w+) sent (.+?) to (\w+)")

    hintPattern = re.compile(
        r"\[root at (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d{3}\]: Notice \(Team #1\): \[Hint\]: (\w+)'s (.+?) is at (.+?) in (\w+)'s World\.")
    for line in infile:

        # Iterate over the sent events
        match = sentPattern.search(line)
        if match:
            # Date and Time
            date = match.group(1)
            time = match.group(2)
            dateTime = date + " " + time

            # Sender
            senderComp = match.group(3)
            sender = senderComp[:-2]
            try:
                senderGame = gameCodeDict[senderComp[-2:]]
            except:
                senderGame = senderComp[-2:]

            # Item
            item = match.group(4)
            print("Sent Match")
            if item.startswith("+"):
                item = "\'" + item
                print("Weird starting character found")

            # Receiver
            receiverComp = match.group(5)
            receiver = receiverComp[:-2]
            try:
                receiverGame = gameCodeDict[receiverComp[-2:]]
            except:
                receiverGame = receiverComp[-2:]
            # Write data to new row.
            csv_writer.writerow(
                [dateTime, sender, senderGame, receiver, receiverGame, item])
        else:
            match = hintPattern.search(line)
            if match:
                date = match.group(1)
                time = match.group(2)
                receiver = match.group(3)
                item = match.group(4)
                location = match.group(5)
                sender = match.group(6)
                print("Working so far:", date, time,
                      receiver, item, location, sender)
