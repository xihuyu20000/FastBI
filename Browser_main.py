import sys

from PyQt5.QtCore import QPoint, QSize, QUrl, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from qtpy import QtCore

from Browser import Ui_MainWindow

# class WebPage(QWebPage):
#     def __init__(self, parent=None):
#         super(WebPage, self).__init__(parent)
#
#     def userAgentForUrl(self, QUrl):
#         return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

class WebEngineView(QWebView):
    windowList = []

    def __init__(self, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.SELECT_FLAG = True
        self.covering = QLabel(self)
        self.current_block = None

    def _initCover(self):
        '''
        遮罩层
        :return:
        '''
        rect = self.current_block.geometry()
        scrollPos = self.page().mainFrame().scrollPosition()
        self.covering.resize(QSize(rect.width(), rect.height()))
        self.covering.move(QPoint(rect.x()-scrollPos.x(), rect.y()-scrollPos.y()))
        self.covering.setStyleSheet("border-width: 4px;border-style: solid;border-color: rgb(255, 170, 0);")
        self.covering.show()

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = QWebView()
        page = QWebPage()
        new_webview.setPage(page)
        win = MainWin()
        win.setCentralWidget(new_webview)
        self.windowList.append(win)  # 注：没有这句会崩溃！！！
        return new_webview

    def mousePressEvent(self, event):
        if self.SELECT_FLAG and event.buttons() == QtCore.Qt.LeftButton:
            self.covering.hide()
            self.current_block = self.page().currentFrame().hitTestContent(event.pos()).element()
            self._initCover()

class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("快速BI工具")
        self.showMaximized()

        self.statusLabel = QLabel()
        self.statusLabel.setMaximumWidth(500)
        self.statusBar().addWidget(self.statusLabel)

        self.browser = QWebEngineView()
        self.browser.load(QUrl("file:///E:/workspace/workspace-python/FastBI/render.html"))
        self.browser.loadFinished.connect(self.on_browserLoadFinished)
        self.browser.loadProgress.connect(self.on_browserLoadProcess)
        self.verticalLayout_browser.addWidget(self.browser)

    @pyqtSlot(int)
    def on_browserLoadProcess(self, process):
        print('加载进度{}%'.format(process))
        self.statusLabel.setText('加载进度{}%'.format(process))

    @pyqtSlot()
    def on_browserLoadFinished(self):
        self.statusLabel.setText('页面加载完成')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWin()
    ui.show()
    sys.exit(app.exec_())