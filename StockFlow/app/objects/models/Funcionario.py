from app.config.conexao import ConexaoSqLite
from sqlite3 import Error as sqliteError
from app.config.response import Response


class Funcionario:
    def __init__(self, funId, funCpf, funNome, funTelefone, funEmail, funUf, funMunicipio, funBairro, funLogradouro, funSituacao, funLogin, funSenha, carId):
        if funId is None:
            funId = 0
        elif type(funId) is not int:
            raise Exception('Id inválido!')
        self.__funId = funId
        self.__funCpf = funCpf
        self.__funNome = funNome
        self.__funTelefone = funTelefone
        self.__funEmail = funEmail
        self.__funUf = funUf
        self.__funMunicipio = funMunicipio
        self.__funBairro = funBairro
        self.__funLogradouro = funLogradouro
        self.__funSituacao = funSituacao
        self.__funLogin = funLogin
        self.__funSenha = funSenha
        with ConexaoSqLite() as conexao:
            if not conexao:
                return Response(500, "Erro ao conectar ao banco de dados!", {})
            try:
                if (conexao.execute("select count(*) from cargo where carid = {};".format(carId))).data[0][0] == 1:
                    self.__carId = carId
                else:
                    return Response(400, "Cargo não encontrado!", {})
            except sqliteError as e:
                raise Response(500, "Erro ao buscar cargo!", e)

    def __enter__(self):
        return self

    @property
    def funId(self):
        return self.__funId

    @property
    def funCpf(self):
        return self.__funCpf

    @property
    def funNome(self):
        return self.__funNome

    @property
    def funTelefone(self):
        return self.__funTelefone

    @property
    def funEmail(self):
        return self.__funEmail

    @property
    def funUf(self):
        return self.__funUf

    @property
    def funMunicipio(self):
        return self.__funMunicipio

    @property
    def funBairro(self):
        return self.__funBairro

    @property
    def funLogradouro(self):
        return self.__funLogradouro

    @property
    def funSituacao(self):
        return self.__funSituacao

    @property
    def funLogin(self):
        return self.__funLogin

    @property
    def funSenha(self):
        return self.__funSenha

    @property
    def carId(self):
        return self.__carId

    @funId.setter
    def funId(self, funId):
        self.__funId = funId

    @funCpf.setter
    def funCpf(self, funCpf):
        self.__funCpf = funCpf

    @funNome.setter
    def funNome(self, funNome):
        self.__funNome = funNome

    @funTelefone.setter
    def funTelefone(self, funTelefone):
        self.__funTelefone = funTelefone

    @funEmail.setter
    def funEmail(self, funEmail):
        self.__funEmail = funEmail

    @funUf.setter
    def funUf(self, funUf):
        self.__funUf = funUf

    @funMunicipio.setter
    def funMunicipio(self, funMunicipio):
        self.__funMunicipio = funMunicipio

    @funBairro.setter
    def funBairro(self, funBairro):
        self.__funBairro = funBairro

    @funLogradouro.setter
    def funLogradouro(self, funLogradouro):
        self.__funLogradouro = funLogradouro

    @funSituacao.setter
    def funSituacao(self, funSituacao):
        self.__funSituacao = funSituacao

    @funLogin.setter
    def funLogin(self, funLogin):
        self.__funLogin = funLogin

    @funSenha.setter
    def funSenha(self, funSenha):
        self.__funSenha = funSenha

    @carId.setter
    def carId(self, carId):
        self.__carId = carId

    def create(self):
        with ConexaoSqLite() as conexao:
            if not conexao:
                return Response(500, "Erro ao conectar ao banco de dados!", {})
            try:
                # Verificar se o funcionario já existe
                if (conexao.execute(f"select count(*) from funcionario where funCpf = {self.__funCpf};")).data[0][0] == 0 and (conexao.execute(f"select count(*) from funcionario where funLogin = {self.__funLogin};")).data[0][0] == 0:
                    
                    query = (f"insert into funcionario (funCpf, funNome, funTelefone, funEmail, funUf, funMinicipio, funBairro, funLogradouro, funSituacao, funLogin, funSenha, carId) values (('{self.__funCpf}', '{self.__funNome}', '{self.__funTelefone}', '{self.__funEmail}', '{self.__funUf}', '{self.__funMinicipio}', '{self.__funBairro}', '{self.__funLogradouro}', '{self.__funSituacao}', '{self.__funLogin}', '{self.__funSenha}', '{self.__carId}')")
                    #conexao.execute(")
                    pass
            except:
                pass
            pass


    @classmethod
    def read(cls, empCnpj):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def __str__(self):
        return ("funId: {}\nfunCpf: {}\nfunNome: {}\nfunTelefone: {}\nfunEmail: {}\nfunUf: {}\nfunMunicipio: {}\nfunBairro: {}\nfunLogradouro: {}\nfunSituacao: {}\nfunLogin: {}\nfunSenha: {}\ncarId: {}".format(self.__funId, self.__funCpf, self.__funNome, self.__funTelefone, self.__funEmail, self.__funUf, self.__funMunicipio, self.__funBairro, self.__funLogradouro, self.__funSituacao, self.__funLogin, self.__funSenha, self.__carId))


fun = Funcionario(None, '1', 'Nome', 'Telefone', 'Email', 'UF', 'Municipio', 'Bairro', 'Logradouro', True, '1', 'Senha', 1)

fun.create()
