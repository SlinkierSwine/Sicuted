# from PyQt5.QtWidgets import QTextEdit, QAction, QPlainTextEdit
# from PyQt5 import QtGui
# from PyQt5.QtCore import Qt
# import syntax_highlighter

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QColor, QPainter, QTextFormat


# class MyTextEdit(QTextEdit):
#     def __init__(self, lang=''):
#         """
#         Inits new MyTextEdit
#         :param lang: str
#         """
#         super().__init__()
#         self.lang = lang
#         self.focused = False
#         self.set_lang(self.lang)
#         self.setContextMenuPolicy(Qt.CustomContextMenu)
#         self.customContextMenuRequested.connect(self._context_menu)
#         self.setTabStopDistance(
#             QtGui.QFontMetricsF(self.font()).horizontalAdvance(' ') * 4)
#
#     def focusInEvent(self, event):
#         super().focusInEvent(event)
#         self.focused = True
#
#     def focusOutEvent(self, event):
#         super().focusOutEvent(event)
#         self.focused = False
#
#     def set_lang(self, lang):
#         """
#         Sets language
#         :param lang: str
#         """
#         if lang == 'python':
#             self.highlighter = syntax_highlighter.PythonHighlighter(self.document())
#         elif lang == '':
#             self.highlighter = None
#
#     def _context_menu(self):
#         self.normal_menu = self.createStandardContextMenu()
#         self._add_custom_menu_items(self.normal_menu)
#         self.normal_menu.exec_(QtGui.QCursor.pos())
#
#     def _add_custom_menu_items(self, menu):
#         menu.addSeparator()
#
#         self.python_syntax = QAction('Python')
#         self.plain_text = QAction('Plain text')
#
#         self.menu_lang = menu.addMenu('Syntax')
#         self.menu_lang.addActions([self.python_syntax, self.plain_text])
#
#         self.python_syntax.triggered.connect(self.set_syntax)
#         self.plain_text.triggered.connect(self.set_syntax)
#
#     def set_syntax(self):
#         """
#         Sets syntax
#         """
#         try:
#             sender = self.sender()
#             if sender == self.python_syntax:
#                 self.set_lang('python')
#             elif sender == self.plain_text:
#                 self.set_lang('')
#         except Exception as e:
#             print(e)

class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    codeEditor = QCodeEditor()
    codeEditor.show()
    sys.exit(app.exec_())