from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtCore import Qt

from database_management.update_database import update_data

class Widget_btn_databases(QWidget):
    def __init__(self,tickers, position, layout):
        super().__init__()
        
        self.tickers = tickers
        self.update_button = QPushButton("Update Databases")
        self.update_button.setMaximumWidth(150)
        
        layout.addWidget(self.update_button, position[0], position[1], alignment=Qt.AlignRight)

    def update_database(self):
        update_data(self.tickers)
        print("Database updated")