class ARG_Checker:
    def __init__(self):
        self.purchase = ""
        self.cost = ""
        self.category = ""
        self.date = ""
        self.func = ""
        self.message = ""

    def set_vals(self, func, purchase, cost, category, date):
        self.purchase = purchase
        self.cost = cost
        self.category = category
        self.date = date
        self.func = func

    # def check(self):

