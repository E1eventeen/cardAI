# Project Name: CardAI - Magic The Gathering Card Generator

## Description:
CardAI is a project that leverages OpenAI's cutting-edge technologies to generate Magic The Gathering (MTG) cards. It consists of two main scripts: `cardAI.py` and `gptConnect.py`. `cardAI.py` is responsible for creating MTG card images based on provided data, while `gptConnect.py` connects to OpenAI's API to enhance the card generation process.

## Getting Started:

### Prerequisites:
Before you can use this project, you'll need the following:

1. Python 3.7 or higher installed on your system.
2. OpenAI API credentials to access GPT-3 and DALL-E models.

### Installation:
1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/your-username/cardAI.git
   cd cardAI
   ```

2. Install the required Python packages.

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API credentials by following the instructions provided by OpenAI.

4. Replace the placeholder API key in the `apiKey.txt` file with your actual credentials.

## Usage:

### cardAI.py
The `cardAI.py` script allows you to generate Magic The Gathering cards with the following functions:

#### `image(dat, hasImage=True, output="output")`
- Generates an MTG card image.
- Parameters:
  - `dat`: A JSON string or dictionary containing card data.
  - `hasImage` (optional): If `True`, a card image will be generated using DALL-E. If `False`, a random Van Gogh painting will be used as the card's background.
  - `output` (optional): The name of the output file (default: "output.png").
- Returns: The generated card image.

### gptConnect.py
The `gptConnect.py` script connects to OpenAI's API and provides the following functions:

#### `getMagicCard(text)`
- Generates a Magic The Gathering card using the provided text as a description.
- Parameters:
  - `text`: The description text for the card.
- Returns: A JSON file representing the generated MTG card.

#### `imageGPT(prompt)`
- Generates an image URL of a DALL-E-generated image based on the given prompt.
- Parameters:
  - `prompt`: The prompt for generating the image.
- Returns: The URL of the DALL-E-generated image.

## Example Usage:
Here's an example of how to use the CardAI project:

```python
from cardAI import image
from gptConnect import getMagicCard, imageGPT

# Generate a Magic The Gathering card image with custom data
card_data = {
    "name": "Card Name",
    "type": "Creature - Beast",
    "power": "4",
    "toughness": "4",
    "flavor_text": "This is an example card.",
}

image(card_data, hasImage=True, output="custom_card.png")

# Generate a Magic The Gathering card using a description
card_description = "A powerful wizard with magical abilities."
generated_card = getMagicCard(card_description)
print(generated_card)

# Generate a DALL-E image based on a prompt
image_url = imageGPT("fantasy landscape")
print(f"DALL-E generated image URL: {image_url}")
```
