from constant_initialization import *
from DatabaseSystem import *
from Reservation_ui import *

class FillResInfo(QMainWindow):
    def __init__(self,previous,selectedRoom,searchedItem):
        QMainWindow.__init__(self, None)
        
        loader = QUiLoader()
        form = loader.load("UI/uiFillResInfo.ui", None)
            
        self.setWindowTitle("SN Group Manager")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setCentralWidget(form)
        self.setFixedSize(display_width,display_height)

        self.db = DatabaseSys()
        self.selectedRoom = selectedRoom
        self.searchedItem = searchedItem

        self.roomNo_l = form.findChild(QLineEdit, "roomNo_lineEdit")
        self.floor_l = form.findChild(QLineEdit, "floor_lineEdit")
        self.roomType_l = form.findChild(QLineEdit, "roomType_lineEdit")
        self.checkin_date_l = form.findChild(QLineEdit, "checkinDate_lineEdit")
        self.checkout_date_l = form.findChild(QLineEdit, "checkoutDate_lineEdit")

        self.roomNo_l.setText(self.selectedRoom[0]) #roomNo
        self.floor_l.setText(self.selectedRoom[1]) #floor
        self.roomType_l.setText(self.selectedRoom[2]) #roomType
        self.checkin_date_l.setText(str(self.searchedItem[1]))
        if self.searchedItem[2]!="9999/99/99":
            self.checkout_date_l.setText(str(self.searchedItem[2]))
        else:
            self.checkout_date_l.setText("No checkout date")

        #filled info
        self.roomNo = self.selectedRoom[0]
        self.floor = self.selectedRoom[1]
        self.roomType = self.selectedRoom[2]
        self.checkin_date = str(self.searchedItem[1])
        self.checkout_date= str(self.searchedItem[2])
        self.resType = self.searchedItem[0]     

        self.first_name = form.findChild(QLineEdit, "first_name_lineEdit")
        self.last_name = form.findChild(QLineEdit, "last_name_lineEdit")
        self.national_id = form.findChild(QLineEdit, "national_id_lineEdit")
        self.line = form.findChild(QLineEdit, "line_lineEdit")
        self.email = form.findChild(QLineEdit, "email_lineEdit")
        self.telephon_no = form.findChild(QLineEdit, "telephon_no_lineEdit")
        self.address1 = form.findChild(QLineEdit, "address1_lineEdit")
        self.address2 = form.findChild(QLineEdit, "address2_lineEdit")
        self.address3 = form.findChild(QLineEdit, "address3_lineEdit")

        #button
        self.previous = previous
        self.back_btn = form.findChild(QPushButton, "back_btn")
        self.back_btn.clicked.connect(self.back)

        self.reserve_btn = form.findChild(QPushButton, "reserve_btn")
        self.reserve_btn.clicked.connect(self.reserve)

    def reserve(self):
        #filled info
        firstname = self.first_name.text()
        lastname = self.last_name.text()
        tel = self.telephon_no.text()
        natID = self.national_id.text()
        line = self.line.text()
        email = self.email.text()
        addr = self.address1.text()+","+self.address2.text()+","+self.address3.text()

        whitespaceFisrtname = firstname.count(" ")
        whitespaceLastname = lastname.count(" ")
        whitespaceTel = tel.count(" ")
        
        #check if not empty
        if (len(firstname)-whitespaceFisrtname)>0 and (len(lastname)-whitespaceLastname)>0 and (len(tel)-whitespaceTel) > 0:
            self.db.reserve(self.roomNo,self.resType,firstname,lastname,natID,line,email,tel,addr,self.checkin_date,self.checkout_date)
            self.reserve_btn.setEnabled(False)
            self.previous.reserve_btn.setEnabled(False)
            self.popup("residence reserved!")
        else :
            self.popup("please fill all * values")
        
    def back(self):
        self.clearText()
        self.previous.show()
        self.hide()

    def clearText(self):
        self.first_name.clear()
        self.last_name.clear()
        self.national_id.clear()
        self.line.clear()
        self.email.clear()
        self.telephon_no.clear()
        self.address1.clear()
        self.address2.clear()
        self.address3.clear()

    def popup(self,text):
        dialog = QDialog(self)
        layout = QVBoxLayout()
        label = QLabel(text)
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
        p.end()
