from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollBar
from PySide6.QtCharts import QChart, QChartView, QCandlestickSeries, QCandlestickSet
from PySide6.QtCore import Qt, QDateTime

class Widget_candlestick_chart(QWidget):
    def __init__(self,ticker,mode, position, layout, max_candles = 100):
        super().__init__()
        
        self.max_candles = max_candles
        
        self.container = QVBoxLayout()
        
        self.chart = QChart()
        self.chart.setTitle(f"{mode} Chart for {ticker}")
        self.chart.legend().hide()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        
        self.chart_view = QChartView(self.chart)
        
        self.container.addWidget(self.chart_view)
        
        self.slider = QScrollBar(Qt.Horizontal)
        self.slider.setMinimum(0)
              
        self.container.addWidget(self.slider)
        
        layout.addLayout(self.container, position[0], position[1])
        
    def plot_data(self, data, start_index):   
        self.chart.removeAllSeries()
                
        self.slider.setMaximum(data.shape[0] - self.max_candles)
        self.slider.setValue(data.shape[0] - self.max_candles)
            
        self.candelstick_series = QCandlestickSeries()
        self.candelstick_series.setDecreasingColor(Qt.red)
        self.candelstick_series.setIncreasingColor(Qt.green)
                
        data_subframe = data.iloc[start_index:]
        for date, day_data in data_subframe.iterrows():
            candlestick_set = QCandlestickSet(day_data['Open'], day_data['High'], day_data['Low'], day_data['Close'], QDateTime(date).toSecsSinceEpoch())
            self.candelstick_series.append(candlestick_set)
        self.chart.addSeries(self.candelstick_series)
        self.chart.createDefaultAxes()

            
    
