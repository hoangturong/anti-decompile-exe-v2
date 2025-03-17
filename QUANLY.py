import antii
antii.protect()
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QTabWidget, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QDialog, QDialogButtonBox, QComboBox, QGridLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QFont, QIcon
import requests

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cài Đặt")
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #2c3e50;")

        layout = QGridLayout()
        
        # Chọn màu nền
        color_label = QLabel("Chọn màu nền:")
        color_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(color_label, 0, 0)
        
        self.color_combo = QComboBox()
        self.color_combo.addItems(["#f5f7fa", "#e0e0e0", "#d5f5e3", "#f5e6cc"])
        self.color_combo.setStyleSheet("color: #2c3e50; background-color: #ecf0f1; padding: 5px; border-radius: 5px;")
        layout.addWidget(self.color_combo, 0, 1)
        
        # Chọn kích thước
        size_label = QLabel("Chọn kích thước:")
        size_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(size_label, 1, 0)
        
        self.size_combo = QComboBox()
        self.size_combo.addItems(["800x600", "1000x700", "1200x800"])
        self.size_combo.setStyleSheet("color: #2c3e50; background-color: #ecf0f1; padding: 5px; border-radius: 5px;")
        layout.addWidget(self.size_combo, 1, 1)
        
        # Nút OK và Apply
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Apply)
        button_box.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        button_box.accepted.connect(self.accept)
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_settings)
        layout.addWidget(button_box, 2, 0, 1, 2)
        
        self.setLayout(layout)
        self.parent = parent

    def apply_settings(self):
        color = self.color_combo.currentText()
        size = self.size_combo.currentText()
        width, height = map(int, size.split("x"))
        self.parent.setStyleSheet(f"background-color: {color};")
        self.parent.setGeometry(100, 100, width, height)

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hướng Dẫn Sử Dụng")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #2c3e50;")

        layout = QVBoxLayout()
        
        # Hướng dẫn sử dụng
        guide_label = QLabel("""
        <h3>Hướng Dẫn Sử Dụng App Quản Lý</h3>
        <p><strong>1. Trình Duyệt:</strong> Mở trang web mặc định.</p>
        <p><strong>2. Check Key:</strong> 
        <p>- Nhập Key và (tùy chọn) IP.</p>
        <p>- Nhấn "Check Key" để kiểm tra.</p>
        <p>- Nếu có IP thì check key cho ip đó.</p>
        <p>- Nếu không có IP, check key cho ip chính bản thân.</p>
        <p>- Kết quả hiển thị trạng thái key và IP.</p>
        <p><strong>3. Check IP:</strong> Hiển thị trang web kiểm tra IP .</p>
        <p><strong>4. Cài Đặt:</strong> Chọn màu nền và kích thước cửa sổ.</p>
        <p><strong>5. Trợ Giúp:</strong> Xem hướng dẫn này.</p>
        <p><strong>API</strong></p>
        <p>- Check key theo ip: https://vantrong.x10.mx/keyip/checkkey.php?ip={ip}&key={key}</p>
        <p>- Check ip: https://vantrong.x10.mx/keyip/?ip</p>
        <p>-Check key ko cần ip, nó tự gét ip: https://vantrong.x10.mx/keyip/?key={key}</p>
        """)
        guide_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        guide_label.setWordWrap(True)
        layout.addWidget(guide_label)
        
        # Nút OK
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

