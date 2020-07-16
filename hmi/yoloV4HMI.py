# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Project\16yolov4-tf2-master\hmi\yoloV4.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(930, 666)
        self.camera = QtWidgets.QGraphicsView(Form)
        self.camera.setGeometry(QtCore.QRect(20, 10, 640, 480))
        self.camera.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.camera.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.camera.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.camera.setObjectName("camera")
        self.text = QtWidgets.QTextBrowser(Form)
        self.text.setGeometry(QtCore.QRect(20, 510, 351, 121))
        self.text.setObjectName("text")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(740, 30, 95, 411))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.con_plc = QtWidgets.QPushButton(self.layoutWidget)
        self.con_plc.setObjectName("con_plc")
        self.verticalLayout.addWidget(self.con_plc)
        self.discon_plc = QtWidgets.QPushButton(self.layoutWidget)
        self.discon_plc.setObjectName("discon_plc")
        self.verticalLayout.addWidget(self.discon_plc)
        self.con_mysql = QtWidgets.QPushButton(self.layoutWidget)
        self.con_mysql.setObjectName("con_mysql")
        self.verticalLayout.addWidget(self.con_mysql)
        self.discon_mysql = QtWidgets.QPushButton(self.layoutWidget)
        self.discon_mysql.setObjectName("discon_mysql")
        self.verticalLayout.addWidget(self.discon_mysql)
        self.start = QtWidgets.QPushButton(self.layoutWidget)
        self.start.setObjectName("start")
        self.verticalLayout.addWidget(self.start)
        self.stop = QtWidgets.QPushButton(self.layoutWidget)
        self.stop.setObjectName("stop")
        self.verticalLayout.addWidget(self.stop)
        self.exit = QtWidgets.QPushButton(self.layoutWidget)
        self.exit.setObjectName("exit")
        self.verticalLayout.addWidget(self.exit)
        self.enable_rs = QtWidgets.QCheckBox(Form)
        self.enable_rs.setGeometry(QtCore.QRect(740, 560, 131, 19))
        self.enable_rs.setObjectName("enable_rs")
        self.text_rs = QtWidgets.QTextBrowser(Form)
        self.text_rs.setGeometry(QtCore.QRect(380, 510, 281, 121))
        self.text_rs.setObjectName("text_rs")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.con_plc.setText(_translate("Form", "连接PLC"))
        self.discon_plc.setText(_translate("Form", "断开PLC"))
        self.con_mysql.setText(_translate("Form", "连接数据库"))
        self.discon_mysql.setText(_translate("Form", "断开数据库"))
        self.start.setText(_translate("Form", "启动"))
        self.stop.setText(_translate("Form", "停止"))
        self.exit.setText(_translate("Form", "退出"))
        self.enable_rs.setText(_translate("Form", "启用语音识别"))

