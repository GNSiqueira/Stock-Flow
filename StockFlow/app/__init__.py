from PySide6.QtWidgets import QMainWindow, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.MyWidget = QWidget()

        self.setCentralWidget(self.MyWidget)

        self.show()


