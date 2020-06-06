from shutil import copyfile

valid_txt_path = "thyroid_dataset/valid_list.txt"
imgs_root = "thyroid_dataset/images/"
valid_imgs_root = "valid_imgs/"

with open(valid_txt_path, "r", encoding="utf-8") as f:
    for line in f.readlines():
        line = line.strip('\n')  #去掉列表中每一个元素的换行符
        copyfile(line, valid_imgs_root+line.split("/")[-1])
        
        