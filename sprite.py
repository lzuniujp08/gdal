import os
from PIL import Image
import numpy as np
import json

root = r"D:/project/year2019/guangzhou_grid/guangzhou-grid-web/static/img/weather_icon_black/"
filenames = os.listdir(root)

plt_json = {}
plt_np = np.zeros(shape=(len(filenames)*30, 30, 4))
for i in range(len(filenames)):
    nep = Image.open(root + filenames[i])
    neppx = list(nep.getdata())
    plt_np[30*i:30*i+nep.size[1],0:nep.size[0]] = np.array(neppx).flatten().reshape(nep.size[1],nep.size[0],4)
    plt_json[filenames[i]] = {
      "x": 0,
      "y": 30*i,
      "width": nep.size[0],
      "height": nep.size[1],
      "pixelRatio": 1,
      "visible": True
    }
print(plt_json)

imm = Image.fromarray(np.uint8(plt_np))
imm.save(root + 'weather.png', 'png')

with open(root + "weather.json", "w") as f:
    json.dump(plt_json, f)
