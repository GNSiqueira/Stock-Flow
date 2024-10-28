from app.config.conexao import ConexaoSqLite
from sqlite3 import Error as sqliteError
from app.config.response import Response


class Categoria:
    def __init__(self, catId, catCategoria, empCnpj):

        self.__catId = catId if catId else 0
        if not isinstance(self.__catId, int):
            raise Exception('Id deve ser inteiro!')

        self.__catCategoria = str(catCategoria).strip()

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

            # Verificar se a categoria já existe
            result = cursor.execute("SELECT count(*) FROM Categoria WHERE catCategoria = ? AND empCnpj = ?;",(self.__catCategoria, self.__empCnpj)).fetchone()
            if result[0] > 0:
                return {
                    'code': 400,
                    'msg': 'Esta categoria já existe!',
                    'data': {}
                }

            # Cadastra a categoria
            cursor.execute("INSERT INTO Categoria(catCategoria, empCnpj) VALUES (?, ?);",(self.__catCategoria, self.__empCnpj))
            conn.commit()

            # Obtém o catId da nova categoria
            self.__catId = cursor.execute("SELECT catId FROM Categoria WHERE catCategoria = ? AND empCnpj = ?;",
                                        (self.__catCategoria, self.__empCnpj)).fetchone()[0]

            return {
                'code': 200,
                'msg': 'Cadastrado com sucesso!',
                'data': {
                    'catId': self.__catId,
                    'catCategoria': self.__catCategoria,
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

            # Listando categorias da empresa
            cursor.execute("select * from categoria where empCnpj = ?;", (empCnpj,))
            result = cursor.fetchall()
            categorias = []
            for categoria in result:
                categorias.append(Categoria(*categoria))
            conn.commit()
            return Response(200, 'Categorias listadas com sucesso!', categorias)

        except(Exception, sqliteError) as error:
            conn.rollback()
            return Response(500, 'Erro ao listar categorias!', error)
        finally:
            cursor.close()
            conexao.desconectar(conn)

    def delete(self):

        conexao = ConexaoSqLite()
        response = conexao.execute("select catid, catcategoria from categoria where catcategoria = '{}' and  empCnpj = '{}';".format(self.__catCategoria, self.__empCnpj))
        if len(response.data) == 1:
            self.catId = int(response.data[0][0])
            response = conexao.execute("delete from categoria where catid = {}".format(self.__catId))
            if response.code == 200:
                return Response(200, "Categoria deletada com sucesso!", {})
            else:
                return Response(500, "Erro ao deletar categoria!", {})
        else:
            return Response(404, "Categoria não encontrada!", {})

    def update(self):
        conexao = ConexaoSqLite()
        if (conexao.execute("select count(*) from categoria where catid = {};".format( self.__catId))).data[0][0] == 1:
            if (conexao.execute("update categoria set catcategoria = '{}' where catid = {};".format(self.__catCategoria, self.__catId))).code == 200:
                return Response(200, "Categoria atualizada com sucesso!", {})
            else:
                return Response(500, "Erro ao atualizar categoria!", {})
        else:
            return Response(404, "Categoria não encontrada!", {})
    @property
    def catId(self):
        return self.__catId

    @property
    def catCategoria(self):
        return self.__catCategoria

    @property
    def empCnpj(self):
        return self.__empCnpj

    @catId.setter
    def catId(self, catId):
        self.__catId = catId

    @catCategoria.setter
    def catCategoria(self, catCategoria):
        self.__catCategoria = catCategoria

    @empCnpj.setter
    def empCnpj(self, empCnpj):
        self.__empCnpj = empCnpj

    def __str__(self):
        return f"catId: {self.__catId}\ncatCategoria: {self.__catCategoria}\nempCnpj: {self.__empCnpj}"
