from constant_initialization import *
from DatabaseSystem import *

class Setting(QMainWindow):
    def __init__(self,menu):
        QMainWindow.__init__(self, None)
        
        loader = QUiLoader()
        form = loader.load("UI/uiSetting.ui", None)
        
        self.setWindowTitle("SN Group Manager")
        self.setWindowIcon(QIcon('images/icon.png'))
        self.setCentralWidget(form)
        self.setFixedSize(display_width,display_height)

        self.db = DatabaseSys()
        
        self.menu = menu
        
        self.back_btn = form.findChild(QPushButton,"back_btn")
        self.back_btn.clicked.connect(self.back)
        
        #Utilities Section
        self.electric = form.findChild(QDoubleSpinBox,"electric_doubleSpinBox")
        self.water = form.findChild(QDoubleSpinBox,"water_doubleSpinBox")
        
        self.electric.setMaximum(999.99)
        self.water.setMaximum(999.99)

        self.water.setValue(float(self.db.getDefault_util("water")))
        self.electric.setValue(float(self.db.getDefault_util("electricity")))
        
        self.utility_update_btn = form.findChild(QPushButton,"utility_update_btn")
        self.utility_update_btn.clicked.connect(self.utility_update)

        self.utility_default_btn = form.findChild(QPushButton,"utility_default_btn")
        self.utility_default_btn.clicked.connect(self.utility_default)


        #Renting Fees Section
        self.studioD = form.findChild(QSpinBox,"studio_daily_spinBox")
        self.studioM = form.findChild(QSpinBox,"studio_monthly_spinBox")
        self.oneBedroomD = form.findChild(QSpinBox,"one_bedroom_daily_spinBox")
        self.oneBedroomM = form.findChild(QSpinBox,"one_bedroom_monthly_spinBox")
        self.twoBedroomD = form.findChild(QSpinBox,"two_bedroom_daily_spinBox")
        self.twoBedroomM = form.findChild(QSpinBox,"two_bedroom_monthly_spinBox")
        
        self.studioD.setMaximum(99999)
        self.studioM.setMaximum(99999)
        self.oneBedroomD.setMaximum(99999)
        self.oneBedroomM.setMaximum(99999)
        self.twoBedroomD.setMaximum(99999)
        self.twoBedroomM.setMaximum(99999)
        
        self.studioD.setValue(int(self.db.getDefault_d("studio")))
        self.studioM.setValue(int(self.db.getDefault_m("studio")))
        self.oneBedroomD.setValue(int(self.db.getDefault_d("1-bedroom")))
        self.oneBedroomM.setValue(int(self.db.getDefault_m("1-bedroom")))
        self.twoBedroomD.setValue(int(self.db.getDefault_d("2-bedroom")))
        self.twoBedroomM.setValue(int(self.db.getDefault_m("2-bedroom")))
        
        self.studio_update_btn = form.findChild(QPushButton,"studio_update_btn")
        self.studio_update_btn.clicked.connect(self.studio_update)
        
        self.studio_default_btn = form.findChild(QPushButton,"studio_default_btn")
        self.studio_default_btn.clicked.connect(self.studio_default)
        
        self.oneBedroom_update_btn = form.findChild(QPushButton,"one_bedroom_update_btn")
        self.oneBedroom_update_btn.clicked.connect(self.oneBedroom_update)
        
        self.oneBedroom_default_btn = form.findChild(QPushButton,"one_bedroom_default_btn")
        self.oneBedroom_default_btn.clicked.connect(self.oneBedroom_default)
        
        self.twoBedroom_update_btn = form.findChild(QPushButton,"two_bedroom_update_btn")
        self.twoBedroom_update_btn.clicked.connect(self.twoBedroom_update)
        
        self.twoBedroom_default_btn = form.findChild(QPushButton,"two_bedroom_default_btn")
        self.twoBedroom_default_btn.clicked.connect(self.twoBedroom_default)

        #Password Section
        self.managerPass = form.findChild(QRadioButton,"manager_radioButton")
        self.receptionistPass = form.findChild(QRadioButton,"receptionist_radioButton")
        
        self.old_password = form.findChild(QLineEdit,"old_password_lineEdit")
        self.new_password = form.findChild(QLineEdit,"new_password_lineEdit")
        self.confirm_new_password = form.findChild(QLineEdit,"confirm_new_password_lineEdit")

        self.old_password.setEchoMode(QLineEdit.Password)
        self.new_password.setEchoMode(QLineEdit.Password)
        self.confirm_new_password.setEchoMode(QLineEdit.Password)

        self.password_update_btn = form.findChild(QPushButton,"password_update_btn")
        self.password_update_btn.clicked.connect(self.password_update)
        self.password_default_btn = form.findChild(QPushButton,"password_default_btn")
        self.password_default_btn.clicked.connect(self.password_default)

    def utility_update(self):
        self.db.setUtilRate("water",float(self.water.value()))
        self.db.setUtilRate("electricity",float(self.electric.value()))
        
    def utility_default(self):
        self.water.setValue(float(self.db.getDefault_util("water")))
        self.electric.setValue(float(self.db.getDefault_util("electricity")))

    def studio_update(self):
        self.db.setting_daily(str(self.studioD.value()),"studio")
        self.db.setting_monthly(str(self.studioM.value()),"studio")

    def studio_default(self):
        self.studioD.setValue(int(self.db.getDefault_d("studio")))
        self.studioM.setValue(int(self.db.getDefault_m("studio")))

    def oneBedroom_update(self):
        self.db.setting_daily(str(self.oneBedroomD.value()),"1-bedroom")
        self.db.setting_monthly(str(self.oneBedroomM.value()),"1-bedroom")

    def oneBedroom_default(self):
        self.oneBedroomD.setValue(int(self.db.getDefault_d("1-bedroom")))
        self.oneBedroomM.setValue(int(self.db.getDefault_m("1-bedroom")))

    def twoBedroom_update(self):
        self.db.setting_daily(str(self.twoBedroomD.value()),"2-bedroom")
        self.db.setting_monthly(str(self.twoBedroomM.value()),"2-bedroom")

    def twoBedroom_default(self):
        self.twoBedroomD.setValue(int(self.db.getDefault_d("2-bedroom")))
        self.twoBedroomM.setValue(int(self.db.getDefault_m("2-bedroom")))

    def password_update(self):
        newpass = self.new_password.text()
        
        if self.managerPass.isChecked() == True :
            if newpass == self.confirm_new_password.text():
                if self.db.getPassword("manager") == self.old_password.text():
                    self.db.setPassword("manager",newpass)
                    self.old_password.clear()
                    self.new_password.clear()
                    self.confirm_new_password.clear()
                    self.popup("Manager password is changed")
                else:
                    self.popup("Password is not correct")
            else :
                self.popup("Confirm password is not match!")
                
        elif self.receptionistPass.isChecked() == True :
            if newpass == self.confirm_new_password.text():
                if self.db.getPassword("receptionist") == self.old_password.text():
                    self.db.setPassword("receptionist",newpass)
                    self.old_password.clear()
                    self.new_password.clear()
                    self.confirm_new_password.clear()
                    self.popup("Receptionist password is changed")                
                else :
                    self.popup("Password is not correct")
            else:
                self.popup("Confirm password is not match!")

    def password_default(self):
        if self.managerPass.isChecked() == True :
            self.db.setDefaultPasswordForManager()
            self.popup("Manager password is set to default")
        elif self.receptionistPass.isChecked() == True :
            self.db.setDefaultPasswordForReceptionist()
            self.popup("Receptionist password is set to default")

    def back(self):
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

    def paintEvent(self, e): #for adding an image
        p = QPainter()
        p.begin(self)
        p.drawImage(QRect(0,0,display_width,display_height), bg)
        p.end()
        
