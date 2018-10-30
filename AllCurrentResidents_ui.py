from constant_initialization import *
from Information_ui import *
from DatabaseSystem import *

class AllCurrentResidents(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self, None)
        
        loader = QUiLoader()
        form = loader.load("UI/uiAllCurrentResidents.ui", None)
        
        self.setWindowTitle("SN Group Manager")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setCentralWidget(form)
        self.setFixedSize(display_width*0.8,display_height*0.8)

        self.db = DatabaseSys()
        
        self.tableWidget = form.findChild(QTableWidget,"tableWidget")
        self.layout = QGridLayout()

        self.resident = self.db.allresident()


        self.showInfo(self.resident)

    def showInfo(self, Residents):
        self.tableWidget.setRowCount(len(self.resident))
        self.tableWidget.setColumnCount(11)
        self.layout.addWidget(self.tableWidget, 0,0)
        row = 0
        for eachRes in Residents:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(eachRes[0])))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(eachRes[1])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(eachRes[2])))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(eachRes[3])))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(str(eachRes[4])))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(str(eachRes[5])))
            self.tableWidget.setItem(row, 6, QTableWidgetItem(str(eachRes[6])))
            self.tableWidget.setItem(row, 7, QTableWidgetItem(str(eachRes[7])))
            self.tableWidget.setItem(row, 8, QTableWidgetItem(str(eachRes[8])))
            self.tableWidget.setItem(row, 9, QTableWidgetItem(str(eachRes[9])))
            self.tableWidget.setItem(row, 10, QTableWidgetItem(str(eachRes[10])))
            self.tableWidget.show()
            row = row+1

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bg)
        p.end()

