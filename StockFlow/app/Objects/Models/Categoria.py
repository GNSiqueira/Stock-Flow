from app.Config.conexao import ConexaoSqLite
from sqlite3 import Error as sqliteError


class Categoria():
    def __init__(self, catId, catCategoria, empCnpj):
        self.__catId = catId if catId else 0
        if not isinstance(self.__catId, int):
            raise Exception('Id deve ser inteiro!')

        self.catCategoria = catCategoria
        self.empCnpj = empCnpj

    def create(self):
        conexao = ConexaoSqLite()
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()

            # Verifica se a empresa existe na base de dados
            result = cursor.execute("select count(*) from empresa where empCnpj = ?;", (self.__empCnpj,)).fetchone()
            if result[0] == 0:
                return {
                    'code' : 400,
                    'msg' : 'Empresa não cadastrada!',
                    'data' : {}
                }

            # Verificar se a categoria já existe
            result = cursor.execute("select count(*) from categoria where catCategoria = ? and empCnpj = ?;", (self.__catCategoria, self.__empCnpj)).fetchone()
            if result[0] > 0:
                return  {
                    'code' : 400,
                    'msg' : 'Está categoria já existe!',
                    'data' : {}
                }

            # Cadastra a categoria
            cursor.execute("insert into categoria(catCategoria, empCnpj) values ( ?, ?);", (self.__catCategoria, self.__empCnpj))
            conn.commit()
            return  {
                'code' : 200,
                'msg' : 'Cadastrado com sucesso!',
                'data' : {
                    'catId' : self.__catId,
                    'catCategoria' : self.__catCategoria,
                    'empCnpj' : self.__empCnpj
                }
            }

        except(Exception, sqliteError) as error:
            conn.rollback()
            return {
                'code' : 500,
                'msg' : 'Erro ao cadastrar!',
                'data' : error
            }
        finally:
            cursor.close()
            conexao.desconectar(conn)


    def read(self):
        pass

    def read(self, id: int):
        pass

    def read(self,  categoria: str):
        pass

    def delete(self):
        pass

    def update(self):
        pass

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

cat = Categoria(None, 'Alimento', '00.000.000/0001-91')
print(cat)
print(cat.create()['msg'])

