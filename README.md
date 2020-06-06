# Semantic segmentation 2 Object detection dataset transform

语义分割数据集转换为目标检测数据集

原语义分割数据集为精灵标注助手标注所得，目录如下图
![tree](tree.jpg)

1.提取图片和label并存储为coco格式: `python transform.py`

2.生成imgs相对路径列表: `python mk_catalogue.py`

3.随机划分训练集、验证集并生成绝对目录列表: `python div_dataset.py`

4.提取验证集图片: `python get_valid_images.py`