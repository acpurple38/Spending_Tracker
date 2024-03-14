from spending_chart import *
from spending_table import *
from spending_db import *

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
        grid.addWidget(self.chart_view, 5, 1, 5, 2)
        grid.addWidget(self.display, 5, 3, 5, 2)
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
            self.category_input.clear()
            self.date_input.clear()

    def search_entries(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        self.display_model.update_data(self.treasury.search_receipts(purchase, cost, category, date))

    def rem_entry(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        self.treasury.rem_entry(purchase, cost, category, date)
        self.display_model.update_data(self.treasury.show_receipts())
        self.purchase_input.clear()
        self.cost_input.clear()
        self.category_input.clear()
        self.date_input.clear()