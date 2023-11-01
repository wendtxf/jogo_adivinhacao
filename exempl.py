# -*- coding: utf-8 -*-

import sqlite3
import random
import os #Adicionado em: 01/11/23 - wendtxf
from datetime import datetime

# importações: o codigo começa importando os módulos necessários para o jogo:
# sqlite3 para interagir com um banco de dados SQLite.
# random para gerar números aleatórios.
# os para realizar a execução de comandos do S.O.
# datetime para trabalhar com datas e horas.

# Nota: O comando "os.system('cls')" está setado para a execução em Windows, caso o programa seja executado em Linux ou MAC deverá ser utilizado da seguinte forma:   "os.system('clear')"

def criar_tabela_partidas():  # função criar_tabela_partidas responsável por criar uma tabela chamada "partidas" no banco de dados SQLite 'exemplo.db', se ela ainda não existir.
    conn = sqlite3.connect(
        "exemplo.db"
    )  # é estabelecida uma conexão com o banco de dados SQLite 'exemplo.db' usando a função 'connect' do módulo 'sqlite3'. Se o banco de dados não existir, ele será criado neste momento.
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT,
            tentativas INTEGER,
            inicio DATETIME,
            fim DATETIME)""")
    # ^aqui foi feita uma instrução sql para criar uma tabela chamada 'partidas' caso ela nao exista. e a tabela tem as colunas: id, nome de usuario, tentativas, inicio e fim.

    conn.close()  # dps de criar a tabela no banco de dados, eu fecho a conexao com o banco de dados

def obter_numero_valido():
    while True:
        numero_str = input ("Digite um número: ")
        try:
            numero = int(numero_str)
            return numero
        except ValueError:
            print("Por favor, digite apenas números, letras e caracteres não são permitidos")

def calculo_media_pontuacao():
    conn = sqlite3.connect('exemplo.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome_usuario, tentativas FROM partidas")
    resultados = cursor.fetchall()
    conn.close()

    pontuacoes = {}
    for nome, tentativas in resultados:
        if nome not in pontuacoes:
            pontuacoes[nome] = []
        pontuacoes[nome].append(tentativas)

    medias = {}
    for nome, tentativas in pontuacoes.items():
        media = sum(tentativas) / len(tentativas)
        medias[nome] = media

    return medias

def iniciar_jogo(nome_usuario):
    numero_secreto = random.randint(1, 100)  # a funcao inicia definindo um numero aleatorio entre 1 e 100 e inicializa o contador de tentativas como 0.
    tentativas = 0
    os.system('cls') #Adicionado em: 01/11/23 - wendtxf
    print(
        f"Bem-vindo, {nome_usuario}! Vamos começar o jogo de adivinhação."
    )  # imprime msg de boas vindas
    print("Estou pensando em um número entre 1 e 100. Tente adivinhar.\n")

    inicio_jogo = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #obtida a data e hora atuais
    while True:
        tentativa = int(input("Digite um número: "))
        tentativas += 1 #loop que dxa que o jogador fzer varias tentativas p adivinhar o numero secreto a cada tentativa, o jogador é solicitado a digitar um número e o contador de tentativas é incrementado.

        if tentativa < numero_secreto:
            print("Tente um número maior.\n")
        elif tentativa > numero_secreto:
            print("Tente um número menor.\n")
        else:
            os.system('cls') #Adicionado em: 01/11/23 - wendtxf
            print(
                f"Parabéns! Você acertou em {tentativas} tentativas.\n"
            )  # dependendo da tentativa do jogador, fornece uma dica se o número a ser adivinhado é maior ou menor. ai se o jogador adivinhar, ele passa para a parte do código onde é parabenizado e o jogo é encerrado.

            fim_jogo = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )  # qnd o jogador adivinha, a data e hora atual são registradas como o fim do jogo.

            conn = sqlite3.connect(
                "exemplo.db"
            )  # dps a função se conecta ao banco de dados e insere os detalhes da partida (nome do usuário, número de tentativas, início e fim do jogo) na tabela 'partidas'.
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO partidas (nome_usuario, tentativas, inicio, fim) VALUES (?, ?, ?, ?)",
                (nome_usuario, tentativas, inicio_jogo, fim_jogo),
            )
            conn.commit()

            conn.close()  # dps de inserir os dados, a conexão com o banco de dados é fechada.

            medias = calculo_media_pontuacao()
            if nome_usuario in medias:
                media_usuario = medias[nome_usuario]
                print(f"Sua média de tentativas: {media_usuario}\n")
                media_total = sum(medias.values()) / len(medias)
                print(f"Média geral dos jogadores: {media_total}\n")

                if media_usuario <= media_total:
                    print("Vc está na média dos jogadores")
                else:
                    print("Vc está acima da média dos jogadores") 
            break  # loop encerrado

    #Adicionado em: 01/11/23 - wendtxf
    print("\n------------------------------")
    replay = str(input("\nDeseja jogar novamente? (s/n): "))
    if replay == 's' or replay == 'S':
        os.system('cls')
        nome_usuario = input("Digite seu nome: ")
        if nome_usuario == '':
            nome_usuario = 'Jogador'
        iniciar_jogo(nome_usuario)
    elif replay == 'n' or replay == 'N':
        os.system('cls')  
    if (replay != 's' and replay != 'S') and (replay !='n' and replay != 'N'):
        print('\nEntrada Inválida')

if __name__ == "__main__":
    os.system('cls') #Adicionado em: 01/11/23 - wendtxf
    nome_usuario = input("Digite seu nome: ")
    if nome_usuario == '':
        nome_usuario = 'Jogador'
    criar_tabela_partidas()
    iniciar_jogo(nome_usuario)