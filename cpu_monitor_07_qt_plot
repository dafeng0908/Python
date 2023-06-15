#
# 如何產生一程序, 此程式碼將透過PyQt5建立一個基本的GUI，並使用QGraphicsScene將圖形顯示在線圖中。每1秒更新1次CPU使用率，將顯示出線圖，其長度代表所有核心的平均使用率。
#
import sys
import psutil
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('CPU Usage Monitor')
        self.setGeometry(100, 100, 800, 600)

        self.graph_points = []  # 記錄折線圖上的每個點
        self.max_points = 60  # 最多顯示60個點，即最近一分鐘的資料
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setWindowTitle('CPU Usage Monitor')
        self.view.setGeometry(100, 100, 600, 400)
        self.setCentralWidget(self.view)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # 每秒更新一次
        
    def update_graph(self):
        cpu_percent = psutil.cpu_percent(percpu=True)
        avg_usage = sum(cpu_percent) / len(cpu_percent)
        self.graph_points.append(avg_usage)
        
        # 移除折線圖上最舊的一點，以維持折線圖長度 60 點
        if len(self.graph_points) > self.max_points:
            self.graph_points.pop(0)
        
        # 清除畫布，重新繪製折線圖
        self.scene.clear()
        self.draw_graph()
        
    def draw_graph(self):
        # 設定畫筆
        pen = QPen(QColor('#0027be'))
        pen.setWidth(2)
        
        # 計算折線圖左上角和右下角的座標位置
        width = self.view.width() - 20
        height = self.view.height() - 20
        left = 10
        top = 10
        right = left + width
        bottom = top + height
        
        # 計算每個點之間的水平距離和垂直距離
        num_points = len(self.graph_points)
        if num_points == 0:
            return
        x_spacing = width / (num_points - 1)
        y_range = max(self.graph_points) - min(self.graph_points)
        if y_range == 0:
            y_range = 1
        y_per_pixel = height / y_range
        
        # 繪製 x 和 y 軸
        self.scene.addLine(left, top, left, bottom, pen)
        self.scene.addLine(left, bottom, right, bottom, pen)
        
        # 繪製平均使用率值
        font = self.scene.font()
        font.setPointSize(10)
        self.scene.setFont(font)
        txt = 'Average CPU Usage: {:.1f}%'.format(self.graph_points[-1])
        self.scene.addText(txt).setPos(left + 10, top + 10)
        
        
        # 繪製折線圖
        pen = QPen(QColor('#0077be'))
        for i in range(num_points - 1):
            x1 = left + i * x_spacing
            y1 = bottom - (self.graph_points[i] - min(self.graph_points)) * y_per_pixel
            x2 = left + (i + 1) * x_spacing
            y2 = bottom - (self.graph_points[i+1] - min(self.graph_points)) * y_per_pixel
            self.scene.addLine(x1, y1, x2, y2, pen)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())