import random
import json
import time

def verificar_cartelas_batidas(cartelas, numeros_sorteados):
    """Verifica se alguma cartela foi batida com todos os números sorteados."""
    cartelas_batidas = []
    
    for numero_cartela, cartela in cartelas.items():
        cartela_batida = True
        for linha in cartela:
            for num in linha:
                if num not in numeros_sorteados:
                    cartela_batida = False
                    break
            if not cartela_batida:
                break

        if cartela_batida:
            cartelas_batidas.append((numero_cartela, cartela))
    
    return cartelas_batidas

def sorteio_bingo(cartelas):
    """Função para realizar o sorteio do bingo conforme os requisitos."""
    numeros_disponiveis = list(range(1, 76))
    numeros_sorteados = random.sample(numeros_disponiveis, 25)  # Sorteia 25 números únicos
    
    print("Números sorteados inicialmente:")
    print(sorted(numeros_sorteados))
    
    while True:
        # Verifica se houve cartelas batidas
        cartelas_batidas = verificar_cartelas_batidas(cartelas, numeros_sorteados)
        
        if cartelas_batidas:
            print("\nCartelas batidas:")
            for numero, cartela in cartelas_batidas:
                print(f"Cartela {numero}: {cartela}")
            print(f"Números sorteados: {sorted(numeros_sorteados)}")
            break
        
        # Se não houver cartelas batidas, sorteia uma nova dezena
        if len(numeros_sorteados) < 75:
            # Cria uma lista de números que ainda não foram sorteados
            numeros_faltantes = [num for num in numeros_disponiveis if num not in numeros_sorteados]
            
            # Sorteia um número dos números faltantes, se houver
            if numeros_faltantes:
                numero_sorteado = random.choice(numeros_faltantes)
                numeros_sorteados.append(numero_sorteado)
                print(f"Número sorteado: {numero_sorteado}")
                time.sleep(2)  # Espera 2 segundos antes de sortear o próximo número
            else:
                print("Não há mais números disponíveis para sortear.")
                break
        else:
            print("Número máximo de sorteios atingido.")
            break

def gerar_cartelas():
    num = int(input("Digite quantas cartelas você deseja criar: "))
    while num <= 0 or num > 10000:
        print("O número de cartelas deve ser entre 1 e 10.000. Tente novamente!")
        num = int(input("Digite novamente quantas cartelas você deseja criar:"))

    cartelas = {}
    while len(cartelas) < num:
        colunas = [[], [], [], [], []]
        intervalos = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]  # Intervalos para B, I, N, G, O

        for i in range(5):  # Itera sobre as colunas B, I, N, G, O
            while len(colunas[i]) < 5:
                numero = random.randint(intervalos[i][0], intervalos[i][1])
                if numero not in colunas[i]:  # Garante que não há números repetidos
                    colunas[i].append(numero)

        cartela = [sorted(coluna) for coluna in colunas]  # Organiza cada coluna em ordem crescente

        numero_correspondente = random.randint(1, 100000)
        if numero_correspondente not in cartelas:
            cartelas[numero_correspondente] = cartela

    return cartelas

def salvar_cartelas(cartelas, inicializar=False):
    """
    Salva as cartelas no arquivo.
    Se inicializar=True, o arquivo é zerado antes de salvar novas cartelas.
    Caso contrário, as novas cartelas são adicionadas ao arquivo existente.
    """
    modo = "w" if inicializar else "a"  # 'w' para zerar o arquivo, 'a' para adicionar ao existente
    with open("cartelas.txt", modo) as arquivo:
        for numero, cartela in cartelas.items():
            # Salva as cartelas em formato JSON
            arquivo.write(f"{numero}: {json.dumps(cartela)}\n")
    
    if inicializar:
        print("Arquivo de cartelas foi inicializado (limpo).")
    else:
        print("Novas cartelas adicionadas ao arquivo 'cartelas.txt'.")

def imprimir_cartela(cartelas, numero_cartela):
    # Verifica se a cartela existe no dicionário
    if numero_cartela not in cartelas:
        print(f"A cartela {numero_cartela} não existe!")
        return

    # Pega a cartela a partir do número fornecido
    cartela = cartelas[numero_cartela]

    # Imprimindo a cartela no formato solicitado
    print("+----+----+----+----+----+")
    print(f"| Cartela: {numero_cartela}         |")
    print("+----+----+----+----+----+")
    print("|  B |  I |  N |  G |  O |")
    print("+----+----+----+----+----+")

    # Imprime cada linha das colunas da cartela
    for c in range(5):  # Existem 5 linhas
        linha = f"| {cartela[0][c]:2} | {cartela[1][c]:2} | {cartela[2][c]:2} | {cartela[3][c]:2} | {cartela[4][c]:2} |"
        print(linha)
        print("+----+----+----+----+----+")

def ler_cartelas():
    try:
        with open("cartelas.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            cartelas = {}

            for linha in linhas:
                numero_cartela, cartela_str = linha.split(": ")
                cartela = json.loads(cartela_str.strip())  # Usa json.loads para converter a string no formato da cartela
                cartelas[int(numero_cartela)] = cartela

        print("Cartelas lidas e organizadas com sucesso.")
        return cartelas

    except FileNotFoundError:
        print("Arquivo 'cartelas.txt' não encontrado.")
        return None
    except json.JSONDecodeError:
        print("Erro ao decodificar o arquivo JSON.")
        return None

def menu_bingo():
    cartelas_geradas = None
    print("--- Seja Bem-Vindo ao Bingo ---")
    print("-="*16)
    print()
    print("Esse é o seu menu de opções:")
    print("1) Gerar Cartelas")
    print("2) Salvar Cartelas")
    print("3) Ler Cartelas")
    print("4) Imprimir Cartela")
    print("5) Sorteio do Bingo")
    print("6) Sair.")
    print()

    while True:
        pergunta = input("Digite um número correspondente à uma ação: ").strip()
        if pergunta == "1":
            cartelas_geradas = gerar_cartelas()
            print(f"{len(cartelas_geradas)} cartelas geradas com sucesso.")
        elif pergunta == "2":
            if cartelas_geradas:
                salvar_cartelas(cartelas_geradas, inicializar=True)
            else:
                print("Nenhuma cartela gerada para salvar.")
        elif pergunta == "3":
            cartelas_geradas = ler_cartelas()
        elif pergunta == "4":
            if cartelas_geradas:
                try:
                    numero = int(input("Digite o número da cartela que deseja imprimir: "))
                    imprimir_cartela(cartelas_geradas, numero)
                except ValueError:
                    print("Por favor, insira um valor válido.")
            else:
                print("Nenhuma cartela carregada.")
        elif pergunta == "5":
            if cartelas_geradas:
                sorteio_bingo(cartelas_geradas)
            else:
                print("Nenhuma cartela carregada.")
        elif pergunta == "6":
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha um número de 1 a 6.")

# Executar o menu principal
menu_bingo()
