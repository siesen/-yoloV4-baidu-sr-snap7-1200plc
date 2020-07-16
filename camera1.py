#把图像预测放到线程会报张量错误，还是图的问题
#-------------------------------------#
#       调用摄像头检测
#-------------------------------------#
from yolo import YOLO
from PIL import Image
import numpy as np
import cv2
import time
import tensorflow as tf
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QGraphicsPixmapItem,QGraphicsScene
from PyQt5.QtGui import QImage,QPixmap
from hmi.yoloV4HMI import Ui_Form
from PyQt5.QtCore import QTimer,QThread,pyqtSignal
from plc.plc_com import plc_db_com
from sql.mysql_database import mysql_db
from nlp.nlp_pred import NLP
import multiprocessing as mp

physical_devices = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)
# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class nlp_thread(QThread):
    text_changed=pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.nlp=NLP()

    def run(self):        
        for i in self.nlp.predict():
            self.text_changed.emit(i)

class yolo_thread(QThread):
    message=pyqtSignal(list)

    def __init__(self,VideoCapture):
        super().__init__()
        self.yolo=YOLO()

        self.cap=cv2.VideoCapture(VideoCapture)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,480)

    def run(self):
        if self.cap.isOpened():
            self.t1 = time.time()
            ret,frame=self.cap.read()
            if not ret:
                self.cap.release()
                #video end
                self.message.emit(['video end'])
            else:
                # 格式转变，BGRtoRGB
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                # 转变成Image
                frame = Image.fromarray(np.uint8(frame))

                # 进行检测
                frame,prompt_text,out_classes = self.yolo.detect_image(frame)
                #返回检测数据
                self.message.emit([frame,prompt_text,out_classes])

class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self,VideoCapture=0):
        super().__init__()
        self.fps=0.0
        # self.yolo = YOLO()
        self.PLC_db_com=plc_db_com()
        self.mydb=mysql_db()

        #如果是摄像头，去黑边
        self.VideoCapture=VideoCapture+cv2.CAP_DSHOW if VideoCapture==0 else VideoCapture
        
        self.backend=nlp_thread()
        self.backend_yolo=yolo_thread(self.VideoCapture)
        
        self.setupUi(self)

        self.timer_camera = QTimer()     #定义定时器视频显示
        self.timer_speech = QTimer()     #定义定时器语音识别
        
        #signal and slot
        self.start.clicked.connect(self.startcheck)
        self.exit.clicked.connect(self.exit_win)
        self.con_plc.clicked.connect(self.connectplc)
        self.discon_plc.clicked.connect(self.disconnectplc)
        self.stop.clicked.connect(self.stopcheck)
        self.con_mysql.clicked.connect(self.connectsql)
        self.discon_mysql.clicked.connect(self.disconnectsql)

        self.backend.text_changed.connect(self.speech_recognize)
        self.backend.finished.connect(self.thread_end)

        self.backend_yolo.message.connect(self.frame_treat)

        self.enable_rs.stateChanged.connect(self.speech_state)
        self.timer_speech.timeout.connect(self.speech_state)
        self.timer_camera.timeout.connect(self.start_yolo)
        
    def thread_end(self):
        if self.enable_rs.isChecked():
            self.timer_speech.start(1000)

    def speech_state(self):
        if self.enable_rs.isChecked():
            self.timer_speech.stop()
            self.backend.start()
        else:
            self.timer_speech.stop()
            self.backend.quit()
            self.backend.terminate()

    def speech_recognize(self,text):
        #语音识别，进行预测
        print(text)
        self.text_rs.setText(text[:-1])
        command=int(text[-1])
        if command==0:
            self.startcheck()
        elif command==1:
            self.stopcheck()
        elif command==2:
            self.connectsql()
        elif command==3:
            self.disconnectsql()
        elif command==4:
            self.connectplc()
        elif command==5:
            self.disconnectplc()
        elif command==6:
            self.enable_rs.setChecked(False)

    def exit_win(self):
        self.close()
     
    def startcheck(self):
        #打开摄像头，如果链接数据库，则创建表
        if self.mydb.connected:
            self.tablename=time.strftime('%Y-%m-%d/%H:%M:%S')
            self.mydb.create_table(self.tablename)
        
        #采集图像
        self.timer_camera.start(10)

    def start_yolo(self):
        self.timer_camera.stop()
        self.backend_yolo.start()
      
    def stopcheck(self):
        self.timer_camera.stop()
        if hasattr(self.backend_yolo,'cap'):
            if self.cap!=[]:
                self.backend_yolo.cap.release()
        self.backend_yolo.quit()
          
    def connectplc(self):
        message='connect plc ok'if self.PLC_db_com.connect() else 'connect plc fail'
        self.text.setText(message)
        #init plc output
        if message=='connect plc ok':
            output=[0,1,2]
            for each in output:
                self.PLC_db_com.write('bool',0,each,0)

    def disconnectplc(self):
        self.PLC_db_com.disconnect()
        self.text.setText('disconnect the plc')

    def connectsql(self):
        message=self.mydb.connect()
        self.text.setText(message)

    def disconnectsql(self):
        self.mydb.discocnnect()
        self.text.setText('disconnect the database')

    def frame_treat(self,message):
        if message==['video end']:
            self.text.setText('video end')
        else:
            frame=message[0]
            prompt_text=message[1]
            out_classes=message[2]

            frame = np.array(frame)

            # RGBtoBGR满足opencv显示格式
            frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

            self.fps  = ( self.fps + (1./(time.time()-self.backend_yolo.t1)) ) / 2
            # print("fps= %.2f"%(self.fps))
            frame = cv2.putText(frame, "fps= %.2f"%(self.fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            #准备把图片显示出来
            img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            #resize to fit the graphic window
            img=cv2.resize(img,(640,480))
            #cv2 format convert to grapics format
            imgframe=QImage(img,img.shape[1],img.shape[0],QImage.Format_RGB888)
            pix=QPixmap.fromImage(imgframe)
            item=QGraphicsPixmapItem(pix)
            #show
            scene=QGraphicsScene()
            scene.addItem(item)
            self.camera.setScene(scene)
            
            #显示框框信息
            self.text.setText(str(prompt_text))

            #输出PLC
            if hasattr(self.PLC_db_com,'plc') and self.PLC_db_com.plc.get_connected():
                output=[0,1,2]
                for each in output:
                    if each in out_classes:                        
                        self.PLC_db_com.write('bool',0,each,1)
                    else:
                        self.PLC_db_com.write('bool',0,each,0)

            #保存数据库
            if self.mydb.connected:
                self.mydb.insert_data(self.tablename,str(prompt_text))

            #事件循环
            self.timer_camera.start(10)
       
if __name__ == "__main__":
    #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    #初始化
    myWin = MyMainForm()
    #myWin.VideoCapture='video/hairpin1.mp4'
    #将窗口控件显示在屏幕上
    myWin.show()
    #程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())