class TipoProduto: 
    def __init__(self):
        self.__kit = 0
        self.__simples = 1
        self.__fabricacao = 2
        self.__materia_prima = 3

    @property
    def kit(self):
        return self.__kit

    @property
    def simples(self):
        return self.__simples

    @property
    def fabricacao(self):
        return self.__fabricacao

    @property
    def materia_prima(self):
        return self.__materia_prima