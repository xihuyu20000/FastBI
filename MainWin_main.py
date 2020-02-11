import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication

from MainWin import Ui_MainWindow


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("快速BI工具")
        self.showMaximized()

        self.dataSourceModel = QStandardItemModel()
        self.dataSourceModel.appendRow(QStandardItem("生产计划表"))
        self.dataSourceModel.appendRow(QStandardItem("销售计划表"))
        self.dataSourceModel.setHorizontalHeaderLabels(['表名'])
        self.treeView_datasource.setModel(self.dataSourceModel)
        self.treeView_datasource.clicked.connect(self.on_treeView_datasource_clicked)

        self.dataTableModel = QStandardItemModel()

        self.tableView_datatable.setModel(self.dataTableModel)

    def on_treeView_datasource_clicked(self, modelIndex):
        '''
        选择不同的字段
        :param modelIndex:
        :return:
        '''
        current_item = self.dataSourceModel.itemFromIndex(modelIndex)
        self.dataTableModel.setHorizontalHeaderLabels(['字段1', '字段2', '字段3'])
        for i in range(100):
            self.dataTableModel.appendRow(
                [QStandardItem(str(i * 10 + 1)), QStandardItem(str(i * 10 + 2)), QStandardItem(str(i * 10 + 3))])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWin()
    ui.show()
    sys.exit(app.exec_())