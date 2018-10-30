from constant_initialization import *
from DatabaseSystem import *

class CancelReservation(QMainWindow):
    def __init__(self,menu):
        QMainWindow.__init__(self, None)
        
        loader = QUiLoader()
        form = loader.load("UI/uiCancelReservation.ui", None)
        
        self.setWindowTitle("SN Group Manager")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setCentralWidget(form)
        self.setFixedSize(display_width,display_height)
        self.menu = menu

        self.first_name = form.findChild(QLineEdit, "first_name_lineEdit")
        self.last_name = form.findChild(QLineEdit, "last_name_lineEdit")
        
        self.search_by_name_btn = form.findChild(QPushButton, "search_by_name_btn")
        self.search_by_name_btn.clicked.connect(self.search_by_name)

        self.tableWidget = form.findChild(QTableWidget, "tableWidget")
        self.layout = QGridLayout()

        self.cancel_reservation_btn = form.findChild(QPushButton, "cancel_reservation_btn")
        self.cancel_reservation_btn.clicked.connect(self.cancel_reservation)
        
        self.back_btn = form.findChild(QPushButton, "back_btn")
        self.back_btn.clicked.connect(self.back)

        self.db = DatabaseSys()

        self.allreserve = self.db.allreserve()
        
        self.tableWidget.setRowCount(len(self.allreserve))
        self.tableWidget.setColumnCount(9)
        self.layout.addWidget(self.tableWidget, 0,0)

        self.showInfo(self.allreserve)
        
    def search_by_name(self):
        self.tableWidget.clearContents()
        
        f_name = self.first_name.text()
        l_name = self.last_name.text()
        out = self.db.searchByName(f_name, l_name)
        
        if(out is not "None"):
            self.showInfo(out)
        else:
            self.popUP("Name not found!!!")

    def cancel_reservation(self):
        if (len(self.tableWidget.selectedRanges())  >0):
            row = self.tableWidget.currentRow()
            roomNo = self.tableWidget.item(row, 2).text()
            indate = self.tableWidget.item(row, 0).text()
            outdate = self.tableWidget.item(row, 1).text()
            self.db.cancelReserve(roomNo,indate,outdate)
            self.tableWidget.removeRow(self.tableWidget.currentRow())    

    def showInfo(self,allReserve):
        row = 0
        for item in allReserve:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(item[9])) #checkinDate
            self.tableWidget.setItem(row, 1, QTableWidgetItem(item[10])) #checkoutDate
            self.tableWidget.setItem(row, 2, QTableWidgetItem(item[0])) #roomNumber
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(self.db.readRoomType(item[0])))) #roomType
            self.tableWidget.setItem(row, 4, QTableWidgetItem(item[2])) #firstname
            self.tableWidget.setItem(row, 5, QTableWidgetItem(item[3])) #lastname
            self.tableWidget.setItem(row, 6, QTableWidgetItem(item[1])) #residence type
            self.tableWidget.setItem(row, 7, QTableWidgetItem(item[4])) #ID
            self.tableWidget.setItem(row, 8, QTableWidgetItem(item[7])) #Tel No
            row += 1

    def popUP(self, txt):
        dialog = QDialog(self)
        layout = QVBoxLayout()
        label = QLabel(str(txt))
        layout.addWidget(label)
        yes_button1 = QPushButton("Yes")
        yes_button1.clicked.connect(dialog.close)
        layout.addWidget(yes_button1)
        dialog.setLayout(layout)
        dialog.show()
        

    def back(self):
        self.menu.show()
        self.hide()

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bg)
        p.end()
