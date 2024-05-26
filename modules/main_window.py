from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from modules.download_from_server import DownloadFromServerWidget
from modules.dragable_tabs import DraggableTabs
from SETTINGS import *
from modules.code_editor import CodeEditor
from modules.style_settings_window import StyleSettings
from modules.database import DataBase
from modules.browser import BrowserApp
from modules.functions import *


class MainWindow(QWidget):
    """Main window"""

    def __init__(self):
        super().__init__()
        self.tab_paths = {}
        self.setWindowTitle('Secuted')
        self.setGeometry(*WINDOW_SIZE)
        self.setWindowIcon(QtGui.QIcon('imgs/icon.png'))

        self.db = DataBase('db.db')
        self.style_settings_window = StyleSettings(self, self.db)

        self.download_from_server_window = DownloadFromServerWidget(self)

        self.layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.setLayout(self.layout)
        self.tab_widget_1 = DraggableTabs(self)
        text_edit = CodeEditor()
        self.tab_widget_1.addTab(text_edit, 'untitled')
        self.layout.addWidget(self.tab_widget_1)
        self.columns_count = 1

        self.tab_widget_2 = None

        self.menubar = QMenuBar(self)
        self.init_actions()
        self.init_menus()
        self.layout.setMenuBar(self.menubar)

        self.connect_actions()
        self.style_settings_window.apply_style_sheet()

    def open_file(self):
        """
        Creates QFileDialog, opens given file and writes it in new QTextEdit
        """
        fpath = QFileDialog.getOpenFileName(self, 'Choose a file', '')[0]
        try:
            if fpath != '' and fpath not in self.tab_paths.values():  # если файл выбран и еще не открыт...
                with open(fpath, encoding='UTF-8') as f:
                    text = f.read()
                    self.new_file_with_text(fpath, text)
            elif fpath in self.tab_paths.values():  # если файл уже открыт, выводим ошибку
                er = QMessageBox(self)
                er.setIcon(QMessageBox.Information)
                er.setWindowTitle('Error')
                er.setText('File is already opened')
                er.exec()
        except Exception as e:
            create_error_msg(e)

    def new_file(self):
        """
        Creates new QTextEdit
        """
        text_edit = CodeEditor()
        self.tab_widget_1.addTab(text_edit, 'untitled')

    def new_file_with_text(self, fpath: str, text) -> None:
        name = fpath.split('/')[-1]
        if name.endswith('.py'):
            new_text_edit = CodeEditor(lang='python')
        else:
            new_text_edit = CodeEditor()

        new_text_edit.setPlainText(text)
        self.tab_widget_1.addTab(new_text_edit, name)
        self.tab_paths[name] = fpath

    def save_file_separately(self):
        """
        Creates QFileDialog and saves existing file at returned path
        If file doesn't exist, calls save_file_as_separately
        """
        try:
            if self.tab_widget_1.currentWidget().focused is True:
                fpath = self.tab_paths.get(self.tab_widget_1.tabText(self.tab_widget_1.currentIndex()))
                if fpath is None:  # если файла не существует, вызываем функцию сохранить как
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
            create_error_msg(e)

    def save_file_as_separately(self):
        """
        Creates QFileDialog and saves new file at returned path
        """
        try:
            if self.tab_widget_1.currentWidget().focused is True:
                current_tab_text = self.tab_widget_1.tabText(self.tab_widget_1.currentIndex())
                if current_tab_text in self.tab_paths.keys():  # если у файла уже есть название, удаляем из tab_paths
                    del self.tab_paths[current_tab_text]

                fpath, name = save_as(self.tab_widget_1)
                if fpath != '' and fpath not in self.tab_paths.values() and fpath is not None:
                    self.tab_paths[name] = fpath  # добавляем новое название файла в tab_paths

            elif self.tab_widget_2.currentWidget().focused is True:
                current_tab_text = self.tab_widget_2.tabText(self.tab_widget_2.currentIndex())
                if current_tab_text in self.tab_paths.keys():
                    del self.tab_paths[current_tab_text]

                fpath, name = save_as(self.tab_widget_2)
                if fpath != '' and fpath not in self.tab_paths.values() and fpath is not None:
                    self.tab_paths[name] = fpath
        except AttributeError:
            pass
        except Exception as e:
            create_error_msg(e)

    def close_file(self, sender):
        """
        :param sender: QTabWidget
        """
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
            create_error_msg(e)

    def close_file_separately(self):
        """
        Closes and saves text in focused QTextWidget
        """
        try:
            if self.tab_widget_1.currentWidget().focused is True:
                self.close_file(self.tab_widget_1)
            elif self.tab_widget_2.currentWidget().focused is True:
                self.close_file(self.tab_widget_2)
        except AttributeError:
            pass
        except Exception as e:
            create_error_msg(e)

    def close_tab(self, index):
        """
        Called when Tab close button is pressed
        Closes tab at index
        :param index: int
        """
        try:
            sender = self.sender()
            if self.tab_paths.get(sender.tabText(index), None) is not None:
                del self.tab_paths[sender.tabText(index)]
            widget = sender.widget(index)
            if widget is not None:
                widget.deleteLater()
            sender.removeTab(index)
        except Exception as e:
            create_error_msg(e)

    def init_actions(self):
        """Initializes actions"""
        # File menu actions
        self.new_action = QAction('New', self)
        self.open_action = QAction('Open', self)
        self.save_action = QAction('Save', self)
        self.save_as_action = QAction('Save as', self)
        self.close_file_action = QAction('Close file', self)
        self.download_from_server_action = QAction('Download from server', self)

        self.all_actions = [self.new_action, self.open_action, self.save_action, self.save_as_action, self.close_file_action, self.download_from_server_action]

        # Browser menu actions
        self.open_browser_action = QAction('Open Browser', self)

        # View menu actions
        self.two_col_layout_action = QAction('Two columns layout', self)
        self.one_col_layout_action = QAction('One column layout', self)
        self.vertical_layout = QAction('Vertical', self)
        self.horizontal_layout = QAction('Horizontal', self)
        self.style = QAction('Style', self)

        # Syntax menu actions
        self.plain_text_action = QAction('Plain text', self)
        self.python_syntax_action = QAction('Python', self)

    def init_menus(self):
        """Initializes menus and adds actions"""
        # File menu
        self.menu_file = self.menubar.addMenu("File")
        self.menu_file.addActions(self.all_actions)

        # Browser menu
        self.menu_browser = self.menubar.addMenu("Browser")
        self.menu_browser.addAction(self.open_browser_action)

        # View menu
        self.menu_view = self.menubar.addMenu('View')

        self.menu_columns = self.menu_view.addMenu('Columns')
        self.menu_columns.addActions([self.one_col_layout_action, self.two_col_layout_action])

        self.menu_layout = self.menu_view.addMenu('Layout orientation')
        self.menu_layout.addActions([self.vertical_layout, self.horizontal_layout])
        self.menu_view.addAction(self.style)

        # Syntax menu
        self.menu_syntax = self.menubar.addMenu('Syntax')
        self.menu_syntax.addActions([self.plain_text_action, self.python_syntax_action])

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
        self.download_from_server_action.triggered.connect(self.download_from_server)

        # Browser menu actions
        self.open_browser_action.triggered.connect(self.open_browser)

        # View menu actions
        self.two_col_layout_action.triggered.connect(self.create_second_column)
        self.one_col_layout_action.triggered.connect(self.remove_second_column)
        self.vertical_layout.triggered.connect(self.set_vertical_layout)
        self.horizontal_layout.triggered.connect(self.set_horizontal_layout)
        self.style.triggered.connect(self.open_style_menu)

        # Syntax menu actions
        self.plain_text_action.triggered.connect(self.set_syntax)
        self.python_syntax_action.triggered.connect(self.set_syntax)

    def create_second_column(self):
        """
        Creates second QTabWidget
        """
        try:
            if self.columns_count < 2:
                self.tab_widget_2 = DraggableTabs(self)
                self.layout.addWidget(self.tab_widget_2)
                self.columns_count += 1

                self.tab_widget_2.tabCloseRequested.connect(self.close_tab)
        except Exception as e:
            create_error_msg(e)

    def remove_second_column(self):
        """
        Removes second QTabWidget and drags all its tabs to the first one
        """
        try:
            if self.columns_count == 2:
                for i in range(self.tab_widget_2.count(), -1, -1):  # перетаскиваем все вкладки со второго виджета на первый
                    self.tab_widget_1.addTab(self.tab_widget_2.widget(i), self.tab_widget_2.tabText(i))
                    widget = self.tab_widget_2.widget(i)
                    if widget is not None:
                        widget.deleteLater()
                    self.tab_widget_2.removeTab(i)
                self.tab_widget_2.setParent(None)
                self.columns_count -= 1
        except Exception as e:
            create_error_msg(e)

    def open_browser(self):
        """
        Opens browser in a new tab
        """
        try:
            browser_app = BrowserApp(HOME_URL)
            self.tab_widget_1.addTab(browser_app, 'Browser')
        except Exception as e:
            create_error_msg(e)

    def download_from_server(self):
        self.download_from_server_window.show()

    def set_horizontal_layout(self):
        """
        Sets window layout to horizontal
        """
        self.layout.setDirection(QBoxLayout.LeftToRight)

    def set_vertical_layout(self):
        """
        Sets window layout to vertical
        """
        self.layout.setDirection(QBoxLayout.TopToBottom)

    def open_style_menu(self):
        """
        Opens StyleSettings window
        """
        self.style_settings_window.show()

    def set_syntax(self):
        """Sets syntax of focused widget"""
        try:
            sender = self.sender()
            if self.focusWidget().__class__ == CodeEditor:
                if sender == self.plain_text_action:
                    self.focusWidget().set_lang('plain')
                elif sender == self.python_syntax_action:
                    self.focusWidget().set_lang('python')
        except Exception as e:
            create_error_msg(e)

    def reset_syntax(self):
        try:
            for i in range(self.tab_widget_1.count()):
                widget = self.tab_widget_1.widget(i)
                if widget.__class__ == CodeEditor:
                    widget.reset_highlighting()
            if self.tab_widget_2 is not None:
                for i in range(self.tab_widget_2.count()):
                    widget = self.tab_widget_2.widget(i)
                    if widget.__class__ == CodeEditor:
                        widget.reset_highlighting()
        except Exception as e:
            create_error_msg(e)
