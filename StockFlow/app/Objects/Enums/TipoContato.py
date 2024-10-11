class TipoContato:
    def __init__(self):
        self.__fornecedor = 0
        self.__cliente = 1
    
    @property
    def fornecedor(self):
        return self.__fornecedor
    
    @property
    def cliente(self):
        return self.__cliente