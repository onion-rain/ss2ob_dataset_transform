import cv2
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import os
from skimage import measure,color
import shutil
import numpy as np
from colorama import Fore, Back, Style

images_root = "new_dataset/images/" # save root
labels_root = "new_dataset/labels/"

root0 = "dataset" # unprocessed dataset
roots = []
root1s = os.listdir(root0) # 112906_ZF-L12mm

for root1 in root1s:
    root2s = os.listdir(root0+"/"+root1) # 112906_ZF_20191129143722385.avi
    for root2 in root2s:
        root3s = os.listdir(root0+"/"+root1+"/"+root2) # 4-横切面
        for root3 in root3s:
            roots.append(root0+"/"+root1+"/"+root2+"/"+root3) 

# thyroid: mask1[300][mask1[300].nonzero()]取值为143/144，判断[140, 150]为thyroid
# thyroid: mask1[300][mask1[300].nonzero()]取值为142，判断[140, 150]为thyroid

for root in roots:
    dirs = os.listdir(root)
    for dir in dirs:
        if dir.endswith(".jpg"):
            
            img_path = root+"/"+dir
            mask1_path = root+"/outputs/attachments/"+dir[:-4]+"_1.png"
            mask2_path = root+"/outputs/attachments/"+dir[:-4]+"_2.png"

            img = cv2.imread(img_path)
            mask1 = cv2.imread(mask1_path, cv2.IMREAD_UNCHANGED) # 读成彩色带透明通道[w, h, (rgbl)]
            mask2 = cv2.imread(mask2_path, cv2.IMREAD_UNCHANGED)

            thyroid_mask = None
            nodule_mask = None
            if mask1 is not None:
                i = 0
                while 1:
                    pixel = mask1[np.argwhere(mask1[..., 3]>200)[i][0]][np.argwhere(mask1[..., 3]>200)[i][1]]

                    if pixel[0] > 180 and pixel[1] < 150 and pixel[2] > 110:
                        assert nodule_mask is None
                        nodule_mask = mask1
                        nodule_mask_path = mask1_path
                        break
                    elif pixel[0] < 180 and pixel[1] > 150 and pixel[2] < 110:
                        assert thyroid_mask is None
                        thyroid_mask = mask1
                        thyroid_mask_path = mask1_path
                        break

                    if i >= len(np.argwhere(mask1[..., 3]>200))-1:
                        # raise Exception("what is this: {}".format(mask1_path))
                        print(Fore.RED+"Error"+Fore.RESET+": what is this: {}".format(mask1_path))
                        break
                    else:
                        i += 1

            if mask2 is not None:
                i = 0
                while 1:
                    pixel = mask2[np.argwhere(mask2[..., 3]>200)[i][0]][np.argwhere(mask2[..., 3]>200)[i][1]]

                    if pixel[0] > 180 and pixel[1] < 150 and pixel[2] > 110:
                        assert nodule_mask is None
                        nodule_mask = mask2
                        nodule_mask_path = mask2_path
                        break
                    elif pixel[0] < 180 and pixel[1] > 150 and pixel[2] < 110:
                        assert thyroid_mask is None
                        thyroid_mask = mask2
                        thyroid_mask_path = mask2_path
                        break

                    if i >= len(np.argwhere(mask2[..., 3]>200))-1:
                        # raise Exception("what is this: {}".format(mask2_path))
                        print(Fore.RED+"Error"+Fore.RESET+": what is this: {}".format(mask2_path))
                        break
                    else:
                        i += 1


            # if mask1[mask1.nonzero()[0][i]][mask1.nonzero()[1][j]][3]
            if thyroid_mask is not None:
                gray_thyroid_mask = thyroid_mask[..., 3] # 直接取透明通道那一维作为灰度图好了
                gray_thyroid_mask = gray_thyroid_mask/255
                _, binary_thyroid_mask = cv2.threshold(gray_thyroid_mask, 0.1, 1, cv2.THRESH_BINARY)
                thyroid_label = label(binary_thyroid_mask)
                thyroid_props = regionprops(thyroid_label)

            if nodule_mask is not None:
                gray_nodule_mask = nodule_mask[..., 3]
                gray_nodule_mask = gray_nodule_mask/255
                _, binary_nodule_mask = cv2.threshold(gray_nodule_mask, 0.1, 1, cv2.THRESH_BINARY)
                nodule_label = label(binary_nodule_mask)
                nodule_props = regionprops(nodule_label)
            
            
            image_path = images_root + dir
            label_path = labels_root + dir[:-4] + ".txt"
            shutil.copyfile(img_path, image_path)
            # os.mknod(label_path)

            with open(label_path, "w+", encoding="utf-8") as f:
                if thyroid_mask is not None:
                    if thyroid_props == []:
                        print(Fore.RED+"Error"+Fore.RESET+": No thyroid bounding box found! label path: {}".format(thyroid_mask_path))
                    for prop in thyroid_props:
                        # print("found thyroid bounding box", prop.bbox)
                        cls_id = 0
                        x = (prop.bbox[1] + prop.bbox[3])/2/img.shape[1]
                        y = (prop.bbox[0] + prop.bbox[2])/2/img.shape[0]
                        w = (prop.bbox[3] - prop.bbox[1])/img.shape[1]
                        h = (prop.bbox[2] - prop.bbox[0])/img.shape[0]
                        label_str = "{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(cls_id, x, y, w, h)
                        f.write(label_str)
                else:
                    print(Fore.YELLOW+"Warning"+Fore.RESET+": No thyroid label found! img path: {}".format(img_path))
                if nodule_mask is not None:
                    if nodule_props == []:
                        print(Fore.RED+"Error"+Fore.RESET+": No nodule bounding box found! label path: {}".format(nodule_mask_path))
                    for prop in nodule_props:
                        # print("found nodule  bounding box", prop.bbox)
                        cls_id = 1
                        x = (prop.bbox[1] + prop.bbox[3])/2/img.shape[1]
                        y = (prop.bbox[0] + prop.bbox[2])/2/img.shape[0]
                        w = (prop.bbox[3] - prop.bbox[1])/img.shape[1]
                        h = (prop.bbox[2] - prop.bbox[0])/img.shape[0]
                        label_str = "{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(cls_id, x, y, w, h)
                        f.write(label_str)
                else:
                    print(Fore.YELLOW+"Warning"+Fore.RESET+": No nodule label found! img path: {}".format(img_path))
                    
            f.close()

            fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
            # ax1.imshow(img)
            # ax2.imshow(mask1)
            # ax3.imshow(mask2)
            # ax4.imshow(img_x)
            # plt.show()

