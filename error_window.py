from PyQt6.QtWidgets import QDialog as QD
from PyQt6.QtWidgets import QDialogButtonBox as QDBB
from PyQt6.QtWidgets import QVBoxLayout as QVBL
from PyQt6.QtWidgets import QLabel as QL

class ErrorDialog(QD):
    def __init__(self, error_mess):
        super().__init__()
        
        self.setWindowTitle("Error")

        ack_button = QDBB.StandardButton.Ok

        self.ack_button = QDBB(ack_button)
        self.ack_button.accepted.connect(self.accept)

        self.layout = QVBL()
        message = QL(error_mess)
        self.layout.addWidget(message)
        self.layout.addWidget(self.ack_button)
        self.setLayout(self.layout)