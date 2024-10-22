from psycopg2 import connect, Error
import sqlite3 as sqlite
from sqlite3 import Error as sqliteError
from app.config.response import Response

class Conexao():
    def conectar(self):
        try:
            conn = connect(
                host="localhost",
                database="StockFlow",
                user="postgres",
                password="123456"
            )
            return conn

        except (Exception, Error) as error:
            return ('Erro ao conectar ao banco de dados!')

    def desconectar(self, conn):
        try:
            if conn is not None:
                conn.close()
                return ('Conexão fechada com sucesso!')

        except (Exception, Error) as error:
            return ('Erro ao fechar a conexão!')
class ConexaoSqLite():
    def __init__(self, database = 'StockFlow.db') -> None:
        self.database = database

    def conectar(self):
        try:
            conn = sqlite.connect(self.database)
            return conn

        except (Exception, sqliteError) as error:
            return {
                'code': 500,
                'msg': ('Erro ao conectar ao banco de dados: ', error)
            }

    def desconectar(self, conn):
        try:
            if conn is not None:
                conn.close()
                return{
                    'code':200,
                    'msg':'Conexão fechada com sucesso!'
                }
        except (Exception, sqliteError) as error:
            return {
                'code':500,
                'msg':('Erro ao fechar a conexão:', error)
            }

    def execute(self, query):
        conn = self.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()
            return Response(200, 'Executado com sucesso!', result)
        except(Exception, Error) as error:
            conn.rollback()
            return Response(500, 'Erro ao executar!', error)
        finally:
            cursor.close()
            self.desconectar(conn)

    def create_table(self):
        try:
            conn = self.conectar()
            self.cursor = conn.cursor()
            self.cursor.executescript("""
-- Tabela Empresa
create table if not exists Empresa (
    empCnpj varchar(18) unique,
    empNome varchar(100) unique,
    empVendas boolean,
    empTelefone varchar(15),--(XX) XXXXX-XXXX
    empEmail varchar(120) unique,
    empSenha varchar(255),
    constraint pk_empresa primary key (empCnpj)
);

-- Tabela Cargo
create table if not exists Cargo (
    carId integer primary key autoincrement,
    carCargo varchar(50),
    empCnpj varchar(18),
    constraint fk_cargo_empresa foreign key (empCnpj) references Empresa(empCnpj)
);

-- Tabela Funcionario
create table if not exists Funcionario (
    funId integer primary key autoincrement,
    funCpf varchar(14) unique,--XXX.XXX.XXX-XX
    funNome varchar(100),
    funTelefone varchar(15) unique,
    funEmail varchar(100) unique,
    funUf varchar(2),
    funMunicipio varchar(100),
    funBairro varchar(100),
    funLogradouro varchar(150),
    funSituacao boolean,
    funLogin varchar(50) unique,
    funSenha varchar(255),
    carId integer,
    constraint fk_funcionario_cargo foreign key (carId) references Cargo(carId)
);

-- Tabela Categoria
create table if not exists Categoria (
    catId integer primary key autoincrement,
    catCategoria varchar(50) unique,
    empCnpj varchar(18),
    constraint fk_categoria_empresa foreign key (empCnpj) references Empresa(empCnpj)
);

-- Tabela Produto
create table if not exists Produto (
    proId integer primary key autoincrement,
    proDescricao varchar(255),
    proCodigo varchar(15),
    proCodigoBarra varchar(13),
    proTipo integer, -- Ex: Kit, Simples, Fabricado, Com variação
    proUnidade varchar(10), --Ex: Mg, L, Kg
    proPrecoVenda numeric(10, 2),
    proPrecoMedio numeric(10, 2),
    proPeso numeric(10, 3),
    proLargura numeric(10, 2),
    proAltura numeric(10, 2),
    proComprimento numeric(10, 2),
    proEstoque integer,
    proEstoqueMin integer,
    proEstoqueMax integer,
    proLocalizacao varchar(100),
    proControleLote boolean,
    catId integer,
    constraint fk_produto_categoria foreign key (catId) references Categoria(catId)
);

-- Tabela Contato
create table if not exists Contato (
    conId integer primary key autoincrement,
    conNome varchar(100),
    conTelefone varchar(15) unique,
    conEmail varchar(100) UNIQUE,
    conTipo integer,
    conIdentificacaoNumero varchar(18), --00.000.000/0000-00  000.000.000-00
    conIdentificacao integer,
    conCep varchar(9),
    conUf varchar(2),
    conMunicipio varchar(100),
    conBairro varchar(100),
    conLogradouro varchar(150)
);

-- Tabela Fornecedor
create table if not exists Fornecedor (
    fornIdProduto integer,
    fornIdContato integer,
    fornPrincipal boolean,
    constraint pk_fornecedor primary key (fornIdProduto, fornIdContato),
    constraint fk_fornecedor_produto foreign key (fornIdProduto) references Produto(proId),
    constraint fk_fornecedor_contato foreign key (fornIdContato) references Contato(conId)
);

-- Tabela Lote
create table if not exists Lote (
    lotId integer primary key autoincrement,
    lotCodigo varchar(50),
    lotQuantidade integer,
    lotMarca varchar(50),
    lotFabricacao date,
    lotValidade date,
    lotStatus boolean,
    proId integer,
    constraint fk_lote_produto foreign key (proId) references Produto(proId)
);

-- Tabela Entrada
create table if not exists Entrada (
    entId integer primary key autoincrement,
    entData date,
    entHora time,
    entObservacao text,
    entTipo integer,
    entValorTotal numeric(10, 2),
    funId integer,
    constraint fk_entrada_funcionario foreign key (funId) references Funcionario(funId)
);

-- Tabela ItemEntrada
create table if not exists ItemEntrada (
    itemIdEntrada integer,
    itemIdLote integer,
    itemQuantidade integer,
    itemPrecoUnit numeric(10, 2),
    constraint pk_itementrada primary key (itemIdEntrada, itemIdLote),
    constraint fk_itementrada_entrada foreign key (itemIdEntrada) references Entrada(entId),
    constraint fk_itementrada_lote foreign key (itemIdLote) references Lote(lotId)
);

-- Tabela Saida
create table if not exists Saida (
    saiId integer primary key autoincrement,
    saiData date,
    saiHora time,
    saiTipo integer,
    saiValorTotal numeric(10, 2),
    funId integer,
    constraint fk_saida_funcionario foreign key (funId) references Funcionario(funId)
);

-- Tabela ItemSaida
create table if not exists ItemSaida (
    itemIdSaida integer,
    itemIdLote integer,
    itemQuantidade integer,
    itemPrecoUnit numeric(10, 2),
    constraint pk_itemsaida primary key (itemIdSaida, itemIdLote),
    constraint fk_itemsaida_saida foreign key (itemIdSaida) references Saida(saiId),
    constraint fk_itemsaida_lote foreign key (itemIdLote) references Lote(lotId)
);

-- Tabela ContatoSaida
create table if not exists ContatoSaida (
    cosIdSaida integer,
    cosIdContato integer,
    constraint pk_contatosaida primary key (cosIdSaida, cosIdContato),
    constraint fk_contatosaida_saida foreign key (cosIdSaida) references Saida(saiId),
    constraint fk_contatosaida_contato foreign key (cosIdContato) references Contato(conId)
);

create table if not exists pagamento (
    pagId integer primary key autoincrement,
    pagValor numeric(10, 2),
    pagParcelas integer,
    pagDataIni date,
    pagDataFim date,
    pagStatus integer,
    pagMetodoPagamento integer,
    saiId integer,
    entId integer,
    constraint fk_pagamento_saida foreign key (saiId) references Saida(saiId),
    constraint fk_pagamento_entrada foreign key (entId) references Entrada(entId)
);


create table if not exists Parcelas (
    parId integer constraint pk_parcelas primary key autoincrement,
    parMetPagamento integer,
    parValor numeric(10, 2),
    parData date,
    parStatus integer,
    pagId integer,
    constraint fk_parcelas_pagamento foreign key (pagId) references Pagamento(pagId)
);
""")
            conn.commit()
            return {
                'code': 200,
                'msg': 'Tabelas criadas!'
            }

        except (Exception, sqliteError) as error:
            retorno = {
                'code': 500,
                'msg': ('Erro criar tabelas:', error)
            }
            print(retorno)
            return retorno

        finally:
            self.cursor.close()
            self.desconectar(conn)

    def dados_iniciais(self):
        try:
            conn = self.conectar()
            self.cursor = conn.cursor()
            self.cursor.executescript("""
            -- Inserir na tabela Empresa
INSERT INTO Empresa (empCnpj, empNome, empVendas, empTelefone, empEmail, empSenha)
VALUES ('00.000.000/0001-91', 'Empresa X', true, '(11) 91234-5678', 'empresa@x.com', 'senha123');

-- Inserir na tabela Cargo
INSERT INTO Cargo (carCargo, empCnpj)
VALUES ('Gerente', '00.000.000/0001-91');

-- Inserir na tabela Funcionario
INSERT INTO Funcionario (funCpf, funNome, funTelefone, funEmail, funUf, funMunicipio, funBairro, funLogradouro, funSituacao, funLogin, funSenha, carId)
VALUES ('000.000.000-00', 'João Silva', '(11) 92345-6789', 'joao@x.com', 'SP', 'São Paulo', 'Centro', 'Rua A, 123', true, 'joao123', 'senha123', 1);

-- Inserir na tabela Categoria
INSERT INTO Categoria (catCategoria, empCnpj)
VALUES ('Eletrônicos', '00.000.000/0001-91');

-- Inserir na tabela Produto
INSERT INTO Produto (proDescricao, proCodigo, proCodigoBarra, proTipo, proUnidade, proPrecoVenda, proPrecoMedio, proPeso, proLargura, proAltura, proComprimento, proEstoque, proEstoqueMin, proEstoqueMax, proLocalizacao, proControleLote, catId)
VALUES ('Smartphone XYZ', 'SP001', '7891234567890', 1, 'Un', 1500.00, 1400.00, 0.2, 7.5, 15.0, 0.8, 50, 10, 100, 'A1', true, 1);

-- Inserir na tabela Contato
INSERT INTO Contato (conNome, conTelefone, conEmail, conTipo, conIdentificacaoNumero, conIdentificacao, conCep, conUf, conMunicipio, conBairro, conLogradouro)
VALUES ('Fornecedor Y', '(11) 93456-7890', 'fornecedor@y.com', 1, '12.345.678/0001-90', 1, '12345-678', 'SP', 'São Paulo', 'Centro', 'Rua B, 456');

-- Inserir na tabela Fornecedor
INSERT INTO Fornecedor (fornIdProduto, fornIdContato, fornPrincipal)
VALUES (1, 1, true);

-- Inserir na tabela Lote
INSERT INTO Lote (lotCodigo, lotQuantidade, lotMarca, lotFabricacao, lotValidade, lotStatus, proId)
VALUES ('LT001', 100, 'Marca X', '2023-01-01', '2025-01-01', true, 1);

-- Inserir na tabela Entrada
INSERT INTO Entrada (entData, entHora, entObservacao, entTipo, entValorTotal, funId)
VALUES ('2024-10-11', '14:30:00', 'Compra de estoque', 1, 5000.00, 1);

-- Inserir na tabela ItemEntrada
INSERT INTO ItemEntrada (itemIdEntrada, itemIdLote, itemQuantidade, itemPrecoUnit)
VALUES (1, 1, 50, 100.00);

-- Inserir na tabela Saida
INSERT INTO Saida (saiData, saiHora, saiTipo, saiValorTotal, funId)
VALUES ('2024-10-12', '15:00:00', 2, 3000.00, 1);

-- Inserir na tabela ItemSaida
INSERT INTO ItemSaida (itemIdSaida, itemIdLote, itemQuantidade, itemPrecoUnit)
VALUES (1, 1, 10, 150.00);

-- Inserir na tabela ContatoSaida
INSERT INTO ContatoSaida (cosIdSaida, cosIdContato)
VALUES (1, 1);

-- Inserir na tabela Pagamento
INSERT INTO Pagamento (pagValor, pagParcelas, pagDataIni, pagDataFim, pagStatus, pagMetodoPagamento, saiId, entId)
VALUES (3000.00, 3, '2024-10-12', '2025-01-12', 1, 2, 1, null);

-- Inserir na tabela Parcelas
INSERT INTO Parcelas (parMetPagamento, parValor, parData, parStatus, pagId)
VALUES (2, 1000.00, '2024-11-12', 1, 1);
""")
            conn.commit()
            return {
                'code' : 200,
                'msg' : 'Dados iniciais inseridos!'
            }

        except (Exception, sqliteError) as error:
            return {
                'code': 500,
                'msg': ('Erro ao inserir dados iniciais: ', error)
            }

        finally:
            self.cursor.close()
            self.desconectar(conn)