from constant_initialization import *
from FillResInfo_ui import *
from DatabaseSystem import *
##from Login_ui import *

class Reservation(QMainWindow):
    def __init__(self,menu):
        QMainWindow.__init__(self, None)
        
        loader = QUiLoader()
        form = loader.load("UI/uiReservation.ui", None)
        
        self.setWindowTitle("SN Group Manager")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setCentralWidget(form)
        self.setFixedSize(display_width,display_height)

        self.db = DatabaseSys()
        
        self.layout = QVBoxLayout()

        self.tableWidget = form.findChild(QTableWidget, "tableWidget")

        self.searchedDate = []

        self.studio_count = form.findChild(QLineEdit,"studio_lineEdit")
        self.oneBedroom_count = form.findChild(QLineEdit,"one_bedroom_lineEdit")
        self.twoBedroom_count = form.findChild(QLineEdit,"two_bedroom_lineEdit")
        
        self.back_btn = form.findChild(QPushButton, "back_btn")
        self.back_btn.clicked.connect(self.back)

        self.reserve_btn = form.findChild(QPushButton, "reserve_btn")
        self.reserve_btn.clicked.connect(self.reserve)
        self.reserve_btn.setEnabled(False)

        self.daily = form.findChild(QRadioButton, "daily_radioButton")
        self.daily.clicked.connect(self.dailyChecked)
        
        self.monthly = form.findChild(QRadioButton, "monthly_radioButton")
        self.monthly.clicked.connect(self.monthlyChecked)
        self.monthly.setChecked(True)
        
        self.fromDate = form.findChild(QDateEdit,"fromDate")
        self.fromDate.setDate(QDate.currentDate())
        self.fromDate.setMinimumDate(QDate.currentDate())
        self.fromDate.dateChanged.connect(self.changeFrom)
        
        self.toDate = form.findChild(QDateEdit,"toDate")
        self.toDate.setDate(QDate.currentDate().addDays(1))
        self.toDate.setMinimumDate(QDate.currentDate().addDays(1))
        
        self.notDecide = form.findChild(QCheckBox,"not_decide_checkBox")
        self.notDecide.stateChanged.connect(self.stateChanged)

        self.roomType = form.findChild(QComboBox,"room_type_comboBox")
        self.floor = form.findChild(QComboBox,"floor_comboBox")

        self.search_btn = form.findChild(QPushButton,"search_btn")
        self.search_btn.clicked.connect(self.search)

        
        self.menu = menu

    def stateChanged(self):
        if self.notDecide.isChecked():
            self.toDate.setEnabled(False)
        else:
            self.toDate.setEnabled(True)

    def dailyChecked(self):
        self.notDecide.setEnabled(False)
        self.notDecide.setChecked(False)

    def monthlyChecked(self):
        self.notDecide.setEnabled(True)

    def changeFrom(self, fromDay):
        self.toDate.setMinimumDate(fromDay.addDays(1))

    def search(self):

        
        startDate = self.fromDate.date().toString("yyyy/MM/dd")

        if self.notDecide.isChecked() == False:
            outDate = self.toDate.date().toString("yyyy/MM/dd") 
        else :
            outDate = "9999/12/31"
            
        self.studio_count.setText(str(self.db.countAvailableRoom("studio",startDate,outDate)))
        self.oneBedroom_count.setText(str(self.db.countAvailableRoom("1-bedroom",startDate,outDate)))
        self.twoBedroom_count.setText(str(self.db.countAvailableRoom("2-bedroom",startDate,outDate)))
        
        if self.roomType.currentIndex()==1:
            roomT = "studio"
        elif self.roomType.currentIndex()==2:
            roomT = "1-bedroom"
        elif self.roomType.currentIndex()==3:
            roomT = "2-bedroom"
        else :
            roomT = "All"
            
        if self.floor.currentIndex() == 1:
            f = "1"
        elif self.floor.currentIndex() == 2:
            f = "2"
        elif self.floor.currentIndex() == 3:
            f = "3"
        elif self.floor.currentIndex() == 4:
            f = "4"
        elif self.floor.currentIndex() == 5:
            f = "5"
        else :
            f = ["1","2","3","4","5"]

        if roomT == "All":
            if f!= ["1","2","3","4","5"]:
                Avai = self.db.searchAllAvailableRoom(f,str(startDate),str(outDate))
            else :
                Avai = (self.db.searchAllAvailableRoom(1,str(startDate),str(outDate)))+(self.db.searchAllAvailableRoom(2,str(startDate),str(outDate)))+(self.db.searchAllAvailableRoom(3,str(startDate),str(outDate)))+(self.db.searchAllAvailableRoom(4,str(startDate),str(outDate)))+(self.db.searchAllAvailableRoom(5,str(startDate),str(outDate)))
        else :
            if f!= ["1","2","3","4","5"]:
                Avai = self.db.searchAvailableRoom(f,roomT,str(startDate),str(outDate))
            else :
                Avai = (self.db.searchAvailableRoom(1,roomT,str(startDate),str(outDate)))+(self.db.searchAvailableRoom(2,roomT,str(startDate),str(outDate)))+(self.db.searchAvailableRoom(3,roomT,str(startDate),str(outDate)))+(self.db.searchAvailableRoom(4,roomT,str(startDate),str(outDate)))+(self.db.searchAvailableRoom(5,roomT,str(startDate),str(outDate)))

        
        self.tableWidget.setRowCount(len(Avai))
        self.tableWidget.setColumnCount(3)
        self.layout.addWidget(self.tableWidget, 0,0)
        row=0
        for i in Avai:
            self.tableWidget.setItem(row,0,QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(row,1,QTableWidgetItem(str(i[1])))
            self.tableWidget.setItem(row,2,QTableWidgetItem(str(i[2])))
            row = row+1

        if self.monthly.isChecked()==True:
            restype = "monthly"
        else :
            restype = "daily"
        
        self.searchedItem = [restype,startDate,outDate]
        self.reserve_btn.setEnabled(True)
    
    def reserve(self):
        if (len(self.tableWidget.selectedRanges())  >0):
            row = self.tableWidget.currentRow()
            selectedRoomno = self.tableWidget.item(row, 0).text()
            selectedRoom = [self.tableWidget.item(row, 0).text(),self.tableWidget.item(row, 1).text(),self.tableWidget.item(row, 2).text()]

            self.FillResInfo = FillResInfo(self,selectedRoom,self.searchedItem)
                
            self.FillResInfo.show()
            self.hide()
        
    def back(self):
        self.menu.show()
        self.hide()

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bg)
        p.end()
