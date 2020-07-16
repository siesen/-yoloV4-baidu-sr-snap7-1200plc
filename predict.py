from yolo import YOLO
from PIL import Image
import tensorflow as tf

physical_devices = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

yolo = YOLO()

while True:
   img = input('Input image filename:')
   try:
       if img=='exit':
           break
       image = Image.open(img)
   except:
       print('Open Error! Try again!')
       continue
   else:
       r_image = yolo.detect_image(image)
       r_image.show()


# import os
# import time        
# path='./VOCdevkit/VOC2007/JPEGImages'
# img_list=os.listdir(path)

# for each in img_list:
#     #concatenate full file name
#     if each[-3:]=='jpg':
#         img_name=os.path.join(path,each)
#         image = Image.open(img_name)
#         r_image=yolo.detect_image(image)
#         r_image.show()
#         time.sleep(1)
