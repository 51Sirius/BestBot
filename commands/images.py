import PIL as pl
from PIL import Image, ImageFont, ImageDraw
import requests
import numpy as np


def create_lvl_card(ctx, rank, rank_name):
    member = ctx.author
    id = ctx.author.id
    image_av = member.avatar_url_as(format='png', size=128)
    url = image_av
    try:
        resp = requests.get(url, stream=True).raw
    except requests.exceptions.RequestException:
        print('Error')
    try:
        img = Image.open(resp)
    except IOError:
        print("Unable to open image")
    img.save('images/w.png', 'png')
    img = Image.open("images/w.png").convert("RGB")
    npImage = np.array(img)
    h, w = img.size
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)
    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    Image.fromarray(npImage).save('images/w.png')
    phon = Image.open('images/phon.png')
    av = Image.open('images/w.png')
    phon.paste(av, (50, 72), av)
    phon.save('images/w.png', 'png')
    rank, score = rank[0], rank[1]
    im = Image.open('images/w.png')
    draw_rank = ImageDraw.Draw(im)
    font = ImageFont.truetype('fonts/third.ttf', size=40)
    font1 = ImageFont.truetype('fonts/third.ttf', size=30)
    draw_rank.text((200, 130), f'{member.nick}', fill=(255, 255, 255), font=font)
    draw_rank.text((150, 318), f'{score[0]} / {score[1]}', fill=(255, 255, 255), font=font1)
    draw_rank.text((350, 260), f'{rank_name}', fill=(255, 255, 255), font=font1)
    kf = score[0] / score[1]
    draw_rank.rectangle((355, 305, int(355 + 390*kf), 355), fill=(255, 255, 255), outline=(0, 0, 0))
    im.save('images/w.png', 'png')
