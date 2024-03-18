import sqlite3
import datetime

class Spending():
    def __init__(self):
        self.treasury = self.open_tracker()
        self.treasurer = self.treasury.cursor()
        self.list_tables = []
        self.categories = []
        self.open_cat = True
        try:
            self.list_tables.append(self.treasurer.execute("SELECT * from Receipts").fetchall())
        except sqlite3.OperationalError:
            self.list_tables.append(self.treasurer.execute("""CREATE TABLE Receipts(Purchase TEXT, Cost REAL,
            Category TEXT, Date TEXT);""").fetchall())

        self.find_cats()

    def open_tracker(self):
        con = None
        try:
            con = sqlite3.connect("spending.db")
            return con
        except:
            print(sqlite3.Error)

    def add_receipt(self, purchase, cost, category, date):
        if purchase == "" or cost == "" or category == "":
            return -1
        if self.open_cat == False and category not in self.categories:
            return -2
        if date == "":
            date = str(datetime.date.today())
        self.treasurer.execute("INSERT INTO Receipts VALUES(?, ?, ?, ?)", (purchase, cost, category, date))
        self.treasury.commit()

    def search_command(self, purchase, cost, category, date, use): #use is either "table" or "chart"
        search_terms = [purchase, cost, category, date]
        search_tuple = ()
        search_cats = ["Purchase", "Cost", "Category", "Date"]
        i = 0
        while i < len(search_terms):
            if search_terms[i] != "":
                search_tuple = search_tuple + (search_terms[i],)
                i += 1
            else:
                search_terms.pop(i)
                search_cats.pop(i)
        if i == 0:
                return -1
        else:
            command = "SELECT "
            if use == "table":
                command += "*" 
            if use == "chart":
                command += "DISTINCT Category"
            command += " FROM Receipts WHERE"
        for i in range(len(search_terms)):
            command += f' {search_cats[i]} LIKE ("%" || ? || "%")'
            if i < len(search_cats) - 1:
                command += " AND "
        command += "ORDER BY Date DESC"
        return [command, search_tuple]
        
    def search_receipts_table(self, purchase, cost, category, date):
        command = self.search_command(purchase, cost, category, date, "table")
        if command == -1:
            return self.treasurer.execute("SELECT * FROM Receipts ORDER BY Date DESC").fetchall()
        self.treasurer.execute(command[0], command[1])
        return self.treasurer.fetchall()
    
    def pie_search(self, purchase, cost, category, date):
        command = self.search_command(purchase, cost, category, date, "chart")
        if command == -1:
            return self.pie_data("chart")
        categories = self.treasurer.execute(command[0], command[1]).fetchall()
        print(categories)
        for i in range(len(categories)):
            categories[i] = categories[i][0]
        data = []
        for i in range(len(categories)):
            search_tuple = (categories[i], ) + command[1]
            self.treasurer.execute("SELECT sum(Cost) FROM Receipts WHERE Category LIKE ('%' || ? || '%')" 
                                   + " AND " +command[0][command[0].index("WHERE")+6:], search_tuple)
            cat_cost = self.treasurer.fetchone()
            cat_cost = cat_cost[0]
            data.append([categories[i], int(cat_cost)])
        return data
    
    def rem_entry(self, purchase, cost, category, date):
        if purchase == "" and cost == "" and category == "" and date == "":
            return
        self.treasurer.execute("""DELETE FROM Receipts WHERE Purchase LIKE ('%' || ? || '%') AND
                               Cost LIKE ('%' || ? || '%') AND Category LIKE ('%' || ? || '%') AND Date LIKE ('%' || ? || '%')""", (purchase, cost, category, date))
        self.treasury.commit()

    def show_receipts(self):
        self.treasurer.execute("SELECT * FROM Receipts ORDER BY Date DESC")
        data = self.treasurer.fetchall()
        return data
    
    def pie_data(self, use): #use is either chart or table, don't want total to appear in chart
        data = []
        self.find_cats()
        for cat in self.categories:
            self.treasurer.execute("SELECT sum(Cost) FROM Receipts WHERE Category LIKE ('%' || ? || '%')", (cat,))
            cat_cost = self.treasurer.fetchone()
            cat_cost = cat_cost[0]
            data.append([cat, int(cat_cost)])
        self.treasurer.execute("SELECT sum(Cost) FROM Receipts")
        tot_cost = self.treasurer.fetchone()
        tot_cost = tot_cost[0]
        if use == "table":
            data.append(["Total",int(tot_cost)])
        return data
    
    def find_cats(self):
        self.categories = self.treasurer.execute("SELECT DISTINCT Category from Receipts").fetchall()
        for i in range(len(self.categories)):
            self.categories[i] = self.categories[i][0]
        if len(self.categories) < 10:
            self.open_cat = True
        else:
            self.open_cat = False