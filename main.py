import requests
import re
import os.path
import json
from PIL import Image, ImageDraw, ImageFont


def get_product_picture(item, quantity):
    text = re.sub(r'\(.*\)', '', item)
    r = requests.get(f'https://www.ah.be/zoeken/api/products/search?query={text}&size=1')
    data = json.loads(r.text)
    print(data)
    product = data['cards'][0]['products'][0]
    image_url = product['images'][1]['url']

    filename = item.replace(' ', '-').replace('"', '')
    path = f"images/{filename}"

    if not (os.path.exists(path + ".png")):
        with open(path + '.png', 'wb') as f:
            im = requests.get(image_url)
            f.write(im.content)

        im = Image.open("images/" + filename + ".png").convert('RGBA')

        width, height = im.size

        new_height = height + 120
        new_im = Image.new('RGB', (width, new_height), (255, 255, 255))

        new_im.paste(im, (0, 60))

        draw = ImageDraw.Draw(new_im)
        font = ImageFont.truetype("arial.ttf", size=30)

        max_width = width
        font_size = 30
        while True:
            text_width, text_height = draw.textsize(item, font=font)
            if text_width <= max_width:
                break
            font_size -= 1
            font = ImageFont.truetype('arial.ttf', font_size)

        x = ((width - text_width) // 2)
        y = height + 75

        draw.text((x, y), item, (0, 0, 0), font=font)
        font = ImageFont.truetype('arial.ttf', 50)
        draw.text((10, 5), quantity, (255, 0, 0), font=font)
        new_im.save("images/" + filename + ".png")


def get_product_list(shopping_list):
    data = shopping_list.replace('Mijn boodschappenlijstje: \n', '').replace('• ', '')
    lines = data.strip().split('\n')
    nested_array = []
    for line in lines:
        match = re.match(r'(\d+)x (.*)', line)
        if match:
            nested_array.append([match.group(1), match.group(2)])

    return nested_array


shopping_list = '''Mijn boodschappenlijstje: 
• 1x AH Blauwe bessen(300 g)
• 1x AH Bospeen(per bos)
• 1x AH Vastkokend aardappelen(3 kg)
• 1x AH Verse spaghetti all'uovo(250 g)
• 2x AH Appelmoes 0%(360 g)
• 1x AH Scharrel kipreepjes(320 g)
• 1x AH Beenham bel(150 g)
• 1x Ganda Natuurlijk gedroogde ham 80 gram bel(80 g)
• 1x AH Luchtige cracker volkoren met rijstbloem(250 g)
• 1x Bertolli Vloeibaar(500 ml)
• 1x AH Verse scharreleieren M(10 stuks)
• 1x AH Magere melk(1 l)
• 1x AH Volle melk(0,5 l)
• 1x Schär Choco chip cookies glutenvrij(100 g)
• 2x AH Water koolzuurvrij(12 x 0,5 l)
• 1x L'OR Espresso forza capsules(20 stuks)
• 1x Douwe Egberts Lungo original capsules voordeelpak(20 stuks)
• 1x Always Dailies fresh & protect inlegkruisjes(30 stuks)
• 1x AH Zacht & sterk toiletpapier 3-laags(18 rollen)
• 1x Ariel Pods original(39 wasbeurten)'''

items = get_product_list(shopping_list)
for i in range(len(items)):
    print(items[i][1])
    get_product_picture(items[i][1], items[i][0])


