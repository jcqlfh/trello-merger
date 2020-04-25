import os
import shutil
import datetime
from PIL import Image, ImageDraw, ImageFont #pip install Pillow
from trello import TrelloClient #pip install py-trello

PATH = "C:\\Users\\candi\\AppData\\Roaming\\Microsoft\\Windows\\Themes\\CachedFiles\\"
TRELLO_BOARD = "Personal"
TRELLO_LIST = "Doing"



def copyfiles(folder):
    for file in os.scandir(folder):
        if not os.path.exists(file.path+".bkp") and file.name.endswith(".jpg"):
            shutil.copyfile(file.path,file.path+".bkp")

def writeImg(text):
    for file in os.scandir(PATH):
        if file.name.endswith(".jpg"):
            with open(file.path+".bkp", "rb") as fp:
                im = Image.open(fp)
                x,y = im.size
                font_type = ImageFont.truetype("calibri.ttf",22)
                draw = ImageDraw.Draw(im)
                row=1
                for line in text.split("\n"):
                    draw.text(xy=(x-400,25*row),text=line,fill=(255,255,255),font=font_type)
                    row=row+1
                im.save(file.path, "JPEG", quality=100, optimize=True, progressive=True)

def getTrello():
    cards = ""
    client = TrelloClient(
        api_key="40cda797e04ae2dfecf8d51a8f542a50",
        api_secret="a165d906b3c880aacad03b169f1d23b439e3800dc4921bdcb7e2d5c9ce71b7ac",
        token="6bc249f26a8d7330072195e2a7b5e331152359aa0bd7eab56e7581ab62918759",
        token_secret=""
    )
    order = 0
    for board in client.list_boards():
        if TRELLO_BOARD in board.name:
            for list in board.list_lists():
                if TRELLO_LIST in list.name:
                    for card in list.list_cards():
                        order += 1
                        cards += str(order) + "o. " + card.name + " (" + format(datetime.datetime.strptime(card.due, "%Y-%m-%dT%H:%M:%S.%fZ"), "%d/%m") + ")\n"
    return cards
    
copyfiles(PATH)
writeImg(getTrello())