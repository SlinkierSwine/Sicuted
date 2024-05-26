from typing import Optional
from PyQt5 import QtWidgets
import requests
from PyQt5.QtCore import Qt
import SETTINGS


class DownloadFromServerWidget(QtWidgets.QWidget):
    get_all_files_url = SETTINGS.FILE_SERVER_URL + "list_files.php"
    download_file_url = SETTINGS.FILE_SERVER_URL + "download.php"

    def __init__(self, main_window: QtWidgets.QMainWindow) -> None:
        super().__init__()

        self.setWindowTitle('Download from server')
        self.setFixedSize(*SETTINGS.DOWNLOAD_FROM_SERVER_WINDOW_SIZE)
        self.move(500, 250)
        self.setWindowModality(Qt.ApplicationModal)

        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)

        self.prev_dirs = []


    def get_files_in_dir(self, dir: Optional[str] = None) -> dict[str, str]:
        params = {"dir": dir} if dir is not None else dict()
        res = requests.get(self.get_all_files_url, params=params)

        if res.status_code != 200:
            raise Exception(f"Something is wrong. Status code: {res.status_code}")

        return res.json()

    def show(self) -> None:
        super().show()

        try:
            self.change_dir()
        except Exception as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage(str(e))
            self.hide()

    def change_dir(self, directory: Optional[str] = None, back: bool = False) -> None:
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().setParent(None)

        try:
            files = self.get_files_in_dir(directory)
        except Exception as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage(str(e))
            self.hide()
            return

        back_btn = None

        if back:
            self.prev_dirs.pop(-1)

        if self.prev_dirs or directory:
            back_btn = QtWidgets.QPushButton()
            back_btn.setText("Back")
            prev_dir = self.prev_dirs[-1] if self.prev_dirs else None
            back_btn.clicked.connect(lambda: self.change_dir(prev_dir, back=True))

        if directory:
            self.prev_dirs.append(directory)

        for dir in files["directories"]:
            btn = QtWidgets.QPushButton()
            btn.setText(dir)
            btn.clicked.connect(lambda: self.change_dir(dir))
            self.layout.addWidget(btn)

        for file in files["files"]:
            btn = QtWidgets.QPushButton()
            btn.setText(file)

            prev_path = "/".join(self.prev_dirs)
            path = prev_path + f"/{file}" if prev_path else file

            btn.clicked.connect(lambda: self.download_file(path))
            self.layout.addWidget(btn)

        if back_btn:
            self.layout.addWidget(back_btn)

    def download_file(self, path: str) -> None:
        params = {"file": path}
        res = requests.get(self.download_file_url, params=params)

        if res.status_code == 200:
            self.main_window.new_file_with_text(path, res.text)
            self.prev_dirs = []
            self.hide()
