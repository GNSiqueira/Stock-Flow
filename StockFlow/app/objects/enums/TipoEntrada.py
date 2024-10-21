class TipoEntrada:
    def __init__(self):
        self.__compra = 0
        self.__doacao = 1
        self.__devolucao = 2
        self.producao = 3
    
    @property
    def compra(self):
        return self.__compra

    @property
    def doacao(self):
        return self.__doacao

    @property
    def devolucao(self):
        return self.__devolucao

    @property
    def producao(self):
        return self.producao