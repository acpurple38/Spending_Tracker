from chart_widge import *
from table_widge import *
from db_handling import *
from error_window import *

from PyQt6.QtWidgets import QWidget as QWidge
from PyQt6.QtWidgets import QLineEdit as QLE
from PyQt6.QtWidgets import QPushButton as QPB
from PyQt6.QtWidgets import QGridLayout as QGL
from PyQt6.QtCharts import QChartView as QCV

class SpendingWidget(QWidge):
    def __init__(self):
        super().__init__()
        self.treasury = Spending()
        self.chart = SpendingChart(self.treasury.pie_data("chart"))
        self.chart_view = QCV(self.chart)
        self.chart_view.show()

        self.purchase_input = QLE()
        self.purchase_label = QL("Purchase:")
        self.cost_input = QLE("##.##")
        self.cost_label = QL("Cost:")
        self.category_input = QLE()
        self.category_label = QL("Category:")
        self.date_input = QLE("YYYY-MM-DD")
        self.date_label = QL("Date:")

        self.add_button = QPB('add')
        self.search_button = QPB('search')
        self.rem_button = QPB('remove')

        self.trans_table = SpendingTableView()
        self.trans_model = SpendingTableModel(["Purchase", "Cost", "Category", "Date Purchased"], self.treasury.show_receipts())
        self.trans_table.setModel(self.trans_model)

        self.pie_table = PieTableView()
        self.pie_model = SpendingTableModel(["Category", "Total"], self.treasury.pie_data("table"))
        self.pie_table.setModel(self.pie_model)

        self.add_button.clicked.connect(self.add_new)
        self.search_button.clicked.connect(self.search_entries)
        self.rem_button.clicked.connect(self.rem_entry)

        grid = QGL()
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
        arg_check = self.arg_formatting("add", purchase, cost, category, date)
        print(arg_check)
        if arg_check[0] == "CODE_ERROR":
            arg_check = arg_check[1:]
            check = self.treasury.add_receipt(arg_check[0], arg_check[1], arg_check[2], arg_check[3])
            self.error_notif ("add", check, arg_check)
        else:
            self.treasury.add_receipt(arg_check[0], arg_check[1], arg_check[2], arg_check[3])
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
        arg_check = self.arg_formatting("search", purchase, cost, category, date)
        if arg_check[0] == "CODE_ERROR":
            self.error_notif("search", [], arg_check)
        else:
            self.trans_model.update_data(self.treasury.search_receipts_table(arg_check[0], arg_check[1], arg_check[2], arg_check[3]))
            pie_data = self.treasury.pie_search(arg_check[0], arg_check[1], arg_check[2], arg_check[3])
            if len(pie_data) != 2:
                self.chart.update_outer(pie_data)
                self.pie_model.update_data(pie_data)
            else:
                self.chart.update_outer(pie_data[0])
                self.pie_model.update_data(pie_data[1])

    def rem_entry(self):
        purchase = self.purchase_input.text()
        cost = self.cost_input.text()
        category = self.category_input.text()
        date = self.date_input.text()
        arg_check = self.arg_formatting("rem", purchase, cost, category, date)
        if arg_check[0] == "CODE_ERROR":
            arg_check = arg_check[1:]
        check = self.treasury.rem_entry(arg_check[0], arg_check[1], arg_check[2], arg_check[3])
        if check != None:
            return self.error_notif("rem", check, arg_check)
        else:
            self.trans_model.update_data(self.treasury.show_receipts())
            self.chart.update_outer(self.treasury.pie_data("chart"))
            self.pie_model.update_data(self.treasury.pie_data("table"))
            self.purchase_input.clear()
            self.cost_input.clear()
            self.category_input.clear()
            self.date_input.clear()

    def arg_formatting(self, func, purchase, cost, category, date):
        if cost == "##.##":
            cost = ""
        if date == "YYYY-MM-DD":
            date = ""
        args = [purchase, cost, category, date]
        errors = ["CODE_ERROR"]
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
                    val = self.date_formatting(func, args[3])
                    if val[0] == -1:
                        errors.append(val[1])
                        return errors
                    else:
                        args[3] = val[1]
            else:
                if func == "add" or func == "rem":
                    errors += args
                    return errors
        return args
    
    def date_formatting(self, func, date):
        new_date = date
        if func != "search":
            if len(new_date) != 10:
                return [-1, -3]
        if len(new_date) < 2 or new_date.count("-") > 2:
            return [-1, -3]
        if len(new_date) == 2:
            new_date = "-"+date+"-"
        new_date = new_date.split("-")
        if ("".join(new_date)).isnumeric():
            if int(new_date[1]) > 12:
                return [-1, -3]
            if len(new_date[0]) == 4 or len(new_date[1]) == 2:
                new_date = "-".join(new_date)
            else:
                return [-1, -3]
        else:
            return [-1, -3]
        return [0, new_date]

    def error_notif(self, func, error_code, arg_check):
        message = ""
        next_message = ""
        miss = 0
        if func == "add" or func == "rem":
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
                if code == -4 and func != "add":
                    message += "Date Value for Remove\n"
                    miss += 1
                if code == -4 and func != "rem" and error_code.index(-3) == -1:
                    if miss == 0:
                        message = "Too many categories, remove one or try again\n"
                    else:
                        message += "\nToo many categories, remove one or try again\n"
        if miss != 0:
                    message = "Missing: \n" + message
        for arg in arg_check:
            if arg == -2:
                next_message += "Cost Format\n"

            if arg == -3:
                next_message += "Date Format\n"
        if next_message != "":
            message += "\nErrors in Values: \n" + next_message
        
        if error_code[0] == -6:
            message = "Value does not exist, check entered values"

        if message != "":
            dlg = ErrorDialog(message)
            dlg.exec()

