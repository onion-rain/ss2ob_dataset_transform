import argparse
import random
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description='network trainer')

parser.add_argument('--train', type=int, default=-1,
                    help='tran dataset capacity(default: -1 means dynamically adjusts based on the valid capacity)')
parser.add_argument('--valid', type=int, default=50,
                    help='valid dataset capacity(default: 0 means no valid dataset)')
args = parser.parse_args()

with open("thyroid_dataset/imgs_catalogue.part", "r", encoding="utf-8")as f:
    img_list = f.readlines()
    img_num = len(img_list)

    if args.train == -1 and args.valid != -1:
        valid_num = args.valid
        train_num = img_num - valid_num
    elif args.train != -1 and args.valid == -1:
        train_num = args.valid
        valid_num = img_num - train_num
    elif args.train != -1 and args.valid != -1:
        train_num = args.train
        valid_num = args.valid
        assert train_num+valid_num <= img_num
    else:
        raise Exception("args 'train' and 'valid' can not equal to -1 at the same time")
    
    img_list = np.array(img_list, dtype = str)
    if train_num > valid_num:
        ids = random.sample(range(0, img_num-1), valid_num)
        valid_list = img_list[ids].tolist()
        train_list = np.delete(img_list, ids).tolist()
    else:
        ids = random.sample(range(0, img_num-1), train_num)
        train_list = img_list[ids].tolist()
        valid_list = np.delete(img_list, ids).tolist()

with open("thyroid_dataset/train_list.txt", "w+", encoding="utf-8")as f:
    for i in range(len(train_list)):
        f.write(current_dir+"/thyroid_dataset"+train_list[i])
with open("thyroid_dataset/valid_list.txt", "w+", encoding="utf-8")as f:
    for i in range(len(valid_list)):
        f.write(current_dir+"/thyroid_dataset"+valid_list[i])

    print()