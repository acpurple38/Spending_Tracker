import PyQt6.QtCharts as QCharts
import PyQt6.QtGui as QGUI

class SpendingChart(QCharts.QChart):
    def __init__(self, data):
        super().__init__()
        self.data = data

        self.outer = QCharts.QPieSeries()
        self.set_outer()
        self.addSeries(self.outer)
    
    def set_outer(self):
        slices = []
        for d in self.data[:-1]:
            sliver = QCharts.QPieSlice(d[0], d[1], parent = None)
            sliver.setColor(QGUI.QColor("#82d3e5"))

            slices.append(sliver)
            self.outer.append(sliver)

    def update_outer(self, new_date):
        self.removeSeries(self.outer)
        self.data = new_date
        del(self.outer)
        self.outer = QCharts.QPieSeries()
        self.set_outer()
        self.addSeries(self.outer)

