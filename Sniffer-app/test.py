# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1067, 869)
        self.Pause = QtWidgets.QPushButton(Form)
        self.Pause.setGeometry(QtCore.QRect(10, 10, 75, 51))
        self.Pause.setMaximumSize(QtCore.QSize(75, 16777215))
        self.Pause.setStyleSheet("")
        self.Pause.setObjectName("Pause")
        self.Download = QtWidgets.QPushButton(Form)
        self.Download.setGeometry(QtCore.QRect(910, 10, 75, 51))
        self.Download.setObjectName("Download")
        self.Reset = QtWidgets.QPushButton(Form)
        self.Reset.setGeometry(QtCore.QRect(820, 10, 75, 51))
        self.Reset.setObjectName("Reset")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(90, 230, 901, 381))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 899, 379))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.Highest_rssi = QtWidgets.QTableWidget(Form)
        self.Highest_rssi.setGeometry(QtCore.QRect(90, 110, 901, 111))
        self.Highest_rssi.setObjectName("Highest_rssi")
        self.Highest_rssi.setColumnCount(0)
        self.Highest_rssi.setRowCount(0)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(360, 50, 51, 21))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label1 = QtWidgets.QLabel(Form)
        self.label1.setGeometry(QtCore.QRect(440, 30, 121, 21))
        self.label1.setObjectName("label1")
        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(470, 60, 91, 21))
        self.label2.setObjectName("label2")
        self.currently_seen = QtWidgets.QLCDNumber(Form)
        self.currently_seen.setGeometry(QtCore.QRect(570, 30, 41, 23))
        self.currently_seen.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"font: 8pt \"Arial\";")
        self.currently_seen.setSmallDecimalPoint(False)
        self.currently_seen.setObjectName("currently_seen")
        self.total_seen = QtWidgets.QLCDNumber(Form)
        self.total_seen.setGeometry(QtCore.QRect(570, 60, 41, 23))
        self.total_seen.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.total_seen.setObjectName("total_seen")
        self.alarms = QtWidgets.QTextEdit(Form)
        self.alarms.setGeometry(QtCore.QRect(90, 650, 441, 201))
        self.alarms.setObjectName("alarms")
        self.messages = QtWidgets.QTextEdit(Form)
        self.messages.setGeometry(QtCore.QRect(550, 650, 441, 201))
        self.messages.setObjectName("messages")
        self.group_tokens = QtWidgets.QTableWidget(Form)
        self.group_tokens.setGeometry(QtCore.QRect(90, 230, 901, 381))
        self.group_tokens.setStyleSheet("")
        self.group_tokens.setObjectName("group_tokens")
        self.group_tokens.setColumnCount(0)
        self.group_tokens.setRowCount(0)
        self.lalarms = QtWidgets.QLabel(Form)
        self.lalarms.setGeometry(QtCore.QRect(90, 620, 91, 21))
        self.lalarms.setObjectName("lalarms")
        self.lmessages = QtWidgets.QLabel(Form)
        self.lmessages.setGeometry(QtCore.QRect(550, 620, 91, 21))
        self.lmessages.setObjectName("lmessages")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Pause.setToolTip(_translate("Form", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Pause</span></p></body></html>"))
        self.Pause.setWhatsThis(_translate("Form", "<html><head/><body><p><br/></p></body></html>"))
        self.Pause.setText(_translate("Form", "Pause"))
        self.Download.setText(_translate("Form", "Download"))
        self.Reset.setText(_translate("Form", "Reset"))
        self.label1.setText(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Currently Seen:</span></p></body></html>"))
        self.label2.setText(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Total Seen:</span></p></body></html>"))
        self.lalarms.setText(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Alarms</span></p></body></html>"))
        self.lmessages.setText(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">Messages</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())