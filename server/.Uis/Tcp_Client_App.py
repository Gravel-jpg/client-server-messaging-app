from PyQt5 import QtCore, QtWidgets
class Ui_Window_Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def Send_Message_Function(self):
        # Client sends string 'key_request;{self.Recipient_Username_Field.text()}'
        # Client sends string 'send_cipher;{self.Message_Field.text()}'
        send_string(f'key_request;{self.Recipient_Username_Field.text()}',s,n,e,True)
        Recipient_Keys = process_string.split(';')[1]
        # [n,e]
        Recipient_Keys = [Recipient_Keys.split(',')[0],Recipient_Keys.split(',')[1]]
        # To locally encrypt the message to the recipients keys
        with open(filename,'r') as f:
            data = json.load(f)
            strings = split_string(self.Message_Field.text())
            for i in strings:
                Msg = ''
                for j in i:
                    Msg += str(data['str_to_int'][j])
                outgoing_ciphertext = str(crypt(int(Msg),int(e),int(n)))
                send_string(outgoing_ciphertext,s,n,e,True)
        
    def Upload_Keys(self):
        new_n, new_d, new_e = generate_keys()
        with open(filename,'r') as f:
            data = json.load(f)
        old_n, old_d = data['keys']['n'],data['keys']['d']
        send_string(f'update_keys;{new_n},{new_e}',s,n,e,True)
        update_json_keys(new_n,new_d)
        try:
            x = process_string(s)
            print('Sucesfully updated keys')
        except:
            update_json_keys(old_n,old_d)
            x = process_string(s)
    def setupUi(self, Window_Main):
        Window_Main.setObjectName("Window_Main")
        self.New_Keys_Button = QtWidgets.QPushButton(Window_Main)
        self.New_Keys_Button.setGeometry(QtCore.QRect(-1, -1, 75, 23))
        self.New_Keys_Button.setObjectName("New_Keys_Button")
        self.widget = QtWidgets.QWidget(Window_Main)
        self.widget.setGeometry(QtCore.QRect(32, 41, 310, 249))
        self.widget.setObjectName("widget")
        self.Window_Main_Layout = QtWidgets.QGridLayout(self.widget)
        self.Window_Main_Layout.setContentsMargins(0, 0, 0, 0)
        self.Window_Main_Layout.setObjectName("Window_Main_Layout")
        self.Recipient_Username_Label = QtWidgets.QLabel(self.widget)
        self.Recipient_Username_Label.setObjectName("Recipient_Username_Label")
        self.Window_Main_Layout.addWidget(self.Recipient_Username_Label, 0, 1, 1, 1)
        self.Recipient_Username_Field = QtWidgets.QLineEdit(self.widget)
        self.Recipient_Username_Field.setObjectName("Recipient_Username_Field")
        self.Window_Main_Layout.addWidget(self.Recipient_Username_Field, 0, 2, 1, 1)
        self.Message_Label = QtWidgets.QLabel(self.widget)
        self.Message_Label.setObjectName("Message_Label")
        self.Window_Main_Layout.addWidget(self.Message_Label, 1, 0, 1, 1)
        self.Message_Field = QtWidgets.QPlainTextEdit(self.widget)
        self.Message_Field.setObjectName("Message_Field")
        self.Window_Main_Layout.addWidget(self.Message_Field, 1, 1, 1, 2)
        self.Send_Button = QtWidgets.QPushButton(self.widget)
        self.Send_Button.setObjectName("Send_Button")
        self.Window_Main_Layout.addWidget(self.Send_Button, 2, 2, 1, 1)
        # Buttons go here
        self.New_Keys_Button.clicked.connect(self.Upload_Keys)
        self.Send_Button.clicked.connect(self.Send_Message_Function)
        self.retranslateUi(Window_Main)
        QtCore.QMetaObject.connectSlotsByName(Window_Main)
    def retranslateUi(self, Window_Main):
        _translate = QtCore.QCoreApplication.translate
        Window_Main.setWindowTitle(_translate("Window_Main", "Send Message"))
        self.New_Keys_Button.setText(_translate("Window_Main", "refresh keys"))
        self.Recipient_Username_Label.setText(_translate("Window_Main", "user:"))
        self.Message_Label.setText(_translate("Window_Main", "message:"))
        self.Send_Button.setText(_translate("Window_Main", "Send"))
