from app.config.conexao import ConexaoSqLite
from sqlite3 import Error as sqliteError
from app.config.response import Response


class Cargo:
    def __init__(self, carId, carCargo, empCnpj):
        #region Formataçao de Id
        self.__carId = carId if carId else 0
        if not isinstance(self.__carId, int):
            raise Exception('Id deve ser inteiro!')
        #endregion
        #region Formataçao de Cargo
        self.__carCargo = str(carCargo).strip()
        #endregion
        #region Formataçao de CNPJ
        if  empCnpj[2] != '.' or empCnpj[6] != '.' or empCnpj[10] != '/' or empCnpj[15] != '-' or len(empCnpj) != 18:
            raise Exception('Formato de CNPJ inválido!')
        else:
            t = empCnpj.replace('.','').replace('/','').replace('-','')
            for i in t:
                if type(int(i)) != int:
                    raise Exception('Formato de CNPJ inválido!')
        self.__empCnpj = str(empCnpj)
        #endregion

    def create(self):
        with ConexaoSqLite() as conexao:
            if conexao is None:
                return Response(500, 'Erro ao conectar com o banco de dados!', {})

            try:
                if conexao.execute("select count(*) from cargo where carcargo = ? and empCnpj = ?;", (self.carCargo, self.empCnpj)).data[0][0] > 0:
                    return Response(400, 'Cargo já existente para está empresa!', {})
                query = "insert into cargo values (null, ?, ?) returning *;"
                result = conexao.execute(query, (self.__carCargo, self.__empCnpj))
                self.carId = result.data[0][0]
            except(Exception, sqliteError) as error:
                return Response(500, 'Erro ao cadastrar o cargo!', {error})
            return Response(200, 'Cargo cadastrado com sucesso!', {})

    @classmethod
    def read(cls, empCnpj):
        with ConexaoSqLite() as conexao:
            if conexao is None:
                return Response(500, 'Erro ao conectar com o banco de dados!', {})

            try:
                if conexao.execute("select count(*) from empresa where empcnpj = ?;", (empCnpj,)).data[0][0] == 0:
                    return Response(404, 'Empresa inexistente!', {})

                query = "select * from cargo where empCnpj = ?;"
                retorno = conexao.execute(query, (empCnpj,))
                cargos = []
                for cargo in retorno.data:
                    cargos.append(cls(*cargo))

            except(Exception, sqliteError) as error:
                return Response(500, 'Erro ao ler os cargos!', {error})

            return Response(200, 'Cargos lidos com sucesso!', cargos)

    def delete(self):
        with ConexaoSqLite() as conexao:
            if conexao is None:
                return Response(500, 'Erro ao conectar com o banco de dados!', {})

            try:
                if conexao.execute("select count(*) from cargo where carid = ?;", (self.__carId,)).data[0][0] == 0:
                    return Response(404, 'Cargo inexistente!', {})

                query = "delete from cargo where carid = ?;"
                conexao.execute(query, (self.carId,))

            except(Exception, sqliteError) as error:
                return Response(500, 'Erro ao deletar o cargo!', {error})

            return Response(200, 'Cargo deletado com sucesso!', {})

    def update(self):
        with ConexaoSqLite() as conexao:
            if conexao is None:
                return Response(500, 'Erro ao conectar com o banco de dados!', {})

            try:
                if conexao.execute("select count(*) from cargo where carid = ?;", (self.__carId,)).data[0][0] == 0:
                    return Response(404, 'Cargo inexistente!', {})

                query = "update cargo set carcargo = ? where carid = ? returning *;"
                cargo = conexao.execute(query, (self.__carCargo, self.__carId)).data

            except(Exception, sqliteError) as error:
                return Response(500, 'Erro ao atualizar o cargo!', {error})

            return Response(200, 'Cargo atualizado com sucesso!', cargo)

    #region Properties(Getters e Setters)
    @property
    def carId(self):
        return self.__carId

    @property
    def carCargo(self):
        return self.__carCargo

    @property
    def empCnpj(self):
        return self.__empCnpj

    @carId.setter
    def carId(self, carId):
        self.__carId = carId

    @carCargo.setter
    def carCargo(self, carCargo):
        self.__carCargo = carCargo

    @empCnpj.setter
    def empCnpj(self, empCnpj):
        self.__empCnpj = empCnpj

    def __str__(self):
        return f"carId: {self.__carId}\ncarCargo: {self.__carCargo}\nempCnpj: {self.__empCnpj}"
    #endregion