class IPDialog(QDialog):
    def __init__(self, ip, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Địa chỉ IP của bạn")
        self.setFixedSize(300, 150)
        self.setStyleSheet("background-color: #2c3e50;")

        layout = QVBoxLayout()
        
        # Hiển thị IP
        ip_label = QLabel(f"Địa chỉ IP của bạn:\n{ip}")
        ip_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(ip_label)
        
        # Nút Sao chép
        copy_button = QPushButton("Sao chép")
        copy_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #219653;
            
            }
        """)
        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(ip))
        layout.addWidget(copy_button)
        
        # Nút OK
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        
        self.setLayout(layout)

class WebApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QUẢN LÝ")
        self.setWindowIcon(QIcon("app.ico"))
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #f5f7fa;")  # Màu nền mặc định
        
        # Tắt menu bar mặc định của hệ điều hành (nếu có)
        self.setMenuBar(None)
        
        # Tạo widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Thanh menu bên trái
        self.menu = QVBoxLayout()
        self.menu_frame = QFrame()
        self.menu_frame.setStyleSheet("""
            background-color: #1e2a38; 
            border-radius: 15px; 
            padding: 20px;
        """)
        self.menu_frame.setLayout(self.menu)
        self.menu.setSpacing(15)
        
        # Các nút menu
        self.browser_button = QPushButton("🌍 Trình Duyệt")
        self.check_key_button = QPushButton("🔑 Check Key")
        self.check_ip_button = QPushButton("📡 Check IP")
        self.settings_button = QPushButton("⚙️ Cài Đặt")
        self.help_button = QPushButton("❓ Trợ Giúp")
        
        for btn in [self.browser_button, self.check_key_button, self.check_ip_button, self.settings_button, self.help_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #34495e; 
                    color: #ecf0f1; 
                    padding: 12px; 
                    border-radius: 8px; 
                    font-size: 14px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #4a6a8a;
                    color: #ffffff;
                }
                QPushButton:pressed {
                    background-color: #2c3e50;
                }
            """)
            btn.setFont(QFont("Arial", 12))
            self.menu.addWidget(btn)
        
        self.menu.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addWidget(self.menu_frame, 2)
        
        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                background-color: #ffffff; 
                border-radius: 15px; 
                padding: 10px;
            }
            QTabBar::tab {
                background-color: #d5dbde; 
                color: #2c3e50; 
                padding: 10px 20px; 
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff; 
                color: #3498db;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #e8ecef;
            }
        """)
        main_layout.addWidget(self.tabs, 5)
        
        # Tab Trình Duyệt
        self.browser_tab = QWidget()
        self.browser_layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://vantrong.x10.mx/keyip/?key=vantrongdeptrai"))
        self.browser_layout.addWidget(self.browser)
        self.browser_tab.setLayout(self.browser_layout)
        self.tabs.addTab(self.browser_tab, "🌍 Trình Duyệt")
        
        # Tab Check Key
        self.check_key_tab = QWidget()
        self.check_key_layout = QVBoxLayout()
        
        # Tiêu đề Check Key
        self.check_key_label = QLabel("Check Key")
        self.check_key_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.check_key_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        self.check_key_layout.addWidget(self.check_key_label)
        
        # Ô nhập Key
        self.key_input_label = QLabel("Key:")
        self.key_input_label.setFont(QFont("Arial", 12))
        self.key_input_label.setStyleSheet("color: #2c3e50;")
        self.check_key_layout.addWidget(self.key_input_label)
        
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Nhập key của bạn")
        self.key_input.setStyleSheet("""
            padding: 10px; 
            border: 2px solid #d5dbde; 
            border-radius: 8px; 
            font-size: 14px;
            background-color: #ffffff;
            color: #000000; /* Đổi màu chữ thành đen */
        """)
        self.check_key_layout.addWidget(self.key_input)
        
        # Ô nhập IP
        self.ip_input_label = QLabel("IP:")
        self.ip_input_label.setFont(QFont("Arial", 12))
        self.ip_input_label.setStyleSheet("color: #2c3e50;")
        self.check_key_layout.addWidget(self.ip_input_label)
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Nhập IP của bạn (tùy chọn)")
        self.ip_input.setStyleSheet("""
            padding: 10px; 
            border: 2px solid #d5dbde; 
            border-radius: 8px; 
            font-size: 14px;
            background-color: #ffffff;
            color: #000000; /* Đổi màu chữ thành đen */
        """)
        self.check_key_layout.addWidget(self.ip_input)
        
        # Nút Check Key
        self.check_button = QPushButton("🔍 Check Key")
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db; 
                color: white; 
                padding: 12px; 
                border-radius: 8px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f6390;
            }
        """)
        self.check_button.clicked.connect(self.check_key)
        self.check_key_layout.addWidget(self.check_button)
        
        # Label kết quả
        self.result_label = QLabel("Nhập key và nhấn Check")
        self.result_label.setFont(QFont("Arial", 12))
        self.result_label.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        self.check_key_layout.addWidget(self.result_label)
        
        self.check_key_layout.addStretch()
        self.check_key_tab.setLayout(self.check_key_layout)
        self.tabs.addTab(self.check_key_tab, "🔑 Check Key")
        
        # Tab Check IP
        self.check_ip_tab = QWidget()
        self.check_ip_layout = QVBoxLayout()
        self.check_ip_browser = QWebEngineView()
        self.check_ip_browser.setUrl(QUrl("https://vantrong.x10.mx/keyip/"))
        self.check_ip_layout.addWidget(self.check_ip_browser)
        self.check_ip_tab.setLayout(self.check_ip_layout)
        self.tabs.addTab(self.check_ip_tab, "📡 Check IP")
        
        # Kết nối các nút menu với tab
        self.browser_button.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        self.check_key_button.clicked.connect(lambda: self.tabs.setCurrentIndex(1))
        self.check_ip_button.clicked.connect(lambda: self.tabs.setCurrentIndex(2))
        self.settings_button.clicked.connect(self.show_settings)
        self.help_button.clicked.connect(self.show_help)
        
        # Lấy IP của máy
        self.get_local_ip()

    def check_key(self):
        key = self.key_input.text().strip()
        ip = self.ip_input.text().strip()
        
        if not key:
            self.result_label.setText("⚠️ Vui lòng nhập key!")
            self.result_label.setStyleSheet("color: #e67e22; margin-top: 10px;")
            return
        
        # Nếu có nhập IP, dùng API mới
        if ip:
            url = f"https://vantrong.x10.mx/keyip/checkkey.php?ip={ip}&key={key}"
        else:
            url = f"https://vantrong.x10.mx/keyip/?key={key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            data = response.json()
            
            if data.get("status"):
                ip_text = f"IP của bạn: {ip}" if ip else f"IP của bạn: {self.local_ip}"
                self.result_label.setText(f"✅ Key hợp lệ!\n{ip_text}")
                self.result_label.setStyleSheet("color: #27ae60; margin-top: 10px;")
            else:
                ip_text = f"IP của bạn: {ip}" if ip else f"IP của bạn: {self.local_ip}"
                self.result_label.setText(f"❌ Key không hợp lệ!\n{ip_text}")
                self.result_label.setStyleSheet("color: #c0392b; margin-top: 10px;")
        except requests.exceptions.RequestException as e:
            self.result_label.setText("⚠️ Lỗi kết nối! Vui lòng kiểm tra mạng.")
            self.result_label.setStyleSheet("color: #e67e22; margin-top: 10px;")
        except ValueError:
            self.result_label.setText("⚠️ Lỗi định dạng dữ liệu từ server!")
            self.result_label.setStyleSheet("color: #e67e22; margin-top: 10px;")

    def get_local_ip(self):
        # Lấy IP của máy
        try:
            response = requests.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            data = response.json()
            self.local_ip = data.get("ip", "Không xác định")
        except requests.exceptions.RequestException:
            self.local_ip = "Không xác định"
        
        # Hiển thị dialog IP
        self.show_ip_dialog()

    def show_ip_dialog(self):
        dialog = IPDialog(self.local_ip, self)
        dialog.exec()

    def show_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def show_help(self):
        dialog = HelpDialog(self)
        dialog.exec()

if __name__ == "__main__":
    #hide_console()
    app = QApplication(sys.argv)
    window = WebApp()
    window.show()
    sys.exit(app.exec())