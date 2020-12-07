from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QStackedLayout
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from SETTINGS import create_error_msg


class App(QWidget):
    def __init__(self, home_url):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.Toolbar = QWidget()
        self.ToolbarLayout = QHBoxLayout()
        self.addressbar = QLineEdit()

        self.addressbar.returnPressed.connect(self.browse_to)

        self.BackButton = QPushButton("<")
        self.BackButton.clicked.connect(self.go_back)

        self.ForwardButton = QPushButton(">")
        self.ForwardButton.clicked.connect(self.go_forward)

        self.ReloadButton = QPushButton("R")
        self.ReloadButton.clicked.connect(self.reload_page)

        # Toolbar
        self.ToolbarLayout.addWidget(self.BackButton)
        self.ToolbarLayout.addWidget(self.ForwardButton)
        self.ToolbarLayout.addWidget(self.ReloadButton)
        self.Toolbar.setLayout(self.ToolbarLayout)
        self.ToolbarLayout.addWidget(self.addressbar)

        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)

        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(home_url))
        self.container.layout.addWidget(self.browser)
        self.browser.urlChanged.connect(self.update_urlbar)

        self.setLayout(self.layout)

    def go_back(self):
        self.browser.back()

    def go_forward(self):
        self.browser.forward()

    def reload_page(self):
        self.browser.reload()

    def update_urlbar(self, url):
        self.addressbar.setText(url.toString())
        self.addressbar.setCursorPosition(0)

    def browse_to(self):
        try:
            text = self.addressbar.text()
            if "http" not in text:
                if "." not in text:
                    url = "https://www.google.com/search?q=" + text
                else:
                    url = "http://" + text
            else:
                url = text
            self.browser.setUrl(QUrl(url))
            self.addressbar.setText(url)
        except:
            create_error_msg(Exception)

