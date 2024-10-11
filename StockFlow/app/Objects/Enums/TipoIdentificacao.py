class TipoIdentificacao: 
    def __init__(self):
        self.__cnpj = 0
        self.__cpf = 1

    @property
    def cnpj(self):
        return self.__cnpj

    @property
    def cpf(self):
        return self.__cpf