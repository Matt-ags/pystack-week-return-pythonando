import __init__
from views.view import SubscriptionService
from models.database import engine
from models.model import Subscription
from decimal import Decimal
from datetime import datetime

class UI:
    def __init__(self):
        self.subscription_service = SubscriptionService(engine)

        # FUNCIONALIDADES:

    # ADICIONAR ASSINATURA:
    def add_subscription(self):
        empresa = input('Nome da empresa: ')
        site = input('Site da empresa: ')
        data_assinatura = datetime.strptime(input('Data de assinatura: '), '%d/%m/%Y')
        valor = Decimal(input('Valor da assinatura: '))
        subscription = Subscription(empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor)
        self.subscription_service.create(subscription)

    # DELETAR ASSINATURA:
    def delete_subscription(self):
        subscriptions = self.subscription_service.list_all()
        # todo: quando excluit uma assinatura, deleta os pagamentos dela tbm, ou de outra forma
        print('Escolha a assinatura que deseja deletar: ')
        for i in subscriptions:
            print(f'{i.id} -> {i.empresa}')

        choise = int(input('Escolha a assinatura: '))
        self.subscription_service.delete(choise)
        print('Assinatura deletada com sucesso!')

    # VALOR TOTAL:
    def total_value(self):
        print(f'Valor total (mensal em assinaturas): R${self.subscription_service.total_value()}')
        

    # MENU:
    def start(self):
        while True:
            print('''
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total
            [4] -> Gastos últimos 12 meses (em desenvolvimento)
            [5] -> Pagar Assinatura (em desenvolvimento)
            [5] -> Sair
            ''')
            choice = int(input('Escolha uma opção: '))
            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscription_service.gen_chart()
            elif choice == 5:
                self.pay()

                # todo: a parte de pagar a assinatura
            else:
                break
    


# chamando:

UI().start()