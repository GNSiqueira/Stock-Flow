from app.config.conexao import ConexaoSqLite
from sqlite3 import Error as sqliteError
from app.config.response import Response


class Funcionario:
    def __init__(self, funId: int, funCpf: str, funNome: str, funTelefone: str, funEmail: str, funUf, funMunicipio, funBairro, funLogradouro, funSituacao, funLogin, funSenha, carId) -> None:
        #region Formataçao de Id
        if funId is None:
            funId = 0
        elif type(funId) is not int:
            raise ValueError('Id inválido!')
        self.__funId = funId
        #endregion
        #region Formataçao de CPF
        if len(funCpf) !=  14 or funCpf[3] != '.' or funCpf[7] != '.' or funCpf[11] != '-': # 000.000.000-00
            raise ValueError('Cpf inválido!')
        t =  funCpf.replace('.', '').replace('-', '') # 00000000000
        for i in t:
            if not i.isnumeric():
                raise ValueError('Cpf inválido!')
        self.__funCpf = funCpf
        #endregion
        #region Formataçao de Nome
        if len(funNome) < 3:
            raise ValueError('Nome inválido!')
        self.__funNome = funNome
        #endregion
        #region Formataçao de Telefone
        if funTelefone[0] != '(' or funTelefone[3] != ')' or funTelefone[4] != ' ' or funTelefone[10] != '-' or len(funTelefone) != 15: #(XX) XXXXX-XXXX
            raise ValueError('Telefone inválido!')
        t = funTelefone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '') # XXXXXXXXXX
        for i in t:
            if not i.isnumeric():
                print(i)
                raise ValueError('Telefone inválido!')
        self.__funTelefone = funTelefone
        #endregion
        #region Formataçao de Email
        if '@' not in funEmail:
            raise ValueError('Email invático!')
        self.__funEmail = funEmail
        #endregion
        #region Formataçao de UF
        if len(funUf) != 2:
            raise ValueError('Uf inválida!')
        self.__funUf = funUf
        #endregion
        #region Formataçao de Municipio
        if len(funMunicipio) < 3:
            raise ValueError('Municipio inválido!')
        self.__funMunicipio = funMunicipio
        #endregion
        #region Formataçao de Bairro
        if len(funBairro) < 3:
            raise ValueError('Bairro inválido!')
        self.__funBairro = funBairro
        #endregion
        #region Formataçao de Logradouro
        if len(funLogradouro) < 3:
            raise ValueError('Logradouro invático!')
        self.__funLogradouro = funLogradouro
        #endregion
        #region Formataçao de Situação
        if funSituacao != 0 and funSituacao != 1:
            raise ValueError('Situação inválida!')
        self.__funSituacao = funSituacao
        #endregion
        #region Formataçao de Login
        for i in str(funLogin):
            if i.isupper():
                raise ValueError('Login inválido!')
        self.__funLogin = funLogin
        #endregion
        #region Formataçao de Senha
        if len(funSenha) < 8:
            raise ValueError('Senha inválida!')
        self.__funSenha = funSenha
        #endregion
        #region Formataçao de Cargo
        with ConexaoSqLite() as conexao:
            if not conexao:
                erro = True
            try:
                if (conexao.execute("select count(*) from cargo where carid = {};".format(carId))).data[0][0] == 1:
                    self.__carId = carId
                else:
                    raise Exception('Cargo inválido!')
            except sqliteError as e:
                pass
        #endregion

    #region Propriedades(Getters e Setters)
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
    #endregion

    def create(self) -> Response:
        with ConexaoSqLite() as conexao:
            if not conexao:
                return Response(500, "Erro ao conectar ao banco de dados!", {})

            try:
                cpf_exists = conexao.execute("SELECT count(*) FROM funcionario WHERE funCpf = ?;", (self.__funCpf,)).data[0][0]
                login_exists = conexao.execute("SELECT count(*) FROM funcionario WHERE funLogin = ?;", (self.__funLogin,)).data[0][0]


                # Verificar se o funcionario já existe
                if cpf_exists == 0 and login_exists == 0:
                    query = """
                        INSERT INTO Funcionario (
                            funCpf,
                            funNome,
                            funTelefone,
                            funEmail,
                            funUf,
                            funMunicipio,
                            funBairro,
                            funLogradouro,
                            funSituacao,
                            funLogin,
                            funSenha,
                            carId
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    info = (
                        self.__funCpf,
                        self.__funNome,
                        self.__funTelefone,
                        self.__funEmail,
                        self.__funUf,
                        self.__funMunicipio,
                        self.__funBairro,
                        self.__funLogradouro,
                        self.__funSituacao,
                        self.__funLogin,
                        self.__funSenha,
                        self.__carId
                    )
                    conexao.execute(query, info)
                    self.funId = conexao.cursor.lastrowid
                else:
                    return Response(400, "Funcionário já existe!", {})
            except(Exception, sqliteError) as error:
                return Response(500, "Erro ao criar o funcionário!", {error})

            return Response(200, "Funcionário criado com sucesso!", {})

    def read(cnpj: str = None) -> Response:
        with ConexaoSqLite() as conexao:
            if not conexao:
                return Response(500, "Erro ao conectar ao banco de dados!", {})

            try:
                query = f"select f.* from funcionario f inner join cargo c on f.carId = c.carId where c.empCnpj = '{cnpj}';"

                result = conexao.execute(query)

                funcionarios = []
                for row in result.data:
                    funcionarios.append(Funcionario(*row))

            except(Exception, sqliteError) as error:
                return Response(500, "Erro ao ler os funcionários!", {error})
            return Response(200, "Funcionários lidos com sucesso!", funcionarios)

    def read_by_id(id: int) -> Response:
        with ConexaoSqLite() as conexao:
            if not conexao:
                return Response(500, "Erro ao conectar ao banco de dados!", {})

            try:
                query = f"select * from funcionario where funId = {id};"
                result = conexao.execute(query)
                result = Funcionario(*result.data[0])
            except(Exception, sqliteError) as error:
                return Response(500, "Erro ao ler o funcionário!", {error})
            return Response(200, "Funcionário lido com sucesso!", result)

    def delete(self) -> Response:
        with ConexaoSqLite() as conexao:
            if not conexao:
                return Response(500, "Erro ao conectar ao banco de dados!", {})

            try:
                query = f"delete from funcionario where funId = {self.funId};"
                conexao.execute(query)

            except(Exception, sqliteError) as error:
                return Response(500, "Erro ao excluir o funcionário!", {error})

            return Response(200, "Funcionário excluído com sucesso!", {})

    def update(self) -> Response:
        with ConexaoSqLite() as conexao:
            if not conexao:
                return Response(500, "Erro ao conectar ao banco de dados!", {})

            try:
                query = f"""
                    UPDATE funcionario
                    SET
                        funCpf = '{self.__funCpf}',
                        funNome = '{self.__funNome}',
                        funTelefone = '{self.__funTelefone}',
                        funEmail = '{self.__funEmail}',
                        funUf = '{self.__funUf}',
                        funMunicipio = '{self.__funMunicipio}',
                        funBairro = '{self.__funBairro}',
                        funLogradouro = '{self.__funLogradouro}',
                        funSituacao = '{self.__funSituacao}',
                        funLogin = '{self.__funLogin}',
                        funSenha = '{self.__funSenha}',
                        carId = '{self.__carId}'
                    WHERE
                        funId = {self.__funId}
                """
                conexao.execute(query)

            except(Exception, sqliteError) as error:
                return Response(500, "Erro ao atualizar o funcionário!", {error})

            return Response(200, "Funcionário atualizado com sucesso!", {})
