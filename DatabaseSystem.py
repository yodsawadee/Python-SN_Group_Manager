import sqlite3
import sys
import datetime

class DatabaseSys():
    def __init__(self):
        self.cn = sqlite3.connect(".\SNGroupSys.db")
        self.cur = self.cn.cursor()
        self.createtableResident()
        self.createtableUtilities() 
        self.createtableUtilitieRate()
        self.createtableRoom()
        self.createtableReserve()
        self.createtableRoomState()
        self.createtableResidentHistory()
        self.createtablePassword()

    def createtableReserve(self):
        self.cur.execute("""create table if not exists[reserve]([room_number] varchar(20) ,[type_of_res] varchar(30),
                                           [first_name] varchar(20),[last_name] varchar(20),
                                           [national_id] varchar(30),[line] varchar(30),[email] varchar(30),
                                           [tel_no] varchar(30),[permanent_address] varchar(100),
                                           [check_in_date] varchar(20),[check_out_date] varchar(20))""")
        self.cn.commit()
        
    def createtableRoomState(self):
        self.cur.execute("""create table if not exists[roomstatus]([room_number] varchar(20) ,
                                           [not_avail_from] varchar(20),[not_avail_to] varchar(20))""")
        self.cn.commit()
        
    def createtableResident(self):
        self.cur.execute("""create table if not exists[resident]([room_number] varchar(20) ,[type_of_res] varchar(30),
                                           [first_name] varchar(20),[last_name] varchar(20),
                                           [national_id] varchar(30),[line] varchar(30),[email] varchar(30),
                                           [tel_no] varchar(30),[permanent_address] varchar(100),
                                           [check_in_date] varchar(20),[check_out_date] varchar(20))""")
       
        self.cn.commit()
          
    def createtableUtilities(self):
        self.cur.execute("""create table if not exists[utilities_unit]([room_number] varchar(20),[month_year] varchar(20),[water_meter_unit] varchar(20),
                        [electricity_meter_unit] varchar(20))""")
        self.cn.commit() 
        
    def createtableUtilitieRate(self):
        s = """select count(*) from sqlite_master where type='table' and name='utilities_rate'"""
        table_exist = self.cur.execute(s).fetchone()
        if  table_exist[0]:
            pass
        else:
            self.cur.execute("""create table if not exists[utilities_rate]([util_type] varchar(20),[rate] decimal,[default_val] decimal)""")
            s = "insert into utilities_rate values(?,?,?)"
            self.cur.execute(s,("water",0.0,0.0))
            self.cur.execute(s,("electricity",0.0,0.0))
        self.cn.commit() 
        
    def createtableRoom(self):
        s = """select count(*) from sqlite_master where type='table' and name='room'"""
        table_exist = self.cur.execute(s).fetchone()
        if  table_exist[0]:
            pass
        else:
            self.cur.execute("""create table if not exists[room]([room_number] varchar(20),[floor] varchar(30),[room_type] varchar(30),[daily_price] varchar(20),
                                           [monthly_price] varchar(20),[default_d] varchar(20),[default_m] varchar(20))""")
            i = 101
            floor = 1
            type_room = "studio"
            
            while(True):
                s = "insert into room values(?,?,?,?,?,?,?)"
                self.cur.execute(s,(i,floor,type_room,'0','0','0','0'))
                i = i+1
                if i == 113:
                    i = 201
                    floor = 2
                if i == 218:
                    i = 301
                    floor = 3
                if i == 318:
                    i = 401
                    floor = 4
                if i == 418:
                    i = 501
                    floor = 5
                if i == 514 or i == 515:
                    type_room = "1-bedroom"
                if i == 512 or i == 513:
                    type_room = "2-bedroom"
                if i == 516:
                    break
        self.cn.commit()
        
    def createtableResidentHistory(self):
        self.cur.execute("""create table if not exists[residenthistory]([room_number] varchar(20) ,[type_of_res] varchar(30),
                                           [first_name] varchar(20),[last_name] varchar(20),
                                           [national_id] varchar(30),[line] varchar(30),[email] varchar(30),
                                           [tel_no] varchar(30),[permanent_address] varchar(100),
                                           [check_in_date] varchar(20),[check_out_date] varchar(20))""")
        self.cn.commit()

    def createtablePassword(self):
        s = """select count(*) from sqlite_master where type='table' and name='password'""" 
        table_exist = self.cur.execute(s).fetchone() 
        if  table_exist[0]: 
            pass 
        else:
            self.cur.execute("""create table if not exists[password]([manager_password] varchar(20),
                                               [receptionist_password] varchar(20))""")
            
            s = "insert into password values (?,?)"
            self.cur.execute(s,("sys","sys"))
        self.cn.commit()
        
    def readRoomInfo(self,room_num):  
        out = "" 
        self.cur.execute("select room_type,daily_price,monthly_price from room where room_number = ?",(room_num,)) 
        temp = self.cur.fetchall() 
        out = "Room type: "+ temp[0][0]+"\n- Daily price: "+ temp[0][1] + "\n- Monthly price: "+ temp[0][2]  
        return out
    
     
    def readResidentInfo(self,room_num):  
        out = "" 
        self.cur.execute("select * from resident where room_number = ?",(room_num,)) 
        temp = self.cur.fetchall()
        if (len(temp) == 0):
            out = "Available"
        else:
            out = "Resident type: "+temp[0][1]+ "\nName: " + temp[0][2]+ " " + temp[0][3] + "\nNational ID: " +\
            temp[0][4] +"\nLine: "+ temp[0][5] +"\nE-mail: "+ temp[0][6] + "\nTel: " +\
            temp[0][7] + "\nAddress: " +temp[0][8]+\
            "\nCheck in date: " + temp[0][9] +"\nCheck out date: " + temp[0][10]
            
        return out

    def readResidentType(self,room_num):  
        temp = "" 
        self.cur.execute("select type_of_res from resident where room_number = ?",(room_num,)) 
        out = self.cur.fetchall()
        if (len(out) == 0):
            temp = "None"
        else:
            temp = out[0][0]
        return temp

    def readRoomType(self,room_num):  
        self.cur.execute("select room_type from room where room_number = ?",(room_num,)) 
        out = self.cur.fetchone() 
        return out[0]

    def searchAllAvailableRoom(self,floor,from_date,to_date):
        from_date = from_date.split("/")
        from_date = datetime.datetime(int(from_date[0]),int(from_date[1]),int(from_date[2])).date()

        to_date = to_date.split("/")
        to_date = datetime.datetime(int(to_date[0]),int(to_date[1]),int(to_date[2])).date()
        
        self.cur.execute("select * from roomstatus")
        allStatus = self.cur.fetchall()
        roomstatus_list = []
        for i in range (len(allStatus)):
            eachRecord = allStatus[i]
            roomNo = eachRecord[0]
            indate = eachRecord[1]
            outdate = eachRecord[2]

            indate = indate.split("/")
            indate = datetime.datetime(int(indate[0]),int(indate[1]),int(indate[2])).date()
            outdate = outdate.split("/")
            outdate = datetime.datetime(int(outdate[0]),int(outdate[1]),int(outdate[2])).date()
            roomstatus_list.append([roomNo,indate,outdate])
            not_available_list = []

        for i in roomstatus_list:
            if from_date == i[1] or to_date==i[2] :
                not_available_list.append(i[0])
            elif (from_date >= i[1] and from_date<=i[2]): #indate <= from_date <= outdate
                not_available_list.append(i[0])
            elif (to_date >= i[1] and to_date <=i[2]): #indate <= to_date <= outdate
                not_available_list.append(i[0])
            elif (from_date <= i[1] and to_date>=i[2]): #from_date <= indate AND to_date >= out_date
                not_available_list.append(i[0])
                
        s = "select room_number,floor,room_type from room where floor = ? "
        self.cur.execute(s,(str(floor)))
        allRoom = self.cur.fetchall()
        for i in allRoom:
            if i[0] in not_available_list:
                allRoom.remove(i)
                
        return allRoom
    
    def searchAvailableRoom(self,floor,room_type,from_date,to_date):
        from_date = from_date.split("/")
        from_date = datetime.datetime(int(from_date[0]),int(from_date[1]),int(from_date[2])).date()

        to_date = to_date.split("/")
        to_date = datetime.datetime(int(to_date[0]),int(to_date[1]),int(to_date[2])).date()
        
        self.cur.execute("select * from roomstatus")
        allStatus = self.cur.fetchall()
        roomstatus_list = []
        for i in range (len(allStatus)):
            eachRecord = allStatus[i]
            roomNo = eachRecord[0]
            indate = eachRecord[1]
            outdate = eachRecord[2]

            indate = indate.split("/")
            indate = datetime.datetime(int(indate[0]),int(indate[1]),int(indate[2])).date()
            outdate = outdate.split("/")
            outdate = datetime.datetime(int(outdate[0]),int(outdate[1]),int(outdate[2])).date()
            roomstatus_list.append([roomNo,indate,outdate])
            not_available_list = []

        for i in roomstatus_list :
            if from_date == i[1] or to_date==i[2] :
                not_available_list.append(i[0])
            elif (from_date >= i[1] and from_date<=i[2]): #indate <= from_date <= outdate
                not_available_list.append(i[0])
            elif (to_date >= i[1] and to_date <=i[2]): #indate <= to_date <= outdate
                not_available_list.append(i[0])
            elif (from_date <= i[1] and to_date>=i[2]): #from_date <= indate AND to_date >= out_date
                not_available_list.append(i[0])

        s = "select room_number,floor,room_type from room where floor = ? and room_type =?"
        self.cur.execute(s,(str(floor),str(room_type)))
        allRoom = self.cur.fetchall()
        for i in allRoom:
            if i[0] in not_available_list:
                allRoom.remove(i)
                
        return allRoom
    
        
    def countAvailableRoom(self,rtype,from_date,to_date):
        from_date = from_date.split("/")
        from_date = datetime.datetime(int(from_date[0]),int(from_date[1]),int(from_date[2])).date()

        to_date = to_date.split("/")
        to_date = datetime.datetime(int(to_date[0]),int(to_date[1]),int(to_date[2])).date()
        
        self.cur.execute("select * from roomstatus")
        allStatus = self.cur.fetchall()
        roomstatus_list = []
        for i in range (len(allStatus)):
            eachRecord = allStatus[i]
            roomNo = eachRecord[0]
            indate = eachRecord[1]
            outdate = eachRecord[2]

            indate = indate.split("/")
            indate = datetime.datetime(int(indate[0]),int(indate[1]),int(indate[2])).date()
            outdate = outdate.split("/")
            outdate = datetime.datetime(int(outdate[0]),int(outdate[1]),int(outdate[2])).date()
            roomstatus_list.append([roomNo,indate,outdate])
            not_available_list = []

        for i in roomstatus_list:
            if from_date == i[1] or to_date==i[2] :
                not_available_list.append(i[0])
            elif (from_date >= i[1] and from_date<=i[2]): #indate <= from_date <= outdate
                not_available_list.append(i[0])
            elif (to_date >= i[1] and to_date <=i[2]): #indate <= to_date <= outdate
                not_available_list.append(i[0])
            elif (from_date <= i[1] and to_date>=i[2]): #from_date <= indate AND to_date >= out_date
                not_available_list.append(i[0])

        self.cur.execute("select count(*) from room where room_type = ? ",(rtype,))
        numRoomType = self.cur.fetchall()
        numRoomType = int(numRoomType[0][0])
        count=0
        
        for i in not_available_list:
            if rtype == self.readRoomType(i) :
                count +=1
        numRoomType = numRoomType-count
                
        return numRoomType
                            
    
    def reserve(self,room_num,type_res,first,last,nat,line,ema,tel,addr,from_date,to_date = "9999/12/31"):
        s = "insert into reserve values(?,?,?,?,?,?,?,?,?,?,?)"
        self.cur.execute(s,(room_num,type_res,first,last,nat,line,ema,tel,addr,from_date,to_date))
        
        self.cur.execute("insert into roomstatus values(?,?,?)",(room_num,from_date,to_date))
        self.cn.commit()
    
    def searchByName(self,f_name,l_name):
        s = "select * from reserve where first_name = ? or last_name = ?"
        self.cur.execute(s,(f_name,l_name))
        out = self.cur.fetchall()
        return out
    
    def cancelReserve(self,room_number,cin_date,cout_date):
        s = "delete from reserve where room_number = ? and check_in_date = ? and check_out_date = ?"
        self.cur.execute(s,(room_number,cin_date,cout_date))
        self.cn.commit()
        
        s = "delete from roomstatus where room_number = ? and not_avail_from = ? and not_avail_to = ?"
        self.cur.execute(s,(room_number,cin_date,cout_date))
        self.cn.commit()
        
    def checkInReserve(self,room_num,type_res,first,last,nat,line,ema,tel,addr,from_date,to_date = "9999/12/31"):
        s = "insert into resident values(?,?,?,?,?,?,?,?,?,?,?)"
        self.cur.execute(s,(room_num,type_res,first,last,nat,line,ema,tel,addr,from_date,to_date))
        
        self.cur.execute("insert into roomstatus values(?,?,?)",(room_num,from_date,to_date))

        s = "delete from reserve where room_number = ? and check_in_date = ? and check_out_date = ?"
        self.cur.execute(s,(room_num,from_date,to_date))
        self.cn.commit()

    def checkInWalk(self,room_num,type_res,first,last,nat,line,ema,tel,addr,from_date,to_date = "9999/12/31"):
        s = "insert into resident values(?,?,?,?,?,?,?,?,?,?,?)"
        self.cur.execute(s,(room_num,type_res,first,last,nat,line,ema,tel,addr,from_date,to_date))
        
        self.cur.execute("insert into roomstatus values(?,?,?)",(room_num,from_date,to_date))
        self.cn.commit()
        
    def checkOut(self,room_number): 
        s = "select check_in_date from resident where room_number = ?"
        self.cur.execute(s,(room_number,))
        temp = self.cur.fetchone()
        
        #FORCE NEW CHECKOUT DATE
        today = str(datetime.date.today())
        today = today.replace("-","/")
        s = "update resident set check_out_date = ? where room_number = ?"
        self.cur.execute(s,(today,room_number,))
        self.cn.commit()
        
        s = "insert into residenthistory select * from resident where room_number = ?"
        self.cur.execute(s,(room_number,))
        self.cn.commit()
        
        s = "delete from resident where room_number = ?"
        self.cur.execute(s,(room_number,))
        self.cn.commit()     

        s = "delete from roomstatus where room_number = ? and not_avail_from = ?"
        self.cur.execute(s,(room_number,temp[0]))
        self.cn.commit()


    def deleteFronRoomstatus(self,room_number):
        s = "select check_in_date from resident where room_number = ?"
        self.cur.execute(s,(room_number,))
        temp = self.cur.fetchone()
        
        s = "delete from roomstatus where room_number = ? and not_avail_from = ?"
        self.cur.execute(s,(room_number,temp[0]))
        self.cn.commit()

    def setting_daily(self,new_daily,room_type):
        s = "select min(daily_price) from room where room_type = ?"
        self.cur.execute(s,(room_type,))
        out = self.cur.fetchall()

        s = "update room set default_d = ? where room_type = ?"
        self.cur.execute(s,(out[0][0],room_type))
        self.cn.commit()
        
        s = "update room set daily_price = ? where room_type = ?"
        self.cur.execute(s,(new_daily,room_type))
        self.cn.commit()
        
    def setting_monthly(self,new_monthly,room_type):
        s = "select min(monthly_price) from room where room_type = ?"
        self.cur.execute(s,(room_type,))
        out = self.cur.fetchall()
       
        s = "update room set default_m = ? where room_type = ?"
        self.cur.execute(s,(out[0][0],room_type))
        self.cn.commit()
        
        s = "update room set monthly_price = ? where room_type = ?"
        self.cur.execute(s,(new_monthly,room_type))
        self.cn.commit()

    def getDefault_m(self,room_type):
        s = "select min(default_m) from room where room_type = ?"
        self.cur.execute(s,(room_type,))
        out = self.cur.fetchall()
        
        s = "update room set monthly_price = ? where room_type = ?"
        self.cur.execute(s,(out[0][0],room_type))
        self.cn.commit()
        return out[0][0]

    def getDefault_d(self,room_type):
        s = "select min(default_d) from room where room_type = ?"
        self.cur.execute(s,(room_type,))
        out = self.cur.fetchall()

        s = "update room set daily_price = ? where room_type = ?"
        self.cur.execute(s,(out[0][0],room_type))
        self.cn.commit()
        return out[0][0]

    def setUtilRate(self,util_type,new_rate): 
        s = "select min(rate) from utilities_rate where util_type = ?"
        self.cur.execute(s,(util_type,))
        out = self.cur.fetchall()
       
        s = "update utilities_rate set default_val = ? where util_type = ?"
        self.cur.execute(s,(out[0][0],util_type))
        self.cn.commit()
        
        s = "update utilities_rate set rate = ? where util_type = ?"
        self.cur.execute(s,(new_rate,util_type))
        self.cn.commit()
        

    def getDefault_util(self,util_type): 
        s = "select min(default_val) from utilities_rate where util_type = ?"
        self.cur.execute(s,(util_type,))
        out = self.cur.fetchall()
        
        s = "update utilities_rate set rate = ? where util_type = ?"
        self.cur.execute(s,(out[0][0],util_type))
        self.cn.commit()
        return out[0][0]
    
    def getUtil(self,room_number,util_type):
        if (util_type == "all"):
            s = "select * from utilities_unit where room_number = ?"
            self.cur.execute(s,(room_number,))
            out = self.cur.fetchall()
            
        elif (util_type == "water"):
            s = "select water_meter_unit from utilities_unit where room_number = ?"
            self.cur.execute(s,(room_number,))
            out = self.cur.fetchall()
            
        elif (util_type == "electricity"):
            s = "select electricity_meter_unit from utilities_unit where room_number = ?"
            self.cur.execute(s,(room_number,))
            out = self.cur.fetchall()
        if (len(out) == 0):
            return "0"
        else:
            return out

    def getUtilDate(self,room_number): 
        s = "select month_year from utilities_unit where room_number = ?"
        self.cur.execute(s,(room_number,))
        out = self.cur.fetchall()
        if (len(out) == 0):
            return "None"
        else:
            return out[0][0]

    def insertUtil(self,room_number,month_year,water_meter_unit,electricity_meter_unit):
        s = "insert into utilities_unit values(?,?,?,?)"
        self.cur.execute(s,(room_number,month_year,water_meter_unit,electricity_meter_unit))
        self.cn.commit()
        
    def editUtil(self,room_number,month_year,new_water_meter_unit,new_electricity_meter_unit):
        s = "update utilities_unit set water_meter_unit = ?,electricity_meter_unit = ? where room_number = ? and month_year = ?"
        self.cur.execute(s,(new_water_meter_unit,new_electricity_meter_unit,room_number,month_year))
        self.cn.commit()

    def setPassword(self,mode,new_pass):
        if  mode == "manager":
            s = "update password set manager_password = ?"
        else:
            s = "update password set receptionist_password = ?"   
        self.cur.execute(s,(new_pass,))
        self.cn.commit()
        
    def getPassword(self,mode):
         if  mode == "manager":
            s = "select manager_password from password"
            
         else:
            s = "select receptionist_password from password"

         self.cur.execute(s)
         out = self.cur.fetchone()
         return out[0]

    def getRoomPrice(self,room_type):
        s = "select daily_price,monthly_price from room where room_type = ?"
        self.cur.execute(s,(room_type,))
        out = self.cur.fetchall() ##[0][0] =daily [0][1] = monthly
        return out

    def getCheckinoutDate(self, room_num):
        s = ("select check_in_date, check_out_date from resident where room_number = ?")
        self.cur.execute(s, (room_num,))
        out = self.cur.fetchall()
        return out
    
    def setDefaultPasswordForManager(self):
        i = "sys"
        self.cur.execute("update password set manager_password = ?",(i,))
        self.cn.commit()

    def setDefaultPasswordForReceptionist(self):
        i = "sys"
        self.cur.execute("update password set receptionist_password = ?",(i,))
        self.cn.commit()

    def checkExceedCheckoutDate(self,room_number):
        s = "select check_out_date from resident where room_number = ?"
        self.cur.execute(s,(room_number,))
        chkout = self.cur.fetchone()
        chkout = chkout[0]
        chkout = chkout.split('/')
        y = int(chkout[0])
        m = int(chkout[1])
        d = int(chkout[2])

        chkout = datetime.datetime(y,m,d).date()
        
        if datetime.date.today() > chkout :
            return True
        else :
            return False

    def checkStatusIftheroomisCheckedIn(self, room_number): 
        self.cur.execute("select room_number from roomstatus where room_number not in (select room_number from reserve)")
        out = self.cur.fetchall()
        temp = []
        l = len(out)+1
        for i in range(l):
            if(i == len(out)):
                continue
            else:
                temp.append(out[i][0])
            
        if room_number in temp:
            return True
        else:
            return False

    def checkStatusIftheroomisReserved(self, room_number): 
        self.cur.execute("select room_number from roomstatus where room_number not in (select room_number from resident)")
        out = self.cur.fetchall()
        temp = []
        l = len(out)+1
        for i in range(l):
            if(i == len(out)):
                continue
            else:
                temp.append(out[i][0])
            
        if room_number in temp:
            return True
        else:
            return False

    def checkReserveByCheckInDay(self,checkin_day): 
        s = "select * from reserve where ? = check_in_date"
        self.cur.execute(s,(checkin_day,))
        out = self.cur.fetchall()
        return out

    def checkReservedResidentInfoByRoomNo(self,room_number): 
        s = "select * from reserve where ? = room_number"
        self.cur.execute(s,(room_number,))
        out = self.cur.fetchall()
        return out[0]

    def allpassword(self):
        self.cur.execute("select * from password")
        out = self.cur.fetchall()
        return out
    
    def allutilities_unit(self):
        self.cur.execute("select * from utilities_unit order by room_number, month_year")
        out = self.cur.fetchall()
        return out
    def allutilities_rate(self):
        self.cur.execute("select * from utilities_rate")
        out = self.cur.fetchall()
        return out
    def allroomstatus(self):
        self.cur.execute("select * from roomstatus")
        out = self.cur.fetchall()
        return out
    def allreserve(self):
       self.cur.execute("select * from reserve")
       
       out = self.cur.fetchall()
       return out
    def allresident(self):
       self.cur.execute("select * from resident")
       out = self.cur.fetchall()
       return out
    def allresidenthistory(self):
       self.cur.execute("select * from residenthistory")
       out = self.cur.fetchall()
       return out
    def allroom(self):
       self.cur.execute("select * from room")
       out = self.cur.fetchall()
       return out
    def test(self,from_date,to_date):
        s = "select room_number from roomstatus where ? between not_avail_from and not_avail_to and ? between not_avail_from and not_avail_to"
        self.cur.execute(s,(from_date,to_date))
        out = self.cur.fetchall()
        return out

    def IsAvailable(self,room_number):
        s = "select room_number from resident where room_number = ?"
        self.cur.execute(s,(room_number,))
        out = self.cur.fetchall()
        if len(out) == 0:
            return True
        else:
            return False

