#-*- coding: utf-8 -*-

import datetime, time
import numpy as np
from PyQt5 import QtCore, QtGui, QtTest
from blinkt import DAT, CLK, set_pixel, show

import socket, time, datetime
from packets import *

class Process(QtCore.QThread):
    Set_Text = QtCore.pyqtSignal(str, str)
    Set_Pixmap = QtCore.pyqtSignal(str, QtGui.QPixmap)
    Set_StyleSheet = QtCore.pyqtSignal(str, str)
    Set_page = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(Process, self).__init__(parent)
        self.Working = True
        self.mainWindow = parent

        self.LED_bar = 0
        self.drs_toggle: bool = False
        self.Lap_all: int = 0
        self.Lap_count: int = 0
        self.img_init()
        
        self.ersDeployMode_text = {0: "None", 1: "Medium", 2: "HotLap", 3: "Overtake"}
        self.ersDeployMode_styleheet = {
            0: "color: rgb(255, 255, 255); background-color: rgb(0, 0, 0);",
            1: "color: rgb(255, 255, 255); background-color: rgb(0, 0, 0);",
            2: "color: rgb(255, 255, 0); background-color: rgb(0, 0, 0);",
            3: "color: rgb(255, 0, 0); background-color: rgb(0, 0, 0);"
        }

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 20777))
        self.sock.settimeout(0.5)

        self.ck_game_start: bool = False
        self.ck_game_udp_time = time.time()
        self.ck_game_udp_out_time: int = 5

    def img_init(self):
        ersStoreEnergy_bar_img = np.full((10, 10, 3), (255, 255, 0), dtype=np.uint8)
        ersStoreEnergy_bar_img = QtGui.QImage(ersStoreEnergy_bar_img, 10, 10, 10*3, QtGui.QImage.Format_RGB888)

        self.ersStoreEnergy_bar = QtGui.QPixmap.fromImage(ersStoreEnergy_bar_img)

        ersStoreEnergy_img = self.ersStoreEnergy_bar.scaled(279, 30)
        self.Set_Pixmap.emit("ERS_Store", ersStoreEnergy_img)

        ersStoreEnergy_img.fill(QtGui.QColor(255, 255, 255))
        ersStoreEnergy_img = ersStoreEnergy_img.scaled(279, 30)
        self.Set_Pixmap.emit("ERS_Deploted", ersStoreEnergy_img)

        self.Set_Text.emit("round", "0/0")
        self.Set_StyleSheet.emit("Drs_led", "background-color: rgb(0, 0, 0);")

    def run(self):
        while self.Working:
            buf = []
            try:
                data, addr = self.sock.recvfrom(1500)
                buf = unpack_udp_packet(data)
            except:
                pass
            if buf:
                if buf.header.packetId == 1:
                    self.Packet_SessionData_Process(buf)

                elif buf.header.packetId == 2:
                    self.Packet_LapData_Process(buf)

                elif buf.header.packetId == 6:
                    self.Packet_CarTelemetryData_Process(buf)

                elif buf.header.packetId == 7:
                    self.Packet_CarStatusData_Process(buf)
                
                elif buf.header.packetId == 8:
                    pass#self.Packet_FinalClassificationData_Process(buf)

                elif buf.header.packetId == 10:
                    self.Packet_CarDamageData_Process(buf)

                if not self.ck_game_start:
                    self.Set_page.emit(0)

                    self.ck_game_start = True
                self.ck_game_udp_time = time.time()
            else:
                if time.time() - self.ck_game_udp_time > self.ck_game_udp_out_time:
                    self.ck_game_start = False
                    self.Set_page.emit(1)
                    ck_ip = socket.gethostbyname(socket.gethostname())
                    ck_ip = "No internet connection." if ck_ip == "127.0.0.1" else F"iP: {ck_ip}"
                    self.Set_Text.emit("label", ck_ip)
                    self.ck_game_udp_time = time.time()

            time.sleep(0.000001)

    def Packet_SessionData_Process(self, dataPack):
        self.All_Lap(dataPack)

    def Packet_LapData_Process(self, dataPack):
            self.LapDataPart(dataPack)

    def Packet_CarTelemetryData_Process(self, dataPack):
            self.CarTelemetryDataPart(dataPack)

    def Packet_CarStatusData_Process(self, dataPack):
            self.Ers(dataPack)
            self.Drs_Available(dataPack)
    
    def Packet_FinalClassificationData_Process(self, dataPack):
        Lap = dataPack.classificationData[dataPack.header.playerCarIndex].numLaps
        print(Lap)
    
    def All_Lap(self, DataPack):
        LapAll = DataPack.totalLaps
        if self.Lap_all != LapAll:
            self.Lap_all = LapAll

    def Packet_CarDamageData_Process(self, dataPack):
        for i, data in enumerate(dataPack.CarDamageData[dataPack.header.playerCarIndex].tyresWear):
            self.Set_Text.emit(F"Wear_{i + 1}", F"{int(data)}%")

    def LapDataPart(self, DataPack):
        self.CurrentLapTime(DataPack)
        self.Current_Lap(DataPack)

    def CurrentLapTime(self, DataPack):
        CurrentLapTime = datetime.datetime.utcfromtimestamp(
            DataPack.lapData[DataPack.header.playerCarIndex].currentLapTime/1000.0)

        CurrentLapTime_hour = F"{CurrentLapTime.hour}:" if CurrentLapTime.hour >= 10 else F"0{CurrentLapTime.hour}:" if CurrentLapTime.hour != 0 else ""
        CurrentLapTime_minute = F"{CurrentLapTime.minute}:" if CurrentLapTime.minute >= 10 else F"0{CurrentLapTime.minute}:" if CurrentLapTime.minute != 0 or CurrentLapTime.hour != 0 else ""
        CurrentLapTime_second = F"{CurrentLapTime.second}." if CurrentLapTime.second >= 10 else F"0{CurrentLapTime.second}."
        CurrentLapTime_microsecond = F"{str(CurrentLapTime.microsecond)[0:3]}"
        self.Set_Text.emit("CurrentLapTime",
                           F"{CurrentLapTime_hour}{CurrentLapTime_minute}{CurrentLapTime_second}{CurrentLapTime_microsecond}")

    def Current_Lap(self, DataPack):
        Lap = DataPack.lapData[DataPack.header.playerCarIndex].currentLapNum
        if Lap != self.Lap_count:
            self.Set_Text.emit("round", F"{Lap}/{self.Lap_all}")
            self.Lap_count = Lap


    def CarTelemetryDataPart(self, DataPack):
        self.Gear_Process(DataPack)
        self.LEDbar_Process(DataPack)
        self.Drs(DataPack)
        self.Set_Text.emit("RPM", F"{DataPack.carTelemetryData[DataPack.header.playerCarIndex].engineRPM}")
        self.Set_Text.emit("Soeed",F"{DataPack.carTelemetryData[DataPack.header.playerCarIndex].speed}")

        for i in range(0, 4):
           self.Set_Text.emit(F"TyresSurfaceTemperature_{i + 1}",
                              F"{DataPack.carTelemetryData[DataPack.header.playerCarIndex].tyresInnerTemperature[i]}'C")

    def Drs(self, DataPack):
        drs_situation = DataPack.carTelemetryData[DataPack.header.playerCarIndex].drs
        self.drs_toggle = True if drs_situation else False
        
        if self.drs_toggle:
            self.Set_StyleSheet.emit("Drs_led", "color: rgb(255, 255, 255);background-color: rgb(0, 255, 0);")

    def Gear_Process(self, DataPack):
        Gear = DataPack.carTelemetryData[DataPack.header.playerCarIndex].gear
        Gear = F"{Gear}" if DataPack.carTelemetryData[
                                      DataPack.header.playerCarIndex].gear > 0 else "N" if Gear != -1 else "R"
        self.Set_Text.emit("Gear", Gear)

    def LEDbar_Process(self, DataPack):
        self.LED_bar = int(DataPack.carTelemetryData[DataPack.header.playerCarIndex].revLightsPercent)
        self.LED_bar = int(self.map(self.LED_bar, 0, 100, 0, 8))

        if self.LED_bar > 4:
          self.Set_StyleSheet.emit("Gear", "color: rgb(255,0,0);")
        else:
          self.Set_StyleSheet.emit("Gear", "color: rgb(255,255,255);")
        try:
            self.mainWindow.L.wr(self.LED_bar)
        except:
            pass

    def Ers(self, DataPack):
        ersDeployMode_num = DataPack.carStatusData[DataPack.header.playerCarIndex].ersDeployMode
        self.Set_Text.emit("RES_Mode", F"{self.ersDeployMode_text[ersDeployMode_num]}")
        self.Set_StyleSheet.emit("RES_Mode", self.ersDeployMode_styleheet[ersDeployMode_num])

        ErsNow = int(self.map(DataPack.carStatusData[DataPack.header.playerCarIndex].ersStoreEnergy, 0, 4000000, 0, 100))
        ersStoreEnergy_img = self.ersStoreEnergy_bar.scaled(int(
            self.map(ErsNow, 0, 100, 0, 279)), 20)

        ErsDeployedNow = int(
            self.map(DataPack.carStatusData[DataPack.header.playerCarIndex].ersDeployedThisLap, 0, 4000000, 0, 100))
        ersDeployed_img = self.ersStoreEnergy_bar.scaled(279-int(
            self.map(ErsDeployedNow, 0, 100, 0, 279)), 20)

        ersStoreEnergy_img.fill(QtGui.QColor(255, int(self.map(ErsNow, 0, 100, 0, 255)), 0))
        # self.Set_StyleSheet.emit("ERS_Store",
        #                              F"color: rgb(255,{255-int(self.map(ErsNow, 0, 10, 0, 255))},0);")
        self.Set_Pixmap.emit("ERS_Store", ersStoreEnergy_img)
        self.Set_Pixmap.emit("ERS_Deploted", ersDeployed_img)

    def Drs_Available(self, DataPack):
        drs_allowed = DataPack.carStatusData[DataPack.header.playerCarIndex].drsAllowed
        if (not self.drs_toggle) and (drs_allowed == 1):
            self.Set_StyleSheet.emit("Drs_led", "color: rgb(255, 255, 255);background-color: rgb(255, 0, 0);")
        elif (not self.drs_toggle) and (drs_allowed == 0):
            self.Set_StyleSheet.emit("Drs_led", "color: rgb(255, 255, 255);background-color: rgb(0, 0, 0);")


    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
