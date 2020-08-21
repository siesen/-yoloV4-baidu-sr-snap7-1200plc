# YOLOV4：You Only Look Once目标检测模型在Tensorflow2当中的实现，加入百度语音识别，通过snap7控制西门子1200PLC
---

### 目录
1. [所需环境 Environment](#所需环境)
2. [注意事项 Attention](#注意事项)
3. [小技巧的设置 TricksSet](#小技巧的设置)
4. [文件下载 Download](#文件下载)
5. [训练步骤 How2train](#训练步骤)
6. [参考资料 Reference](#Reference)

### 概述
检测三个分类，硬币，发夹，玩具。  
语音识别源自baidu，语义分类为全连接网络。  
使用snap7连接西门子1200plc。  
目标检测YOLOV4框架源码源自 https://github.com/bubbliiiing/yolov4-tf2   
yoloV4源码详解UP主B站有视频 地址：https://www.bilibili.com/video/BV1yK411J7Zc

### 所需环境
python==3.7
tensorflow-gpu==2.2.0
pyaudio==0.2.11
baidu-aip==2.2.18.0
jieba==0.42.1
python-snap7==0.11
opencv==4.2.0

### 注意事项
**yoloV4和nlp处理有两个神经网络，keras载入有报错。我采用了折衷的方法，nlp预测模型时报错就重新载入模型，这样避免了报错，但损失了效率。有好的方法请告诉我** 

**camera.py把yoloV4预测放在主线程，没有问题。camera1.py把yoloV4预测放在子线程，运行时会报错，应该还是两个网络模型载入的问题，有解决方式请告诉我**

**语音识别本想使用sphinx，但无论英文还是中文，识别率很低，所以换成了baidu语音识别。如果知道如何训练和改进sphinx模型，请告诉我。**

**才学python半年，代码有改进和提高的地方请告诉我哈，感谢赐教!**  

### 小技巧的设置
在train.py和train_eager.py文件下：   
1、mosaic参数可用于控制是否实现Mosaic数据增强。   
2、Cosine_scheduler可用于控制是否使用学习率余弦退火衰减。   
3、label_smoothing可用于控制是否Label Smoothing平滑。  

在train_eager.py文件下：   
1、regularization参数可用于控制是否实现正则化损失。  

### 文件下载
相关文件链接在 文件链接.txt中
init-loss8.4.h5是本案例检测硬币，发夹，玩具的权重  
yolo4_weights.h5是coco数据集的权重。  
yolo4_voc_weights.h5是voc数据集的权重。  
video文件夹是用于生成训练图片的视频文件，也可以用来做预测用  
train_images是分解后的训练图片  
train_nlp是训练语音识别的文本文件

### 训练步骤
1、本文使用VOC格式进行训练。  
2、训练前将标签文件放在VOCdevkit文件夹下的VOC2007文件夹下的Annotation中。  
3、训练前将图片文件放在VOCdevkit文件夹下的VOC2007文件夹下的JPEGImages中。  
4、在训练前利用voc2yolo3.py文件生成对应的txt。  
5、再运行根目录下的voc_annotation.py，运行前需要将classes改成你自己的classes。  
```python
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
```
6、就会生成对应的2007_train.txt，每一行对应其图片位置及其真实框的位置。  
7、在训练前需要修改model_data里面的voc_classes.txt文件，需要将classes改成你自己的classes。  
8、运行train.py即可开始训练。
训练过程可以参考原UP主

### Reference
https://github.com/bubbliiiing/yolov4-tf2  
https://github.com/qqwweee/keras-yolo3/  
https://github.com/Cartucho/mAP  
https://github.com/Ma-Dan/keras-yolo4  
