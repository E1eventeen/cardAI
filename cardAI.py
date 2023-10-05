from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import urllib.request
import gptConnect
import os, random

TEXT_WIDTH = 60

# Text Query is 250 tokens or roughly $0.000875 a query 1142 -> $1
# Image Query is $0.016 a query, or 62 images -> $1
# A commander deck is roughly $1.68

def image(dat, hasImage = True, output = "output"):
    if type(dat) is str:
        dat = eval(dat)

    if not "name" in dat:
        dat["name"] = "Card Name"
    if not "typeLine" in dat:
        dat["typeLine"] = "Type Line"
    if not "keywords" in dat:
        dat["keywords"] = []
    if not "abilityDescriptions" in dat:
        dat["abilityDescriptions"] = []
    if not "flavorText" in dat:
        dat["flavorText"] = "Flavor Text"
    if not "power" in dat:
        dat["power"] = 1
    if not "toughness" in dat:
        dat["toughness"] = 1
    if not "imageDescription" in dat:
        dat["imageDescription"] = "Abstract Art"
    if not "manaCost" in dat or dat["typeLine"] == "Land":
        dat["manaCost"] = {
        "red": 0,
        "blue": 0,
        "green": 0,
        "black": 0,
        "white": 0,
        "colorless": 0
    }

    tempColor = random.randint(1, 10)    
    img = Image.open("templates/" + str(tempColor) + ".png")
    draw = ImageDraw.Draw(img)
    #print(dat)
    #Write Card Name
    if len(dat["name"]) > 15:
        size = 32
        fontName = ImageFont.truetype("comicbd.ttf", size)
        draw.text((96, 76 + (42 - size)),dat["name"],(0,0,0),font=fontName)
    else:
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
        while True:
            cursorY += 25
            last_space = line.rfind(' ', 0, TEXT_WIDTH)
            if last_space == -1 or len(line) <= TEXT_WIDTH:
                break
            draw.text((104, cursorY), line[:last_space], (0, 0, 0), font=fontBody)
            line = line[last_space + 1:]
            
        if line:
            draw.text((104, cursorY), line, (0, 0, 0), font=fontBody)

        cursorY += 10

    cursorY += 20
    line = '"' + dat["flavorText"] + '"'
    fontBody = ImageFont.truetype("comici.ttf", 24)
    while True:
        cursorY += 25
        last_space = line.rfind(' ', 0, TEXT_WIDTH)
        if last_space == -1 or len(line) <= TEXT_WIDTH:
            break
        draw.text((104, cursorY), line[:last_space], (0, 0, 0), font=fontBody)
        line = line[last_space + 1:]
        
    if line:
        draw.text((104, cursorY), line, (0, 0, 0), font=fontBody)

    #Paste Mana Icons

    cursorX = 835
    cx = 40
    cy = 90

    colors = ["green","red","black","blue","white"]
    totalMana = 0
    colorLess = dat["manaCost"]["colorless"]
    if colorLess > 0:
        totalMana = 1
    for color in colors:
        totalMana += dat["manaCost"][color]
    if totalMana > 5:
        cx = 30
        cy = 95
    
    mask = Image.new('L', (cx, cx), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, cx, cx), fill=255)
    
    for color in colors:
        try:
            icon = Image.open("icons/" + color + ".png")
            icon = icon.resize((cx, cx), Image.LANCZOS)
            for i in range(dat["manaCost"][color]):
                img.paste(icon, (cursorX, cy), mask)
                cursorX -= round(cx * 1.25)
        except:
            continue


    if colorLess > 15:
        colorLess = 15
    if colorLess > 0:
        icon = Image.open("icons/" + str(colorLess) + ".png")
        icon = icon.resize((cx, cx), Image.LANCZOS)
        img.paste(icon, (cursorX, cy), mask)
        

    #Paste Image
    if hasImage:
        url = gptConnect.imageGPT(dat["imageDescription"])
        urllib.request.urlretrieve(url, "cardArt.png")
        cardArt = Image.open("cardArt.png")
    else:
        cardArt = Image.open("Van.gogh.paintings/" + random.choice(os.listdir("Van.gogh.paintings/")))
    
    cardArt = cardArt.resize((808, 593), Image.LANCZOS)
    #cardArt = cardArt.crop((0, 28, 808, 780))
    #cardArt.save("cardArt.png")
    #alteredArt = Image.open("cardArt.png")
    img.paste(cardArt, (84, 163))
    
    cardArt.close()
    if hasImage:
        os.remove("cardArt.png")
    img.save(str(output) + '.png')
    return img

#image(gptConnect.getMagicCard(input("Describe your magic card: ")), hasImage = False)
