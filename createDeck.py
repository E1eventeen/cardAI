from cardAI import image
from gptConnect import getMagicCard
import time, os

inputFileName = "Deck List.txt"
outputDirectoryName = "RFP/"

if not os.path.exists(outputDirectoryName):
    os.makedirs(outputDirectoryName)

deckLength = 60
showImage = True
start = 34

startTime = time.time()

print("Generating a " + str(deckLength) + " card deck with" + "out" * (not showImage) + " images")
if not showImage:
    print("Costing about $" + str(round(0.000875 * deckLength,3)))
else:
    print("Costing about $" + str(round(0.016875 * deckLength,3)))

with open(inputFileName, "r") as f:
    queries = f.readlines()

for i in range(start, deckLength):
    try:
        if (i >= len(queries)):
            queries.append("Missing Dog")
        image(getMagicCard(queries[i]), hasImage = showImage, output = outputDirectoryName + str(i + 1))
        seconds = time.time() - startTime
        minutes = seconds // 60
        seconds = seconds % 60
        print("#" + str(i + 1) + ": " + queries[i].rstrip() + "-" * (30 - len(queries[i][0:-1])) + str(round(minutes)) + " minutes and " + str(round(seconds,3)) + " seconds elapsed.")
       
    except Exception as error:
        print(error)
        print("Error! Retrying...")
        i -= 1
        continue
