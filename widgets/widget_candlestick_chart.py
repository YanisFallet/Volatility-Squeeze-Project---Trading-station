from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollBar
from PySide6.QtCharts import QChart, QChartView, QCandlestickSeries, QCandlestickSet
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QWheelEvent

import yfinance as yf
from datetime import datetime

class MyChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)
        self.scrollbar = None  # Will be set from outside

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.scrollbar:
            delta = event.angleDelta().y()
            if delta > 0:  # Scrolled up
                self.scrollbar.setValue(self.scrollbar.value() - 8)
            elif delta < 0:  # Scrolled down
                self.scrollbar.setValue(self.scrollbar.value() + 8)


class Widget_candlestick_chart(QWidget):
    def __init__(self, ticker, mode, position, layout, max_candles=10):
        super().__init__()
        
        self.ticker = ticker
        self.mode = mode

        self.max_candles = max_candles
        self.data = None  # Pour stocker les données

        self.container = QVBoxLayout()

        self.chart = QChart()
        self.chart.setTitle(f"{mode} Chart for {ticker}")
        self.chart.legend().hide()
        # self.chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.slider = QScrollBar(Qt.Horizontal)
        self.slider.setMinimum(0)

        self.chart_view = MyChartView(self.chart)
        self.chart_view.scrollbar = self.slider

        self.container.addWidget(self.chart_view)

        

        # Connectez la barre de défilement au slot de mise à jour
        self.slider.valueChanged.connect(self.update_plot)

        self.container.addWidget(self.slider)

        layout.addLayout(self.container, position[0], position[1])

    def plot_data(self, data):
        # Sauvegardez les données pour une utilisation ultérieure
        self.data = data
        self.chart.setTitle(f"{self.mode} Chart for {self.ticker}")
        self.slider.setMaximum(data.shape[0] - self.max_candles)
        self.slider.setValue(data.shape[0] - 5*self.max_candles)
        self.update_plot(self.slider.value())

    def update_plot(self, start_index):
        self.chart.removeAllSeries()

        self.candelstick_series = QCandlestickSeries()
        self.candelstick_series.setDecreasingColor(Qt.red)
        self.candelstick_series.setIncreasingColor(Qt.green)

        data_subframe = self.data.iloc[start_index:]
        for date, day_data in data_subframe.iterrows():
            candlestick_set = QCandlestickSet(day_data['Open'], day_data['High'], day_data['Low'], day_data['Close'],
                                              QDateTime(date).toSecsSinceEpoch())
            self.candelstick_series.append(candlestick_set)

        self.chart.addSeries(self.candelstick_series)
        self.chart.createDefaultAxes()
        
    def real_time_data(self):
        now = datetime.now()
        if is_market_open_europe(now):
            current_data = yf.download(tickers = self.ticker, start=now.today(), end=now)
            print(current_data)
            pass
        else:
            return 

def is_market_open_europe(date : datetime):
    if date.weekday() >= 5 or date.time() < datetime.time(9,0) or date.time() > datetime.time(17,35):
        return False
    else : return True
        
    
        
            
    
