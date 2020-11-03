from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWebEngineWidgets import *
from dragable_tabs import DragableTabs


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Secuted')
        self.setGeometry(500, 250, 800, 600)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.tab_widget_1 = DragableTabs(self)
        text_edit = QTextEdit()
        self.tab_widget_1.addTab(text_edit, 'untitled')
        self.layout.addWidget(self.tab_widget_1)
        self.columns_count = 1

        self.menubar = QMenuBar(self)
        self.init_actions()
        self.init_menus()
        self.layout.setMenuBar(self.menubar)

        self.connect_actions()

        with open('./css/styles.css') as ss:
            self.styleshit = ss.read()
        self.setStyleSheet(self.styleshit)

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose a file', '')[0]
        try:
            with open(fname) as f:
                data = f.read()
                new_text_edit = QTextEdit()
                new_text_edit.setText(data)
                self.tab_widget_1.addTab(new_text_edit, fname)
        except Exception as e:
            print(e)

    def new_file(self):
        text_edit = QTextEdit()
        self.tab_widget_1.addTab(text_edit, 'untitled')

    def save_file_as(self):
        fname = QFileDialog.getSaveFileName()[0]
        print(fname)
        text_edit = self.tab_widget_1.widget(self.tab_widget_1.currentIndex())
        with open(fname, 'w', encoding='UTF-8') as f:
            f.write(text_edit.toPlainText())

    def init_actions(self):
        """Initializes actions"""
        # File menu actions
        self.new_action = QAction('New', self)
        self.open_action = QAction('Open', self)
        self.save_action = QAction('Save', self)
        self.save_as_action = QAction('Save as', self)
        self.close_file_action = QAction('Close file', self)

        # Browser menu actions
        self.open_browser_action = QAction('Open Browser', self)

        # View menu actions
        self.two_col_layout_action = QAction('Set two columns layout', self)

    def init_menus(self):
        """Initializes menus and adds actions"""
        # File menu
        self.menu_file = self.menubar.addMenu("File")
        self.menu_file.addAction(self.new_action)
        self.menu_file.addAction(self.open_action)
        self.menu_file.addAction(self.save_action)
        self.menu_file.addAction(self.save_as_action)
        self.menu_file.addAction(self.close_file_action)

        # Browser menu
        self.menu_browser = self.menubar.addMenu("Browser")
        self.menu_browser.addAction(self.open_browser_action)

        # View menu
        self.menu_view = self.menubar.addMenu('View')
        self.menu_view.addAction(self.two_col_layout_action)

    def connect_actions(self):
        """Connects actions with functions"""
        # File menu actions
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_as_action.triggered.connect(self.save_file_as)

        # Browser menu actions
        self.open_browser_action.triggered.connect(self.open_browser)

        # View menu actions
        self.two_col_layout_action.triggered.connect(self.create_second_column)

    def create_second_column(self):
        if self.columns_count < 2:
            self.tab_widget_2 = DragableTabs(self)
            text_edit = QTextEdit()
            self.tab_widget_2.addTab(text_edit, 'untitled')
            self.layout.addWidget(self.tab_widget_2)
            self.columns_count += 1

    def open_browser(self):
        try:
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl("http://www.google.com"))
            self.tab_widget_1.addTab(self.browser, 'Browser')
        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())
