import json
import os

root = []

root0 = "dataset"

root1s = os.listdir(root0) # 112906_ZF-L12mm

for root1 in root1s:
    root2s = os.listdir(root0+"/"+root1) # 112906_ZF_20191129143722385.avi
    for root2 in root2s:
        root3s = os.listdir(root0+"/"+root1+"/"+root2) # 4-横切面
        for root3 in root3s:
            root.append(root0+"/"+root1+"/"+root2+"/"+root3) 

json_path = os.path.join(path)
assert os.path.isfile(json_path), "No json configuration file found at {}".format(json_path)
with open(json_path, "r", encoding='UTF-8') as f:
    label = json.load(f)
    # self.__dict__.update(params)
    print(label)