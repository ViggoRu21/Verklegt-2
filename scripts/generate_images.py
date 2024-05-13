import os
import random
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


def generate_logo(company_name):
    width, height = 400, 300
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Background color
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image.paste(bg_color, [0, 0, width, height])
    try:
        font = ImageFont.truetype("arial.ttf", random.randint(20, 40))  # Random font size
    except IOError:
        font = ImageFont.load_default()

    #  Text
    text_width, text_height = draw.textbbox((0, 0), company_name, font=font)[2:]
    text_position = ((width - text_width) / 2, (height - text_height) / 2)
    text_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.text(text_position, company_name, font=font, fill=text_color)

    # Shapes
    for _ in range(random.randint(1, 5)):
        shape_type = random.choice(['rectangle', 'ellipse'])
        x0, x1 = sorted([random.randint(0, width), random.randint(0, width)])
        y0, y1 = sorted([random.randint(0, height), random.randint(0, height)])
        shape_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if shape_type == 'rectangle':
            draw.rectangle([x0, y0, x1, y1], outline=shape_color, width=2)
        elif shape_type == 'ellipse':
            draw.ellipse([x0, y0, x1, y1], outline=shape_color, width=2)

    # Save
    logo_directory = os.path.join('media/logos')
    if not os.path.exists(logo_directory):
        os.makedirs(logo_directory)
    logo_filename = f'{company_name.replace(" ", "_")}.png'
    logo_path = os.path.join(logo_directory, logo_filename)
    image.save(logo_path)

    return os.path.join('logos', logo_filename)
