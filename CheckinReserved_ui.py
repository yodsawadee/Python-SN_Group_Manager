from constant_initialization import *
from DatabaseSystem import *
import datetime

class CheckinReserved(QMainWindow):
    def __init__(self,menu):
        QMainWindow.__init__(self, None)
        
        loader = QUiLoader()
        form = loader.load("UI/uiCheckinReserved.ui", None)

        self.db = DatabaseSys()
        self.menu = menu

        self.setWindowTitle("SN Group Manager")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setCentralWidget(form)
        self.setFixedSize(display_width,display_height)

        self.roomtype_l = form.findChild(QLineEdit,"roomType_lineEdit")
        self.checkin_date_de = form.findChild(QDateEdit, "checkin_dateEdit")
        self.checkout_date_de = form.findChild(QDateEdit, "checkout_dateEdit")
        self.checkin_date_de.setDate(QDate.currentDate())
        self.checkout_date_de.setDate(QDate.currentDate().addDays(1))
        
        self.search_btn = form.findChild(QPushButton, "search_btn")
        self.search_btn.clicked.connect(self.search)

        self.search_name_lineEdit = form.findChild(QLineEdit, "search_by_name_lineEdit")
        self.search_lastname_lineEdit = form.findChild(QLineEdit, "search_by_lastname_lineEdit")

        self.check_in_btn = form.findChild(QPushButton, "check_in_btn")
        self.check_in_btn.clicked.connect(self.check_in)
        self.check_in_btn.setEnabled(False)

        self.first_name = form.findChild(QLineEdit, "first_name_lineEdit")
        self.last_name = form.findChild(QLineEdit, "last_name_lineEdit")
        self.national_id = form.findChild(QLineEdit, "national_id_lineEdit")
        self.line = form.findChild(QLineEdit, "line_lineEdit")
        self.email = form.findChild(QLineEdit, "email_lineEdit")
        self.telephon_no = form.findChild(QLineEdit, "telephon_no_lineEdit")
        self.address1 = form.findChild(QLineEdit, "address1_lineEdit")
        self.address2 = form.findChild(QLineEdit, "address2_lineEdit")
        self.address3 = form.findChild(QLineEdit, "address3_lineEdit")

        currentDate = str(datetime.date.today())
        currentDate = currentDate.replace("-","/")

        self.tableWidget = form.findChild(QTableWidget, "tableWidget")

        self.todayReservedRoom = self.db.checkReserveByCheckInDay(currentDate)
        self.showInfo(self.todayReservedRoom)

        self.back_btn = form.findChild(QPushButton, "back_btn")
        self.back_btn.clicked.connect(self.back)

        #tablewidget
        self.tableWidget.cellClicked.connect(self.itemisSelected)

    def showInfo(self,item):
        self.tableWidget.clearContents()
        
        self.layout = QVBoxLayout()
        
        self.tableWidget.setRowCount(len(item))
        self.tableWidget.setColumnCount(3)
        self.layout.addWidget(self.tableWidget, 0,0)
        row=0
        for i in item:
            self.tableWidget.setItem(row,0,QTableWidgetItem(str(i[2])))
            self.tableWidget.setItem(row,1,QTableWidgetItem(str(i[1])))
            self.tableWidget.setItem(row,2,QTableWidgetItem(str(i[0])))
            row = row+1

    def itemisSelected(self):
        self.check_in_btn.setEnabled(True)
        row = self.tableWidget.currentRow()
        selectedRoom = [self.tableWidget.item(row, 0).text(),self.tableWidget.item(row, 1).text(),self.tableWidget.item(row, 2).text()]
        self.roomNo = str(self.tableWidget.item(row, 2).text())
        res = self.db.checkReservedResidentInfoByRoomNo(self.roomNo)
        self.resType = self.tableWidget.item(row, 1).text()
        name = res[2]
        lastname = res[3]
        natID = res[4]
        line = res[5]
        email = res[6]
        tel = res[7]
        addr = res[8]
        checkinD = res[9]
        checkoutD = res[10]

        checkinD = checkinD.split('/')
        checkinD = datetime.datetime(int(checkinD[0]),int(checkinD[1]),int(checkinD[2]))
        checkoutD = checkoutD.split('/')
        checkoutD = datetime.datetime(int(checkoutD[0]),int(checkoutD[1]),int(checkoutD[2]))
        
        addr = addr.split(",")
        self.first_name.setText(name)
        self.last_name.setText(lastname)
        self.national_id.setText(natID)
        self.line.setText(line)
        self.email.setText(email)
        self.telephon_no.setText(tel)
        self.address1.setText(addr[0])
        self.address2.setText(addr[1])
        self.address3.setText(addr[2])  
        
        self.roomtype_l.setText(self.db.readRoomType(self.roomNo)) 
        self.checkin_date_de.setDate(checkinD)
        self.checkout_date_de.setDate(checkoutD) 
        
        
    def search(self):
        self.tableWidget.clearContents()
        allReserve = self.db.searchByName(self.search_name_lineEdit.text(),self.search_lastname_lineEdit.text())

        if(allReserve is not None):
            self.showInfo(allReserve)
        else:
            self.popUP("Name not found!!!")
            
    def check_in(self):
        #filled info

        firstname = self.first_name.text()
        lastname = self.last_name.text()
        tel = self.telephon_no.text()
        natID = self.national_id.text()
        line = self.line.text()
        email = self.email.text()
        addr = self.address1.text()+","+self.address2.text()+","+self.address3.text()
        chkin = str(self.checkin_date_de.date())
        chkout = str(self.checkout_date_de.date())
        print(chkin)

        whitespaceFisrtname = firstname.count(" ")
        whitespaceLastname = lastname.count(" ")
        whitespaceTel = tel.count(" ")
        whitespacNatID = natID.count(" ")
        whitespaceAddr = addr.count(" ")
        
        #check if not empty
        if (len(firstname)-whitespaceFisrtname)>0 and (len(lastname)-whitespaceLastname)>0 and (len(tel)-whitespaceTel) > 0 and (len(natID)-whitespaceFisrtname)>0 and (len(addr)-whitespaceAddr)>2:
            self.db.checkInReserve(self.roomNo,self.resType,firstname,lastname,natID,line,email,tel,addr,chkin,chkout)
            self.popup("residence checkd in!")
            self.tableWidget.removeRow(self.tableWidget.currentRow())
            self.check_in_btn.setEnabled(False)
        else :
            self.popup("please fill all * values")

        

    def back(self):
        self.clearText()
        self.menu.show()
        self.hide()

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

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bg)
        p.end()

