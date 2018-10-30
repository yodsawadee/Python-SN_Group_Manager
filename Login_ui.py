from Menu_ui import *
from constant_initialization import *
from DatabaseSystem import *

class Login(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        
        loader = QUiLoader()
        form = loader.load("UI/uiLogin.ui", None)

        self.db = DatabaseSys()
        
        self.setWindowTitle("SN Group Manager")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setCentralWidget(form)
        self.setFixedSize(display_width,display_height)

        self.login_btn = form.findChild(QPushButton, "login_btn")
        self.login_btn.clicked.connect(self.menu)

        self.username = form.findChild(QLineEdit, "username_lineEdit")
        self.password = form.findChild(QLineEdit, "password_lineEdit")

        self.password.setEchoMode(QLineEdit.Password)    

    def menu(self):
        rec_password = self.db.getPassword("receptionist")
        manager_password = "manager"

        if self.username.text() == "receptionist" and self.password.text() == rec_password:
            self.menu = Menu("receptionist")
            self.menu.show()
            self.hide()
        elif self.username.text() == "manager" or self.password.text() == manager_password:
            self.menu = Menu("manager")
            self.menu.show()
            self.hide()
        else:
            self.popUP("invalid password or username")

    def popUP(self, txt):
        dialog = QDialog(self)
        layout = QVBoxLayout()
        label = QLabel(str(txt))
        layout.addWidget(label)
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        dialog.setLayout(layout)
        dialog.show()

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bg)
        p.drawImage(QRect((display_width-title_font_width)/2, 125, 543, 84), title_font_img)
        p.end()


def main():
    app = QApplication(sys.argv)
    w = Login()
    
    w.show()
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
