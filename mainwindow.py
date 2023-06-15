from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget

import utilities as ut
from database_management.update_database import load_symbols

from widgets.widget_extra_charts import Widget_extra_charts
from widgets.widget_search_line import Widget_Search_Line
from widgets.widget_btn_databases import Widget_btn_databases
from widgets.widget_strategy import Widget_Strategy
from widgets.widget_candlestick_chart import Widget_candlestick_chart

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Trading App")
        
        self.tickers = load_symbols()
        
        # Initialisation des widgets de l'interface utilisateur
        self.init_ui()

        self.strategy_widget._load_watchlist()
        
        self.on_ticker_selected("MC.PA")
        
        # Connexion des signaux et slots
        self.strategy_widget.strategy_button.clicked.connect(self.strategy_widget.activate_strategy)

        self.strategy_widget.list_widget.itemDoubleClicked.connect(self.strategy_widget.remove_tickers_from_qlist)

        self.strategy_widget.list_widget.itemSelectionChanged.connect(
            lambda: self.on_ticker_selected(self.strategy_widget.list_widget.currentItem().text())
        )
        
        self.strategy_widget.search_bar_completer.activated.connect(self.strategy_widget.add_to_list)

        self.strategy_widget.search_bar.returnPressed.connect(
            lambda: self.strategy_widget.add_to_list(self.strategy_widget.search_bar.text())
        )
        
        self.strategy_widget.table.itemSelectionChanged.connect(
            lambda: self.on_ticker_selected(self.strategy_widget.table.selectedItems()[0].text())                                                        
        )

        self.btn_database_widget.update_button.clicked.connect(self.btn_database_widget.update_database)

        self.search_line.search_line.returnPressed.connect(
            lambda: self.on_ticker_selected(self.search_line.search_line.text())
        )

  

    def init_ui(self):
        central_widget = QWidget()
        layout = QGridLayout(central_widget)

        self.search_line = Widget_Search_Line(tickers=self.tickers, position=(0,0), layout=layout)
        
        self.btn_database_widget = Widget_btn_databases(tickers=self.tickers, position=(0,1), layout=layout)
        
        self.chart_daily = Widget_candlestick_chart(ticker="MC.PA", mode="Daily", position=(1,0), layout=layout)
        
        self.chart_weekly = Widget_candlestick_chart(ticker="MC.PA", mode="Weekly", position=(2,0), layout=layout)
        
        self.strategy_widget = Widget_Strategy(tickers=self.tickers, position=(1,1), layout=layout)
        
        self.extra_chart = Widget_extra_charts(position=(2,1), layout=layout)

        self.setCentralWidget(central_widget)

    def on_ticker_selected(self, ticker):
        self.chart_daily.ticker = ticker
        self.chart_weekly.ticker = ticker
        
        self.data = ut.get_stock_data(ticker=ticker)
        self.chart_daily.plot_data(self.data)
        df_weekly = ut.daily_to_weekly(self.data)
        self.chart_weekly.plot_data(df_weekly)

        
    
                    
        