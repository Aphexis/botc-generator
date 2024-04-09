from PIL import Image, ImageDraw
import json
import requests
import os
from tqdm import tqdm
import textgenerator

def create_circular_icon(icon_path, text_path, background_path, output_path, token_size, icon_padding, extra_icon_padding_h):
    # Load images
    icon = Image.open(icon_path).convert("RGBA")
    background = Image.open(background_path).convert("RGBA")
    text = Image.open(text_path).convert("RGBA")

    # Calculate circle diameter in pixels
    circle_diameter = token_size

    # Resize icon to fit inside the circle (with padding)
    # if (not oversized):
    #     icon_padding = 70 # 15%
    # else:
    #     icon_padding = 130 # 28%
    icon = icon.resize((circle_diameter-icon_padding, circle_diameter-icon_padding), Image.LANCZOS)

    # Resize background to fit inside the circle
    background = background.resize((circle_diameter, circle_diameter))

    # Paste icon onto the background
    icon_padding_w = icon_padding // 2
    icon_padding_h = icon_padding // 2 - extra_icon_padding_h
    background.paste(icon, ((background.width - circle_diameter) // 2 + icon_padding_w, (background.height - circle_diameter) // 2 + icon_padding_h), icon)
    text_padding_w = (circle_diameter - text.width) // 2
    text_padding_h = (circle_diameter - text.height) // 2
    background.paste(text, ((background.width - circle_diameter) // 2 + text_padding_w, (background.height - circle_diameter) // 2 + text_padding_h), text)

    # Create a circular mask
    mask = Image.new("L", (circle_diameter, circle_diameter), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, circle_diameter, circle_diameter), fill=255)

    # Apply mask to the icon
    background.putalpha(mask)

    # Save the final image
    background.save(output_path)

def create_text(text, pad_size, font_filepath, font_size, color, size, shadow, output_filename):
    textgenerator.curved_text_to_image(
        textgenerator.pad_text(text, pad_size),
        font_filepath=font_filepath, # "dum1.ttf",
        font_size=font_size,
        color=color,
        curve_degree=-360,
        image_width=size, #460,
        image_height=size, #460,
        # padding=padding, #100,
        shadow=shadow,
        filename=output_filename
    )

def create_token(char):
    # char: id, image, reminders, name
    # oversized is a custom addition to the json that indicates if the icon will be too large at the default size
    # raiseToken is a custom addition to the json that indicates the token image should be raised slightly on the text
    text_outputfile = f"output/{char['name']}_text.png"
    # create_text(char['name'], "#000000", True, text_outputfile)    
    oversized = char.get("oversized", False)
    raise_token = char.get("raiseToken", False)
    if (not oversized):
        icon_padding = 70 # 15%
    else:
        icon_padding = 130 # 28%
    if (raise_token or oversized):
        icon_padding_h = 20
    else:
        icon_padding_h = 0
    create_text(text=char['name'], pad_size=40, font_filepath="dum1.ttf", font_size=70, color="#000000", size=360, shadow=True, output_filename=text_outputfile)
    create_circular_icon(
        icon_path=requests.get(char['image'], stream=True).raw,
        text_path=text_outputfile,
        background_path="tokenbg_wideoutline.png",
        output_path=f"output/{char['name']}_token.png",
        token_size=460,
        # oversized=char.get("oversized", False),
        # raise_token=char.get("raiseToken", False)
        icon_padding=icon_padding,
        extra_icon_padding_h=icon_padding_h
    )
    os.remove(text_outputfile) # cleanup the text files

def create_reminders(char):
    oversized = char.get("oversized", False)
    raise_token = char.get("raiseToken", False)
    if (not oversized):
        icon_padding = 40 # 15%
    else:
        icon_padding = 70 # 28%
    if (raise_token or oversized):
        icon_padding_h = 10
    else:
        icon_padding_h = 5
    # print(oversized, raise_token, icon_padding, icon_padding_h)
    for reminder in char['reminders']:
        text_outputfile = f"output/{char['name']}_{reminder}.png" 
        create_text(text=reminder, pad_size=60, font_filepath="Trade Gothic LT Std Regular.otf", font_size=30, color="#FFFFFF", size=170, shadow=False, output_filename=text_outputfile) 
        create_circular_icon(
            icon_path=requests.get(char['image'], stream=True).raw,
            text_path=text_outputfile,
            background_path="reminderbg_outlined.png",
            output_path=f"output/{char['name']}_{reminder}_reminder.png",
            token_size=200,
            icon_padding=icon_padding,
            extra_icon_padding_h=icon_padding_h
        )
        os.remove(text_outputfile) # cleanup the text file

def create_from_json(json_path):
    with open(json_path) as json_file:
        data = json.load(json_file)
        for char in tqdm(data):
            if char['id'] == "_meta" or "image" not in char or char['team'] == "fabled":
                continue # ignore
            # print(char['name'])
            create_token(char)
            create_reminders(char)

# Check whether the specified path exists or not
folder_exists = os.path.exists("output")
if not folder_exists:
   # Create a new directory because it does not exist
   os.makedirs("output")

# Example usage:
# create_circle_icon("icon.png", "Short text", "background.jpg", "output.png", "YourFont.ttf", 10)  # Assuming 10 pixels per millimeter
# create_token("fenrisagent_defenders_of_europa_ravenswood.png", "fenrisagent_text.png", "tokenbg_wideoutline.png", "output.png", "dum1.ttf", 10)  # Assuming 10 pixels per millimeter
# create_from_json("botc_scythe.json")

# akiko = {
#     "id": "akiko_defenders_of_europa_ravenswood",
#     "image": "https://www.bloodstar.xyz/p/nobadinohz/defenders_of_europa_ravenswood/akiko_defenders_of_europa_ravenswood.png",
#     "otherNightReminder": "If Akiko has unused trap tokens, they choose a player and give a finger signal. Apply relevant effects.",
#     "reminders": [
#       "1: Evil does not act",
#       "2: Poisoned",
#       "3: No vote",
#       "4: Poisoned"
#     ],
#     "name": "Akiko",
#     "team": "townsfolk",
#     "ability": "Each night*, choose a player and an unused trap (1-4): If 1 and the player is evil, they do not act for 2 nights; if 3, they lose their vote(s) tomorrow; if even, they are poisoned until the second time they use their ability.",
#     "otherNight": 4,
#     "oversized": True
#   }
# create_reminders(akiko)
# create_token(akiko)

# vesna =   {
#     "id": "vesna_defenders_of_europa_ravenswood",
#     "image": "https://www.bloodstar.xyz/p/nobadinohz/defenders_of_europa_ravenswood/vesna_defenders_of_europa_ravenswood.png",
#     "otherNightReminder": "On Night 2, Vesna chooses two players: If either are evil, Vesna is poisoned. On Night 3, point to the relevant players. On Night 4, point to the relevant players.",
#     "reminders": ["Chosen", "Chosen", "Poisoned"],
#     "name": "Vesna",
#     "team": "outsider",
#     "ability": "On your second night, choose 2 players (not yourself): If either are evil, you are poisoned for the rest of the game. The next night, learn who they targeted that night. The next night, learn up to 2 related players.",
#     "otherNight": 19
#   }
# create_reminders(vesna)

kar = {
    "id": "kar_defenders_of_europa_ravenswood",
    "image": "https://www.bloodstar.xyz/p/nobadinohz/defenders_of_europa_ravenswood/kar_defenders_of_europa_ravenswood.png",
    "otherNightReminder": "Kar might choose a player. If this player is a demon, decrease the Demon targets by 1 tonight, and the chosen player switches seats with Zehra.",
    "reminders": ["-1 Desolation Targets", "Demon chosen", "No ability"],
    "setup": True,
    "name": "Kar",
    "team": "townsfolk",
    "ability": "Once per game, at night*, choose a player: If a Demon is chosen, decrease the number of Demon targets by 1 tonight; they switch seats with Zehra. [+Zehra]",
    "otherNight": 5,
    "raiseToken": True
    # "oversized": True
  }
# create_token(kar)
create_reminders(kar)