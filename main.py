class ContaBanco:
    def __init__(self, nome, cpf, agencia, conta):
        self.nome = nome
        self.cpf = cpf
        self.agencia = agencia
        self.conta = conta
        self.saldo_inicial = 0
        self.transacoes = self.criar_transacoes(nome,agencia,conta,cpf)

    def criar_transacoes(self,nome, agencia, conta, cpf):
        with open(f'transacoes_{conta}_{agencia}_{nome}.txt','w',encoding='utf-8') as arquivo:
            arquivo.write(f'{conta}|{agencia}|{nome}|{cpf}')


conta_david = ContaBanco('David','02849567852', '1587','0025654')

print(conta_david.cpf, conta_david.agencia, conta_david.nome, conta_david.conta)