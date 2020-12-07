from modules.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
import ctypes
from SETTINGS import APP_ID


if __name__ == '__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)
    app = QApplication(sys.argv)
    screen = MainWindow()
    screen.show()
    sys.exit(app.exec_())
