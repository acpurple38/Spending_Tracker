from chart_widge import *
from table_widge import *
from db_handling import *
from error_window import *

class SpendingWidget(QWidge.QWidget):
    def __init__(self):
        super().__init__()
        self.treasury = Spending()
        self.chart = SpendingChart(self.treasury.pie_data("chart"))
        self.chart_view = QCharts.QChartView(self.chart)
        self.chart_view.show()

        self.purchase_input = QWidge.QLineEdit()
        self.purchase_label = QWidge.QLabel("Purchase:")
        self.cost_input = QWidge.QLineEdit("##.##")
        self.cost_label = QWidge.QLabel("Cost:")
        self.category_input = QWidge.QLineEdit()
        self.category_label = QWidge.QLabel("Category:")
        self.date_input = QWidge.QLineEdit("YYYY-MM-DD")
        self.date_label = QWidge.QLabel("Date:")

        self.add_button = QWidge.QPushButton('add')
        self.search_button = QWidge.QPushButton('search')
        self.rem_button = QWidge.QPushButton('remove')

        self.trans_table = SpendingTableView()
        self.trans_model = SpendingTableModel(["Purchase", "Cost", "Category", "Date Purchased"], self.treasury.show_receipts())
        self.trans_table.setModel(self.trans_model)

        self.pie_table = PieTableView()
        self.pie_model = SpendingTableModel(["Category", "Total"], self.treasury.pie_data("table"))
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

        self.error_check = False
        self.error_mess = ""

    def add_new(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        check = self.treasury.add_receipt(purchase, cost, category, date)
        if check[0] == "CODE_ERROR":
            arg_check = self.arg_formatting(purchase, cost, category, date)
            self.error_notif("add", check, arg_check)
        else:
            self.trans_model.update_data(self.treasury.show_receipts())
            self.chart.update_outer(self.treasury.pie_data("chart"))
            self.pie_model.update_data(self.treasury.pie_data("table"))
            self.purchase_input.clear()
            self.cost_input.clear()
            self.category_input.clear()
            self.date_input.clear()
            
    def search_entries(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        self.trans_model.update_data(self.treasury.search_receipts_table(purchase, cost, category, date))
        pie_data = self.treasury.pie_search(purchase, cost, category, date)
        self.chart.update_outer(pie_data)
        self.pie_model.update_data(pie_data)

    def rem_entry(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        check = self.treasury.rem_entry(purchase, cost, category, date)
        if check[0] == "CODE_ERROR":
            self.error_notif("rem", check)
        else:
            self.trans_model.update_data(self.treasury.show_receipts())
            self.chart.update_outer(self.treasury.pie_data("chart"))
            self.pie_model.update_data(self.treasury.pie_data("table"))
            self.purchase_input.clear()
            self.cost_input.clear()
            self.category_input.clear()
            self.date_input.clear()

    def arg_formatting(self, purchase, cost, category, date):
        args = [purchase, cost, category, date]
        errors = []
        for i in range(len(args)):
            if args[i] != "":
                if i != 1 and i != 3:
                    args[i] = args[i].strip()
                    args[i] = args[i].split(" ")
                    if len(args[i]) > 1:
                        for i in range(len(args[i])):
                            if args[i][i][0].isalpha():
                                args[i][i] = args[i][i].capitalize()
                    args[i] = " ".join(args[i])
                elif i == 1:
                    args[1] = args[1].split(".")
                    while i < len(args[1]):
                        if not args[1][i].isnumeric() or len(args[1]) > 2:
                            errors.append(-2)
                            i = len(args[1])
                    args[1] = ".".join(args[1])
                else:
                    if len(args[3]) != 10:
                        errors.append(-3)
                        return errors
                    else:
                        args[3] = args[3].split("-")
                        if ("".join(args[3])).isnumeric():
                            if len(args[3][0]) == 4:
                                args[3] = "-".join(args[3])
                            else:
                                errors.append(-3)
                                return errors
                        else:
                            errors.append(-3)
                            return errors
        return args

    def error_notif(self, func, error_code, arg_check):
        message = ""
        miss = 0
        if func == "add" or func == "rem":
            message += "Missing: \n"
            for code in error_code:
                if code == -1:
                    message += "Purchase Info\n"
                    miss += 1
                if code == -2:
                    message += "Cost Value\n"
                    miss += 1
                if code == -3:
                    message += "Category Value\n"
                    miss += 1
                elif code == -4 and func != "add":
                    message += "Date Value for Remove\n"
                    miss += 1
                if code == -4 and func != "rem":
                    if miss == 0:
                        message = "Too many categories, remove one or try again\n"
                    else:
                        message += "\nToo many categories, remove one or try again\n"
        if len(arg_check) > 0:
            message += "\nErrors in Values: \n"
        for arg in arg_check:
            if arg == -2:
                message += "Cost Format\n"
            if arg == -3:
                message += "Date Format\n"

        if message != "":
            dlg = ErrorDialog(message)
            dlg.exec()

