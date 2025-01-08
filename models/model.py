# Vamos usar o ORM "sqlmodel"
from sqlmodel import Field, SQLModel, create_engine, Relationship

# É importante lembrar que tem dados que não são obrigatórios, como o site, então precisamos importar essa "fução":
from typing import Optional

# Tambem precisamos de datas, então vamos importar o datetime
from datetime import date

# Alem de numeros decimais!
from decimal import Decimal

# Show, mas qual a primeia tabela que vamos criar? A de armazenar assinaturas!
class Subscription(SQLModel, table=True): # é a classe que transforma a tabela em um objeto
    id: int = Field(primary_key=True) # Olha, é o id, é unico, uma chave primario, e o proprio banco de dados vai gerar
    empresa: str 
    site: Optional[str] = None # O site é opcional, então se não for passado, ele vai ser nulo
    data_assinatura: date
    valor: Decimal


# Vmos criar uma nova tabela com as pagas
class Payments(SQLModel, table=True):
    id: int = Field(primary_key=True)
    subscription_id: int = Field(foreign_key="subscription.id") # O id da assinatura, é uma chave estrangeira
    subscription: Subscription = Relationship() # É uma relação com a tabela de assinaturas
    date: date

# Show, temos uma "tabela", o código... Mas como transformamos em uma tabela do banco de dados em si?

# VERIFICAR DATABASE.PY

# Deixei separado, neste arquivo acessamos as models, no database, criamos o banco de dados
# Da o mesmo resultado, mas é mais organizado