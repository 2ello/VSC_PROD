class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(925, 680)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(120, 0, 780, 600))
        self.tabWidget.setMaximumSize(QtCore.QSize(780, 600))
        self.tabWidget.setObjectName("tabWidget")       
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(0, 40, 780, 500))
        pixmap = QtGui.QPixmap('mathematicsStatGraphPaint.png')
        self.label.setPixmap(pixmap)
        self.tabWidget.addTab(self.tab, "")  
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(0, 40, 780, 500))
        pixmap = QtGui.QPixmap('informaticsStatGraphPaint.png')
        self.label_2.setPixmap(pixmap)
        self.tabWidget.addTab(self.tab_2, "")  
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(0, 40, 780, 500))
        pixmap = QtGui.QPixmap('languageStatGraphPaint.png')
        self.label_3.setPixmap(pixmap)
        self.tabWidget.addTab(self.tab_3, "")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 120, 600))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(10, 150, 100, 22))
        self.pushButton.setObjectName("pushButton")
        self.pushButton2 = QtWidgets.QPushButton(self.frame)
        self.pushButton2.setGeometry(QtCore.QRect(10, 180, 100, 22))
        self.pushButton2.setObjectName("update result")
        #ДАТА
        self.dateEdit = QtWidgets.QDateEdit(self.frame)
        self.dateEdit.setGeometry(QtCore.QRect(10, 20, 100, 22))
        self.dateEdit.setDate(QtCore.QDate(dt.date.today()))
        self.dateEdit.setObjectName("dateEdit")
        #БАЛЛЫ
        self.ComboBox100 = QtWidgets.QComboBox(self.frame)
        self.ComboBox100.setGeometry(QtCore.QRect(10, 80, 100, 22))
        self.ComboBox100.setObjectName("ComboBox100")
        self.ComboBox100.addItems(map(str, list(range(0,101))))
        #ПРЕДМЕТ
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(10, 50, 100, 22))
        self.comboBox.setObjectName("comboBox")
        comboBoxItems = ("mathematics","informatics","language")
        self.comboBox.addItems(comboBoxItems)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.add_functions()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "mathematics"))  # noqa: E501
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "informatics"))  # noqa: E501
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "language"))  # noqa: E501
        self.pushButton.setText(_translate("MainWindow", "save result"))
        self.pushButton2.setText(_translate("MainWindow", "delete result"))


    def add_functions(self):

        self.pushButton.clicked.connect(lambda: self.SaveResult())
        self.pushButton2.clicked.connect(lambda: self.deleteScore())


    def SaveResult(self):
    
        db_file = "ExamsStat\stat.db"
        # предмет
        subject = self.comboBox.currentText()
        # дата
        user_date = str(self.dateEdit.date())
        date = user_date.split("(")[1].replace(")","")
        # баллы
        score = self.ComboBox100.currentText()
        createDb(db_file, subject)
        insert_into(subject, score, date, db_file)
        self.rePaint(subject)


    def deleteScore(self):

        db_file = "ExamsStat\stat.db"
        # предмет
        subject = self.comboBox.currentText()
        # дата
        user_date = str(self.dateEdit.date())
        date = user_date.split("(")[1].replace(")","")
        
        if self.delAscept(date):
            try:
                deleteScoreFromDB(subject, date, db_file)
                self.rePaint(subject)
            except:  # noqa: E722
                print("ошибка, модуль deleteScore не хочет удалять запись")


    def delAscept(self, date):
        result = QtWidgets.QMessageBox.question(MainWindow, "", 
        f"Вы действительно хотите удалить запись от {date} числа?", 
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
        QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False


    def rePaint(self, subject):
        try:
            subjectGraph(subject)
            if subject == "mathematics":
                self.label.setPixmap(QtGui.QPixmap(f"{subject}StatGraphPaint.png"))
            elif subject == "informatics":
                self.label_2.setPixmap(QtGui.QPixmap(f"{subject}StatGraphPaint.png"))
            elif subject == "language":
                self.label_3.setPixmap(QtGui.QPixmap(f"{subject}StatGraphPaint.png"))
            try:
                os.remove(f"{subject}StatGraphPaint.png")
            except:  # noqa: E722
                print(f"{subject}StatGraphPaint.png не найден")
        except:  # noqa: E722
            createDb("ExamsStat\stat.db", subject)
            try: 
                self.rePaint(subject)
            except:  # noqa: E722
                pass


if __name__ == '__main__': 

    from PyQt5 import QtCore, QtGui, QtWidgets
    import datetime as dt
    import sys
    import os

    from db import createDb, insert_into, startedPointsGraph, deleteScoreFromDB
    from graph import subjectGraph

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    startedPointsGraph("ExamsStat\stat.db")

    ui.rePaint("mathematics")
    ui.rePaint("informatics")
    ui.rePaint("language")

    MainWindow.show()
    sys.exit(app.exec_())