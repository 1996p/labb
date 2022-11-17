import sys
from PyQt5 import QtWidgets, uic
from PyQt5.Qt import *
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from solve import refraction_reflection_graph


class Canvas(FigureCanvasQTAgg):
    def __init__(self, fig, parent=None):
        super(Canvas, self).__init__(fig)


class Application(QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('main.ui', self)
        # self.resize(1366, 768)
        self.init_UI()
        self.connectUi()

    def init_UI(self):
        self.setWindowIcon(QIcon('Ok.png'))
        self.canvas = None
        self.companovka_for_mpl = QVBoxLayout(self.MplWidget)

    def connectUi(self):
        self.ui.solveBtn.clicked.connect(self.prepare_canavas_and_toolbar)
        self.ui.clearBtn.clicked.connect(self.clear_fields)

    def prepare_canavas_and_toolbar(self):
        try:

            left_border = float(self.ui.left_border.text())
            right_border = float(self.ui.right_border.text())
            eps = float(self.ui.eps.text())
        except Exception:
            self.ui.error.setText("Заполните все поля")
            return

        else:
            self.ui.error.setText('')

        if left_border >= right_border:
            self.ui.error.setText("Левая граница\nне может\nбыть меньше\nправой")
            return

        if not(0 < eps < 1):
            self.ui.error.setText("Точность\nдолжна быть\n >0 & <1")
            return

        try:
            fig = refraction_reflection_graph(self, left_border, right_border, eps)
        except ValueError:
            self.ui.error.setText("В промежутке нет корней...")
            return

        if self.canvas:
            self.companovka_for_mpl.removeWidget(self.toolbar)
            self.companovka_for_mpl.removeWidget(self.canvas)
            self.toolbar.deleteLater()
            self.canvas.deleteLater()
            self.canvas.hide()
            self.toolbar.hide()
        # +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        self.canvas = Canvas(fig)  # (self.fig)
        self.companovka_for_mpl.addWidget(self.canvas)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.companovka_for_mpl.addWidget(self.toolbar)

    def clear_fields(self):
        self.ui.eps.setText('')
        self.ui.result.setText('')
        self.ui.left_border.setText('')
        self.ui.right_border.setText('')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Application()
    mainWindow.show()
    sys.exit(app.exec_())