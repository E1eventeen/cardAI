from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import urllib.request
import gptConnect
import os, random

# Text Query is 250 tokens or roughly $0.000875 a query 1142 -> $1
# Image Query is $0.016 a query, or 62 images -> $1

def image(dat, hasImage = True, output = "output"):
    if type(dat) is str:
        dat = eval(dat)
    img = Image.open("template.png")
    draw = ImageDraw.Draw(img)
    print(dat)
    #Write Card Name
    fontName = ImageFont.truetype("comicbd.ttf", 42)
    draw.text((96, 76),dat["name"],(0,0,0),font=fontName)

    #Write Card Type
    fontType = ImageFont.truetype("comic.ttf", 42)
    draw.text((96, 766),dat["typeLine"],(0,0,0),font=fontType)

    #Write Card Power / Toughness
    draw.text((773, 1212),str(dat["power"]) + "/" + str(dat["toughness"]),(0,0,0),font=fontType)

    #Write Main Body
    cursorY = 864
    fontBody = ImageFont.truetype("comic.ttf", 24)
    
    keyWords = "" 
    for keyWord in dat["keywords"]:
        keyWords += keyWord + ", "
    keyWords = keyWords[:-2]

    bodyText = [keyWords] + dat["abilityDescriptions"]

    for line in bodyText:
        while(True):
            draw.text((104, cursorY),line[0:65],(0,0,0),font=fontBody)
            cursorY += 25
            line = line[65:]
            if line == "":
                break
            else:
                if line[0] == " ":
                    line = line[1:]
        cursorY += 10

    cursorY += 20
    line = '"' + dat["flavorText"] + '"'
    fontBody = ImageFont.truetype("comici.ttf", 24)
    while(True):
            draw.text((104, cursorY),line[0:65],(0,0,0),font=fontBody)
            cursorY += 25
            line = line[65:]
            if line == "":
                break
            else:
                if line[0] == " ":
                    line = line[1:]
            

    #Paste Mana Icons

    cursorX = 835
    colors = ["green","red","black","blue","white"]
    for color in colors:
        try:
            icon = Image.open("icons/" + color + ".png")
            icon = icon.resize((40, 40), Image.LANCZOS)
            for i in range(dat["manaCost"][color]):
                img.paste(icon, (cursorX, 90))
                cursorX -= 50
        except:
            continue

    colorLess = dat["manaCost"]["colorless"]
    if colorLess > 15:
        colorLess = 15
    if colorLess > 0:
        icon = Image.open("icons/" + str(colorLess) + ".png")
        icon = icon.resize((40, 40), Image.LANCZOS)
        img.paste(icon, (cursorX, 90))
        

    #Paste Image
    if hasImage:
        url = gptConnect.imageGPT(dat["imageDescription"])
        urllib.request.urlretrieve(url, "cardArt.png")
        cardArt = Image.open("cardArt.png")
    else:
        cardArt = Image.open("Van.gogh.paintings/" + random.choice(os.listdir("Van.gogh.paintings/")))
    
    cardArt = cardArt.resize((808, 593), Image.LANCZOS)
    img.paste(cardArt, (84, 163))
    
    img.save(str(output) + '.png')
    return img

#image(gptConnect.getMagicCard(input("Describe your magic card: ")), hasImage = False)
