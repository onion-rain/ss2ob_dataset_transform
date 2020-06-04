import cv2
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import os
from skimage import measure,color
import shutil

images_root = "new_dataset/images/"
labels_root = "new_dataset/labels/"

root0 = "dataset"
roots = []
root1s = os.listdir(root0) # 112906_ZF-L12mm

for root1 in root1s:
    root2s = os.listdir(root0+"/"+root1) # 112906_ZF_20191129143722385.avi
    for root2 in root2s:
        root3s = os.listdir(root0+"/"+root1+"/"+root2) # 4-横切面
        for root3 in root3s:
            roots.append(root0+"/"+root1+"/"+root2+"/"+root3) 

# imgs_path = []
# mask1s_path = []
# mask2s_path = []
for root in roots:
    dirs = os.listdir(root)
    for dir in dirs:
        if dir.endswith(".jpg"):
            
            img_path = root+"/"+dir
            mask1_path = root+"/outputs/attachments/"+dir[:-4]+"_1.png"
            mask2_path = root+"/outputs/attachments/"+dir[:-4]+"_2.png"

            img = cv2.imread(img_path)
            mask1 = cv2.imread(mask1_path, 0) # 读成灰度图
            mask2 = cv2.imread(mask2_path, 0)

            if mask1 is not None:
                mask1 = mask1/255
                _, binary_mask1 = cv2.threshold(mask1, 0.5, 1, cv2.THRESH_BINARY)
                label1 = label(binary_mask1)
                props1 = regionprops(label1)

            if mask2 is not None:
                mask2 = mask2/255
                _, binary_mask2 = cv2.threshold(mask2, 0.5, 1, cv2.THRESH_BINARY)
                label2 = label(binary_mask2)
                props2 = regionprops(label2)
            
            
            image_path = images_root + dir
            label_path = labels_root + dir[:-4] + ".txt"
            shutil.copyfile(img_path, image_path)
            # os.mknod(label_path)

            with open(label_path, "w+", encoding="utf-8") as f:
                if mask1 is not None:
                    for prop in props1:
                        print("found bounding box", prop.bbox)
                        cls_id = 0
                        x = (prop.bbox[1] + prop.bbox[3])/2/img.shape[1]
                        y = (prop.bbox[0] + prop.bbox[2])/2/img.shape[0]
                        w = (prop.bbox[3] - prop.bbox[1])/img.shape[1]
                        h = (prop.bbox[2] - prop.bbox[0])/img.shape[0]
                        label_str = "{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(cls_id, x, y, w, h)
                        f.write(label_str)
                if mask2 is not None:
                    for prop in props2:
                        print("found bounding box", prop.bbox)
                        cls_id = 1
                        x = (prop.bbox[1] + prop.bbox[3])/2/img.shape[1]
                        y = (prop.bbox[0] + prop.bbox[2])/2/img.shape[0]
                        w = (prop.bbox[3] - prop.bbox[1])/img.shape[1]
                        h = (prop.bbox[2] - prop.bbox[0])/img.shape[0]
                        label_str = "{} {:.6f} {:.6f} {:.6f} {:.6f}\n".format(cls_id, x, y, w, h)
                        f.write(label_str)
                    
            f.close()

            fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
            # ax1.imshow(img)
            # ax2.imshow(mask1)
            # ax3.imshow(mask2)
            # ax4.imshow(img_x)
            # plt.show()

