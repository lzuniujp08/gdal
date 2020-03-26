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
    for k in range(len(neppx)):
        for y in range(nep.size[1]):
            for x in range(nep.size[0]):
                for z in range(4):
                    plt_np[30 * i + y, x, z] = neppx[y * nep.size[0] + x][z]
    plt_json[filenames[i]] = {
      "x": 0,
      "y": 30 * i,
      "width": nep.size[0],
      "height": nep.size[1],
      "pixelRatio": 1,
      "visible": "true"
    }
print(plt_json)

imm = Image.fromarray(np.uint8(plt_np))
imm.save(root + 'weather.png', 'png')

with open(root + "weather.json", "w") as f:
    json.dump(plt_json, f)
