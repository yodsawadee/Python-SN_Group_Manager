from constant_initialization import *
from Information_ui import *

from DatabaseSystem import *

class UtilitiesRecord(QMainWindow):
    def __init__(self, roomNo=None):
        QMainWindow.__init__(self, None)
        
        loader = QUiLoader()
        form = loader.load("UI/uiUtilitiesRecord.ui", None)
        
        self.setWindowTitle("SN Group Manager")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setCentralWidget(form)
        self.setFixedSize(display_width*0.8,display_height*0.8)

        self.db = DatabaseSys()
        
        self.tableWidget = form.findChild(QTableWidget,"uti_tableWidget")
        self.layout = QGridLayout()

        self.roomNo = roomNo

        self.showInfo(self.roomNo)

    def showInfo(self, rN):
        roomNo = rN
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(5)
        self.layout.addWidget(self.tableWidget, 0,0)
        self.tableWidget.setItem(0, 0, QTableWidgetItem(str(roomNo)))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.db.readResidentType(roomNo))))
        self.tableWidget.setItem(0, 2, QTableWidgetItem(str(self.db.getUtilDate((roomNo)))))
        self.tableWidget.setItem(0, 3, QTableWidgetItem(str(self.db.getUtil(roomNo,"electricity")[0][0])))
        self.tableWidget.setItem(0, 4, QTableWidgetItem(str(self.db.getUtil(roomNo,"water")[0][0])))    
        self.tableWidget.show()

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bg)
        p.end()

