from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic
from modules import syntax_highlighter, code_editor
from SETTINGS import STYLE_SETTINGS_WINDOW_SIZE
from modules.functions import create_error_msg


class StyleSettings(QWidget):
    """Меню настроек внешнего вида"""
    def __init__(self, main_window, db):
        """
        Inits new StyleSettings
        :param main_window: QWidget
        :param db: DataBase
        """
        super().__init__()
        self.db = db
        self.main_window = main_window
        uic.loadUi('ui_files/style_settings.ui', self)

        self.setWindowTitle('Style Settings')
        self.setWindowIcon(QtGui.QIcon('imgs/icon.png'))
        self.setFixedSize(*STYLE_SETTINGS_WINDOW_SIZE)
        self.move(500, 250)
        self.setWindowModality(Qt.ApplicationModal)

        self.preview_code_editor = code_editor.CodeEditor(self)
        self.preview_code_editor.setGeometry(0, 0, 0, 0)
        self.preview_code_editor.setPlainText('''import sys

def function(args):
    ''' + "'''Some function'''" + '''
    print('blabla')

class Class:
    """Some class"""
    def __init__(self):
        self.numbers = [1, 2, 3, 4, 5]
        # Comment
        self.res = 1 + 2
''')
        self.preview_label = QLabel('Choose syntax:', self)
        self.preview_label.setGeometry(0, 0, 0, 0)
        self.preview_combo_box = QComboBox(self)
        self.preview_combo_box.addItems(['Python', 'Plain text'])
        self.preview_combo_box.setGeometry(0, 0, 0, 0)

        self.info_label = QLabel('Click the "Save and apply" button to see changes', self)
        self.info_label.setGeometry(0, 0, 0, 0)

        self.connect_actions()
        self.set_default_values()

    def connect_actions(self):
        """
        Connects actions to functions
        """
        try:
            self.page_combo_box.activated[int].connect(self.stackedWidget.setCurrentIndex)
            self.page_combo_box.currentIndexChanged.connect(self.add_preview_box)
            self.preview_combo_box.activated.connect(self.change_preview_syntax)

            self.mw_background_color_toolbtn.clicked.connect(self.choose_color)
            self.mw_font_color_toolbtn.clicked.connect(self.choose_color)
            self.mw_selected_color_toolbtn.clicked.connect(self.choose_color)

            self.te_background_color_toolbtn.clicked.connect(self.choose_color)
            self.te_font_color_toolbtn.clicked.connect(self.choose_color)
            self.line_highlighter_color_toolbtn.clicked.connect(self.choose_color)

            self.keywords_toolbtn.clicked.connect(self.choose_color)
            self.operators_toolbtn.clicked.connect(self.choose_color)
            self.braces_toolbtn.clicked.connect(self.choose_color)
            self.defclass_toolbtn.clicked.connect(self.choose_color)
            self.string_toolbtn.clicked.connect(self.choose_color)
            self.multiline_string_toolbtn.clicked.connect(self.choose_color)
            self.comments_toolbtn.clicked.connect(self.choose_color)
            self.self_toolbtn.clicked.connect(self.choose_color)
            self.numbers_toolbtn.clicked.connect(self.choose_color)

            self.save_new_preset_btn.clicked.connect(self.save_new_preset)
            self.cancel_btn.clicked.connect(self.close)
            self.load_preset_btn.clicked.connect(self.load_preset)
            self.save_btn.clicked.connect(self.save_preset)
            self.delete_btn.clicked.connect(self.delete_preset)
        except Exception as e:
            create_error_msg(e)

    def add_preview_box(self, index):
        """Добавляет превью подсветки текста"""
        try:
            if index == 2:
                self.setFixedSize(1175, 530)
                self.preview_code_editor.setGeometry(760, 60, 400, 375)
                self.preview_label.setGeometry(760, 30, 100, 20)
                self.preview_combo_box.setGeometry(860, 30, 100, 20)
                self.info_label.setGeometry(760, 450, 500, 20)
            else:
                self.setFixedSize(*STYLE_SETTINGS_WINDOW_SIZE)
                self.preview_code_editor.setGeometry(0, 0, 0, 0)
        except Exception as e:
            create_error_msg(e)

    def change_preview_syntax(self):
        try:
            self.preview_code_editor.set_lang(self.preview_combo_box.currentText())
        except Exception as e:
            create_error_msg(e)

    def set_default_values(self):
        """
        Sets current preset values in fields
        """
        try:
            mw, te, sh = self.db.get_current_preset()

            self.mw_background_color.setText(mw[1])
            self.mw_font.setCurrentFont(QtGui.QFont(mw[2]))
            self.mw_font_color.setText(mw[3])
            self.mw_font_size.setText(mw[4])
            self.mw_selected_color.setText(mw[5])

            self.te_background_color.setText(te[1])
            self.te_font.setCurrentFont(QtGui.QFont(te[2]))
            self.te_font_color.setText(te[3])
            self.te_font_size.setText(te[4])
            self.line_highlighter_color.setText(te[5])

            self.keywords.setText(sh[1])
            self.operators.setText(sh[2])
            self.braces.setText(sh[3])
            self.defclass.setText(sh[4])
            self.string.setText(sh[5])
            self.multiline_string.setText(sh[6])
            self.comments.setText(sh[7])
            self.self_l.setText(sh[8])
            self.numbers.setText(sh[9])
        except Exception as e:
            create_error_msg(e)

    def choose_color(self):
        """
        Sets QLineEdit text as a color chosen from QColorDialog
        """
        sender = self.sender()
        color = QColorDialog.getColor()
        if color.isValid():
            if sender == self.mw_background_color_toolbtn:
                self.mw_background_color.setText(color.name())
            elif sender == self.mw_font_color_toolbtn:
                self.mw_font_color.setText(color.name())
            elif sender == self.mw_selected_color_toolbtn:
                self.mw_selected_color.setText(color.name())

            elif sender == self.te_background_color_toolbtn:
                self.te_background_color.setText(color.name())
            elif sender == self.te_font_color_toolbtn:
                self.te_font_color.setText(color.name())
            elif sender == self.line_highlighter_color_toolbtn:
                self.line_highlighter_color.setText(color.name())

            elif sender == self.keywords_toolbtn:
                self.keywords.setText(color.name())
            elif sender == self.operators_toolbtn:
                self.operators.setText(color.name())
            elif sender == self.braces_toolbtn:
                self.braces.setText(color.name())
            elif sender == self.defclass_toolbtn:
                self.defclass.setText(color.name())
            elif sender == self.string_toolbtn:
                self.string.setText(color.name())
            elif sender == self.multiline_string_toolbtn:
                self.multiline_string.setText(color.name())
            elif sender == self.comments_toolbtn:
                self.comments.setText(color.name())
            elif sender == self.self_toolbtn:
                self.self_l.setText(color.name())
            elif sender == self.numbers_toolbtn:
                self.numbers.setText(color.name())

    def get_data(self, from_main_window=False, from_text_editor=False, from_syntax_highlighter=False):
        """
        Gets values from fields
        :return: list[dict, dict, dict]
        """
        data = []
        if from_main_window:
            main_window_data = {
                'bgcolor': self.mw_background_color.text(),
                'font': self.mw_font.currentFont().family(),
                'font color': self.mw_font_color.text(),
                'font size': self.mw_font_size.text(),
                'selected item color': self.mw_selected_color.text()
            }
            data.append(main_window_data)

        if from_text_editor:
            text_editor_data = {
                'bgcolor': self.te_background_color.text(),
                'font': self.te_font.currentFont().family(),
                'font color': self.te_font_color.text(),
                'font size': self.te_font_size.text(),
                'line_highlighter_color': self.line_highlighter_color.text()
            }
            data.append(text_editor_data)

        if from_syntax_highlighter:
            syntax_highlighter_data = {
                'keywords': self.keywords.text(),
                'operators': self.operators.text(),
                'braces': self.braces.text(),
                'defclass': self.defclass.text(),
                'string': self.string.text(),
                'multiline_string': self.multiline_string.text(),
                'comments': self.comments.text(),
                'self_color': self.self_l.text(),
                'numbers': self.numbers.text()
            }

            data.append(syntax_highlighter_data)
        return data

    def save_new_preset(self):
        """
        Saves new preset in data base
        """
        try:
            name, ok_pressed = QInputDialog.getText(self, "Preset name",
                                                    "Set preset name")
            if ok_pressed:
                if name in self.db.get_all_presets():
                    msg = QMessageBox(QMessageBox.Information, 'Info', 'Preset with this name already exists')
                    msg.exec()
                    ok_pressed = False
                else:
                    main_window_data, text_editor_data, syntax_highlighter_data =\
                        self.get_data(from_main_window=True, from_text_editor=True, from_syntax_highlighter=True)

                    self.db.create_new_preset(name, main_window_data, text_editor_data, syntax_highlighter_data)
                    self.db.set_current_preset(name)
                    self.set_default_values()
                    self.apply_style_sheet()

        except Exception as e:
            create_error_msg(e)
        else:
            if ok_pressed:
                msg = QMessageBox(QMessageBox.Information, 'Info', 'Preset was saved successfully')
                msg.exec()

    def save_preset(self):
        """
        Saves existing preset
        If preset doesn't exist calls save_new_preset
        """
        try:
            current_preset_name = self.db.get_current_preset_name()
            if current_preset_name == 'Default':
                self.save_new_preset()
            else:
                mw, te, sh = self.get_data(from_main_window=True, from_text_editor=True, from_syntax_highlighter=True)
                self.db.update_preset(current_preset_name, mw, te, sh)
                self.apply_style_sheet()
        except Exception as e:
            create_error_msg(e)
        else:
            if current_preset_name != 'Default':
                msg = QMessageBox(QMessageBox.Information, 'Info', 'Preset was saved successfully')
                msg.exec()

    def load_preset(self):
        """
        Sets chosen from QInputDialog preset as current
        """
        try:
            presets = self.db.get_all_presets()
            preset, ok_pressed = QInputDialog.getItem(
                self, "Choose preset", "Choose a preset that you want to load",
                presets, 1, False)
            if ok_pressed:
                self.db.set_current_preset(preset)
                self.set_default_values()
                self.apply_style_sheet()

        except Exception as e:
            create_error_msg(e)

    def delete_preset(self):
        """
            Deletes chosen from QInputDialog preset
        """
        try:
            presets = list(filter(lambda x: x != 'Default', self.db.get_all_presets()))
            if presets:
                preset, ok_pressed = QInputDialog.getItem(
                    self, "Choose preset", "Choose a preset that you want to delete",
                    presets, 1, False)
                if ok_pressed:
                    self.db.delete_preset(preset)
                    self.db.set_current_preset('Default')
                    self.set_default_values()
                    self.apply_style_sheet()
            else:
                ok_pressed = False

        except Exception as e:
            create_error_msg(e)
        else:
            if ok_pressed:
                msg = QMessageBox(QMessageBox.Information, 'Info', 'Preset was deleted successfully')
                msg.exec()

    def apply_style_sheet(self):
        """
        Applies style sheet to main window and sets styles to syntax_highlighter
        """
        try:
            main_window_data, text_editor_data, syntax_highlighter_data =\
                self.get_data(from_main_window=True, from_text_editor=True, from_syntax_highlighter=True)
            self.main_window.setStyleSheet('''QWidget {
        background: %s;
        color: %s;
        font-family: %s;
        font-size: %s;
    }
    
    QPlainTextEdit {
        background: %s;
        border-radius: 5px;
        font-family: %s;
        font-size: %s;
    }
    
    QTabBar::tab {
        height: 20px;
        min-width: 70px;
    }
    
    QTabBar::close-button {
         image: url(imgs/close-button);
         transition: 0.2s;
     }
     
     QTabBar::close-button:hover {
        image: url(imgs/close-button_hover);
     }
    
    QMenuBar {
        border-bottom: 1px inset #202020;
    }
    
    QMenuBar::item:selected {
         background-color: %s;
    }
    
    QMenu {
        margin: 2px;
        border: 1px solid transparent;
        text-align: center;
    }
    
    QMenu::item:selected {
        background: %s;
    }''' % (main_window_data['bgcolor'],
            main_window_data['font color'],
            main_window_data['font'],
            main_window_data['font size'],
            text_editor_data['bgcolor'],
            text_editor_data['font'],
            text_editor_data['font size'],
            main_window_data['selected item color'],
            main_window_data['selected item color']))

            self.preview_code_editor.setStyleSheet('''QPlainTextEdit {
        background: %s;
        border-radius: 5px;
        font-family: %s;
        font-size: %s;
        color: %s;
    }''' % (text_editor_data['bgcolor'],
            text_editor_data['font'],
            text_editor_data['font size'],
            main_window_data['font color']))

            syntax_highlighter.custom_styles(syntax_highlighter_data)
            code_editor.STYLES['highlight_color'] = QtGui.QColor(text_editor_data['line_highlighter_color'])
            code_editor.STYLES['line_number_color'] = QtGui.QColor(text_editor_data['bgcolor'])
            code_editor.STYLES['number_color'] = QtGui.QColor(main_window_data['font color'])
            preset_name = self.db.get_current_preset_name()
            self.current_preset_label.setText(preset_name)
            self.setWindowTitle(preset_name + ' - Style Settings')
            self.main_window.reset_syntax()
            self.preview_code_editor.set_lang('python')
        except Exception as e:
            create_error_msg(e)
