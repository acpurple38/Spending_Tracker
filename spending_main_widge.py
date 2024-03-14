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

        self.purchase_input = QWidge.QLineEdit()
        self.purchase_label = QWidge.QLabel("Purchase:")
        self.cost_input = QWidge.QLineEdit()
        self.cost_label = QWidge.QLabel("Cost:")
        self.category_input = QWidge.QLineEdit()
        self.category_label = QWidge.QLabel("Category:")
        self.date_input = QWidge.QLineEdit()
        self.date_label = QWidge.QLabel("Date:")

        self.add_button = QWidge.QPushButton('add')
        self.search_button = QWidge.QPushButton('search')
        self.rem_button = QWidge.QPushButton('remove')

        self.trans_table = SpendingTableView()
        self.trans_model = SpendingTableModel(["Purchase", "Cost", "Category", "Date Purchased"], self.treasury.show_receipts())
        self.trans_table.setModel(self.trans_model)

        self.pie_table = PieTableView()
        self.pie_model = SpendingTableModel(["Category", "Total"], self.treasury.pie_data())
        self.pie_table.setModel(self.pie_model)

        self.add_button.clicked.connect(self.add_new)
        self.search_button.clicked.connect(self.search_entries)
        self.rem_button.clicked.connect(self.rem_entry)

        grid = QWidge.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.purchase_label, 0, 0, 1, 1)
        grid.addWidget(self.purchase_input, 0, 1, 1, 11)

        grid.addWidget(self.cost_label, 0, 12, 1, 1)
        grid.addWidget(self.cost_input, 0, 13, 1, 3)

        grid.addWidget(self.category_label, 1, 0, 1, 1)
        grid.addWidget(self.category_input, 1, 1, 1, 11)

        grid.addWidget(self.date_label, 1, 12, 1, 1)
        grid.addWidget(self.date_input, 1, 13, 1, 3)
        
        grid.addWidget(self.add_button, 4, 0, 1, 4)
        grid.addWidget(self.rem_button, 4, 4, 1, 4)
        grid.addWidget(self.search_button, 4, 8, 1, 4)
        grid.addWidget(self.chart_view, 5, 0, 8, 8)
        grid.addWidget(self.trans_table, 5, 8, 4, 8)
        grid.addWidget(self.pie_table, 9, 8, 4, 8)
        self.setLayout(grid)

    def add_new(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        check = self.treasury.add_receipt(purchase, cost, category, date)
        if check != "missing":
            self.trans_model.update_data(self.treasury.show_receipts())
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
        self.trans_model.update_data(self.treasury.search_receipts(purchase, cost, category, date))

    def rem_entry(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        self.treasury.rem_entry(purchase, cost, category, date)
        self.trans_model.update_data(self.treasury.show_receipts())
        self.purchase_input.clear()
        self.cost_input.clear()
        self.category_input.clear()
        self.date_input.clear()