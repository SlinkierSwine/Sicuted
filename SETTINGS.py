from PyQt5.QtWidgets import QMessageBox

HOME_URL = "http://www.google.com"
APP_ID = u'Sicuted.1.0'
WINDOW_SIZE = 500, 250, 800, 600


def create_error_msg(e):
    """
    Creates error QMessageBox
    :param e: Exception
    """
    er = QMessageBox()
    er.setWindowTitle('Error')
    er.setIcon(QMessageBox.Critical)
    er.setText(str(e))
    er.exec()