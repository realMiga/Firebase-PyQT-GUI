# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import pyrebase
import sys
from time import sleep
import datetime
import json
import os
import RPi.GPIO as GPIO
from pi_sht1x import SHT1x
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import *

signin_status = False
enter = 0
    
userEmail=""
userPass=""

now = datetime.datetime.now()
time1 = now.strftime("%d %B %Y at %H:%M:%S")

#Enter firebase real-time databse credentials here
config = {"apiKey": "Enter your api key here",
          "authDomain": "Enter your auth domain here",
          "databaseURL": "Enter database URL here",
          "projectId": "Enter Project ID",
          "storageBucket": "Enter storage bucket",
          "messagingSenderId": "Enter ms_id"}

qTimer = QTimer()

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

class dataThread(QThread): #dataThread not closing itself
    signal = pyqtSignal() 
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
            
    def run(self):
        while True:
            now = datetime.datetime.now()
            time1 = now.strftime("%d %B %Y at %H:%M:%S")
            with SHT1x(18, 23, gpio_mode=GPIO.BCM) as sensor:
                config = {"apiKey": "Enter your api key here",
                          "authDomain": "Enter your auth domain here",
                          "databaseURL": "Enter database URL here",
                          "projectId": "Enter Project ID",
                          "storageBucket": "Enter storage bucket",
                          "messagingSenderId": "Enter ms_id"}
                firebase = pyrebase.initialize_app(config)
                auth = firebase.auth()
                db = firebase.database()
                user = auth.sign_in_with_email_and_password(userEmail, userPass)
                temp = sensor.read_temperature()
                hum = sensor.read_humidity(temp)
                dew1 = sensor.calculate_dew_point(temp, hum)
                data = {'Time Batch': time1, 'Temperature': temp,  'Humidity': hum,  'Dew Point': dew1}
                result = db.child("pol2").child("SHT10").push(data, user['idToken'])
            print(str(result))
            self.signal.emit()
            sleep(5)
            QApplication.processEvents()

