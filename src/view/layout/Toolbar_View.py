from PySide6 import QtCore, QtWidgets, QtGui

from util.Theme_Util import ThemeUtil
from util.System_Util import SystemUtil
from common.const.Global_Const import Global_Const

from Translator import Translator


class Toolbar_View:
    def __init__(self, login_window):
        self.translator = Translator()
        self.login_window = login_window

    def logout(self):
        if self.login_window.main_window is not None:
            self.login_window.main_window.close()

        self.login_window.show_again()

    def main(self):
        toolbarWidget = QtWidgets.QWidget()
        toolbarWidget.setStyleSheet("background-color: #292929;")

        toolbar = QtWidgets.QHBoxLayout(toolbarWidget)
        toolbar.setContentsMargins(10, 10, 10, 10)

        toolbar.addStretch()

        profile_image_label = QtWidgets.QLabel()
        profile_image_label.setFixedSize(40, 40)
        profile_image_label.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        pixmap = QtGui.QPixmap(SystemUtil.get_image_path("profile.png"))
        scaled_pixmap = pixmap.scaled(
            40,
            40,
            QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            QtCore.Qt.TransformationMode.SmoothTransformation,
        )

        mask = QtGui.QPixmap(40, 40)
        mask.fill(QtCore.Qt.transparent)
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, 40, 40)
        painter = QtGui.QPainter(mask)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        painter.setBrush(QtCore.Qt.black)
        painter.drawPath(path)
        painter.end()

        rounded_pixmap = QtGui.QPixmap(40, 40)
        rounded_pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(rounded_pixmap)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.end()

        profile_image_label.setPixmap(rounded_pixmap)

        profile_menu = QtWidgets.QMenu()
        ThemeUtil.get(parent=profile_menu, name_file=Global_Const.Theme.MENU_THEME)

        system_menu = QtWidgets.QMenu(self.translator.menu_t("system"))
        ThemeUtil.get(parent=system_menu, name_file=Global_Const.Theme.MENU_THEME)

        minimize_action = system_menu.addAction(self.translator.menu_t("minimize"))
        minimize_action.triggered.connect(SystemUtil.minimize_window)

        exit_action = system_menu.addAction(self.translator.menu_t("exit"))
        exit_action.triggered.connect(SystemUtil.close_window)

        profile_menu.addMenu(system_menu)

        logout_action = profile_menu.addAction(self.translator.menu_t("logout"))

        def test_logout():
            self.logout()

        logout_action.triggered.connect(test_logout)

        def open_profile_menu(event):
            profile_menu.exec(event.globalPosition().toPoint())

        profile_image_label.mousePressEvent = open_profile_menu

        toolbar.addWidget(profile_image_label)

        return toolbarWidget
