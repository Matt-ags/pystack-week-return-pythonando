import sys, os
sys.path.append(os.path.abspath(os.curdir))
# A ordem aqui é importante, acima importamos o engine, que é a conexão com o banco de dados
# Alem disso, o sys.path.append(os.path.abspath(os.curdir)) é para importar o arquivo models/database.py, que está em outro diretório
# Para com fim, importamos o engine, que é a conexão com o banco de dados, assim tendo as "ações"