import json
import os

path = "112906_ZF_20191129143722385.avi/4-横切面\outputs/112906_ZF_20191129143722385_169.json"

json_path = os.path.join(path)
assert os.path.isfile(json_path), "No json configuration file found at {}".format(json_path)
with open(json_path, "r", encoding='UTF-8') as f:
    label = json.load(f)
    # self.__dict__.update(params)
    print(label)