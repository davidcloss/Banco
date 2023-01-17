from datetime import datetime

class ContaBanco:
    def __init__(self, nome, cpf, agencia, conta):
        self.nome = nome
        self.cpf = cpf
        self.agencia = agencia
        self.conta = conta
        self.saldo = 0
        self.transacoes = self.criar_transacoes(nome,agencia,conta,cpf)


    def deposito(self, valor):
        self.saldo += valor
        self.transacoes_deposito(valor)

    def saque(self, valor):
        self.saldo = self.saldo - valor
        self.transacoes_saque(valor)

    def criar_transacoes(self,nome, agencia, conta, cpf):
        with open(f'transacoes_{conta}_{agencia}_{nome}.txt','w',encoding='utf-8') as arquivo:
            arquivo.write(f'{conta}|{agencia}|{nome}|{cpf}')

    def transacoes_saque(self,valor):
        with open(f'transacoes_{self.conta}_{self.agencia}_{self.nome}.txt','a',encoding='utf-8') as arquivo:
            arquivo.write(f'\nS,-{valor}')

    def transacoes_deposito(self,valor):
        with open(f'transacoes_{self.conta}_{self.agencia}_{self.nome}.txt','a',encoding='utf-8') as arquivo:
            arquivo.write(f'\nD,+{valor}')





conta_david = ContaBanco('David','02849567852', '1587','0025654')
conta_david.deposito(50)
conta_david.saque(10)
print(conta_david.cpf, conta_david.agencia, conta_david.nome, conta_david.conta, conta_david.saldo)