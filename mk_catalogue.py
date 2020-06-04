import os

root = "/home/xueruini/onion_rain/pytorch/dataset/thyroid/"

imgs = os.listdir(root+"images")
labels = os.listdir(root+"labels")

with open("imgs_catalogue.part", "w+", encoding="utf-8") as f:
    for path in imgs:
        path = "/images/" + path + "\r\n"
        f.write(path)

# with open("labels_catalogue.part", "w+", encoding="utf-8") as f:
#     for path in labels:
#         path = "/labels/" + path + "\r\n"
#         f.write(path)