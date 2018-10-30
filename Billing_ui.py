from constant_initialization import *
from Bill_ui import *
from DatabaseSystem import *

class Billing(QMainWindow):
    def __init__(self, menu):
        QMainWindow.__init__(self, None)

        loader = QUiLoader()
        form = loader.load("UI/uiBilling.ui", None)

        self.setWindowTitle("SN Group Manager")
        self.setCentralWidget(form)
        self.setFixedSize(display_width, display_height)
        self.menu = menu
        self.db = DatabaseSys()
        self.w = None
        self.e = None
        self.r = None
        self.cb = form.findChild(QComboBox, "roomno")
        self.cb.addItems(["101", "102", "103", "104", "105", "106", "107", "108",
                         "109", "110", "111", "112", "113", "201", "202", "203",
                         "204", "205", "206", "207", "208", "209", "210", "211",
                         "212", "213", "214", "215", "216", "217", "301", "302",
                         "303", "304", "305", "306", "307", "308", "309", "310",
                         "311", "312", "313", "314", "315", "316", "317", "401",
                         "402", "403", "404", "405", "406", "407", "408", "409",
                         "410", "411", "412", "413", "414", "415", "416", "417",
                         "501", "502", "503", "504", "505", "506", "507", "508",
                         "509", "510", "511", "512", "513", "514", "515"])

        

        self.room_layout = QVBoxLayout()
        self.res_layout = QVBoxLayout()
        
        self.water = form.findChild(QSpinBox, "winput")
        self.water.setMaximum(9999)
        
        self.electricity = form.findChild(QSpinBox, "einput")
        self.electricity.setMaximum(9999)

        self.back_btn = form.findChild(QPushButton, "back")
        self.back_btn.clicked.connect(self.back)

        self.cont_btn = form.findChild(QPushButton, "cont")
        self.cont_btn.clicked.connect(self.cont)

        self.showinfo_btn = form.findChild(QPushButton, "showinfo_btn")
        
        
        self.showinfo_btn.clicked.connect(lambda: self.showInfo(self.cb.currentText()))

        self.roomInfo_listWidget = form.findChild(QListWidget, "roomInfo_listWidget")
        self.resInfo_listWidget = form.findChild(QListWidget, "resInfo_listWidget")
        

    def showInfo(self, roomNo):
        self.roomNo = roomNo

        #room_layout
        self.clearInfo(self.room_layout)
        self.room_layout.addWidget(QLabel(str("-------")+str(roomNo)+str("-------\n") + self.db.readRoomInfo(roomNo)))
        self.roomInfo_listWidget.setLayout(self.room_layout)
        self.roomInfo_listWidget.show()
        
        #res_layout
        self.clearInfo(self.res_layout)
        self.res_layout.addWidget(QLabel(str("-------")+str(roomNo)+str("-------\n") + self.db.readResidentInfo(roomNo)))
        self.resInfo_listWidget.setLayout(self.res_layout)
        self.resInfo_listWidget.show()

    def back(self):
        self.menu.show()
        self.hide()

    def cont(self):
        self.w = self.water.text()
        self.e = self.electricity.text()
        self.r = self.cb.currentText()
        if self.db.IsAvailable(self.r) == False:
            self.bill = Bill(self, self.r, self.w, self.e)
            self.bill.show()
            self.hide()
        else:
            self.popUP("This room has no occupant")
    
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

    def clearInfo(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearInfo(item.layout)

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bg)
        p.end()



    

   
    

    
