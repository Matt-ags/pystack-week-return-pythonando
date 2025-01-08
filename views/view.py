# Em views vai ser toda a lógica, desde cadastrar assinaturas, pagar assinaturas, etc
import __init__
from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date, datetime

class SubscriptionService: # Com isso, consigo as ações, é meio confuso, mas imagine que com isso eu consigo "manipular" o banco de dados
# ORIENAR O PYTHON PARA BUSCAR O BANCO DE DADOS CERTO:
    def __init__(self, engine):
        self.engine = engine

# CRIAR ASSINATURAS:
    def create(self, subscription: Subscription): # Cria uma assinatura
        with Session(self.engine) as session:
            session.add(subscription)
            session.commit() # ele salva a alterção, o crtl s
            return subscription

# LISTAR ASSINATURAS: 
    def list_all(self): # Lista todas as assinaturas
        with Session(self.engine) as session:
            statement = select(Subscription) # trazendo todos os dados do banco
            results = session.exec(statement).all() # executando o treco
        return results

# DELETAR ASSINATURAS:
    def delete(self, id):
        with Session(self.engine) as session: 
            statement = select(Subscription).where(Subscription.id == id) # where com base no parametro
            result = session.exec(statement).one()
            session.delete(result) # isso que deleta memo
            session.commit()
        

# FUNÇÃO PARA VERIFICAR SE UMA ASSINATURA JÁ FOI PAGA:
    def _has_pay(self, results):
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False
        

# FUNÇÃO PARA PAGAMENTO:
    def pay(self, subscription: Subscription):
        with Session(self.engine) as session: # Com isso, eu consigo acessar o banco de dados
            # vamos verificar se a assnaura ja estava paga no mes
            statement = select(Payments).join(Subscription).where(Subscription.empresa == subscription.empresa) # eee saldades do "where" no sql ;-;
            results = session.exec(statement).all()
            # print(results)

            if self._has_pay(results):
                question = input('Essa conta já foi paga esse mês, deseja pagar novamente? Y ou N: ')

                if not question.upper() == 'Y':
                    return 
                
            pay = Payments(subscription_id=subscription.id, date=date.today())
            session.add(pay)
            session.commit()
            
# FUNÇÃO VALOR TOTAL (quanto estou gastando com assinaturas por mes):
    def total_value(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()

            total = 0
            for result in results:
                total = total + result.valor

            return float(total)

# Mano, olha que treco doido, 
# Vamos criar a parte dos gráficos, que vai gerar um grafico dos ultimos 12 meses. Dai o que acontece, imagine que estamos no mes 2, vamos omeçar  a voltar certo? -1, etc... MAS, vamos chegar no 1, que se tirar, vai ficar mes 0.

# ABAIXO SÃO AS PARTES DOS GRÁFICOS:
# NÃO ESTÃO FUNCIONANDO, RETORNAR APÓS A "FINALIZAÇÃO" DO SISTEMA, 

#O EIXO X, AS DATAS: 
    def _get_last_12_months_native(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        for i in range(12):
            last_12_months.append((month, year))
            month = month - 1
            if month == 0: # Se o mes chegar a 0, ele vai para o 12, e tira 1 do ano
                month = 12
                year = year - 1
        return last_12_months[::-1] # Vamos inverter a lista, para ficar do mais antigo para o mais novo (usa esses ::)
# Dai temos que fazer que ao chegar ao mes 0, fique 12, e tira 1 do ano!

#EIXO Y, VALORES
    def _get_values_for_months(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()

            value_for_months = []
            for i in last_12_months:
                value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value = value + float(result.subscription.valor)
                value_for_months.append(value)
            return value_for_months


#GERAR O GRÁFICO (ACREDITO QUE SEJA A RAIZ DO PROBLEMA DE NÃO FUNCIONAR):
    def gen_chart(self):
        last_12_months = self._get_last_12_months_native()
        values_for_months = self._get_values_for_months(last_12_months)
        last_12_months2 = []
        for i in last_12_months: #CORRIGIR O PROBLEMA DE SÓ APARECER O MES, NÃO O ANO
            last_12_months2.append(i[0])

        import matplotlib.pyplot as plt # instalamos a matplotlib para a criação de gráficos

        plt.plot(last_12_months2, values_for_months)
        plt.show()

# ABAIXO É O GABARITO, TROCANDO POR ELE DA OUTRO TIPO DE ERRO:
    # self.subscription_service.gen_chart()
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # AttributeError: 'SubscriptionService' object has no attribute 'gen_chart'
# def _get_last_12_months_native(self):
#     today = datetime.now()
#     year = today.year
#     month = today.month
#     last_12_months = []
#     for _ in range(12):
#         last_12_months.append((month, year))
#         month -= 1
#         if month == 0:
#             month = 12
#             year -= 1
#     return last_12_months[::-1]

# def _get_values_for_months(self, last_12_months):
#     with Session(self.engine) as session:
#         statement = select(Payments)
#         results = session.exec(statement).all()

#         value_for_months = []
#         for i in last_12_months:
#             value = 0
#             for result in results:
#                 if result.date.month == i[0] and result.date.year == i[1]:
#                     value += float(result.subscription.valor)

#             value_for_months.append(value)
#     return value_for_months

# def gen_chart(self):
#     last_12_months = self._get_last_12_months_native()
#     values_for_months = self._get_values_for_months(last_12_months)
#     last_12_months = list(map(lambda x: x[0], self._get_last_12_months_native()))
#     import matplotlib.pyplot as plt
#     plt.plot(last_12_months, values_for_months)
#     plt.show()



ss = SubscriptionService(engine) # Agora eu consigo acessar o banco de dados
