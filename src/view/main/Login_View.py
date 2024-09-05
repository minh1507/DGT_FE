from PySide6 import QtWidgets, QtGui, QtCore

from view.main.Main_View import MainView


class Login_View(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.main_window = None
        self.setWindowTitle("Login")
        self.setFixedSize(400, 350)
        self.setWindowIcon(QtGui.QIcon('./src/asset/image/logo.png'))

        # Set the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        self.setStyleSheet("background-color: #ecf0f1;")  # Light background color

        # Title Label
        title_label = QtWidgets.QLabel("Login", self)
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title_label)

        # Username input
        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("""
            padding: 12px;
            font-size: 16px;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: black;
        """)

        # Password input
        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password.setStyleSheet("""
            padding: 12px;
            font-size: 16px;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
            color: black;
        """)

        self.show_password_checkbox = QtWidgets.QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #2c3e50;  /* Text color */
                padding: 5px;    /* Padding around the checkbox */
            }
            QCheckBox::indicator {
                width: 10px; /* Size of the checkbox */
                height: 10px;
                border: 1px solid #3498db; /* Border color */
                background-color: white; /* Background color */
            }
            QCheckBox::indicator:unchecked {
                background-color: white; /* Background color when unchecked */
            }
            QCheckBox::indicator:checked {
                background-color: #3498db; /* Background color when checked */
                border-color: #2980b9; /* Darker border color when checked */
            }
            QCheckBox::indicator:checked:pressed {
                background-color: #2980b9; /* Even darker color when pressed */
                border-color: #1f5a8b; /* Even darker border color when pressed */
            }
        """)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        self.login_button = QtWidgets.QPushButton("Login", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 11px;
                font-size: 14px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.login_button.clicked.connect(self.check_login)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.login_button)

        layout.addStretch()

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
        self.main_window.showFullScreen()
        self.main_window.show()
        self.close()

    def show_again(self):
        if self.main_window:
            self.main_window.close()

        self.username.clear()
        self.password.clear()
        self.show_password_checkbox.setChecked(False)
        self.show()
