from PySide6 import QtWidgets

from util.Theme_Util import ThemeUtil
from common.const.Global_Const import Global_Const
from Module import Module

from view.layout.Toolbar_View import Toolbar_View

class MainView(QtWidgets.QWidget):
    def __init__(self, login_window):
        super().__init__()

        ThemeUtil.get(parent=self, name_file=Global_Const.Theme.CORE_THEME)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = Toolbar_View(login_window)
        layout.addWidget(toolbar.main())

        for i in Module.widgets:
            layout.addWidget(i())

        layout.addStretch()
