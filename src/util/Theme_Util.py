import importlib.resources

from common.const.Global_Const import Global_Const


class ThemeUtil:
    @staticmethod
    def get(parent=None, name_file=""):
        theme_file = importlib.resources.files(Global_Const.Path.PATH_1) / name_file

        with theme_file.open("r") as f:
            parent.setStyleSheet(f.read())
