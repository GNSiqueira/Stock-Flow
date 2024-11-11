import sys
from PySide6.QtWidgets import QApplication
from app import MainWindow
from app.config.conexao import ConexaoSqLite


if __name__ == "__main__":
    db = ConexaoSqLite()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
