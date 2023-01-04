import requests
from bs4 import BeautifulSoup
import os.path
import json
from PIL import Image, ImageDraw, ImageFont


def get_product_picture(query, quantity):
    r = requests.get(f'https://www.ah.be/zoeken/api/products/search?query={query}&size=1')
    data = json.loads(r.text)
    product = data['cards'][0]['products'][0]
    image_url = product['images'][1]['url']

    filename = query.replace(' ', '-').replace('"', '')
    path = f"images/{filename}"

    if not (os.path.exists(path + ".png")):
        with open(path + '.png', 'wb') as f:
            im = requests.get(image_url)
            f.write(im.content)

        im = Image.open("images/" + filename + ".png").convert('RGBA')

        width, height = im.size

        new_height = height + 65
        new_im = Image.new('RGB', (width, new_height), (230, 230, 230))

        new_im.paste(im, (0, 0))

        draw = ImageDraw.Draw(new_im)
        font = ImageFont.truetype("arial.ttf", size=30)

        max_width = width
        font_size = 30
        while True:
            text_width, text_height = draw.textsize(query, font=font)
            if text_width <= max_width:
                break
            font_size -= 1
            font = ImageFont.truetype('arial.ttf', font_size)

        x = (width - text_width) // 2
        y = height + 15

        draw.text((x, y), query, (0, 0, 0), font=font)
        new_im.save("images/" + filename + ".png")


get_product_picture("AH Volle melk(0,5 l)")
