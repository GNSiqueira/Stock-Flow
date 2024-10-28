from app.config.conexao import ConexaoSqLite
from sqlite3 import Error as sqliteError
from app.config.response import Response


class Cargo:
    def __init__(self, carId, carCargo, empCnpj):

        self.__carId = carId if carId else 0
        if not isinstance(self.__carId, int):
            raise Exception('Id deve ser inteiro!')

        self.__carCargo = str(carCargo).strip()

        conexao = ConexaoSqLite()
        if (conexao.execute("select count(*) from empresa where empcnpj = '{}'".format(empCnpj))).data[0][0] > 0:
            self.__empCnpj = str(empCnpj)
        else:
            raise Exception('CNPJ inválido!')


    def create(self):
        conexao = ConexaoSqLite()
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()

            # Verificar se a cargo já existe
            result = cursor.execute("SELECT count(*) FROM Cargo WHERE carCargo = ? AND empCnpj = ?;",(self.__carCargo, self.__empCnpj)).fetchone()
            if result[0] > 0:
                return {
                    'code': 400,
                    'msg': 'Esta cargo já existe!',
                    'data': {}
                }

            # Cadastra a cargo
            cursor.execute("INSERT INTO Cargo(carCargo, empCnpj) VALUES (?, ?);",(self.__carCargo, self.__empCnpj))
            conn.commit()

            # Obtém o carId da nova cargo
            self.__carId = cursor.execute("SELECT carId FROM Cargo WHERE carCargo = ? AND empCnpj = ?;",
                                        (self.__carCargo, self.__empCnpj)).fetchone()[0]

            return {
                'code': 200,
                'msg': 'Cadastrado com sucesso!',
                'data': {
                    'carId': self.__carId,
                    'carCargo': self.__carCargo,
                    'empCnpj': self.__empCnpj
                }
            }

        except Exception as error:
            conn.rollback()
            return {
                'code': 500,
                'msg': 'Erro ao cadastrar!',
                'data': str(error)
            }
        finally:
            cursor.close()
            conexao.desconectar(conn)

    @classmethod
    def read(cls, empCnpj):
        conexao = ConexaoSqLite()
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()

            # Listando cargos da empresa
            cursor.execute("select * from cargo where empCnpj = ?;", (empCnpj,))
            result = cursor.fetchall()
            cargos = []
            for cargo in result:
                cargos.append(Cargo(*cargo))
            conn.commit()
            return Response(200, 'Cargos listadas com sucesso!', cargos)

        except(Exception, sqliteError) as error:
            conn.rollback()
            return Response(500, 'Erro ao listar cargos!', error)
        finally:
            cursor.close()
            conexao.desconectar(conn)

    def delete(self):

        conexao = ConexaoSqLite()
        response = conexao.execute("select carid, carcargo from cargo where carcargo = '{}' and  empCnpj = '{}';".format(self.__carCargo, self.__empCnpj))
        if len(response.data) == 1:
            self.carId = int(response.data[0][0])
            response = conexao.execute("delete from cargo where carid = {}".format(self.__carId))
            if response.code == 200:
                return Response(200, "Cargo deletada com sucesso!", {})
            else:
                return Response(500, "Erro ao deletar cargo!", {})
        else:
            return Response(404, "Cargo não encontrada!", {})

    def update(self):
        conexao = ConexaoSqLite()
        if (conexao.execute("select count(*) from cargo where carid = {};".format( self.__carId))).data[0][0] == 1:
            if (conexao.execute("update cargo set carcargo = '{}' where carid = {};".format(self.__carCargo, self.__carId))).code == 200:
                return Response(200, "Cargo atualizada com sucesso!", {})
            else:
                return Response(500, "Erro ao atualizar cargo!", {})
        else:
            return Response(404, "Cargo não encontrada!", {})
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
