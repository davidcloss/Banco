from datetime import datetime, timedelta

class ContaBanco:

    def __init__(self, nome, cpf, agencia, conta):
        self._nome = nome
        self._cpf = self._cadastro_cpf(cpf)
        self._agencia = agencia
        self._conta = conta
        self._saldo = 0
        self._transacoes = self._criar_transacoes(nome, agencia, conta, cpf)

    def deposito(self, valor):
        self._saldo += valor
        self._transacoes_deposito(valor)

    def saque(self, valor):
        self._saldo = self._saldo - valor
        self._transacoes_saque(valor)

    def transferencia(self, valor_transferencia, conta_destino):
        self._saldo = self._saldo - valor_transferencia
        conta_destino._saldo += valor_transferencia
        self._transacoes_transferencia_realizada(valor_transferencia)
        self._transacoes_transferencia_recebida(valor_transferencia, conta_destino)

    def _transacoes_saque(self,valor):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self._data()},S,-{valor}')

    def _transacoes_deposito(self,valor):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self._data()},D,+{valor}')

    def _transacoes_transferencia_realizada(self, valor):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self._data()},T,-{valor}')

    def _transacoes_transferencia_recebida(self, valor, conta_destino):
        with open(f'transacoes_{conta_destino._conta}_{conta_destino._agencia}_{conta_destino._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self._data()},T,+{valor}')

    def _data(self):
        return datetime.now().date()

    def _criar_transacoes(self, nome, agencia, conta, cpf):
        with open(f'transacoes_{conta}_{agencia}_{nome}.txt','w',encoding='utf-8') as arquivo:
            arquivo.write(f'{conta}|{agencia}|{nome}|{cpf}')


    def _ajusta_digitos_cpf(self, cpf):
        if len(cpf) < 11:
            return print('Número de dígitos incorretos, favor verificar seu CPF novamente.')
        elif len(cpf) > 11:
            return print('Número de dígitos incorretos, favor verificar seu CPF novamente.')
        else:
            return cpf

    def _ajusta_cpf(self, cpf):
        cpf = cpf.replace('.','')
        cpf = cpf.replace('-','')
        cpf = cpf.replace(',','')
        cpf = cpf.replace(' ', '')
        cpf = self._ajusta_digitos_cpf(cpf)
        return cpf

    def _verifica_cadastro_cpf(self, cpf):
        with open('relacao_clientes_banco_dinheiro_barato.txt', 'r', encoding='utf-8') as arquivo:
            docs = arquivo.readlines()
            for i, doc in enumerate(docs):
                doc = doc.replace('\n', '')
                docs[i] = doc
            if cpf in docs:
                return 1
            else:
                return cpf

    def _fim_cadastro_cpf(self,cpf,cad):
        if cad == 1:
            return print('CPF já cadastrado, favor entre em contato com a agência')
        else:
            with open(f'relacao_clientes_banco_dinheiro_barato.txt', 'a', encoding='utf-8') as arquivo:
                arquivo.write(f'{cpf}\n')

    def _cadastro_cpf(self, cpf):
        cpf = self._ajusta_cpf(cpf)
        cad = self._verifica_cadastro_cpf(cpf)
        self._fim_cadastro_cpf(cpf, cad)





conta_david = ContaBanco('David','028.496.678-28', '16487','0025654')
conta_david.deposito(5000)
conta_david.saque(946)
conta_luan = ContaBanco('Luan', '175.930,637-95', '21553', '4816')
conta_david.transferencia(513, conta_luan)