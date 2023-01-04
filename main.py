import requests
from bs4 import BeautifulSoup
import os.path
import json
from PIL import Image, ImageDraw, ImageFont


def get_product_picture(query):
    r = requests.get(f'https://www.ah.be/zoeken/api/products/search?query={query}&size=1')
    data = json.loads(r.text)
    product = data['cards'][0]['products'][0]
    product_url = f"https://www.ah.be{product['link']}"
    image_url = product['images'][1]['url']

    filename = query.replace(' ', '-').replace('"', '')
    path = f"images/{filename}"

    if not (os.path.exists(path + ".png")):
        with open(path + '.png', 'wb') as f:
            im = requests.get(image_url)
            f.write(im.content)

        im = Image.open("images/" + filename + ".png").convert('RGBA')

        draw = ImageDraw.Draw(im)

        font = ImageFont.truetype("arial.ttf", size=20)

        width, height = im.size

        max_width = width - 20
        font_size = 16
        while True:
            text_width, text_height = draw.textsize(query, font=font)
            if text_width <= max_width:
                break
            font_size -= 1
            font = ImageFont.truetype('arial.ttf', font_size)

        x = (width - text_width) // 2

        rect_y2 = height
        y = rect_y2 - text_height

        # Draw a rectangle behind the text
        rect_x1 = x - 5  # Add some padding around the text
        rect_y1 = y - 5
        rect_x2 = x + text_width + 5
        draw.rectangle((rect_x1, rect_y1, rect_x2, rect_y2), fill=(255, 255, 255))

        draw.text((x, y), query, (0, 0, 0), font=font)
        im.save("images/" + filename + ".png")


get_product_picture("Douwe Egberts Lungo original capsules voordeelpak(20 stuks)")