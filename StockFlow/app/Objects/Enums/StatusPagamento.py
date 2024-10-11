class StatusPagamento: 
    def __init__(self):
        self.__pago = 0 
        self.__antecipado = 1
        self.__pendente = 2
        self.__atrasado = 3

    @property
    def pago(self):
        return self.__pago

    @property
    def antecipado(self):
        return self.__antecipado

    @property
    def pendente(self):
        return self.__pendente

    @property
    def atrasado(self):
        return self.__atrasado