class Ui_MainWindow(object):
    def __init__(self, parent = None):
        super(Ui_MainWindow, self).__init__()
        self.dthread = dataThread()
        self.dthread.signal.connect(self.finished)
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(758, 600)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(620, 30, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        ###################################################
        self.pushButton_2.clicked.connect(self.signin)
        ###################################################
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 30, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 30, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 30, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 70, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setAutoFillBackground(False)
        self.pushButton_3.setObjectName("pushButton_3")
        ###################################################
        self.pushButton_3.clicked.connect(self.forgot)
        ###################################################
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(270, 70, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        ###################################################
        self.pushButton_4.clicked.connect(self.create)
        ###################################################
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 130, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(80, 220, 61, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(60, 260, 71, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(310, 220, 111, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(330, 260, 81, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(510, 220, 181, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(120, 410, 61, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(70, 470, 111, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(60, 530, 121, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(440, 470, 141, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(110, 440, 71, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(130, 380, 51, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(70, 500, 111, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(480, 410, 101, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(470, 440, 111, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(500, 380, 81, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(390, 500, 191, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(390, 530, 191, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(530, 320, 71, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(50, 320, 81, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(290, 320, 111, 21))
        font = QtGui.QFont()
        font.setFamily("PibotoLt")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(620, 250, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        ##################################################
        self.pushButton_5.clicked.connect(self.timer1)
        ##################################################
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(390, 70, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        ###################################################
        self.pushButton_6.clicked.connect(self.verify)
        ###################################################
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(200, 30, 151, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(460, 30, 151, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(520, 70, 171, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(140, 210, 151, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(140, 250, 151, 31))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(140, 310, 101, 31))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setGeometry(QtCore.QRect(410, 210, 81, 31))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(410, 250, 81, 31))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_9.setGeometry(QtCore.QRect(510, 250, 101, 31))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_10.setGeometry(QtCore.QRect(410, 310, 91, 31))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_11.setGeometry(QtCore.QRect(600, 310, 81, 31))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_12.setGeometry(QtCore.QRect(190, 370, 101, 31))
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_13.setGeometry(QtCore.QRect(190, 400, 101, 31))
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.lineEdit_14 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_14.setGeometry(QtCore.QRect(190, 430, 101, 31))
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.lineEdit_15 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_15.setGeometry(QtCore.QRect(190, 520, 101, 31))
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.lineEdit_16 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_16.setGeometry(QtCore.QRect(190, 490, 101, 31))
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.lineEdit_17 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_17.setGeometry(QtCore.QRect(190, 460, 101, 31))
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_18.setGeometry(QtCore.QRect(580, 370, 101, 31))
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.lineEdit_19 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_19.setGeometry(QtCore.QRect(580, 400, 101, 31))
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.lineEdit_20 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_20.setGeometry(QtCore.QRect(580, 430, 101, 31))
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.lineEdit_21 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_21.setGeometry(QtCore.QRect(580, 460, 101, 31))
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.lineEdit_22 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_22.setGeometry(QtCore.QRect(580, 490, 101, 31))
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.lineEdit_23 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_23.setGeometry(QtCore.QRect(580, 520, 101, 31))
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(170, 120, 521, 71))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 758, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuClose = QtWidgets.QMenu(self.menubar)
        self.menuClose.setObjectName("menuClose")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_As)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuClose.menuAction())
        # set interval to 1 s
        qTimer.setInterval(3000) # 1000 ms = 1 s
        # connect timeout signal to signal handler
        qTimer.timeout.connect(self.loaddata)
        # start timer
        qTimer.start()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def signin(self):
        global signin_status
        userEmail = self.lineEdit.text()
        userPass = self.lineEdit_2.text()
        # Log the user in
        user = auth.sign_in_with_email_and_password(userEmail, userPass)
        self.textEdit.setText(str(auth.get_account_info(user['idToken']))) #implement if user_id then else
        if (user['idToken']):
            self.lineEdit_3.setText("Sign in successfull!!!")
            signin_status = True
        else:
            self.lineEdit_3.setText("Unsuccessfull!!!")
            signin_status = False
            
    def forgot(self):
        global userEmail
        userEmail = self.lineEdit.text()#check wrong password
        #Reset Password
        auth.send_password_reset_email(userEmail)
        self.lineEdit_3.setText("Check mail to reset password!!!")
    
    def create(self): #not working, thread required
        new_userEmail = self.lineEdit.text()
        new_userPass = self.lineEdit_2.text()
        global signin_status
        if signin_status == True:
            auth.create_user_with_email_and_password(new_userEmail, new_userPass)
            self.lineEdit_3.setText("Account Created!!!")
        else:
            self.lineEdit_3.setText("Admin signin required!!!")
        #Creating users
    
    def verify(self): #not working thread required
        global signin_status
        auth.get_account_info(user['idToken'])
        #Verify Email
        if signin_status == True:
            auth.send_email_verification(user['idToken'])
            self.lineEdit_3.setText("Check mail to verify!!!")
            self.textEdit.append(str(auth.get_account_info(user['idToken'])))
        else:
            self.lineEdit_3.setText("Sign in to verify!!!")
            
    def timer1(self):
        global enter
        enter = 1
        
    def loaddata(self):
        global signin_status
        global enter
        if (signin_status == True and enter ==1):
            qTimer.stop()
            self.dthread.start()
            self.lineEdit_4.setText("NIT Rourkela")
            self.lineEdit_7.setText("ISDR01")
            self.lineEdit_8.setText("Active")
        else:
            print("Status: Not Connected")
    
    def finished(self):
        with SHT1x(18, 23, gpio_mode=GPIO.BCM) as sensor:
            temp = sensor.read_temperature()
            hum = sensor.read_humidity(temp)
            dew1 = sensor.calculate_dew_point(temp, hum)
            now = datetime.datetime.now()
            time1 = now.strftime("%d %B %Y at %H:%M:%S")
       
        self.textEdit.append(str(time1) + " , " + str(temp) + "°C, " + str(hum)+ "%, " + str(dew1) + "°C \n")
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.lineEdit_5.setText(str(time1))
        self.lineEdit_6.setText(str(temp) + "°C")
        self.lineEdit_10.setText(str(hum) + "%")
        self.lineEdit_11.setText(str(dew1) + "°C")
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "Sign In"))
        self.label.setText(_translate("MainWindow", "E-mail :"))
        self.label_3.setText(_translate("MainWindow", "User Login"))
        self.label_2.setText(_translate("MainWindow", "Password :"))
        self.pushButton_3.setText(_translate("MainWindow", "Forgot Password"))
        self.pushButton_4.setText(_translate("MainWindow", "Create User"))
        self.label_4.setText(_translate("MainWindow", "Log Console"))
        self.label_5.setText(_translate("MainWindow", "Location"))
        self.label_6.setText(_translate("MainWindow", "Date / Time"))
        self.label_7.setText(_translate("MainWindow", "Sensor Node ID"))
        self.label_8.setText(_translate("MainWindow", "Node Status"))
        self.label_9.setText(_translate("MainWindow", "Required Sensor Node ID:"))
        self.label_10.setText(_translate("MainWindow", "Oxygen"))
        self.label_11.setText(_translate("MainWindow", "Carbon Dioxide"))
        self.label_12.setText(_translate("MainWindow", "Carbon Monoxide"))
        self.label_13.setText(_translate("MainWindow", "Hydrogen Sulphide"))
        self.label_14.setText(_translate("MainWindow", "Ammonia"))
        self.label_15.setText(_translate("MainWindow", "Ozone"))
        self.label_16.setText(_translate("MainWindow", "Sulphur Dioxide"))
        self.label_17.setText(_translate("MainWindow", "Nitric Oxide"))
        self.label_18.setText(_translate("MainWindow", "Nitrous Oxide"))
        self.label_19.setText(_translate("MainWindow", "Methane"))
        self.label_20.setText(_translate("MainWindow", "Particulate Matter (PM10)"))
        self.label_21.setText(_translate("MainWindow", "Particulate Matter (PM2.5)"))
        self.label_22.setText(_translate("MainWindow", "Dew Point"))
        self.label_23.setText(_translate("MainWindow", "Temperature"))
        self.label_24.setText(_translate("MainWindow", "Relative Humidity"))
        self.pushButton_5.setText(_translate("MainWindow", "Enter"))
        self.pushButton_6.setText(_translate("MainWindow", "Verify E-mail"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuClose.setTitle(_translate("MainWindow", "Close"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()

