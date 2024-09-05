from PySide6 import QtWidgets, QtGui
from view.main.Main_View import MainView

class Login_View(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.main_window = None
        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)
        self.setWindowIcon(QtGui.QIcon('path/to/your/icon.png'))

        # Set the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(15)

        # Username input
        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("padding: 10px; font-size: 16px;")

        # Password input
        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setStyleSheet("padding: 10px; font-size: 16px;")

        self.show_password_checkbox = QtWidgets.QCheckBox("Show Password", self)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        self.login_button = QtWidgets.QPushButton("Login", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
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

        self.center_on_screen()

    def center_on_screen(self):
        frame_geom = self.frameGeometry()
        screen_center = QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        frame_geom.moveCenter(screen_center)
        self.move(frame_geom.topLeft())

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)

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

