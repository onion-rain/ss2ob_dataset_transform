import cv2
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt
import os
from skimage import measure,color

roots = []

root0 = "dataset"

root1s = os.listdir(root0) # 112906_ZF-L12mm

for root1 in root1s:
    root2s = os.listdir(root0+"/"+root1) # 112906_ZF_20191129143722385.avi
    for root2 in root2s:
        root3s = os.listdir(root0+"/"+root1+"/"+root2) # 4-横切面
        for root3 in root3s:
            roots.append(root0+"/"+root1+"/"+root2+"/"+root3) 

imgs_path = []
mask1s_path = []
mask2s_path = []
for root in roots:
    dirs = os.listdir(root)
    for dir in dirs:
        if dir.endswith(".jpg"):
            imgs_path.append(root+"/"+dir)
            mask1s_path.append(root+"/outputs/attachments/"+dir[:-4]+"_1.png")
            mask2s_path.append(root+"/outputs/attachments/"+dir[:-4]+"_2.png")

for i, img_path in enumerate(imgs_path):
    
    mask1_path = mask1s_path[i]
    mask2_path = mask2s_path[i]

    img = cv2.imread(img_path)
    mask1 = cv2.imread(mask1_path, 0)/255 # 读成灰度图
    mask2 = cv2.imread(mask2_path, 0)/255

    _, binary_mask1 = cv2.threshold(mask1, 0.5, 1, cv2.THRESH_BINARY)
    _, binary_mask2 = cv2.threshold(mask2, 0.5, 1, cv2.THRESH_BINARY)

    label1 = label(binary_mask1)
    label2 = label(binary_mask2)

    props1 = regionprops(label1)
    props2 = regionprops(label2)
    img_x = img.copy()
    for prop in props1:
        print("found bounding box", prop.bbox)
        cv2.rectangle(img_x, (prop.bbox[1], prop.bbox[0]), (prop.bbox[3], prop.bbox[2]), (255, 0, 0), 2)
    for prop in props2:
        print("found bounding box", prop.bbox)
        cv2.rectangle(img_x, (prop.bbox[1], prop.bbox[0]), (prop.bbox[3], prop.bbox[2]), (255, 0, 0), 2)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
    ax1.imshow(img)
    ax2.imshow(mask1)
    ax3.imshow(mask2)
    ax4.imshow(img_x)
    plt.show()