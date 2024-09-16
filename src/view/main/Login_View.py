from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from view.main.Main_View import MainView


class Login_View(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.main_window = None
        self.setWindowTitle("Login")
        self.setFixedSize(400, 350)
        self.setWindowIcon(QtGui.QIcon('./src/asset/image/logo.png'))

        # Set a dark background color for the widget
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
        """)

        # Set the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Title Label
        title_label = QtWidgets.QLabel("Login", self)
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ecf0f1;
        """)
        layout.addWidget(title_label)

        # Username input
        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("""
            padding: 12px;
            font-size: 16px;
            border: 1px solid #7f8c8d;
            border-radius: 5px;
            background-color: #34495e;
            color: #ecf0f1;
        """)
        layout.addWidget(self.username)

        # Password input
        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("""
            padding: 12px;
            font-size: 16px;
            border: 1px solid #7f8c8d;
            border-radius: 5px;
            background-color: #34495e;
            color: #ecf0f1;
        """)
        layout.addWidget(self.password)

        # Show password checkbox
        self.show_password_checkbox = QtWidgets.QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #ecf0f1;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 12px;
                height: 12px;
                border: 1px solid #3498db;
                background-color: #ecf0f1;
            }
            QCheckBox::indicator:unchecked {
                background-color: #ecf0f1;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db;
            }
            QCheckBox::indicator:checked:pressed {
                background-color: #2980b9;
            }
        """)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        # Login button
        self.login_button = QtWidgets.QPushButton("Login", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                font-size: 14px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        # Stretch to push widgets upwards
        layout.addStretch()

        # Center the window on the screen
        self.center_on_screen()

    def center_on_screen(self):
        frame_geom = self.frameGeometry()
        screen_center = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        frame_geom.moveCenter(screen_center)
        self.move(frame_geom.topLeft())

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def check_login(self):
        if not self.username.text() or not self.password.text():
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        if self.username.text() == "user" and self.password.text() == "password":
            self.accept_login()
        else:
            QtWidgets.QMessageBox.warning(self, "Login Error", "Incorrect username or password.")

    def accept_login(self):
        self.main_window = MainView(self)
        self.main_window.setMinimumSize(800, 690)
        self.main_window.setWindowFlags(Qt.FramelessWindowHint)
        self.main_window.show()
        self.close()

    def show_again(self):
        if self.main_window:
            self.main_window.close()

        self.username.clear()
        self.password.clear()
        self.show_password_checkbox.setChecked(False)
        self.show()
