from modules import syntax_highlighter
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QTextOption


STYLES = {
    'highlight_color': QColor('#525252'),
    'line_number_color': QColor('#202020'),
    'number_color': QColor('#d5e6d3'),
}


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.editor.get_line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None, lang=''):
        super().__init__(parent)
        self.lang = lang
        self.focused = False
        self.line_number_area = LineNumberArea(self)

        self.setWordWrapMode(QTextOption.NoWrap)
        self.set_lang(self.lang)
        self.update_line_number_area_width(0)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.insertPlainText(' ' * 4)
        else:
            super().keyPressEvent(event)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focused = True

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focused = False

    def set_lang(self, lang):
        """
            Sets language
            :param lang: str
        """
        self.lang = lang
        if lang.lower() == 'python':
            self.highlighter = syntax_highlighter.PythonHighlighter(self.document())
        elif lang.lower() == 'plain' or lang == '' or lang.lower() == 'plain text':
            self.highlighter = None
            self.setPlainText(self.toPlainText())

    def reset_highlighting(self):
        self.highlighter = None
        self.setPlainText(self.toPlainText())
        self.set_lang(self.lang)

    def get_line_number_area_width(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.get_line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.get_line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = STYLES['highlight_color']
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)

        painter.fillRect(event.rect(), STYLES['line_number_color'])

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(block_number + 1)
                painter.setPen(STYLES['number_color'])
                painter.drawText(0, int(top), self.line_number_area.width(), height, Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
