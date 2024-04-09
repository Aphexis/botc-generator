from wand.image import Image
from wand.font import Font
from wand.display import display
from wand.drawing import Drawing
from wand.color import Color
import wand

# https://stackoverflow.com/questions/68979045/how-can-i-draw-a-curved-text-using-python-converting-text-to-curved-image
# https://stackoverflow.com/questions/32337481/changing-a-canvas-size-without-rescaling-image-using-wand-and-imagemagick

def adjust_ratio(img, w_dst, h_dst):

    img.transform(resize="{0}x{1}".format(w_dst,h_dst))

    w_bor = (w_dst - img.width)/2
    h_bor = (h_dst - img.height)/2

    if w_bor>0:
        img.border(color=Color('transparent'),width=w_bor,height=0)
    else:
        img.border(color=Color('transparent'),width=0,height=h_bor)
    # return img

def curved_text_to_image(
text: str,
font_filepath: str,
font_size: int,
color: str,  #assumes hex string
curve_degree: int,
image_width: int,
image_height: int,
padding: int):
    """
    Uses ImageMagik / wand - so have to ensure its installed.
    """
    with wand.image.Image(width=image_width, height=image_height, resolution=(600, 600)) as img: # open an image
        with Drawing() as draw:   # open a drawing object
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
            
        
        with Drawing() as draw:   # open a drawing object
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
            # img.resize(image_width-padding)
            img.transform(resize=f'{image_width-padding}x{image_height-padding}>')
            # print(height, width, draw.font_size)
            # print(image_width, image_height)
            print(img.width, img.height)
            # offset_x = (image_width - img.width) // 2
            # offset_y = (image_height - img.height) - padding
            # print(offset_x, offset_y)
            # img.extent(image_width, image_height, -offset_x, -offset_y)
            img.save(filename='arc_text.png')
            return img

curved_text_to_image(
"              Fenris Agent              ",
"dum1.ttf",
font_size=70,
color="#000000",
curve_degree=-360,
image_width=440,
image_height=440,
padding=15)