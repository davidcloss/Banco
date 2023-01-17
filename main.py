from datetime import datetime, timedelta

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

    def transferencia(self, valor_transferencia, conta_destino):
        self.valor = self.saldo - valor_transferencia
        conta_destino.saldo += valor_transferencia
        self.transacoes_transferencia_realizada(valor_transferencia)
        self.transacoes_transferencia_recebida(valor_transferencia, conta_destino)

    def criar_transacoes(self,nome, agencia, conta, cpf):
        with open(f'transacoes_{conta}_{agencia}_{nome}.txt','w',encoding='utf-8') as arquivo:
            arquivo.write(f'{conta}|{agencia}|{nome}|{cpf}')

    def transacoes_saque(self,valor):
        with open(f'transacoes_{self.conta}_{self.agencia}_{self.nome}.txt','a',encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self.data()},S,-{valor}')

    def transacoes_deposito(self,valor):
        with open(f'transacoes_{self.conta}_{self.agencia}_{self.nome}.txt','a',encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self.data()},D,+{valor}')

    def transacoes_transferencia_realizada(self, valor):
        with open(f'transacoes_{self.conta}_{self.agencia}_{self.nome}.txt','a',encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self.data()},T,-{valor}')

    def transacoes_transferencia_recebida(self, valor, conta_destino):
        with open(f'transacoes_{conta_destino.conta}_{conta_destino.agencia}_{conta_destino.nome}.txt','a',encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self.data()},T,+{valor}')

    def data(self):
        return datetime.now().date()



conta_david = ContaBanco('David','02849567852', '1587','0025654')
conta_david.deposito(3000)
conta_david.saque(500)
conta_luan = ContaBanco('Luan', '01459371801', '4598', '0066458')
conta_luan.deposito(1500)
conta_luan.saque(150)
conta_luan.transferencia(50,conta_david)
print(conta_david.cpf, conta_david.agencia, conta_david.nome, conta_david.conta, conta_david.saldo)
print(conta_luan.cpf, conta_luan.agencia, conta_luan.nome, conta_luan.conta, conta_luan.saldo)