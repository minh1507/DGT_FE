import sys
from PySide6 import QtWidgets

from view.main.Login_View import Login_View

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    login = Login_View()
    login.show()

    sys.exit(app.exec())
