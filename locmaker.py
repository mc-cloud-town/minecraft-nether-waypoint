import json
from PIL import Image, ImageDraw, ImageFont

with open("./data/survival.json","r",encoding="utf-8") as file:
    data = [{"name":i["name"],"pos":i["pos"]} for i in json.load(file) if i["dim"] == -1]
center = next((point["pos"] for point in data if "大廳" in point["name"]), {"x":0,"y":0,"z":0})

map_max_point = max([max(abs(point["pos"]["x"]),abs(point["pos"]["z"])) for point in data])
print(map_max_point)

img = Image.new("RGB",(int(map_max_point*2),int(map_max_point*2)),(255,255,255))
draw = ImageDraw.Draw(img)

for point in data:
    x = point["pos"]["x"] + map_max_point
    y = point["pos"]["z"] + map_max_point
    draw.ellipse((x-2,y-2,x+2,y+2),(0,255,0))
    draw.text((x+3,y+3),point["name"],(0,0,255))

img.show()