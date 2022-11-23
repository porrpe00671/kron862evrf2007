
from urllib.request import urlopen
import json


class GugikData:

    def GetData():
        file = ""
        with urlopen("http://www.gugik.gov.pl/__data/assets/text_file/0016/1843/gugik-evrf2007.txt") as conn:
            file = conn.read()

        array = file.splitlines()
        _a = []

        for i in range(0, len(array)):
            try:
                l_ = array[i].decode('UTF-8').split('\t')
                _a.append([float(l_[0]), float(l_[1]), float(l_[2])])
            except:
                None

        json_data = json.dumps(_a, separators=(',', ':'))

        with open("db.json", mode='w') as f:
            f.write(json_data)
            f.close()
