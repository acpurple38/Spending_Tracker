import sys

from main_widge import *

class SpendingWindow(QWidge.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Spending Tracker")
        self.resize(900, 800)
        self.center = SpendingWidget()
        self.setCentralWidget(self.center)

        self.show()

def main():
    app = QWidge.QApplication(sys.argv)
    ui = SpendingWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()