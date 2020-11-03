from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
from PyQt5.QtWebEngineWidgets import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.columns_n = 1
        with open('./css/styles.css') as ss:
            self.styleshit = ss.read()
        self.setStyleSheet(self.styleshit)
        uic.loadUi('main_window.ui', self)
        self.actionSet_two_columns_layout.triggered.connect(self.two_columns_layout)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.actionOpen_Brouser.triggered.connect(self.open_browser)
        self.tab.installEventFilter(self)

    def open_browser(self):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.tabWidget.addTab(self.browser, 'Browser')

    def two_columns_layout(self):
        if self.columns_n < 2:
            self.right_column = QTabWidget()
            tab = QTextEdit()
            self.right_column.addTab(tab, 'Open file')
            self.horizontalLayout.addWidget(self.right_column)
            self.columns_n += 1
            self.right_column.setTabsClosable(True)
            self.right_column.setDocumentMode(True)
            self.right_column.setMovable(True)
            self.right_column.setTabShape(QTabWidget.Triangular)
            self.right_column.setStyleSheet(self.styleshit)
            tab.setStyleSheet(self.styleshit)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ContextMenu:
            menu = QMenu(self)
            menu.addAction('ad')
            menu.exec_(event.globalPos())
            return True
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())
