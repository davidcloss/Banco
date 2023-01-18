from datetime import datetime, timedelta

class ContaBanco:

    def __init__(self, nome, cpf, agencia, conta):
        self._nome = nome
        self._cpf = cpf
        self._agencia = agencia
        self._conta = conta
        self._saldo = 0
        self._transacoes = self.criar_transacoes(nome, agencia, conta, cpf)


    def deposito(self, valor):
        self._saldo += valor
        self.transacoes_deposito(valor)

    def saque(self, valor):
        self._saldo = self._saldo - valor
        self.transacoes_saque(valor)

    def transferencia(self, valor_transferencia, conta_destino):
        self._saldo = self._saldo - valor_transferencia
        conta_destino._saldo += valor_transferencia
        self.transacoes_transferencia_realizada(valor_transferencia)
        self.transacoes_transferencia_recebida(valor_transferencia, conta_destino)

    def criar_transacoes(self,nome, agencia, conta, cpf):
        with open(f'transacoes_{conta}_{agencia}_{nome}.txt','w',encoding='utf-8') as arquivo:
            arquivo.write(f'{conta}|{agencia}|{nome}|{cpf}')

    def transacoes_saque(self,valor):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self.data()},S,-{valor}')

    def transacoes_deposito(self,valor):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self.data()},D,+{valor}')

    def transacoes_transferencia_realizada(self, valor):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self.data()},T,-{valor}')

    def transacoes_transferencia_recebida(self, valor, conta_destino):
        with open(f'transacoes_{conta_destino._conta}_{conta_destino._agencia}_{conta_destino._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self.data()},T,+{valor}')

    def data(self):
        return datetime.now().date()



conta_david = ContaBanco('David','02849567852', '1587','0025654')
print(conta_david._saldo)
conta_david.deposito(3000)
print(conta_david._saldo)
conta_david.saque(500)
print(conta_david._saldo)
conta_luan = ContaBanco('Luan', '01459371801', '4598', '0066458')
print(conta_luan._saldo)
conta_luan.deposito(1500)
print(conta_luan._saldo)
conta_luan.saque(150)
print(conta_luan._saldo)
conta_luan.transferencia(50,conta_david)
print(conta_luan._saldo)
print(conta_david._saldo)
