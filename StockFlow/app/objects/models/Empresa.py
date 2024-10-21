from app.config.conexao import ConexaoSqLite
from sqlite3 import Error as sqliteError
from app.config.conexao import response


class Empresa():
    def __init__(self, empCnpj, empNome, empVendas, empTelefone, empEmail, empSenha):
        if empCnpj[2] != '.' or empCnpj[6] != '.' or empCnpj[10] != '/' or empCnpj[15] != '-' or len(empCnpj) != 18:
            print('Formato deCNPJ inválido!')
            raise Exception('Formato de CNPJ inválido')
        else:
            self.__empCnpj = empCnpj
        self.__empNome = empNome
        self.__empVendas = empVendas
        if empTelefone[0] != '(' or empTelefone[3] != ')' or empTelefone[4] != ' ' or empTelefone[10] != '-' or len(empTelefone) != 15: #(XX) XXXXX-XXXX
            print('Formato de telefone inválido!')
            raise Exception('Formato de telefone inválido')
        else:
            self.__empTelefone = empTelefone
        if '@' not in empEmail:
            print('Formato de email inválido!')
            raise Exception('Formato de email inválido')
        else:
            self.__empEmail = empEmail
        if len(empSenha) < 8:
            print('Senha muito fraca!')
            raise Exception('Senha muito fraca')
        else:
            self.__empSenha = empSenha

    @property
    def empCnpj(self):
        return self.__empCnpj

    @property
    def empNome(self):
        return self.__empNome

    @property
    def empVendas(self):
        return self.__empVendas

    @property
    def empTelefone(self):
        return self.__empTelefone

    @property
    def empEmail(self):
        return self.__empEmail

    @property
    def empSenha(self):
        return self.__empSenha

    @empCnpj.setter
    def empCnpj(self, empCnpj):
        if empCnpj[2] != '.' or empCnpj[6] != '.' or empCnpj[10] != '/' or empCnpj[15] != '-' or len(empCnpj) != 18:
            print('Formato deCNPJ inválido!')
            raise Exception('Formato de CNPJ inválido')
        else:
            self.__empCnpj = empCnpj

    @empNome.setter
    def empNome(self, empNome):
        self.__empNome = empNome

    @empVendas.setter
    def empVendas(self, empVendas):
        self.__empVendas = empVendas

    @empTelefone.setter
    def empTelefone(self, empTelefone):
        if empTelefone[0] != '(' or empTelefone[3] != ')' or empTelefone[4] != ' ' or empTelefone[10] != '-' or len(empTelefone) != 15: #(XX) XXXXX-XXXX
            print('Formato de telefone inválido!')
            raise Exception('Formato de telefone inválido')
        else:
            self.__empTelefone = empTelefone

    @empEmail.setter
    def empEmail(self, empEmail):
        if '@' not in empEmail:
            print('Formato de email inválido!')
            raise Exception('Formato de email inválido')
        else:
            self.__empEmail = empEmail

    @empSenha.setter
    def empSenha(self, empSenha):
        if len(empSenha) < 8:
            print('Senha muito fraca!')
            raise Exception('Senha muito fraca')
        else:
            self.__empSenha = empSenha

    def __str__(self):
        return f"empCnpj: {self.__empCnpj}, empNome: {self.__empNome}, empVendas: {self.__empVendas}, empTelefone: {self.__empTelefone}, empEmail: {self.__empEmail}, empSenha: {self.__empSenha} \n"

    def __repr__(self):
        return self.__str__()

    def create(self):
        conexao = ConexaoSqLite()
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()
            result = cursor.execute("insert into empresa values (?,?,?,?,?,?);", (self.__empCnpj, self.__empNome, self.__empVendas, self.__empTelefone, self.__empEmail, self.__empSenha))
            conn.commit()
            print('Empresa cadastrada com êxito!')
            return ('Empresa cadastrada com êxito!')

        except (Exception, sqliteError) as error:
            conn.rollback()
            print(error)
            print('Erro ao cadastrar a empresa!')
            return ('Erro ao cadastrar a empresa!')
        finally:
            cursor.close()
            conexao.desconectar(conn)

    @classmethod
    def read(cls):
        conexao = ConexaoSqLite()
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Empresa;")
        rows = cursor.fetchall()
        conexao.desconectar(conn)
        empresas = []
        for row in rows:
            empresa = cls(*row)
            empresas.append(empresa)
        return empresas

    @classmethod
    def read(cls, cnpj):
        conexao = ConexaoSqLite()
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()
            query = "select * from empresa where empCnpj = ?;"
            cursor.execute(query, (cnpj,))
            result = cursor.fetchone()
            if result is None:
                print('Nenhuma empresa encontrada!')
                return ('Nenhuma empresa encontrada!')
            print('Empresa encontrada com sucesso!')
            print (cls(*result))
            return cls(*result)
        except (Exception, sqliteError) as error:
            conn.rollback()
            print('Erro ao buscar em presa!')
            return ('Erro ao buscar em presa!')
        finally:
            cursor.close()
            conexao.desconectar(conn)

    def update(self):
        conexao = ConexaoSqLite()
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()
            query = "update empresa set empNome = ?, empVendas = ?, empTelefone = ?, empEmail = ?, empSenha = ? where empCnpj = ?;"
            cursor.execute(query, (self.__empNome, self.__empVendas, self.__empTelefone, self.__empEmail, self.__empSenha, self.__empCnpj))
            conn.commit()
            print('Empresa atualizada com sucesso!')
            return ('Empresa atualizada com sucesso!')
        except (Exception, sqliteError) as error:
            conn.rollback()
            print('Erro ao atualizar a empresa!')
            return ('Erro ao atualizar a empresa!')
        finally:
            cursor.close()
            conexao.desconectar(conn)

    def delete(self):
        conexao = ConexaoSqLite()
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()
            query = "delete from empresa where empCnpj = ?;"
            cursor.execute(query, (self.__empCnpj,))
            conn.commit()
            print('Empresa excluída com sucesso!')
            return ('Empresa excluída com sucesso!')
        except(Exception, sqliteError) as error:
            conn.rollback()
            print('Erro ao excluir a empresa!')
            return ('Erro ao excluir a empresa!')
        finally:
            cursor.close()
            conexao.desconectar(conn)

empresa = Empresa("12.345.678/9f12-34", "Nome dfa emfresa", True, "(11) 99999-9999", "9ffWt@example.com", "12345687")
empresa.create()
input("Pressione Enter para continuar...")
empresa.read("12.345.678/9012-34")
input("Pressione Enter para continuar...")
empresa.delete()
