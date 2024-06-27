import os
import textwrap

# Função para limpar a tela do terminal
def limpar_tela():
    if os.name == 'posix':  # Unix/Linux/MacOS/BSD/etc
        _ = os.system('clear')
    elif os.name == 'nt':  # Windows
        _ = os.system('cls')

def mostrar_menu():
    menu = """
    =============MENU BANCÁRIO=============

    Escolha uma opção:
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Novo Usuário
    [5] Nova Conta
    [6] Listar Contas
    [7] Sair

    =======================================
    ===> """
    return input(menu)

def depositar(saldo, extrato, /):
    limpar_tela()
    valor = float(input("Informe o valor do depósito: "))
        
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: \tR$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("Erro na operação! O valor informado é inválido.")

    return saldo, extrato

def sacar(*, saldo, extrato, limite, numero_saques, limite_saques):
    limpar_tela()
    valor = float(input("Informe o valor do saque: "))
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    
    if excedeu_saldo:
        print("Erro na operação! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Erro na operação! O valor do saque ultrapassa o limite.")
    elif excedeu_saques:
        print("Erro na operação! Número máximo de saques ultrapassado.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: \t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("Erro na operação! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, /, *, extrato):
    limpar_tela()
    print("\n=============== EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)
    print(f"Saldo: \t\tR$ {saldo:.2f}")
    print("========================================")

def criar_usuario(lista_usuarios):
    limpar_tela()
    print("Cadastro de novo usuário\n")
    cpf = input("Informe o CPF para cadastro: ")

    # Verifica se o CPF já está cadastrado
    for usuario in lista_usuarios:
        if usuario['cpf'] == cpf:
            print("\nErro: Já existe um usuário cadastrado utilizando este CPF.")
            return
    
    nome = input("Nome: ")
    data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
    logradouro = input("Logradouro: ")


    # Se não encontrar o CPF na lista, adiciona o novo usuário
    novo_usuario = {
        'nome': nome,
        'data_nasc': data_nasc,
        'cpf': cpf,
        'logradouro': logradouro
    }
    lista_usuarios.append(novo_usuario)
    print("\nUsuário cadastrado com sucesso.")

def criar_conta(lista_contas, lista_usuarios, numero_conta, agencia):
    limpar_tela()
    cpf = input("CPF do usuário: ")

    for usuario in lista_usuarios:
        if usuario['cpf'] == cpf:
            conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
            lista_contas.append(conta)
            print("\nConta criada com sucesso!")
            return

    print("\nErro: Não existe usuário cadastrado com este CPF.")

def listar_contas(lista_contas):
    limpar_tela()
    if not lista_contas:
        print("Não há contas cadastradas.")
    else:
        print("\n===== CONTAS CADASTRADAS =====\n")
        print("-" * 30)
        for conta in lista_contas:
            print(f"Agência: {conta['agencia']}")
            print(f"Número da Conta: {conta['numero_conta']}")
            print(f"Titular: {conta['usuario']['nome']}")
            print("-" * 30)


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    numero_conta = 1

    lista_usuarios = []
    lista_contas = []

    while True:
        limpar_tela()
        opcao_escolhida = mostrar_menu()

        if opcao_escolhida == "1":
            saldo, extrato = depositar(saldo, extrato)
            
        elif opcao_escolhida == "2":
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            

        elif opcao_escolhida == "3":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao_escolhida == "4":
            criar_usuario(lista_usuarios)

        elif opcao_escolhida == "5":
            criar_conta(lista_contas, lista_usuarios, numero_conta, AGENCIA)
            numero_conta += 1

        elif opcao_escolhida == "6":
            listar_contas(lista_contas)

        elif opcao_escolhida == "7":
            limpar_tela()
            print("Programa finalizado. Até mais!\n\n")
            break

        else:
            limpar_tela()
            print("Operação inválida, por favor selecione corretamente a operação desejada.")

        input("\nPressione Enter para voltar ao menu...")

main()
