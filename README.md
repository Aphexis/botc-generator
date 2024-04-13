# botc-generator
Generates token pngs for a botc script based on a json input file.

## Usage
Generate token by calling `create_from_json(path_to_json)` within `tokengenerator.py`.

### Input
The json file is the same format as a json that could be accepted into [bloodstar.xyz](bloodstar.xyz).

There are two custom parameters that can be added to the JSON:
- `oversized: true` indicates that the token's image is oversized and needs to be shrunk more and raised to not overlap with text 
- `raiseToken: true` indicates that the token's image needs to be raised to not overlap with text

If both `oversized` and `raiseToken` are present, the raise effect will only be applied once.

Specific tweaks to the amount of padding, size of text, etc. can be tweaked directly within the script.

### Output
Output is within `output/characters` and `output/reminders` for character and reminder tokens respectively.

There are various token backgrounds that can be used, based on the desired usage of token images. 
- `tokenbg_wideoutline.png` is the character token background optimized for printing. It has a light dotted outline that is meant to be a cutting guide if hand-cutting custom tokens.
- `reminderbg_hex.png` is similarly an outlined hex shape (non-standard for BOTC tokens) for ease of printing and cutting, although standard circular backgrounds are also avaliable.

## Implementation Notes
`create_text` in `tokengenerator` is used to generate text. `create_text` calls  `curved_text_to_image` in `textgenerator.py`.
- To have the appropriate amount of radius of curving, the text is padded with spaces to reach a total maximum length. To increase the RADIUS of the curved text, change the `pad_size` parameter of `create_text`.
- To increase the font size, change the `font_size` parameter of `create_text`

Background images are sourced from [Blood on the Clocktower Online](https://online.bloodontheclocktower.com/).