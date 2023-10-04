import openai

with open("apiKey.txt", "r") as f:
	openai.api_key = f.read()

messages = [ {"role": "system", "content": 
              "You are a intelligent assistant."} ]

query = """Generate a magic the gathering card in the following JSON format: {
    "name": "Card Name",
    "manaCost": {
        "red": 0,
        "blue": 0,
        "green": 0,
        "black": 0,
        "white": 0,
        "colorless": 0
    },
    "typeLine": "Card Type",
    "keywords": [],
    "abilityDescriptions": [],
    "flavorText": "Flavor Text",
    "power": 0,
    "toughness": 0,
    "imageDescription": "Image Description"
}

The card should have an appropriate mana cost relative to its strengths, and vice versa.
If the card is a land, it should have a mana cost of 0.
The card should follow the following description, and have at least one ability or keyword, and require at least 1 mana: 
"""

def getMagicCard(text):
    messages = [{"role": "user", "content": query + text}]
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
    return chat.choices[0].message.content

def imageGPT(prompt):
    response = openai.Image.create(
        prompt=prompt + ", in the art style of magic the gathering",
        n=1,
        size="256x256"
        )
    return response["data"][0]["url"]
