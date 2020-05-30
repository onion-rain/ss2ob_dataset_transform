import cv2
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt


from skimage import measure,color

imgPath = "data/train_images/test.jpg"
# imgPath = "112906_ZF_20191129143722385.avi/4-横切面/outputs/attachments/112906_ZF_20191129143722385_169_1.png"
img_0 = cv2.imread(imgPath)
mask = cv2.imread(imgPath.replace('images', 'labels').replace('.jpg', '.png'), 0)/255

ret, binary = cv2.threshold(mask, 0.5, 1, cv2.THRESH_BINARY)

label_0 = label(binary)
dst=color.label2rgb(label_0)  #根据不同的标记显示不同的颜色
print('regions number:',label_0.max()+1)  #显示连通区域块数(从0开始标记)

props = regionprops(label_0)
img_1 = img_0.copy()
for prop in props:
    print("found bounding box", prop.bbox)
    cv2.rectangle(img_1, (prop.bbox[1], prop.bbox[0]), (prop.bbox[3], prop.bbox[2]), (255, 0, 0), 2)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.imshow(img_0)
ax2.imshow(mask)
ax3.imshow(img_1)
plt.show()