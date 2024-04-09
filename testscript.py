from PIL import Image, ImageDraw, ImageFont

def create_circle_icon(icon_path, text_path, background_path, output_path, font_path, ppmm):
    # Load images
    icon = Image.open(icon_path).convert("RGBA")
    background = Image.open(background_path).convert("RGBA")
    text = Image.open(text_path).convert("RGBA")

    # Calculate circle diameter in pixels
    circle_diameter = int(45 * ppmm)

    # Resize icon to fit inside the circle (with padding)
    icon_padding = 20
    icon = icon.resize((circle_diameter-icon_padding, circle_diameter-icon_padding), Image.LANCZOS)
    # text = text.resize((circle_diameter, circle_diameter), Image.LANCZOS)

    # Resize background to fit inside the circle
    background = background.resize((circle_diameter, circle_diameter))

    # Paste icon onto the background
    background.paste(icon, ((background.width - circle_diameter + icon_padding) // 2, (background.height - circle_diameter + icon_padding) // 2), icon)
    padding_w = (circle_diameter - text.width) // 2
    padding_h = (circle_diameter - text.height) // 2
    background.paste(text, ((background.width - circle_diameter) // 2 + padding_w, (background.height - circle_diameter) // 2 + padding_h), text)

    # Create a circular mask
    mask = Image.new("L", (circle_diameter, circle_diameter), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, circle_diameter, circle_diameter), fill=255)

    # Apply mask to the icon
    background.putalpha(mask)

    # Save the final image
    background.save(output_path)

# Example usage:
# create_circle_icon("icon.png", "Short text", "background.jpg", "output.png", "YourFont.ttf", 10)  # Assuming 10 pixels per millimeter
create_circle_icon("fenrisagent_defenders_of_europa_ravenswood.png", "arc_text.png", "tokenbg_outlined.png", "output.png", "dum1.ttf", 10)  # Assuming 10 pixels per millimeter
