import PIL as pl
from PIL import Image, ImageFont, ImageDraw
import requests
import numpy as np


def create_card(member, rank, rank_name):
    image_av = str(member.avatar) + "?size=128"
    url = image_av
    try:
        resp = requests.get(url, stream=True).raw
    except requests.exceptions.RequestException:
        print('Error')
    try:
        img = Image.open(resp)
    except IOError:
        print("Unable to open image")
    img.save('src/card/w.png', 'png')
    img = Image.open("src/card/w.png").convert("RGB")
    npImage = np.array(img)
    h, w = img.size
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)
    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    Image.fromarray(npImage).save('src/card/w.png')
    phon = Image.open('src/card/phon.png')
    av = Image.open('src/card/w.png')
    phon.paste(av, (50, 72), av)
    phon.save('src/card/w.png', 'png')
    rank, score = rank[0], rank[1]
    im = Image.open('src/card/w.png')
    draw_rank = ImageDraw.Draw(im)
    font = ImageFont.truetype('src/card/third.ttf', size=40)
    font1 = ImageFont.truetype('src/card/third.ttf', size=30)
    draw_rank.text((200, 130), f'{member.nick}', fill=(255, 255, 255), font=font)
    draw_rank.text((150, 318), f'{score[0]} / {score[1]}', fill=(255, 255, 255), font=font1)
    draw_rank.text((350, 260), f'{rank_name}', fill=(255, 255, 255), font=font1)
    kf = score[0] / score[1]
    draw_rank.rectangle((355, 305, int(355 + 390*kf), 355), fill=(255, 255, 255), outline=(0, 0, 0))
    im.save('src/card/w.png', 'png')