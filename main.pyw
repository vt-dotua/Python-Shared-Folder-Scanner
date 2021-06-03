import sys
from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QApplication, QMainWindow, QButtonGroup,QAbstractButton
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from copy import copy, deepcopy
from smb.SMBConnection import SMBConnection
import ipaddress
import socket
from ping3 import ping
import re
import win32com
import wmi
import win32gui, win32con

class ScunNet():

        IP = r"(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5])\.(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5])\.(?:1\d?\d?|[1-9]\d?|2[0-4]?\d?|0|25[0-5])\.(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5])"
        IP_range = r"((?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5])(?:-(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5]))?)\.((?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5])(?:-(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5]))?)\.((?:1\d?\d?|[1-9]\d?|2[0-4]?\d?|0|25[0-5])(?:-(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5]))?)\.((?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5])(?:-(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5]))?)"
        IP_mask = r"(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5])\.(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5])\.(?:1\d?\d?|[1-9]\d?|2[0-4]?\d?|0|25[0-5])\.(?:1\d?\d?|[1-9]\d?|0|2[0-4]?\d?|25[0-5])/(?:\d|[1-2]\d|3[0-2])"    
        
        def __IPmask(self, ip):
            rIP = []
            for i in ipaddress.ip_network(ip):
                rIP.append(str(i))
            return rIP

        def __IPrange(self, ip, matchIP_range):
            rIP = []
            octet = [[] for i in range(4)]
            for j in range(1, 5):
                if matchIP_range[j].find('-') != -1:
                    temp = matchIP_range[j].split('-')
                    for i in range(int(temp[0]), int(temp[1])+1):
                        octet[j-1].append(str(i))
                else:
                    octet[j-1].append(matchIP_range[j])

            for a in octet[0]:
                for b in octet[1]:
                    for c in octet[2]:
                        for d in octet[3]:
                            rIP.append('{0}.{1}.{2}.{3}'.format(a,b,c,d))
            return rIP

        def __IP_transformer(self, ip):
            matchIP = re.fullmatch(self.IP, ip)
            matchIP_range = re.fullmatch(self.IP_range, ip)
            matchIP_mask = re.fullmatch(self.IP_mask, ip)
            
            if matchIP_range and not matchIP:
                resultRange = self.__IPrange(ip, matchIP_range)
            elif matchIP:
                resultRange = [ip]
            elif matchIP_mask:
                resultRange = self.__IPmask(ip)
            else:
                resultRange = ""

            return resultRange

        def __ScunAliveHost(self, ip_range, timeScun=0.1):
                aliveHost = []
                for i in ip_range:
                        hPing = ping(i, timeout=timeScun)
                        if hPing != None:
                                aliveHost.append(str(i))
                return aliveHost
        
        def FindAliveHost(self, ip, timeScun=0.1):
            ip_range = self.__IP_transformer(ip)
            aliveHost = self.__ScunAliveHost(ip_range, timeScun)
            NetHost = []
            for i in aliveHost:
                oneItem = []
                try:
                    remoteName = socket.getfqdn(i)
                    oneItem.append(remoteName)
                    oneItem.append(i)
                    NetHost.append(deepcopy(oneItem))
                except Exception as ex:
                    print('IP_scun_host:', ex)
                    continue 

            return NetHost

        def FindSharedFolders(self, ip, userName="", userPassword="", timeScun=0.1):
                ip_range = self.__IP_transformer(ip)
                aliveHost = self.__ScunAliveHost(ip_range, timeScun)
                NetFolder = []

                for i in aliveHost:
                        tempResult = []
                        listFolder = []
                        
                        try:
                                remoteName = socket.getfqdn(i)
                                smbCon = SMBConnection(username=userName, password=userPassword,
                                        my_name = socket.gethostname(), remote_name = remoteName,
                                        domain="")
                                smbCon.connect(ip=i)
                                for l in smbCon.listShares():
                                        listFolder.append(l.name)
                        except Exception as ex:
                                print("Exception : ",i, ex)
                                continue 
                        finally:
                                smbCon.close()
                        tempResult.append(i)
                        tempResult.append(remoteName)
                        tempResult.append(deepcopy(listFolder))  
                        NetFolder.append(deepcopy(tempResult))
                return NetFolder
        
        def LocalSharedFolders(self):
            LocalFolder = []
            c = wmi.WMI ()
            for share in c.Win32_Share ():
                if re.fullmatch("[A-Za-z]\$", share.Name) == None:
                    LocalFolder.append(share.Name)
            
            return LocalFolder

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui_file = QFile("gui_main.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        #self.ui.ip_field.setText('192.168.1.100-105')
        self.ui.scunButton.clicked.connect(self.Start_Scun) 

        self.ui.scunButton.setEnabled(False)
        self.ip_flag = False
        self.speed_flag = True

        self.ui.ip_field.textChanged[str].connect(self.Check_ip_ui)
        self.ui.speed_field.textChanged[str].connect(self.Check_speed_ui)

        self.choiceGroup = QButtonGroup()
        self.choiceGroup.addButton(self.ui.radio_folder)
        self.choiceGroup.addButton(self.ui.radio_local_folder)
        self.choiceGroup.addButton(self.ui.radio_host)

        #self.radioButton = QAbstractButton() 

        self.choiceGroup.buttonClicked.connect(self.Change_radio)

        self.t = 0

    def ShowResultFolder(self, folders):
        setBlock ="""
        <div>
        <p class='ip'>IP адреса: {0}</p>
        <p class='host'>І'мя ПК: {1}</p>
        <p>Розшарені папки:</p>
        <ul>
            {2}
        </ul>
        </div>
        <div><div>
        """
        showFolder = []
        tempF = ""
        for i in folders:
            for k in i[2]:
                tempF += "<li>"+k+"</li>"
            i[2] = tempF
            tempF=""
        
        for f in folders:
            self.ui.show_field.append(setBlock.format(f[0], f[1], f[2]))

    def ShowResultHost(self, host):
        setBlock ="""
        <div>
        <p class='ip'>І'мя хоста: {0} </p>
        <p class='ip'>        IP: {1} </p>
        <p class='ip'>    Статус: активний</p>
        </div>
        <div><div>
        """
        for h in host:
            self.ui.show_field.append(setBlock.format(h[0], h[1]))
    
    def ShowLocalFolder(self, folders):
        setBlock ="""
        <div>
        <p>Розшарені папки:</p>
        <ul>
            {0}
        </ul>
        </div>
        <div></div>
        """

        ShowF = ""
        for i in folders:
            ShowF += "<li>"+i+"</li>"
        
        self.ui.show_field.append(setBlock.format(ShowF))
    
    def Check_speed(self):
        speedV = self.ui.speed_field.text()
        matchIP = re.fullmatch(r"\d+(?:\.\d+)?", speedV)
        if matchIP:
            floatSpeed = float(speedV)
            if floatSpeed >= 0.001 and floatSpeed <= 1: 
                self.speed_flag = True
            else:
                self.speed_flag = False     
        else:
            self.speed_flag = False
        
        if self.ip_flag and self.speed_flag:
            self.ui.scunButton.setEnabled(True)
        else:
            self.ui.scunButton.setEnabled(False)

    
    def Check_ip(self):
        ip = self.ui.ip_field.text()
        matchIP = re.fullmatch(ScunNet.IP, ip)
        matchIP_range = re.fullmatch(ScunNet.IP_range, ip)
        matchIP_mask = re.fullmatch(ScunNet.IP_mask, ip)
        if matchIP or matchIP_range or matchIP_mask:

            if matchIP_range and not matchIP:
                flag = []
                for i in range(1,5):
                    if matchIP_range[i].find('-') != -1:
                        splitIP = matchIP_range[i].split('-')
                        if int(splitIP[0]) < int(splitIP[1]):
                            flag.append(True)
                        else:
                            flag.append(False)            
                if False in flag:
                    self.ip_flag = False
                else:
                    self.ip_flag = True
            else:
                self.ip_flag = True
        else:  
            self.ip_flag = False
        
        if self.ip_flag and self.speed_flag:
            self.ui.scunButton.setEnabled(True)
        else:
            self.ui.scunButton.setEnabled(False)

    @Slot()
    def Change_radio(self):
        if self.ui.radio_local_folder.isChecked():
            self.ui.scunButton.setEnabled(True)
        else:
            self.Check_speed()
            self.Check_ip()   

    @Slot()
    def Check_speed_ui(self):
        self.Check_speed()


    @Slot()
    def Check_ip_ui(self):
        self.Check_ip()

    @Slot()
    def Start_Scun(self):
        if not self.ui.radio_local_folder.isChecked():
            ip = self.ui.ip_field.text()
            speed = float(self.ui.speed_field.text())
            name = self.ui.name_field.text()
            pasword = self.ui.pasword_field.text()

        self.ui.show_field.setText('')
        ScunN = ScunNet()

        if self.ui.radio_folder.isChecked():
            folders = ScunN.FindSharedFolders(ip=ip, timeScun=speed)        
            self.ShowResultFolder(folders)

        elif self.ui.radio_host.isChecked():
            host = ScunN.FindAliveHost(ip=ip, timeScun=speed)
            self.ShowResultHost(host)

        elif self.ui.radio_local_folder.isChecked():
            folders = ScunN.LocalSharedFolders()
            self.ShowLocalFolder(folders) 
    

if __name__ == "__main__":
    #hide = win32gui.GetForegroundWindow()
    #win32gui.ShowWindow(hide , win32con.SW_HIDE)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.ui.show()
    sys.exit(app.exec_())