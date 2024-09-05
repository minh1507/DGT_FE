from pathlib import Path
from PySide6 import QtWidgets


class SystemUtil:
    @staticmethod
    def get_image_path(image_name):
        base_dir = Path(__file__).resolve().parent
        image_dir = base_dir / ".." / "asset" / "image"
        return str(image_dir / image_name)

    @staticmethod
    def minimize_window():
        widget = QtWidgets.QApplication.activeWindow()
        if widget:
            widget.showMinimized()

    @staticmethod
    def close_window():
        widget = QtWidgets.QApplication.activeWindow()
        if widget:
            widget.close()
