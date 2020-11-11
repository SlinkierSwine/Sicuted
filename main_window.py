from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
from PyQt5.QtWebEngineWidgets import *
from dragable_tabs import DragableTabs
from SETTINGS import *
from text_editor import MyTextEdit


def save(sender, path):
    try:
        text_edit = sender.currentWidget()
        with open(path, 'w', encoding='UTF-8') as f:
            f.write(text_edit.toPlainText())
    except Exception as e:
        print(f'Save error: {e}')


def save_as(sender):
    try:
        fpath = QFileDialog.getSaveFileName()[0]
        print(fpath)
        if fpath != '':
            text_edit = sender.currentWidget()
            text = text_edit.toPlainText()
            with open(fpath, 'w', encoding='UTF-8') as f:
                f.write(text)
        else:
            return None, None
        
    except Exception as e:
        print(f"Save as error: {e}")
    else:
        name = fpath.split('/')[-1]
        sender.setTabText(sender.currentIndex(), name)
        if name.endswith('.py'):
            sender.currentWidget().set_lang('python')
        return fpath, name


def create_save_file_msg():
    msg = QMessageBox()
    msg.setWindowTitle('Save changes')
    msg.setIcon(QMessageBox.Question)
    msg.setText('Save file')
    msg.setInformativeText('Do you want to save changes before closing the file?')
    msg.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    msg.setDefaultButton(QMessageBox.Save)
    return msg.exec()


