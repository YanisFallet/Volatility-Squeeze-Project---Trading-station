from PySide6.QtWidgets import QWidget, QLineEdit, QCompleter
from PySide6.QtCore import Qt

class Widget_Search_Line(QWidget):
    def __init__(self,tickers, position, layout):
        super().__init__()
        self.completer = QCompleter(tickers)
        
        self.search_line = QLineEdit(self)
        self.search_line.setPlaceholderText("Search a ticker")
        self.search_line.setStyleSheet("QLineEdit { margin-left: 10px; }")  # Ajout de padding
        self.search_line.setCompleter(self.completer)

        self.search_line.setMaximumWidth(200)
        self.search_line.setMinimumWidth(200)
        
        layout.addWidget(self.search_line, position[0], position[1], alignment=Qt.AlignLeft)
        


