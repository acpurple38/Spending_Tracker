from PyQt6.QtCharts import QChart
from PyQt6.QtCharts import QPieSeries as QPSe
from PyQt6.QtCharts import QPieSlice as QPSl
from PyQt6.QtGui import QColor as QCol

class SpendingChart(QChart):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.colors = ['#36175E', '#005f73', '#0a9396', '#94d2bd',
                '#e9d8a6', '#ee9b00',  '#ca6702', '#bb3e03',
                '#ae2012', '#9b2226', '#611619', '000000' ]

        self.outer = QPSe()
        self.set_outer()
        self.addSeries(self.outer)
        self.legend().setVisible(False)
    
    def set_outer(self):
        slices = []
        color = 0
        for d in self.data:
            sliver = QPSl(d[0], d[1], parent = None)
            sliver.setLabelVisible(True)
            sliver.setColor(QCol(self.colors[color]))
            color += 1
            if len(self.data) > len(self.colors) and color == len(self.colors):
                color = 0

            slices.append(sliver)
            self.outer.append(sliver)

    def update_outer(self, new_date):
        self.removeSeries(self.outer)
        self.data = new_date
        del(self.outer)
        self.outer = QPSe()
        self.set_outer()
        self.addSeries(self.outer)