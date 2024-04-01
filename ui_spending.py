from sys import exit as sysexit
from sys import argv as sysargv
from main_widge import *
from PyQt6.QtWidgets import QMainWindow as QMW
from PyQt6.QtWidgets import QApplication as QApp

class SpendingWindow(QMW):
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
    app = QApp(sysargv)
    ui = SpendingWindow()
    sysexit(app.exec())

if __name__ == "__main__":
    main()