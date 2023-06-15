from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLineEdit, QHBoxLayout, QScrollBar
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtCore import Qt

class Widget_extra_charts(QWidget):
    def __init__(self,position,layout):
        super().__init__()
        
        self.container = QVBoxLayout()
        self.container.setContentsMargins(0, 5, 0, 0)
        
        self.extra_chart = QChart()
        self.extra_chart.setTitle("Extra Chart")
        self.extra_chart.legend().hide()
        
        
        self.extra_series = QLineSeries()
        self.extra_series.append(0, 0)
        self.extra_series.append(1, 1)
        self.extra_series.append(2, 3)
        
        
        self.extra_chart.addSeries(self.extra_series)
        self.extra_chart.createDefaultAxes()
        
        self.extra_chart_view = QChartView(self.extra_chart)
        
        self.last_row = QHBoxLayout()
        
        self.chart_type = QComboBox()
        self.chart_type.addItems(["Line", "Candlestick", "Bar", "Area", "Spline", "Scatter"])
        
        self.qline_parameters = QLineEdit(self)
        
        self.last_row.addWidget(self.qline_parameters)
        self.last_row.addWidget(self.chart_type)
        
        self.scrollbar = QScrollBar(Qt.Horizontal)
        self.scrollbar.setMaximum(100)
        self.scrollbar.setMinimum(0)
        
        self.container.addLayout(self.last_row)
        self.container.addWidget(self.extra_chart_view)
        self.container.addWidget(self.scrollbar)
        
        layout.addLayout(self.container, position[0], position[1])
        
        
        