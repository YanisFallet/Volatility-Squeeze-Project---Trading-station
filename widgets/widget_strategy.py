from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout,QPushButton, QLineEdit, QCompleter, QTableWidget, QTableWidgetItem, QComboBox, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt

import strategies.strategies as st
from functools import partial
import json

class Widget_Strategy(QWidget):
    def __init__(self, tickers,position, layout):
        super().__init__()
        self.container = QVBoxLayout()
        self.first_row = QHBoxLayout()
        self.second_row = QHBoxLayout()
        
        self.container.setContentsMargins(0, 0, 0, 10)
        
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Add to watchlist")
        self.search_bar_completer = QCompleter(tickers)
        self.search_bar.setCompleter(self.search_bar_completer)
        
        self.first_row.addWidget(self.search_bar)
        
        self.strategy_select = QComboBox()
        self.strategy_select.addItems(self.get_list_strategies())

        self.first_row.addWidget(self.strategy_select)
        
        self.strategy_button = QPushButton("Activate Strategy")
        
        self.first_row.addWidget(self.strategy_button)
        
        self.container.addLayout(self.first_row)
        
        self.table = QTableWidget()
        self.second_row.addWidget(self.table)
        
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        
        self.second_row.addWidget(self.list_widget)
        
        self.container.addLayout(self.second_row)
        self.container.setContentsMargins(0, 0, 0, 40)
        
        layout.addLayout(self.container, position[0], position[1])
    
    
    def get_list_strategies(self):
        return st.l
    
    def activate_strategy(self):
        strategy = st.__dict__[self.strategy_select.currentText()]()
        dict_data = strategy.screener()
        if not dict_data:  # Ajout d'une vérification pour éviter le calcul inutile lorsque dict_data est vide
            return

        data = [
            (key, (values,) if not isinstance(values, (tuple, list)) else tuple(values)) 
            for key, values in dict_data.items()
        ]
        max_columns = max(len(item[1]) + 2 for item in data)

        # Fonction locale pour rendre le formatage plus concis et cohérent
        def to_str(item):
            return f"{item:.5f}" if isinstance(item, float) else str(item)

        self.table.setRowCount(len(data))
        self.table.setColumnCount(max_columns)
        
        for i, row_data in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(to_str(row_data[0]))) 
            for j, item in enumerate(row_data[1], start=1):
                self.table.setItem(i, j, QTableWidgetItem(to_str(item)))  
            
            btn = QPushButton('+')
            btn.clicked.connect(partial(self.add_to_list, row_data[0]))
            self.table.setCellWidget(i, 2, btn)

        self.table.resizeColumnsToContents()
        
    def _get_watchlist_items(self):
        return [self.list_widget.item(i).text() for i in range(self.list_widget.count())]

    def _update_watchlist_file(self):
        with open("data/watchlist.json", "w") as f:
            json.dump(self._get_watchlist_items(), f)
        
    def add_to_list(self, s: str):
        if s not in self._get_watchlist_items():
            self.list_widget.addItem(s)
            self._update_watchlist_file()
            

    def remove_tickers_from_qlist(self):
        self.list_widget.takeItem(self.list_widget.currentRow())
        self._update_watchlist_file()

    def _load_watchlist(self):
        with open("data/watchlist.json", "r") as f:
            watchlist = json.load(f)
        for ticker in watchlist:
            item = QListWidgetItem(ticker)
            item.setData(Qt.UserRole, ticker)
            self.list_widget.addItem(item)