def create_error_msg(parent, e):
    er = QMessageBox(parent)
    er.setWindowTitle('Error')
    er.setIcon(QMessageBox.Critical)
    er.setText(str(e))
    er.exec()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.tab_paths = {}
        self.setWindowTitle('Secuted')
        self.setGeometry(500, 250, 800, 600)

        self.layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(self.layout)
        self.tab_widget_1 = DragableTabs(self)
        text_edit = MyTextEdit(lang='p')
        text_edit.setTabStopDistance(
            QtGui.QFontMetricsF(text_edit.font()).horizontalAdvance(' ') * 4)
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
        fpath = QFileDialog.getOpenFileName(self, 'Choose a file', '')[0]
        try:
            if fpath != '' and fpath not in self.tab_paths.values():
                with open(fpath, encoding='UTF-8') as f:
                    data = f.read()
                    name = fpath.split('/')[-1]
                    if name.endswith('.py'):
                        new_text_edit = MyTextEdit(lang='python')
                    else:
                        new_text_edit = MyTextEdit()
                    new_text_edit.setText(data)
                    self.tab_widget_1.addTab(new_text_edit, name)
                    self.tab_paths[name] = fpath
            elif fpath in self.tab_paths.values():
                er = QMessageBox(self)
                er.setIcon(QMessageBox.Information)
                er.setWindowTitle('Error')
                er.setText('File is already opened')
                er.exec()
        except Exception as e:
            create_error_msg(self, e)

    def new_file(self):
        text_edit = MyTextEdit()
        self.tab_widget_1.addTab(text_edit, 'untitled')

    def save_file_separately(self):
        try:
            if self.tab_widget_1.currentWidget().focused is True:
                fpath = self.tab_paths.get(self.tab_widget_1.tabText(self.tab_widget_1.currentIndex()))
                if fpath is None:
                    self.save_file_as_separately()
                else:
                    save(self.tab_widget_1, fpath)
            elif self.tab_widget_2.currentWidget().focused is True:
                fpath = self.tab_paths.get(self.tab_widget_2.tabText(self.tab_widget_2.currentIndex()))
                if fpath is None:
                    self.save_file_as_separately()
                else:
                    save(self.tab_widget_2, fpath)
        except AttributeError:
            pass
        except Exception as e:
            create_error_msg(self, e)

    def save_file_as_separately(self):
        try:
            if self.tab_widget_1.currentWidget().focused is True:
                fpath, name = save_as(self.tab_widget_1)
                if fpath != '' and fpath not in self.tab_paths.values() and fpath is not None:
                    self.tab_paths[name] = fpath
            elif self.tab_widget_2.currentWidget().focused is True:
                fpath, name = save_as(self.tab_widget_2)
                if fpath != '' and fpath not in self.tab_paths.values() and fpath is not None:
                    self.tab_paths[name] = fpath
        except AttributeError:
            pass
        except Exception as e:
            create_error_msg(self, e)

    def close_file(self, sender):
        try:
            res = create_save_file_msg()
            index = sender.currentIndex()
            widget = sender.widget(index)
            if res == QMessageBox.Save:
                self.save_file_separately()
                if self.tab_paths.get(sender.tabText(index), None) is not None:
                    del self.tab_paths[sender.tabText(index)]
                    widget.deleteLater()
                    sender.removeTab(index)
            elif res == QMessageBox.Discard:
                if self.tab_paths.get(sender.tabText(index), None) is not None:
                    del self.tab_paths[sender.tabText(index)]
                widget.deleteLater()
                sender.removeTab(index)
        except Exception as e:
            create_error_msg(self, e)

    def close_file_separately(self):
        try:
            if self.tab_widget_1.currentWidget().focused is True:
                self.close_file(self.tab_widget_1)
            elif self.tab_widget_2.currentWidget().focused is True:
                self.close_file(self.tab_widget_2)
        except AttributeError:
            pass
        except Exception as e:
            create_error_msg(self, e)

    def close_tab(self, index):
        try:
            sender = self.sender()
            if self.tab_paths.get(sender.tabText(index), None) is not None:
                del self.tab_paths[sender.tabText(index)]
            widget = sender.widget(index)
            if widget is not None:
                widget.deleteLater()
            sender.removeTab(index)
        except Exception as e:
            create_error_msg(self, e)

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
        self.two_col_layout_action = QAction('Two columns layout', self)
        self.one_col_layout_action = QAction('One column layout', self)
        self.vertical_layout = QAction('Vertical', self)
        self.horizontal_layout = QAction('Horizontal', self)
        self.python_syntax = QAction('Python')

    def init_menus(self):
        """Initializes menus and adds actions"""
        # File menu
        self.menu_file = self.menubar.addMenu("File")
        actions = [self.new_action, self.open_action, self.save_action, self.save_as_action, self.close_file_action]
        self.menu_file.addActions(actions)

        # Browser menu
        self.menu_browser = self.menubar.addMenu("Browser")
        self.menu_browser.addAction(self.open_browser_action)

        # View menu
        self.menu_view = self.menubar.addMenu('View')

        self.menu_columns = self.menu_view.addMenu('Columns')
        self.menu_columns.addActions([self.one_col_layout_action, self.two_col_layout_action])

        self.menu_layout = self.menu_view.addMenu('Layout orientation')
        self.menu_layout.addActions([self.vertical_layout, self.horizontal_layout])

        self.menu_lang = self.menu_view.addMenu('Syntax')
        self.menu_lang.addAction(self.python_syntax)

    def connect_actions(self):
        """Connects actions with functions"""

        # Tab close button
        self.tab_widget_1.tabCloseRequested.connect(self.close_tab)

        # File menu actions
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file_separately)
        self.save_as_action.triggered.connect(self.save_file_as_separately)
        self.close_file_action.triggered.connect(self.close_file_separately)

        # Browser menu actions
        self.open_browser_action.triggered.connect(self.open_browser)

        # View menu actions
        self.two_col_layout_action.triggered.connect(self.create_second_column)
        self.one_col_layout_action.triggered.connect(self.remove_second_column)
        self.vertical_layout.triggered.connect(self.set_vertical_layout)
        self.horizontal_layout.triggered.connect(self.set_horizontal_layout)

        self.python_syntax.triggered.connect(self.set_syntax)

    def create_second_column(self):
        try:
            if self.columns_count < 2:
                self.tab_widget_2 = DragableTabs(self)
                self.layout.addWidget(self.tab_widget_2)
                self.columns_count += 1

                self.tab_widget_2.tabCloseRequested.connect(self.close_tab)
        except Exception as e:
            create_error_msg(self, e)

    def remove_second_column(self):
        try:
            if self.columns_count == 2:
                for i in range(self.tab_widget_2.count(), -1, -1):
                    self.tab_widget_1.addTab(self.tab_widget_2.widget(i), self.tab_widget_2.tabText(i))
                    widget = self.tab_widget_2.widget(i)
                    if widget is not None:
                        widget.deleteLater()
                    self.tab_widget_2.removeTab(i)
                self.tab_widget_2.setParent(None)
                self.columns_count -= 1
        except Exception as e:
            create_error_msg(self, e)

    def open_browser(self):
        try:
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl(home_url))
            self.tab_widget_1.addTab(self.browser, 'Browser')
        except Exception as e:
            create_error_msg(self, e)

    def set_horizontal_layout(self):
        self.layout.setDirection(QBoxLayout.LeftToRight)

    def set_vertical_layout(self):
        self.layout.setDirection(QBoxLayout.TopToBottom)

    def set_syntax(self):
        try:
            if self.tab_widget_1.currentWidget().focused is True:
                if self.sender() == self.python_syntax:
                    self.tab_widget_1.currentWidget().set_lang('python')

            if self.tab_widget_2.currentWidget().focused is True:
                if self.sender() == self.python_syntax:
                    self.tab_widget_2.currentWidget().set_lang('python')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())
