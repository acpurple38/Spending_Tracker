import PyQt6.QtCore as QCore
import PyQt6.QtWidgets as QWidge

class SpendingTableModel(QCore.QAbstractTableModel):
    def __init__(self, table_data = None, parent = None):
        super().__init__()

        if table_data is None:
            table_data = [["", "", ""]]
        
        self.table_data = table_data

        self.headers = ["Purchase", "Cost", "Category", "Date Purchased"]
        
        # self.sort_changed_signal = QCore.pyqtSignal(int, int)
    
    def rowCount(self, parent = None, *args, **kwargs):
        return len(self.table_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.headers)

    def headerData(self, section, orientation, role = None):
        if role == QCore.Qt.ItemDataRole.DisplayRole and orientation == QCore.Qt.Orientation.Horizontal:
            return self.headers[section]
        
    def data(self, index, role = None):
        if role == QCore.Qt.ItemDataRole.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.table_data[row][column]
            return value
        
    def update_data(self, new_data):
        self.layoutAboutToBeChanged.emit()
        self.table_data = new_data
        self.layoutChanged.emit()

class SpendingTableView(QWidge.QTableView):
    def __init__(self):
        super().__init__()
        self.setVisible(True)

    def resizeEvent(self, event):
        width = event.size().width()
        self.setColumnWidth(0, int(width * 0.30))
        self.setColumnWidth(1, int(width * 0.20))
        self.setColumnWidth(2, int(width * 0.25))
        self.setColumnWidth(3, int(width * 0.25))