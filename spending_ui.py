import sys

import PyQt6.QtCore as QCore
import PyQt6.QtWidgets as QWidge
import PyQt6.QtGui as QGUI
import PyQt6.QtCharts as QCharts
from spending_db import Spending

class SpendingTableModel(QCore.QAbstractTableModel):
    def __init__(self, table_data = None, parent = None):
        super().__init__()

        if table_data is None:
            table_data = [["", "", ""]]
        
        self.table_data = table_data

        self.headers = ["Purchase", "Cost", "Category", "Date Purchased"]
        
        # self.sort_changed_signal = QCore.pyqtSignal(int, int)
    
    def rowCount(self, parent = None, *args, **kwargs):
        return len(self.table_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def headerData(self, section, orientation, role = None):
        if role == QCore.Qt.ItemDataRole.DisplayRole and orientation == QCore.Qt.Orientation.Horizontal:
            return self.headers[section]
        
    def data(self, index, role = None):
        if role == QCore.Qt.ItemDataRole.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.table_data[row][column]
            return value
        
    def update_data(self, new_data):
        self.layoutAboutToBeChanged.emit()
        self.table_data = new_data
        self.layoutChanged.emit()

class SpendingTableView(QWidge.QTableView):
    def __init__(self):
        super().__init__()
        self.setVisible(True)

    def resizeEvent(self, event):
        width = event.size().width()
        self.setColumnWidth(0, int(width * 0.30))
        self.setColumnWidth(1, int(width * 0.30))
        self.setColumnWidth(2, int(width * 0.20))
        self.setColumnWidth(3, int(width * 0.20))

class SpendingChart(QCharts.QChart):
    def __init__(self, data):
        super().__init__()
        self.data = data

        self.outer = QCharts.QPieSeries()
        self.set_outer()
        self.addSeries(self.outer)
    
    def set_outer(self):
        slices = []
        for d in self.data:
            sliver = QCharts.QPieSlice(d[0], d[1], parent = None)
            sliver.setLabelVisible()
            sliver.setColor(QGUI.QColor("#82d3e5"))
            sliver.setLabelBrush(QGUI.QColor("#82d3e5"))

            slices.append(sliver)
            self.outer.append(sliver)

    def update_outer(self, new_date):
        self.removeSeries(self.outer)
        self.data = new_date
        del(self.outer)
        self.outer = QCharts.QPieSeries()
        self.set_outer()
        self.addSeries(self.outer)
        
        

    def update_chart(self):
        self.Geometry

class SpendingWidget(QWidge.QWidget):
    def __init__(self):
        super().__init__()
        self.treasury = Spending()
        self.chart = SpendingChart(self.treasury.pie_data())
        self.chart_view = QCharts.QChartView(self.chart)
        self.chart_view.show()

        self.purchase_input = QWidge.QLineEdit("Purchase")
        self.cost_input = QWidge.QLineEdit("Cost")
        self.category_input = QWidge.QLineEdit("Category")
        self.date_input = QWidge.QLineEdit("Date")
        self.add_button = QWidge.QPushButton('add')
        self.search_button = QWidge.QPushButton('search')
        self.rem_button = QWidge.QPushButton('remove')
        self.display = SpendingTableView()
        self.display_model = SpendingTableModel(self.treasury.show_receipts())
        self.display.setModel(self.display_model)

        self.add_button.clicked.connect(self.add_new)
        self.search_button.clicked.connect(self.search_entries)
        self.rem_button.clicked.connect(self.rem_entry)

        grid = QWidge.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.purchase_input, 1, 1, 1, 2)
        grid.addWidget(self.date_input, 1, 3, 1, 2)
        grid.addWidget(self.cost_input, 2, 1, 1, 2)
        grid.addWidget(self.category_input, 2, 3, 1, 2)
        grid.addWidget(self.add_button, 3, 1, 1, 1)
        grid.addWidget(self.rem_button, 3, 2, 1, 1)
        grid.addWidget(self.search_button, 3, 3, 1, 1)
        grid.addWidget(self.chart_view, 5, 1, 3, 4)
        grid.addWidget(self.display, 8, 1, 3, 4)
        self.setLayout(grid)

    def add_new(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        check = self.treasury.add_receipt(purchase, cost, category, date)
        if check != "missing":
            self.display_model.update_data(self.treasury.show_receipts())
            self.chart.update_outer(self.treasury.pie_data())
            self.purchase_input.clear()
            self.cost_input.clear()
            self.date_input.clear()

    def search_entries(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        date = self.date_input.text()
        self.display_model.update_data(self.treasury.search_receipts(purchase, cost, date))

    def rem_entry(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        self.treasury.rem_entry(purchase, cost, category, date)
        self.display_model.update_data(self.treasury.show_receipts())
        self.purchase_input.clear()
        self.cost_input.clear()
        self.date_input.clear()

class SpendingWindow(QWidge.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Spending Tracker")
        self.resize(700, 600)
        self.center = SpendingWidget()
        self.setCentralWidget(self.center)

        self.show()


def main():
    app = QWidge.QApplication(sys.argv)
    ui = SpendingWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()