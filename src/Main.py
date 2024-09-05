import sys
from PySide6 import QtWidgets, QtGui, QtCore
from view.main.Login_View import Login_View

class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super().__init__()

        self.pixmap = QtGui.QPixmap(600, 400)
        self.draw_splash()

        self.setPixmap(self.pixmap)

    def draw_splash(self):
        painter = QtGui.QPainter(self.pixmap)

        # Draw the background image
        background_pixmap = QtGui.QPixmap("./src/asset/image/background.jpg")
        background_pixmap = background_pixmap.scaled(self.pixmap.size(), QtCore.Qt.IgnoreAspectRatio,
                                                     QtCore.Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, background_pixmap)

        overlay = QtGui.QPixmap(self.pixmap.size())
        overlay.fill(QtGui.QColor(0, 0, 0, 150))
        painter.drawPixmap(0, 0, overlay)

        logo_pixmap = QtGui.QPixmap("./src/asset/image/logo.png")
        logo_pixmap = logo_pixmap.scaled(300, 150, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        logo_rect = QtCore.QRect((self.pixmap.width() - logo_pixmap.width()) // 2, 50, logo_pixmap.width(),
                                 logo_pixmap.height())
        painter.drawPixmap(logo_rect, logo_pixmap)

        font = QtGui.QFont("Helvetica Neue", 20, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))

        painter.end()

    def show_loading_screen(self):
        QtCore.QTimer.singleShot(3000, self.finish_loading)

    def finish_loading(self):
        self.close()

def main():
    app = QtWidgets.QApplication([])

    splash = SplashScreen()
    splash.show()

    splash.show_loading_screen()

    login = Login_View()

    splash.finish_loading = lambda: (splash.close(), login.show())

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
