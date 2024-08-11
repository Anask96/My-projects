from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from test import Ui_Form
from shared import DataStorage, pause_event, stop_event
import sys
import threading


class window(QtWidgets.QMainWindow):

    headers = DataStorage.headers_gui
    num_alarms = 0

    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_table_data)
        self.timer.timeout.connect(self.update_rssi_table)
        self.timer.timeout.connect(self.display_total)
        self.timer.timeout.connect(self.display_seen)
        self.timer.timeout.connect(self.display_message)
        self.timer.timeout.connect(self.display_alarms)
        self.timer.start(500)  # Interval in milliseconds (500ms)

        self.ui.Download.clicked.connect(self.download_csv)
        self.ui.Reset.clicked.connect(self.reset_group_table)
        self.ui.Pause.clicked.connect(self.pause_data_read)

    def download_csv(self):
        DataStorage.download_data()

    def reset_group_table(self):
        DataStorage.reset_group()
        self.loadGroupTokens(DataStorage.group)

    def pause_data_read(self):
        if not pause_event.is_set():
            pause_event.set()
        else: 
            pause_event.clear()

    def display_seen(self):
        self.ui.currently_seen.display(str(DataStorage.get_total_group_tokens()))

    def display_total(self):
        self.ui.total_seen.display(str(DataStorage.get_total_tokens()))

    def display_message(self):
        if not DataStorage.output_buffer.empty():
            current_text = self.ui.messages.toPlainText()
            message = DataStorage.output_buffer.get()
            new_text = f"{message}\n{current_text}"
            self.ui.messages.setPlainText(new_text)

    def display_alarms(self):
        self.ui.alarms.clear()
        with DataStorage.Lock_alarm:
            for alarm, value in DataStorage.alarm.items():
                self.ui.alarms.append(value)
            

    def loadHighestRssi(self, GroupTokens):
        with DataStorage.lock_group:
            self.ui.Highest_rssi.setRowCount(1)

        self.ui.Highest_rssi.setColumnCount(6)
        self.ui.Highest_rssi.setHorizontalHeaderLabels(self.headers)     #headers
        self.ui.Highest_rssi.setColumnWidth(0, 100)
        self.ui.Highest_rssi.setColumnWidth(1, 100)
        self.ui.Highest_rssi.setColumnWidth(2, 220)
        self.ui.Highest_rssi.setColumnWidth(3, 220)
        self.ui.Highest_rssi.setColumnWidth(4, 110)
        self.ui.Highest_rssi.setColumnWidth(5, 134)

        highest_rssi_token = ""
        highest_rssi = 0
        with DataStorage.lock_group:
            for token, values in GroupTokens.items():
                rssi = int(values[6])
                if rssi > highest_rssi:
                    highest_rssi = rssi
                    highest_rssi_token = token


        if highest_rssi != 0:
            self.ui.Highest_rssi.setItem(0,0, QTableWidgetItem(str(highest_rssi_token)))          #Row
            self.ui.Highest_rssi.setItem(0,1, QTableWidgetItem(str(GroupTokens[highest_rssi_token][0])))  
            self.ui.Highest_rssi.setItem(0,2, QTableWidgetItem(str(GroupTokens[highest_rssi_token][1]))) 
            self.ui.Highest_rssi.setItem(0,3, QTableWidgetItem(str(GroupTokens[highest_rssi_token][2]))) 
            self.ui.Highest_rssi.setItem(0,4, QTableWidgetItem(str(GroupTokens[highest_rssi_token][3]))) 
            self.ui.Highest_rssi.setItem(0,5, QTableWidgetItem(str(GroupTokens[highest_rssi_token][5])))

        


    def loadGroupTokens(self, GroupTokens):
        with DataStorage.lock_group:
            self.ui.group_tokens.setRowCount(len(GroupTokens))   # Use this based on the data in group

        self.ui.group_tokens.setColumnCount(6)
        self.ui.group_tokens.setHorizontalHeaderLabels(self.headers)     #headers
        self.ui.group_tokens.setColumnWidth(0, 100)
        self.ui.group_tokens.setColumnWidth(1, 100)
        self.ui.group_tokens.setColumnWidth(2, 220)
        self.ui.group_tokens.setColumnWidth(3, 220)
        self.ui.group_tokens.setColumnWidth(4, 110)
        self.ui.group_tokens.setColumnWidth(5, 134)
        
        row_index = 0
        with DataStorage.lock_group:
            for token, values in GroupTokens.items():
                self.ui.group_tokens.setItem(row_index,0, QTableWidgetItem(str(token)))          #Row
                self.ui.group_tokens.setItem(row_index,1, QTableWidgetItem(str(values[0])))  
                self.ui.group_tokens.setItem(row_index,2, QTableWidgetItem(str(values[1]))) 
                self.ui.group_tokens.setItem(row_index,3, QTableWidgetItem(str(values[2]))) 
                self.ui.group_tokens.setItem(row_index,4, QTableWidgetItem(str(values[3]))) 
                self.ui.group_tokens.setItem(row_index,5, QTableWidgetItem(str(values[5])))
                row_index += 1

    def update_rssi_table(self):
        self.loadHighestRssi(DataStorage.group)

    def update_table_data(self):
        self.loadGroupTokens(DataStorage.group)
        
Lock_ui = threading.Lock()
app = QtWidgets.QApplication(sys.argv)
win = window()

def create_app():
    win.show()
    sys.exit(app.exec_())