from datetime import datetime, timedelta

class ContaBanco:

    def __init__(self, nome, cpf, agencia, conta):
        self._transacoes = self._criar_transacoes(nome, agencia, conta, self._ajusta_cpf(cpf))
        self._nome = nome
        self._cpf = self._cadastro_cpf(cpf)
        self._agencia = agencia
        self._conta = conta
        self._saldo = 0
        self._credito_especial = 0
        self._saque_maximo = self._limite_saque()


    def deposito(self, valor):
        self._saldo += valor
        self._transacoes_deposito(valor)

    def saque(self, valor):
        self._saque_maximo = self._limite_saque()
        if self._limite_saque_transferencia(valor) == 1:
            self._saldo = self._saldo - valor
            self._transacoes_saque(valor)
        else:
            print(f'Não é possível realizar esse saque, favor consulte seu saldo')

    def transferencia(self, valor_transferencia, conta_destino):
        self._saque_maximo = self._limite_saque()
        if self._limite_saque_transferencia(valor_transferencia) == 1:
            self._saldo = self._saldo - valor_transferencia
            conta_destino._saldo += valor_transferencia
            self._transacoes_transferencia_realizada(valor_transferencia)
            self._transacoes_transferencia_recebida(valor_transferencia, conta_destino)
        else:
            print(f'Não é possível realizar essa transferência, favor consulte seu saldo')

    def credito_especial(self, credito_especial):
        self._credito_especial = credito_especial



    def extrato(self, data_inicial, data_final):
        data_inicial = self._tratando_datas(data_inicial)
        data_final = self._tratando_datas(data_final)
        dados = self._tratamento_transacao()
        return self._criar_extrato(data_inicial, data_final, dados)

    def _tratando_datas(self, data):
        data = datetime.strptime(data, '%d/%m/%Y')
        return data

    def _tratamento_transacao(self):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt','r',encoding='utf-8') as arquivo:
            arquivo = arquivo.readlines()
            cabecalho = arquivo[0]
            transacoes = arquivo[1:]
            conta, agencia, nome_cliente, cpf = cabecalho.split('|')
            cpf = cpf.replace('\n', '')
            for i,transacao in enumerate(transacoes):
                transacao = transacao.replace('\n', '')
                transacoes[i] = transacao.split(',')
        return (conta, agencia, nome_cliente, cpf, transacoes)

    def _tratamento_transacao(self):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'r') as arquivo:
            doc = arquivo.readlines()
            cabecalho = doc[0]
            transacoes = doc[1:]
            conta, agencia, nome_cliente, cpf = cabecalho.split('|')
            cpf = cpf.replace('\n', '')
            for i, transacao in enumerate(transacoes):
                transacao = transacao.replace('\n', '')
                transacoes[i] = transacao.split(',')
        return [conta, agencia, nome_cliente, cpf, transacoes]

    def _saldo_inicial_saldo_final(self, sinal, valor):
        saldo = 0
        if sinal == '+':
            saldo = saldo + int(valor)
        else:
            saldo = saldo - int(valor)
        return saldo

    def _transacoes_extrato(self, transacoes, data_inicial, data_final, arquivo):
        for transacao in transacoes:
            for tran in transacao:
                data, operacao, sinal, valor = tran
                data = self._tratando_datas(data)
            if data >= data_inicial and data <= data_final:
                saldo_final = self._saldo_inicial_saldo_final(sinal, valor)
                data = data.strftime('%d/%m/%Y')
                arquivo.write(f'  {data}  |  {operacao}  |  {sinal}{valor}  \n')
                arquivo.write(f'Salndo Final: {saldo_final}')
            else:
                saldo_inicial = self._saldo_inicial_saldo_final(sinal, valor)
                arquivo.write(f'Saldo Inicial: {saldo_inicial}\n\n\n')

    def _escreve_cabecalho(self, arquivo):
        cabecalho = 'Nome: {} \n\nAgência:{}       Conta:{}'.format(self._nome ,self._agencia, self._conta)
        transacoes = arquivo[4:]
        corta_linha = '-' * 40
        arquivo.write(f'{cabecalho}\n{corta_linha}\n')
        return transacoes

    def _criar_extrato(self, data_inicial, data_final, dados):
        with open(f'extrato_{str(data_inicial.date())}_{str(data_final.date())}.txt', 'a', encoding='utf-8') as arquivo:
            self._transacoes_extrato(dados, data_inicial, data_final, arquivo)















    def _limite_saque(self):
        return  self._saldo + self._credito_especial

    def _limite_saque_transferencia(self, valor):
        if valor > self._saque_maximo:
            return 0
        else:
            return 1

    def _transacoes_saque(self,valor):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self._data_atual()},S,-,{valor}')

    def _formatar_numero_cpf(self, cpf):
        pass


    def _transacoes_deposito(self, valor):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self._data_atual()},D,+,{valor}')

    def _transacoes_transferencia_realizada(self, valor):
        with open(f'transacoes_{self._conta}_{self._agencia}_{self._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self._data_atual()},T,-,{valor}')

    def _transacoes_transferencia_recebida(self, valor, conta_destino):
        with open(f'transacoes_{conta_destino._conta}_{conta_destino._agencia}_{conta_destino._nome}.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'\n{self._data_atual()},T,+,{valor}')

    def _data_atual(self):
        return datetime.now().strftime('%d/%m/%Y')

    def _criar_transacoes(self, nome, agencia, conta, cpf):
        if self._verifica_cadastro_cpf(self._ajusta_cpf(cpf)) == 1:
            pass
        else:
            with open(f'transacoes_{conta}_{agencia}_{nome}.txt','a',encoding='utf-8') as arquivo:
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
        with open(f'relacao_clientes_banco_dinheiro_barato.txt', 'a', encoding='utf-8') as arquivo:
            pass
        with open(f'relacao_clientes_banco_dinheiro_barato.txt', 'r', encoding='utf-8') as arquivo:
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
                arquivo.write(f'{cpf}\n') # estudar uma forma de por data e ainda fazer a verificação do CPF

    def _cadastro_cpf(self, cpf):
        cpf = self._ajusta_cpf(cpf)
        cad = self._verifica_cadastro_cpf(cpf)
        self._fim_cadastro_cpf(cpf, cad)




conta_david = ContaBanco('David','028.496.678-28', '16487','0025654')
conta_luan = ContaBanco('Luan', '175.930,637-95', '21553', '4816')
conta_david.deposito(15000)
conta_david.credito_especial(50000)
conta_david.saque(5000)
conta_luan.deposito(80000)
conta_luan.deposito(20000)
conta_david.transferencia(2000, conta_luan)
conta_david.saque(500)
conta_luan.transferencia(6000, conta_david)
conta_david.extrato('19/01/2023','21/01/2023')