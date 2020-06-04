from shutil import copyfile

valid_txt_path = "/home/xueruini/onion_rain/pytorch/dataset/thyroid/valid_imgs_catalogue.txt"
imgs_root = "/home/xueruini/onion_rain/pytorch/dataset/thyroid/images/"
valid_imgs_root = "/home/xueruini/onion_rain/pytorch/dataset/thyroid/valid_imgs/"

with open(valid_txt_path, "r", encoding="utf-8") as f:
    for line in f.readlines():
        line = line.strip('\n')  #去掉列表中每一个元素的换行符
        copyfile(line, valid_imgs_root+line.split("/")[-1])
        
        