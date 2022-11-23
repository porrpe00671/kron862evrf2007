import converter as cnv
# uncommand when you want to refresh data from GUGIK
# from gugikData import GugikData
import math
import sys
import time
import json
import utils

C = cnv.Converter()

# Performance measurement - Start
start_time = time.time()

out = []
minX = sys.float_info.max
maxX = -sys.float_info.min
minY = sys.float_info.max
maxY = -sys.float_info.min

with open("data.txt", encoding='utf-8') as f:
    for line in f:
        l_ = line.split('\t')
        l_[0] = float(l_[0])
        l_[1] = float(l_[1])
        l_[2] = float(l_[2])
        out.append(C.Method1(l_[0], l_[1]))
        if minX > out[-1][0]:
            minX = out[-1][0]
        if maxX < out[-1][0]:
            maxX = out[-1][0]
        if minY > out[-1][1]:
            minY = out[-1][1]
        if maxY < out[-1][1]:
            maxY = out[-1][1]

# uncommand when you want to refresh data from GUGIK
# GugikData.GetData()

data = []

with open("db.json", encoding='utf-8') as f:
    file = f.readlines()
    data = json.loads(file[0])

minX = math.floor(minX * 100) / 100
minY = math.floor(minY * 100) / 100
maxX = math.ceil(maxX * 100) / 100
maxY = math.ceil(maxY * 100) / 100

_data = []

for i in data:
    if i[0] >= minX and i[1] >= minY and i[0] <= maxX and i[1] <= maxY:
        _data.append(i)

del data

outp = []
for i in out:
    x = i[0]
    y = i[1]
    rect = utils.find_rectangle_coordinates(_data, x, y)
    interpolation = utils.bilinear_interpolation(x, y, rect)
    outp.append((x, y, interpolation))

print(json.dumps(outp, separators=(',', ':')))
# Performance measurement - End
print("--- %s seconds ---" % (time.time() - start_time))
