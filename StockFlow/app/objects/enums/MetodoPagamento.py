class MetodoPagamento:

    def __init__(self):
        self.__pix = 0
        self.__dinheiro = 1
        self.__cartao_credito = 2
        self.__cartão_debito = 3
        self.__boleto = 4
        self.__cheque = 5

    @property
    def pix(self):
        return self.__pix

    @property
    def dinheiro(self):
        return self.__dinheiro

    @property
    def cartao_credito(self):
        return self.__cartao_credito

    @property
    def cartao_debito(self):
        return self.__cartão_debito

    @property
    def boleto(self):
        return self.__boleto

    @property
    def cheque(self):
        return self.__cheque