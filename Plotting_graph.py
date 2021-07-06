import sys
from PyQt4 import QtGui

import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import random
from PyQt4 import QtCore

i=0
j=0
class mplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True)
        super(mplCanvas, self).__init__(figure=self.fig)
        self.setParent(parent)
        self.init_figure()

    def init_figure(self):
        pass


class CustomFigCanvas(mplCanvas):
    def __init__(self, *args, **kwargs):
        mplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateFigure)
        self.timer.start(100)

    def init_figure(self):
        global i,j
        self.values = [0]
        self.values1 = [0]
        self.xaxis1 = [i]
        self.xaxis2 = [j]
        self.ax.set_title("Realtime Waveform Plot")
        self.ax.set_xlabel("Count")
        self.ax.set_ylabel("PER")
        self.ax.axis([0, 100, 0, 100])
        self.line1 = self.ax.plot(self.xaxis1,self.values,'r')
        self.line2 = self.ax.plot(self.xaxis2,self.values1,'g')

    def addData(self):
        global i,j
        i=i+1
        if(i<20):
            self.xaxis1.append(i)
            self.values.append(random.randrange(0,100))
        else:
            j=j+1
            self.xaxis2.append(j)
            self.values1.append(random.randrange(0,100))

    def updateFigure(self):
        global i
        self.addData()
        # CurrentXAxis1 = np.arange(len(self.values1)-100, len(self.values1), 1)
        if(i<20):
            self.line1 = self.ax.plot(self.xaxis1,self.values,'r')
        else:
            self.line2 = self.ax.plot(self.xaxis2,self.values1,'g')
        self.ax.axis([0,100, 0, 100])
        self.draw()
        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_widget = QtGui.QWidget()
    l = QtGui.QVBoxLayout(main_widget)
    graph = CustomFigCanvas(main_widget)
    l.addWidget(graph)
    main_widget.show()
    sys.exit(app.exec_())