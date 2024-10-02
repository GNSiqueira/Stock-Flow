from psycopg2 import connect, Error
import sqlite3 as sqlite
from sqlite3 import Error as sqliteError

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
            print('Conexão estabelecida com sucesso!')
            return conn
    
        except (Exception, sqliteError) as error:
            print('Erro ao conectar ao banco de dados:', error)
            return {
                'status': 1,
                'msg': ('Erro ao conectar ao banco de dados: ', error)
            }
        
    def desconectar(self, conn):
        try:
            if conn is not None: 
                conn.close()
                print('Conexão fechada com sucesso!')
                return('Conexão fechada com sucesso!')
        except (Exception, sqliteError) as error:
            print('Erro ao fechar a conexão!')
            return('Erro ao fechar a conexão!')

    def create_table(self):
        try:
            conn = self.conectar()
            self.cursor = conn.cursor()
            self.cursor.executescript("""
            -- Tabela Empresa
            create table if not exists Empresa (
                empCnpj varchar(18),
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
                proDescricao varchar(255) unique,
                proCodigo varchar(50) unique,
                proCodigoBarra varchar(13) unique,
                proTipo varchar(50), -- Ex: Kit, Simples, Fabricado, Com variação
                proUnidade varchar(10), --Ex: Mg, L, Kg
                proPrecoVenda numeric(10, 2),
                proPrecoMedio numeric(10, 2),
                proPrecoCusto numeric(10, 2),
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
                conTipo varchar(4) check(conTipo in ('FORNECEDOR', 'CLIENTE')),
                conIdentificacao varchar(10) check(conIdentificacao in ('CNPJ', 'CPF')),
                conIdentificacaoNumero varchar(18), --00.000.000/0000-00  000.000.000-00
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
                lotDataEntrega date,
                lotTimeEntrada time,
                proId integer,
                constraint fk_lote_produto foreign key (proId) references Produto(proId)
            );

            -- Tabela Entrada
            create table if not exists Entrada (
                entId integer primary key autoincrement,
                entData date,
                entHora time,
                entObservacao text,
                entTipo integer check(entTipo in (1, 2, 3, 4, 5, 6, 7, 8)), --'COMPRA','DEVOLUÇÃO_CLIENTE','TRANSFERÊNCIA', 'PRODUÇÃO'
                                                                        --'AJUSTE_INVENTÁRIO','DOAÇÃO','BONIFICAÇÃO','IMPORTAÇÃO'
                entValorTotal numeric(10, 2),
                funId integer, 
                constraint fk_entrada_funcionario foreign key (funId) references Funcionario(funId)
            );

            -- Tabela ItemEntrada
            create table if not exists ItemEntrada (
                itemIdEntrada integer,
                itemIdLote integer,
                itemQuantidade integer,
                itemData date,
                itemHora time,
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
                saiTipo integer CHECK (saiTipo IN (1, 2, 3, 4, 5, 6, 7, 8, 9)), -- 'VENDA', 'DEVOLUÇÃO_FORNECEDOR', 'TRANSFERÊNCIA',
                                                                            -- 'CONSUMO', 'PERDA', 'QUEBRA', 'VENCIMENTO',
                                                                            -- 'DOAÇÃO', 'BONIFICAÇÃO'
                saiValorTotal numeric(10, 2),
                funId integer, 
                constraint fk_saida_funcionario foreign key (funId) references Funcionario(funId)
            );

            -- Tabela ItemSaida
            create table if not exists ItemSaida (
                itemIdSaida integer,
                itemIdLote integer,
                itemQuantidade integer,
                itemData date,
                itemHora time,
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
            """)
            conn.commit()
            self.cursor.close()
            self.desconectar(conn)
            print('Tabelas criadas com sucesso!')
            return 'Comando executado com sucesso!'

        except (Exception, sqliteError) as error:
            retorno = {
                'status': 1,
                'msg': ('Erro ao executar o comando:', error)
            }
            print(retorno)
            return retorno
        
    def dados_iniciais(self):
        try:
            conn = self.conectar()
            self.cursor = conn.cursor()
            self.cursor.executescript("""
                -- Inserindo uma empresa
                INSERT INTO Empresa (empCnpj, empNome, empVendas, empTelefone, empEmail, empSenha)
                VALUES ('12.345.678/0001-95', 'Empresa Teste', 1, '(11) 98765-4321', 'contato@empresateste.com', 'senha123');
                INSERT INTO Empresa (empCnpj, empNome, empVendas, empTelefone, empEmail, empSenha)
                VALUES ('13.345.678/0001-95', 'Empresa 4este', 1, '(31) 98765-4321', 'cdontato@empresateste.com', 'senha123');

                -- Inserindo um cargo
                INSERT INTO Cargo (carCargo, empCnpj)
                VALUES ('Gerente', '12.345.678/0001-95');

                -- Inserindo um funcionário
                INSERT INTO Funcionario (funCpf, funNome, funTelefone, funEmail, funUf, funMunicipio, funBairro, funLogradouro, funSituacao, funLogin, funSenha, carId)
                VALUES ('123.456.789-00', 'João Silva', '(11) 91234-5678', 'joao.silva@empresa.com', 'SP', 'São Paulo', 'Centro', 'Rua das Flores, 123', TRUE, 'joaosilva', 'senha456', 1);

                -- Inserindo uma categoria
                INSERT INTO Categoria (catCategoria, empCnpj)
                VALUES ('Eletrônicos', '12.345.678/0001-95');

                -- Inserindo um produto
                INSERT INTO Produto (proDescricao, proCodigo, proCodigoBarra, proTipo, proUnidade, proPrecoVenda, proPrecoMedio, proPrecoCusto, proPeso, proLargura, proAltura, proComprimento, proEstoque, proEstoqueMin, proEstoqueMax, proLocalizacao, proControleLote, catId)
                VALUES ('Celular XYZ', '123ABC', '7894561231234', 'Simples', 'Un', 1500.00, 1200.00, 1000.00, 0.5, 7.5, 15.0, 1.0, 100, 10, 200, 'A-12', TRUE, 1);

                -- Inserindo um contato (cliente)
                INSERT INTO Contato (conNome, conTelefone, conEmail, conTipo, conIdentificacao, conIdentificacaoNumero, conCep, conUf, conMunicipio, conBairro, conLogradouro)
                VALUES ('Cliente Teste', '(11) 98765-6789', 'cliente@teste.com', 'CLIENTE', 'CPF', '111.222.333-44', '12345-678', 'SP', 'São Paulo', 'Centro', 'Rua das Laranjeiras, 45');

                -- Inserindo um fornecedor
                INSERT INTO Fornecedor (fornIdProduto, fornIdContato, fornPrincipal)
                VALUES (1, 1, TRUE);

                -- Inserindo um lote
                INSERT INTO Lote (lotCodigo, lotQuantidade, lotMarca, lotFabricacao, lotValidade, lotStatus, lotDataEntrega, lotTimeEntrada, proId)
                VALUES ('LOT123', 50, 'Marca XYZ', '2024-01-01', '2025-01-01', TRUE, '2024-01-05', '14:30:00', 1);

                -- Inserindo uma entrada
                INSERT INTO Entrada (entData, entHora, entObservacao, entTipo, entValorTotal, funId)
                VALUES ('2024-01-05', '14:30:00', 'Compra de produtos', 1, 75000.00, 1);

                -- Inserindo um item de entrada
                INSERT INTO ItemEntrada (itemIdEntrada, itemIdLote, itemQuantidade, itemData, itemHora, itemPrecoUnit)
                VALUES (1, 1, 50, '2024-01-05', '14:30:00', 1500.00);

                -- Inserindo uma saída
                INSERT INTO Saida (saiData, saiHora, saiTipo, saiValorTotal, funId)
                VALUES ('2024-02-01', '10:15:00', 1, 3000.00, 1);

                -- Inserindo um item de saída
                INSERT INTO ItemSaida (itemIdSaida, itemIdLote, itemQuantidade, itemData, itemHora, itemPrecoUnit)
                VALUES (1, 1, 2, '2024-02-01', '10:15:00', 1500.00);

                -- Inserindo um contato de saída
                INSERT INTO ContatoSaida (cosIdSaida, cosIdContato)
                VALUES (1, 1);

            """)
            conn.commit()
            self.cursor.close()
            self.desconectar(conn)
            retorno = 'Inserindo dados iniciais com sucesso!'
            print(retorno)
            return retorno

        except (Exception, sqliteError) as error:
            retorno = {
                'status': 1,
                'msg': ('Erro ao executar o comando:', error)
            }

            conn.rollback()

            if error == "('Erro ao executar o comando:', IntegrityError('UNIQUE constraint failed: Empresa.empCnpj'))}":
                obanco = 'Dados já inseridos!'
                print(obanco)
            else: 
                print(retorno)
            return retorno
