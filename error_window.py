import PyQt6.QtWidgets as QWidge

class ErrorDialog(QWidge.QDialog):
    def __init__(self, error_mess):
        super().__init__()
        
        self.setWindowTitle("Error")

        ack_button = QWidge.QDialogButtonBox.StandardButton.Ok

        self.ack_button = QWidge.QDialogButtonBox(ack_button)
        self.ack_button.accepted.connect(self.accept)

        self.layout = QWidge.QVBoxLayout()
        message = QWidge.QLabel(error_mess)
        self.layout.addWidget(message)
        self.layout.addWidget(self.ack_button)
        self.setLayout(self.layout)