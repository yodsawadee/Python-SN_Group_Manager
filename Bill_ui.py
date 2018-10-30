from constant_initialization import *
from Billing_ui import *
from DatabaseSystem import *
import datetime

class Bill(QMainWindow):
    def __init__(self, billing, room, water, electric):
        QMainWindow.__init__(self, None)

        loader = QUiLoader()
        form = loader.load("UI/uiBill.ui", None)
        
        self.billing = billing
        
        self.setWindowTitle("SN Group Manager")
        self.setCentralWidget(form)
        self.setFixedSize(display_width,display_height)
        self.setStyleSheet('white')
        
        self.db = DatabaseSys()
        self.room = room
        self.w = int(water)
        self.e = int(electric)
        self.t = 0
        self.checkout = str(datetime.date.today()).replace('-','/')
    
        self.info = form.findChild(QLabel, "info")

        self.water = form.findChild(QLabel, "water")
        
        self.electricity = form.findChild(QLabel, "elect")

        self.r = form.findChild(QLabel, "room")
        
        self.total = form.findChild(QLabel, "total")
        
        self.back_btn = form.findChild(QPushButton, "back")
        self.back_btn.clicked.connect(self.back)

        self.save_btn = form.findChild(QPushButton, "save")
        self.save_btn.clicked.connect(self.save)

        self.setInfo()
        self.getElectricityPrice()
        self.getWaterPrice()
        self.getRoomPrice()
        self.setTotal()
        self.updateUnit()

    def setInfo(self):
        self.result = self.db.readResidentInfo(self.room) + "\n" + self.db.readRoomInfo(self.room)
        self.info.setText(self.result)

    def getWaterPrice(self):
        w = self.db.getUtil(self.room, "water")
        if type(w) == list:
            w = w[0][0]
        w = int(w)
        
        if self.w < w: #meter resets after it exceeds 9999
            total = (9999 - w) + self.w
        elif self.w >= w:
            total = self.w - w

        if self.db.readResidentType(self.room) == 'monthly':
            price = total * float(self.db.getDefault_util("water"))
            self.t = self.t + price
            result = "Water cost: " + str(price)
            self.water.setText(result)
        elif self.db.readResidentType(self.room) == 'daily':
            result = 'Water used: ' + str(total)
            self.water.setText(result)


    def getElectricityPrice(self):
        e = self.db.getUtil(self.room, "electricity")
        if type(e) == list:
            e = e[0][0]
        e = int(e)
        
        if self.e < e: #meter resets after it exceeds 9999
            total = (9999 - e) + self.e
        elif self.e >= e:
            total = self.e - e
            
        if self.db.readResidentType(self.room) == 'monthly':    
            price = total * float(self.db.getDefault_util("electricity"))
            self.t = self.t + price
            result = "Electricity cost: " + str(price)
            self.electricity.setText(result)
        elif self.db.readResidentType(self.room) == 'daily':
            result = 'Electricity used: ' + str(total)
            self.electricity.setText(result)

    def getRoomPrice(self):
        if self.db.readResidentType(self.room) == "daily": 
            price = self.db.getRoomPrice(self.db.readRoomType(self.room))
            price = int(price[0][0])
            inDate = self.db.getCheckinoutDate(self.room)[0][0]
            outDate = self.checkout
            inyear, inmonth, inday = inDate.split('/')
            outyear, outmonth, outday = outDate.split('/')
            checkin = datetime.date(int(inyear), int(inmonth), int(inday))
            checkout = datetime.date(int(outyear), int(outmonth), int(outday))
            duration = checkout - checkin
            duration = duration.days
            if duration == 0:
                duration = 1
            price = duration*price
            self.t = self.t + (price)
            result = "Room cost: " + str(price)
            self.r.setText(result)
            
        elif self.db.readResidentType(self.room) == "monthly":
            price = self.db.getRoomPrice(self.db.readRoomType(self.room))
            price = int(price[0][1])
            self.t = self.t + price
            result = "Room cost: " + str(price)
            self.r.setText(result)

    def updateUnit(self):
        if self.db.getUtil(self.room, "water") == '0' or self.db.getUtil(self.room, "electricity") == '0':
            self.db.insertUtil(self.room, self.checkout, str(self.w), str(self.e))

        else:
            self.db.editUtil(self.room, self.checkout, str(self.w), str(self.e))
         
    def setTotal(self):
        result = "Total: " + str(self.t)
        self.total.setText(result)
        
    def back(self):
        self.billing.show()
        self.hide()

    def save(self):
        filename = 'Bills/billshot.jpg'
        p = QPixmap.grabWindow(self.winId(), 0, 0, 800, 400)
        p.save(filename, 'jpg')
        
        image = QImage("Bills/billshot.jpg")
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        time = datetime.datetime.now().strftime('%H:%M:%S')
        time = time.replace(':', '-')
        f = "Bills/bill_" + str(self.room) + "_" + str(datetime.date.today()) + "_" + time + ".pdf"
        printer.setOutputFileName(f)

        painter = QPainter()
        painter.begin(printer)
        painter.drawImage(QRect(0,0,display_width,display_height), image)
        painter.end()

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bill_bg)

        p.end()

        
        
        
