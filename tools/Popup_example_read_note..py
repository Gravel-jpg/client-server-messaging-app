import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow, QDialog

from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton
class Ui_Window_Login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.new_windows = []
        self.counter = 0
    def closeEvent(self, event):
        print('close event triggered')
        for window in QApplication.topLevelWidgets():
            window.close()
        event.accept()
    def recieve_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Recieve_Message(s)
        self.ui.setupUi(self.window)
        self.window.setGeometry(400+self.counter,300+self.counter,400,300)
        self.window.show()
        self.new_windows.append(self.window)
        self.counter += 25
    def setupUi(self, Window_Login):
        Window_Login.setObjectName("Window_Login")
        Window_Login.resize(400, 300)
        Window_Login.setAccessibleName("")
        self.Password_label = QtWidgets.QLabel(Window_Login)
        self.Password_label.setGeometry(QtCore.QRect(94, 116, 50, 16))
        self.Password_label.setObjectName("Password_label")
        self.Username_Label = QtWidgets.QLabel(Window_Login)
        self.Username_Label.setGeometry(QtCore.QRect(94, 90, 51, 16))
        self.Username_Label.setObjectName("Username_Label")
        self.Login_Button = QtWidgets.QPushButton(Window_Login)
        self.Login_Button.setGeometry(QtCore.QRect(151, 142, 75, 23))
        self.Login_Button.setObjectName("Login_Button")
        self.Create_Prompt_Button = QtWidgets.QPushButton(Window_Login)
        self.Create_Prompt_Button.setGeometry(QtCore.QRect(151, 171, 83, 23))
        self.Create_Prompt_Button.setObjectName("Create_Prompt_Button")
        self.Username_Field = QtWidgets.QLineEdit(Window_Login)
        self.Username_Field.setGeometry(QtCore.QRect(151, 90, 133, 20))
        self.Username_Field.setObjectName("Username_Field")
        self.Password_field = QtWidgets.QLineEdit(Window_Login)
        self.Password_field.setGeometry(QtCore.QRect(151, 116, 133, 20))
        self.Password_field.setObjectName("Password_field")


        Window_Login.closeEvent = self.closeEvent

        # Buttons go here
        # self.quit.triggered.connect(self.closeEvent)
        self.Login_Button.clicked.connect(self.recieve_window)
        self.retranslateUi(Window_Login)
        QtCore.QMetaObject.connectSlotsByName(Window_Login)
    def retranslateUi(self, Window_Login):
        _translate = QtCore.QCoreApplication.translate
        Window_Login.setWindowTitle(_translate("Window_Login", "Login"))
        self.Password_label.setText(_translate("Window_Login", "password:"))
        self.Username_Label.setText(_translate("Window_Login", "username:"))
        self.Login_Button.setText(_translate("Window_Login", "Login"))
        self.Create_Prompt_Button.setText(_translate("Window_Login", "Create Account"))
class Ui_Recieve_Message(QWidget):
    def __init__(self,text):
        super().__init__()
        self.text = text
    def closeEvent(self, event):
        print('close event triggered for popup')
        ui.counter -= 25
        event.accept()
    def setupUi(self, Recieve_Message):
        Recieve_Message.setObjectName("Recieve_Message")
        Recieve_Message.resize(400, 300)
        self.layoutWidget = QtWidgets.QWidget(Recieve_Message)
        self.layoutWidget.setGeometry(QtCore.QRect(7, 22, 381, 271))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QPlainTextEdit(self.layoutWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setPlainText(self.text)
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")

        Recieve_Message.closeEvent = self.closeEvent

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.retranslateUi(Recieve_Message)
        QtCore.QMetaObject.connectSlotsByName(Recieve_Message)
    def retranslateUi(self, Recieve_Message):
        _translate = QtCore.QCoreApplication.translate
        Recieve_Message.setWindowTitle(_translate("Recieve_Message", "Recieve Message"))
        self.label.setText(_translate("Recieve_Message", "Message:"))

if __name__ == '__main__':
    s = 'example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text example text '
    import sys
    app = QtWidgets.QApplication(sys.argv)        
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Window_Login()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())