class Ui_Window_Login(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def Main_Window_Function(self):
        widget.setCurrentWidget(page3)
    def Create_Prompt_Function(self):
        widget.setCurrentWidget(page2)
    def Login_Function(self):
        send_string(f'login_attempt;{self.Username_Field.text()},{self.Password_Field.text()}',s,n,e,True)
        if eval(process_string(s).split(';')[1]):
            print('Login True')
            self.Main_Window_Function()
        else:
            print('Error Login False')
    def setupUi(self, Window_Login):
        Window_Login.setObjectName("Window_Login")
        Window_Login.setAccessibleName("")
        self.Password_Label = QtWidgets.QLabel(Window_Login)
        self.Password_Label.setGeometry(QtCore.QRect(94, 116, 50, 16))
        self.Password_Label.setObjectName("Password_Label")
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
        self.Password_Field = QtWidgets.QLineEdit(Window_Login)
        self.Password_Field.setGeometry(QtCore.QRect(151, 116, 133, 20))
        self.Password_Field.setObjectName("Password_Field")
        self.retranslateUi(Window_Login)
        QtCore.QMetaObject.connectSlotsByName(Window_Login)
        # Buttons go here
        self.Login_Button.clicked.connect(self.Login_Function)
        self.Create_Prompt_Button.clicked.connect(self.Create_Prompt_Function)
    def retranslateUi(self, Window_Login):
        _translate = QtCore.QCoreApplication.translate
        Window_Login.setWindowTitle(_translate("Window_Login", "Login"))
        self.Password_Label.setText(_translate("Window_Login", "password:"))
        self.Username_Label.setText(_translate("Window_Login", "username:"))
        self.Login_Button.setText(_translate("Window_Login", "Login"))
        self.Create_Prompt_Button.setText(_translate("Window_Login", "Create Account"))
class Ui_Window_Create(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    def Back_Function(self):
        widget.setCurrentWidget(page1)
    def Main_Window_Function(self):
        widget.setCurrentWidget(page3)
    def Upload_Account(self):
        new_n, new_d, new_e = generate_keys()
        send_string(f'create_acc;{self.New_Username_Field},{self.New_Password_Field},{new_n},{new_e}',s,n,e,True)
        if eval(process_string(s)).split(';')[1]:
            update_json_keys(new_n,new_d)
            self.Main_Window_Function()
        else:
            print('Login not verified by server')
    def setupUi(self, Window_Create):
        Window_Create.setObjectName("Window_Create")
        self.Back_Button = QtWidgets.QPushButton(Window_Create)
        self.Back_Button.setGeometry(QtCore.QRect(-1, -1, 75, 23))
        self.Back_Button.setObjectName("Back_Button")
        self.New_Username_Label = QtWidgets.QLabel(Window_Create)
        self.New_Username_Label.setGeometry(QtCore.QRect(94, 90, 51, 16))
        self.New_Username_Label.setObjectName("New_Username_Label")
        self.New_Password_Field = QtWidgets.QLineEdit(Window_Create)
        self.New_Password_Field.setGeometry(QtCore.QRect(150, 116, 133, 20))
        self.New_Password_Field.setObjectName("New_Password_Field")
        self.New_Password_Label = QtWidgets.QLabel(Window_Create)
        self.New_Password_Label.setGeometry(QtCore.QRect(93, 116, 50, 16))
        self.New_Password_Label.setObjectName("New_Password_Label")
        self.New_Username_Field = QtWidgets.QLineEdit(Window_Create)
        self.New_Username_Field.setGeometry(QtCore.QRect(151, 90, 133, 20))
        self.New_Username_Field.setObjectName("New_Username_Field")
        self.Create_Accoun_Button = QtWidgets.QPushButton(Window_Create)
        self.Create_Accoun_Button.setGeometry(QtCore.QRect(151, 171, 83, 23))
        self.Create_Accoun_Button.setObjectName("Create_Accoun_Button")
        # Buttons go here
        self.Back_Button.clicked.connect(self.Back_Function)
        self.retranslateUi(Window_Create)
        QtCore.QMetaObject.connectSlotsByName(Window_Create)
    def retranslateUi(self, Window_Create):
        _translate = QtCore.QCoreApplication.translate
        Window_Create.setWindowTitle(_translate("Window_Create", "Create Account"))
        self.New_Username_Label.setText(_translate("Window_Create", "username:"))
        self.New_Password_Label.setText(_translate("Window_Create", "password:"))
        self.Create_Accoun_Button.setText(_translate("Window_Create", "Create Account"))
        self.Back_Button.setText(_translate("Window_Create", "Back"))
if __name__ == '__main__':
    import sys, socket
    from client_functions import *
    host = '192.168.0.19'
    port = 9100
    s = socket.socket()
    try:
        s.connect((host,port))
        print('connected')
        n = process_string(s).split(';')[1]
        e,n = n.split(',')[1],n.split(',')[0]
        print(f'n:{n}\ne:{e}')
    except Exception as ex:
        print(ex)
        print('ERROR couldnt connect')
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    #Making 3 widgets as objects,
    page1 = Ui_Window_Login()
    page2 = Ui_Window_Create()
    page3 = Ui_Window_Main()
    #Stack all 3 widgets into the window
    widget.addWidget(page1)
    widget.addWidget(page2)
    widget.addWidget(page3)
    #Set window size
    widget.setFixedSize(400,300)
    #Setting up first window shown
    widget.setCurrentWidget(page3)
    widget.show()
    sys.exit(app.exec_())