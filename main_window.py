from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWebEngineWidgets import *
from dragable_tabs import DragableTabs


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.tab_paths = {}
        self.setWindowTitle('Secuted')
        self.setGeometry(500, 250, 800, 600)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.tab_widget_1 = DragableTabs(self)
        # text_edit = QTextEdit()
        # self.tab_widget_1.addTab(text_edit, 'untitled')
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
            if fname != '' and fname not in self.tab_paths.values():
                with open(fname, encoding='UTF-8') as f:
                    data = f.read()
                    name = fname.split('/')[-1]
                    new_text_edit = QTextEdit()
                    new_text_edit.setText(data)
                    self.tab_widget_1.addTab(new_text_edit, name)
                    self.tab_paths[name] = fname
            elif fname in self.tab_paths.values():
                er = QMessageBox(self)
                er.setIcon(QMessageBox.Information)
                er.setWindowTitle('Error')
                er.setText('File is already opened')
                er.exec()
        except Exception as e:
            er = QMessageBox(self)
            er.setWindowTitle('Error')
            er.setText(str(e))
            er.exec()

    def new_file(self):
        text_edit = QTextEdit()
        self.tab_widget_1.addTab(text_edit, 'untitled')

    def save_file(self):
        path = self.tab_paths.get(self.tab_widget_1.tabText(self.tab_widget_1.currentIndex()))
        if path is None:
            self.save_file_as()
        else:
            try:
                text_edit = self.tab_widget_1.widget(self.tab_widget_1.currentIndex())
                with open(path, 'w', encoding='UTF-8') as f:
                    f.write(text_edit.toPlainText())
            except Exception as e:
                print(e)

    def save_file_as(self):
        try:
            fname = QFileDialog.getSaveFileName()[0]
            if fname != '':
                name = fname.split('/')[-1]
                text_edit = self.tab_widget_1.widget(self.tab_widget_1.currentIndex())
                self.tab_widget_1.setTabText(self.tab_widget_1.currentIndex(), name)
                with open(fname, 'w', encoding='UTF-8') as f:
                    f.write(text_edit.toPlainText())
        except Exception as e:
            print(e)

    def close_file(self):
        if self.tab_widget_1.count() != 0:
            msg = QMessageBox()
            msg.setWindowTitle('Save changes')
            msg.setIcon(QMessageBox.Question)
            msg.setText('Save file')
            msg.setInformativeText('Do you want to save changes before closing the file?')
            msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Save)
            res = msg.exec()
            if res == QMessageBox.Save:
                self.save_file()
                self.tab_widget_1.widget(self.tab_widget_1.currentIndex()).deleteLater()
                self.tab_widget_1.removeTab(self.tab_widget_1.currentIndex())
            elif res == QMessageBox.Discard:
                self.tab_widget_1.widget(self.tab_widget_1.currentIndex()).deleteLater()
                self.tab_widget_1.removeTab(self.tab_widget_1.currentIndex())

    def close_tab(self):
        sender = self.sender()
        widget = sender.widget(sender.currentIndex())
        if widget is not None:
            widget.deleteLater()
        sender.removeTab(sender.currentIndex())

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
        self.one_col_layout_action = QAction('Set one column layout', self)

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

        # Tab close button
        self.tab_widget_1.tabCloseRequested.connect(self.close_tab)

        # File menu actions
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action.triggered.connect(self.save_file_as)
        self.close_file_action.triggered.connect(self.close_file)

        # Browser menu actions
        self.open_browser_action.triggered.connect(self.open_browser)

        # View menu actions
        self.two_col_layout_action.triggered.connect(self.create_second_column)
        self.one_col_layout_action.triggered.connect(self.remove_second_column)

    def create_second_column(self):
        if self.columns_count < 2:
            self.tab_widget_2 = DragableTabs(self)
            # text_edit = QTextEdit()
            # self.tab_widget_2.addTab(text_edit, 'untitled')
            self.layout.addWidget(self.tab_widget_2)
            self.columns_count += 1

            self.menu_view.removeAction(self.two_col_layout_action)
            self.menu_view.addAction(self.one_col_layout_action)

            self.tab_widget_2.tabCloseRequested.connect(self.close_tab)

    def remove_second_column(self):
        for i in range(self.tab_widget_2.count(), -1, -1):
            self.tab_widget_1.addTab(self.tab_widget_2.widget(i), self.tab_widget_2.tabText(i))
            widget = self.tab_widget_2.widget(i)
            if widget is not None:
                widget.deleteLater()
            self.tab_widget_2.removeTab(i)
        self.menu_view.removeAction(self.one_col_layout_action)
        self.menu_view.addAction(self.two_col_layout_action)
        self.tab_widget_2.setParent(None)
        self.columns_count -= 1

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
