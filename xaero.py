import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math


def paint_chinese_opencv(im, chinese, pos, color):
    img_PIL = Image.fromarray(cv.cvtColor(im, cv.COLOR_BGR2RGB))
    font = ImageFont.truetype('setofont.ttf', 16)
    fillColor = color  
    position = pos  
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, chinese, font=font, fill=fillColor)

    img = cv.cvtColor(np.asarray(img_PIL), cv.COLOR_RGB2BGR)
    return img


# C:\Users\phill\Desktop\遊戲\MultiMC\instances\1.18.2\.minecraft\XaeroWaypoints\Multiplayer_cloudtown.ml\dim%-1\mw$94871466_1.txt
filename = input("Enter the fileurl: ")
ct = 0
points = []
maxp = []
zoom = 1
with open(filename, "r", encoding="utf-8") as file:
    for line in file:
        if ct < 3:
            ct += 1
            continue
        line = line.split(":")
        t = {
            "x": int(line[3]),
            "y": int(line[5]),
            "name": line[1]
        }
        maxp.append(line[3])
        maxp.append(line[5])
        points.append(t)
centerx = 0
centery = 0
for i in points:
    if "大廳" in i["name"]:
        centerx = i["x"]
        centery = i["y"]
        break
if centerx == 0 and centery == 0:
    maxp = int(max(maxp)*zoom+300)
else:
    maxp = 0
    for i in points:
        if math.sqrt(math.pow(i["x"], 2)+math.pow(i["y"], 2))*zoom > maxp:
            maxp = math.sqrt(math.pow(i["x"], 2)+math.pow(i["y"], 2))*zoom
    maxp = int(maxp+math.sqrt(math.pow(centerx, 2) +
               math.pow(centery, 2))*zoom+300)

img = np.zeros((maxp, maxp, 3), np.uint8)
img[:] = (255, 255, 255)

cv.line(img, (maxp, int(maxp/2)), (-maxp, int(maxp/2)), (0, 0, 0), 1)
cv.line(img, (int(maxp/2), maxp), (int(maxp/2), -maxp), (0, 0, 0), 1)


for i in points:
    cv.circle(img, (int(i["x"]*zoom+int(maxp/2)-centerx*zoom),
              int(i["y"]*zoom+int(maxp/2)-centery*zoom)), 2, (0, 255, 0), 3)
    img = paint_chinese_opencv(img, i["name"], (int(
        i["x"]*zoom+int(maxp/2)-centerx*zoom+3), int(i["y"]*zoom+int(maxp/2)-centery*zoom)+3), (0, 0, 255))
    if i["x"]- centerx > 0 and i["y"]- centery > 0:
        if i["x"] - centerx > i["y"] - centery: # 如果x軸大於y軸

            cv.line(img, (int(i["x"]*zoom+int(maxp/2)-centerx*zoom), int(i["y"]*zoom+int(maxp/2) -
                    centery*zoom)), (int(i["x"]*zoom+int(maxp/2)-centerx*zoom), int(maxp/2)), (0, 0, 0), 1) # y軸移動
        else:
            cv.line(img, (int(i["x"]*zoom+int(maxp/2)-centerx*zoom), int(i["y"]*zoom+int(maxp/2) -
                    centery*zoom)), (int(maxp/2), int(i["y"]*zoom+int(maxp/2)-centery*zoom)), (0, 0, 0), 1) # x
    else:
        if i["x"] - centerx > i["y"] - centery: # 如果x軸大於y軸
            cv.line(img, (int(i["x"]*zoom+int(maxp/2)-centerx*zoom), int(i["y"]*zoom+int(maxp/2) -
                    centery*zoom)), (int(maxp/2), int(i["y"]*zoom+int(maxp/2)-centery*zoom)), (0, 0, 0), 1) # x
            print("now is x")
        else:
            cv.line(img, (int(i["x"]*zoom+int(maxp/2)-centerx*zoom), int(i["y"]*zoom+int(maxp/2) -
                    centery*zoom)), (int(i["x"]*zoom+int(maxp/2)-centerx*zoom), int(maxp/2)), (0, 0, 0), 1) # y軸移動
            print("now is y")
    

cv.imwrite("line.png", img)