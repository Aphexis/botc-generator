from wand.image import Image
from wand.font import Font
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color
import wand

# https://stackoverflow.com/questions/68979045/how-can-i-draw-a-curved-text-using-python-converting-text-to-curved-image
# https://stackoverflow.com/questions/32337481/changing-a-canvas-size-without-rescaling-image-using-wand-and-imagemagick

def curved_text_to_image(
text: str,
font_filepath: str,
font_size: int,
color: str,  #assumes hex string
curve_degree: int,
image_width: int,
image_height: int,
shadow:bool,
filename: str):
    """
    Uses ImageMagik / wand - so have to ensure its installed.
    """
    with wand.image.Image(width=image_width, height=image_height, resolution=(600, 600)) as img: # open an image
        if shadow:
            with Drawing() as draw:   # Create the white shadow underneath text
                # assign font details
                draw.font = font_filepath
                draw.font_size = font_size
                draw.fill_color = wand.color.Color("#FFFFFF")
                # get size of text
                metrics = draw.get_font_metrics(img, text)
                height, width = int(metrics.text_height)+20, int(metrics.text_width) # add some padding on height to account for letters like g

                # resize the image
                img.resize(width, height)
                # draw the text
                draw.text(0+1, height-20+1, text) # slight offset
                draw(img)
                img.gaussian_blur(4, 2)
            
        with Drawing() as draw:   # Create text
            # assign font details
            draw.font = font_filepath
            draw.font_size = font_size
            draw.fill_color = wand.color.Color(color)
            # get size of text
            metrics = draw.get_font_metrics(img, text)
            height, width = int(metrics.text_height)+20, int(metrics.text_width) # add some padding on height to account for letters like g

            # resize the image
            img.resize(width, height)
            # draw the text
            draw.text(0, height-20, text)
            draw(img)
            img.virtual_pixel = 'transparent'
            
            # curve_degree arc, rotated 0 degrees - ie at the top
            if curve_degree >= 0:
                img.distort('arc', (curve_degree, 0))
            else:
                # rotate it 180 degrees, then distory and rotate back 180 degrees
                img.rotate(180)
                img.distort('arc', (abs(curve_degree), 180))
            img.format = 'png'
            # print("before", img.width, img.height)
            img.transform(resize=f'{image_width}x{image_height}>')
            # print("after", img.width, img.height)
            img.save(filename=filename)
            return img

def straight_text_to_image(
text: str,
font_filepath: str,
font_size: int,
color: str,  #assumes hex string
image_width: int,
image_height: int,
shadow:bool,
filename: str):
    """
    Uses ImageMagik / wand - so have to ensure its installed.
    """
    with wand.image.Image(width=image_width, height=image_height, resolution=(600, 600)) as img: # open an image
        if shadow:
            with Drawing() as draw:   # Create the white shadow underneath text
                # assign font details
                draw.font = font_filepath
                draw.font_size = font_size
                draw.fill_color = wand.color.Color("#FFFFFF")
                # get size of text
                metrics = draw.get_font_metrics(img, text)
                height, width = int(metrics.text_height)+20, int(metrics.text_width) # add some padding on height to account for letters like g

                # resize the image
                img.resize(width, height)
                # draw the text
                draw.text(0+1, height-20+1, text) # slight offset
                draw(img)
                img.gaussian_blur(4, 2)
            
        with Drawing() as draw:   # Create text
            # assign font details
            draw.font = font_filepath
            draw.font_size = font_size
            draw.fill_color = wand.color.Color(color)
            # get size of text
            metrics = draw.get_font_metrics(img, text)
            height, width = int(metrics.text_height)+20, int(metrics.text_width) # add some padding on height to account for letters like g

            # resize the image
            img.resize(width, height)
            # draw the text
            draw.text(0, height-20, text)
            draw(img)
            img.virtual_pixel = 'transparent'
            img.save(filename=filename)
            return img

def pad_text(s, total_len):
    
    padding_needed = (total_len - len(s)) // 2 # padding needed on each side
    # print(total_len, len(s), padding_needed)
    return " " * padding_needed + s + " " * padding_needed

# print(pad_text("Fenris Agent", len("              Fenris Agent              ")))

# curved_text_to_image(
# pad_text("Fenris Agent", 40),
# # "              Fenris Agent              ",
# "dum1.ttf",
# font_size=70,
# color="#000000",
# curve_degree=-360,
# image_width=460,
# image_height=460,
# padding=100,
# filename="fenrisagent_text.png")

# straight_text_to_image(
# "straight text",
# # "              Fenris Agent              ",
# "dum1.ttf",
# font_size=70,
# color="#000000",
# image_width=460,
# image_height=460,
# shadow=False,
# filename="fenrisagent_text.png")
