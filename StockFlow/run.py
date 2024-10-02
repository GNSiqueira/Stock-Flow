import sys
from PySide6.QtWidgets import QApplication
from app import MainWindow
from app.Config.conexao import ConexaoSqLite


if __name__ == "__main__":
    db = ConexaoSqLite()
    db.conectar()
    db.create_table()
    db.dados_iniciais()
    db.desconectar()
    
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

