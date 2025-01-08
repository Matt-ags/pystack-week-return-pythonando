from sqlmodel import Field, SQLModel, create_engine
from .model import * # Quando fu criar a tabela de payments, fui aqui e tirei o ponto e rodei este arquivo, e deu certo.

# Vamos usar o banco de dados SQLITE, nativo do python

# Alem do mais, por aqui, caso no futuro eu troque o banco de dados, é só mudar a URL, e o resto do código vai funcionar, tipo, do sqlite para o mysql, etc...
# O sql model ele já transforma no tipo de dado automaticamente, então não precisa se preocupar com isso

# ABAIXO SÃO CÓDIGOS NECESSÁRIOS PARA A CRIAÇÃO DO BANCO DE DADOS:

sqlite_file_name = "database.db" # O nome do arquivo do banco de dados
sqlite_url = f"sqlite:///{sqlite_file_name}" # A URL do banco de dados

# Agora a engine, que vai criar, o usuario, tipo, etc...

engine = create_engine(sqlite_url, echo=False) # O echo é para mostrar o que está acontecendo, no final, com tudo funcionando, deixa false

if __name__ == "__main__": # Toda ve que eu rodar um arquivo, ele fala de qual arquivo foi rodado. Executa ela caso é executado por ele mesmo
    SQLModel.metadata.create_all(engine) # Cria todas as tabelas do banco de dados

# O daora que ao rodar, com python models/model.py, ele cria o arquivo database.db, e a tabela subscription, e no console, mostra o código sql :D
