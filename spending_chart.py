import PyQt6.QtCharts as QCharts
import PyQt6.QtGui as QGUI
import random

class SpendingChart(QCharts.QChart):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.colors = ["#36175E", '#005f73', '#0a9396', '#94d2bd',
                '#e9d8a6', '#ee9b00',  '#ca6702',
                '#bb3e03', '#ae2012', '#9b2226']


        self.outer = QCharts.QPieSeries()
        self.set_outer()
        self.addSeries(self.outer)
    
    def set_outer(self):
        slices = []
        color = 0
        for d in self.data[:-1]:
            sliver = QCharts.QPieSlice(d[0], d[1], parent = None)
            sliver.setColor(QGUI.QColor(self.colors[color]))
            color += 1

            slices.append(sliver)
            self.outer.append(sliver)

    def update_outer(self, new_date):
        self.removeSeries(self.outer)
        self.data = new_date
        del(self.outer)
        self.outer = QCharts.QPieSeries()
        self.set_outer()
        self.addSeries(self.outer)