from PyQt5.QtWidgets import QTextEdit, QAction
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import syntax_highlighter


class MyTextEdit(QTextEdit):
    def __init__(self, lang=''):
        super().__init__()
        self.lang = lang
        self.focused = False
        self.set_lang(self.lang)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._context_menu)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused = True

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focused = False

    def set_lang(self, lang):
        if lang == 'python':
            self.highlighter = syntax_highlighter.PythonHighlighter(self.document())
        elif lang == '':
            self.highlighter = None

    def _context_menu(self):
        self.normal_menu = self.createStandardContextMenu()
        self._add_custom_menu_items(self.normal_menu)
        self.normal_menu.exec_(QtGui.QCursor.pos())

    def _add_custom_menu_items(self, menu):
        menu.addSeparator()
        self.python_syntax = QAction('Python')
        self.plain_text = QAction('Plain text')
        menu.addActions([self.python_syntax, self.plain_text])
        self.python_syntax.triggered.connect(self.set_syntax)
        self.plain_text.triggered.connect(self.set_syntax)

    def set_syntax(self):
        try:
            sender = self.sender()
            if sender == self.python_syntax:
                self.set_lang('python')
            elif sender == self.plain_text:
                self.set_lang('')
        except Exception as e:
            print(e)
