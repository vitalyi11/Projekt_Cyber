import sys
import subprocess
import platform
import re
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QTabWidget, QTextEdit, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QTimer, QProcess
from PyQt5.QtGui import QIcon

class WifiScanner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle("Narzędzia sieci")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Dodanie widgetu z zakładkami
        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        # Zakładka Skaner WiFi
        self.wifi_tab = QWidget()
        self.tab_widget.addTab(self.wifi_tab, "Skaner WiFi")
        self.wifi_layout = QVBoxLayout(self.wifi_tab)

        self.wifi_table = QTableWidget()
        self.wifi_table.setColumnCount(4)
        self.wifi_table.setHorizontalHeaderLabels(["SSID", "Kanał", "Częstotliwość (GHz)", "Siła sygnału (dBm)"])
        self.wifi_table.horizontalHeader().setStretchLastSection(True)
        self.wifi_layout.addWidget(self.wifi_table)

        self.scan_button = QPushButton("Skanuj sieci WiFi")
        self.scan_button.clicked.connect(self.scan_wifi)
        self.wifi_layout.addWidget(self.scan_button)

        self.timer = QTimer()
        self.timer.timeout.connect(self.scan_wifi)
        self.timer.start(10000)

        self.traceroute_tab = QWidget()
        self.tab_widget.addTab(self.traceroute_tab, "Traceroute")
        self.traceroute_layout = QVBoxLayout(self.traceroute_tab)

        self.traceroute_label = QLabel("Adres docelowy:")
        self.traceroute_layout.addWidget(self.traceroute_label)

        self.traceroute_input = QLineEdit()
        self.traceroute_input.returnPressed.connect(self.run_traceroute)
        self.traceroute_layout.addWidget(self.traceroute_input)

        self.traceroute_button = QPushButton("Uruchom Traceroute")
        self.traceroute_button.clicked.connect(self.run_traceroute)
        self.traceroute_layout.addWidget(self.traceroute_button)

        self.traceroute_output = QTextEdit()
        self.traceroute_output.setReadOnly(True)
        self.traceroute_layout.addWidget(self.traceroute_output)

        self.ping_tab = QWidget()
        self.tab_widget.addTab(self.ping_tab, "Ping")
        self.ping_layout = QVBoxLayout(self.ping_tab)

        self.ping_label = QLabel("Adres docelowy:")
        self.ping_layout.addWidget(self.ping_label)

        self.ping_input = QLineEdit()
        self.ping_input.returnPressed.connect(self.run_ping)
        self.ping_layout.addWidget(self.ping_input)

        self.ping_button = QPushButton("Uruchom Ping")
        self.ping_button.clicked.connect(self.run_ping)
        self.ping_layout.addWidget(self.ping_button)

        self.ping_output = QTextEdit()
        self.ping_output.setReadOnly(True)
        self.ping_layout.addWidget(self.ping_output)

        self.netstat_tab = QWidget()
        self.tab_widget.addTab(self.netstat_tab, "Netstat")
        self.netstat_layout = QVBoxLayout(self.netstat_tab)
        
        self.netstat_button = QPushButton("Wyświetl Netstat")
        self.netstat_button.clicked.connect(self.run_netstat)
        self.netstat_layout.addWidget(self.netstat_button)

        self.netstat_output = QTextEdit()
        self.netstat_output.setReadOnly(True)
        self.netstat_layout.addWidget(self.netstat_output)
        
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        self.process.finished.connect(self.process_finished)
        self.current_tab = ""



    def scan_wifi(self):
        self.current_tab = "wifi" 
        self.wifi_table.setRowCount(0)
        networks = self.get_wifi_networks()

        for i, network in enumerate(networks):
            self.wifi_table.insertRow(i)
            for j, value in enumerate(network):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.wifi_table.setItem(i, j, item)

    def get_wifi_networks(self):
        networks = []
        os_name = platform.system()

        try:
            if os_name == "Windows":
                output = subprocess.check_output(["netsh", "wlan", "show", "networks", "mode=Bssid"], encoding='utf-8', errors='ignore')
                
                current_ssid = None
                current_data = {"channel": "N/A", "frequency": "N/A", "signal": "N/A"}
                
                for line in output.split('\n'):
                    line = line.strip()
                    
                    if "SSID" in line and "BSSID" not in line:
                        if current_ssid:
                            networks.append([
                                current_ssid,
                                current_data["channel"],
                                current_data["frequency"],
                                current_data["signal"]
                            ])
                        
                        ssid_match = re.search(r'SSID \d+ : (.+)', line)
                        if ssid_match:
                            current_ssid = ssid_match.group(1).strip()
                            current_data = {"channel": "N/A", "frequency": "N/A", "signal": "N/A"}

                    if "Channel" in line or "Kanał" in line:
                        channel_match = re.search(r': (\d+)', line)
                        if channel_match:
                            channel = channel_match.group(1)
                            current_data["channel"] = channel
                            if int(channel) <= 14:
                                current_data["frequency"] = "2.4"
                            else:
                                current_data["frequency"] = "5"
                    
                    if "Signal" in line or "Sygnał" in line:
                        signal_match = re.search(r': (\d+)%', line)
                        if signal_match:
                            signal_percent = int(signal_match.group(1))
                            signal_dbm = -100 + (signal_percent / 2)
                            current_data["signal"] = f"{int(signal_dbm)}"
                
                if current_ssid:
                    networks.append([
                        current_ssid,
                        current_data["channel"],
                        current_data["frequency"],
                        current_data["signal"]
                    ])
        except Exception as e:
            print(f"Błąd podczas skanowania: {e}")
            
        return networks   

    def run_traceroute(self):
        self.current_tab = "traceroute"
        target = self.traceroute_input.text()
        if not target:
            return

        self.traceroute_output.clear()
        self.traceroute_output.append(f"Tracing route to {target}...\n")
        command = ["tracert", target]
        self.process.start(command[0], command[1:])

    def run_ping(self):
        self.current_tab = "ping"
        target = self.ping_input.text()
        if not target:
            return

        self.ping_output.clear()
        self.ping_output.append(f"Ping do {target}...\n")
        command = ["ping", target]
        self.process.start(command[0], command[1:])

    def run_netstat(self):
        self.current_tab = "netstat"
        self.netstat_output.clear()
        self.netstat_output.append("Running netstat...\n")
        command = ["netstat", "-a", "-n", "-o"]
        self.process.start(command[0], command[1:])

    def handle_output(self):
        if self.current_tab == "traceroute":
            data = self.process.readAllStandardOutput().data().decode(errors='ignore')
            self.traceroute_output.append(data)
        elif self.current_tab == "netstat":
            data = self.process.readAllStandardOutput().data().decode(errors='ignore')
            self.netstat_output.append(data)
        elif self.current_tab == "ping":
            data = self.process.readAllStandardOutput().data().decode(errors='ignore')
            self.ping_output.append(data)
            

    def handle_error(self):
         if self.current_tab == "traceroute":
            data = self.process.readAllStandardError().data().decode(errors='ignore')
            self.traceroute_output.append(data)
         elif self.current_tab == "netstat":
            data = self.process.readAllStandardError().data().decode(errors='ignore')
            self.netstat_output.append(data)
         elif self.current_tab == "ping":
            data = self.process.readAllStandardError().data().decode(errors='ignore')
            self.ping_output.append(data)

    def process_finished(self):
        if self.current_tab == "traceroute":
            self.traceroute_output.append("Traceroute completed.")
        elif self.current_tab == "netstat":
            self.netstat_output.append("Netstat completed.")
        elif self.current_tab == "ping":
            self.ping_output.append("Ping completed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WifiScanner()
    window.show()
    sys.exit(app.exec_())