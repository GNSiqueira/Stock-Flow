class TipoSaida:
    def __init__(self):
        self.__venda = 0 
        self.__consumo_interno = 1
        self.__perda_ou_danificacao = 2
        self.__devolucao = 3

    @property
    def venda(self):
        return self.__venda

    @property
    def consumo_interno(self):
        return self.__consumo_interno

    @property
    def perda_ou_danificacao(self):
        return self.__perda_ou_danificacao

    @property
    def devolucao(self):
        return self.__devolucao