from Login_ui import *
from Information_ui import *
from Reservation_ui import *
from CancelReservation_ui import *
from CheckinWalkin_ui import *
from CheckinReserved_ui import *
from Checkout_ui import *
from Setting_ui import *
from Billing_ui import *

class Menu(QMainWindow):
    def __init__(self,mode):
        QMainWindow.__init__(self, None)
        
        loader = QUiLoader()
        form = loader.load("UI/uiMenu.ui", None)
        
        self.setWindowTitle("SN Group Manager")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setCentralWidget(form)
        self.setFixedSize(display_width,display_height)

        self.information_btn = form.findChild(QPushButton, "information_btn")
        self.information_btn.clicked.connect(self.information_ui)

        self.reservation_btn = form.findChild(QPushButton, "reservation_btn")
        self.reservation_btn.clicked.connect(self.reservation_ui)

        self.reservation_btn = form.findChild(QPushButton, "cancel_reservation_btn")
        self.reservation_btn.clicked.connect(self.cancel_reservation_ui)

        self.checkin_walk_in_btn = form.findChild(QPushButton, "check_in_walk_in_btn")
        self.checkin_walk_in_btn.clicked.connect(self.checkin_walkin_ui)

        self.checkin_reserved_btn = form.findChild(QPushButton, "check_in_reserved_btn")
        self.checkin_reserved_btn.clicked.connect(self.checkin_reserved_ui)

        self.check_out_btn = form.findChild(QPushButton, "check_out_btn")
        self.check_out_btn.clicked.connect(self.check_out_ui)

        self.billing_btn = form.findChild(QPushButton, "billing_btn")
        self.billing_btn.clicked.connect(self.billing_ui)

        self.setting_btn = form.findChild(QPushButton, "setting_btn")
        self.setting_btn.clicked.connect(self.setting_ui)
        
        self.status = form.findChild(QLabel, "Status")
        self.mode = mode
        if self.mode == "manager":
            self.status.setText("Manager")
        else :
            self.status.setText("Receptionist")
            self.billing_btn.setEnabled(False)
            self.setting_btn.setEnabled(False)

    def information_ui(self):
        self.information = Information(self)  
        self.information.show()
        self.hide()
            
    def reservation_ui(self):
        self.reservation = Reservation(self)
        self.reservation.show()
        self.hide()

    def cancel_reservation_ui(self):
        self.cancel_reservation = CancelReservation(self)
        self.cancel_reservation.show()
        self.hide()

    def checkin_walkin_ui(self):
        self.checkin_walkin = CheckinWalkin(self)
        self.checkin_walkin.show()
        self.hide()

    def checkin_reserved_ui(self):
        self.checkin_reserved = CheckinReserved(self)
        self.checkin_reserved.show()
        self.hide()

    def check_out_ui(self):
        self.check_out = Checkout(self)
        self.check_out.show()
        self.hide()

    def billing_ui (self):
        self.billing = Billing(self)
        self.billing.show()
        self.hide()

    def setting_ui(self):
        self.setting = Setting(self)
        self.setting.show()
        self.hide()

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bg)
        p.drawImage(QRect((display_width-title_font_width)/2, 45, 543, 84), title_font_img)
        p.drawImage(QRect(40, 150, 399, 365), building_img)
        p.end()
        
