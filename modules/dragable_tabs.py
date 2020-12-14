from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Source: https://forum.qt.io/topic/67542/drag-tabs-between-qtabwidgets/6
# Так же скопировал и изменил под свои нужды

class DraggableTabs(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.tabBar = self.tabBar()
        self.tabBar.setMouseTracking(True)
        self.indexTab = None
        self.setTabShape(QTabWidget.Triangular)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.setTabsClosable(True)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return

        globalPos = self.mapToGlobal(e.pos())
        tabBar = self.tabBar
        posInTab = tabBar.mapFromGlobal(globalPos)
        self.indexTab = tabBar.tabAt(e.pos())
        tabRect = tabBar.tabRect(self.indexTab)

        pixmap = QPixmap(tabRect.size())
        tabBar.render(pixmap, QPoint(), QRegion(tabRect))
        mimeData = QMimeData()
        drag = QDrag(tabBar)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        cursor = QCursor(Qt.OpenHandCursor)
        drag.setHotSpot(e.pos() - posInTab)
        drag.setDragCursor(cursor.pixmap(), Qt.MoveAction)
        dropAction = drag.exec_(Qt.MoveAction)

    def dragEnterEvent(self, e):
        e.accept()
        if e.source().parentWidget() != self:
            return

        self.parent.TABINDEX = self.indexOf(self.widget(self.indexTab))

    def dragLeaveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        if e.source().parentWidget() == self:
            return

        e.setDropAction(Qt.MoveAction)
        e.accept()
        counter = self.count()

        if counter == 0:
            self.addTab(e.source().parentWidget().widget(self.parent.TABINDEX),
                        e.source().tabText(self.parent.TABINDEX))
        else:
            self.insertTab(counter + 1, e.source().parentWidget().widget(self.parent.TABINDEX),
                           e.source().tabText(self.parent.TABINDEX))

