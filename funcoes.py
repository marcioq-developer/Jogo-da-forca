'''Cores'''
verde = "\033[92m"
vermelho = "\033[91m"
amarelo = "\033[93m"
azul = "\033[94m"
reset = "\033[0m"
cinza = "\033[90m"
ciano = "\033[96m"
laranja = "\033[38;5;208m"

'''Funções básicas do menu de interação'''

import random

def ler_palavras(arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as arq:
            return arq.read().splitlines()
    except:
        return []
def salvar_palavras(arquivo, palavras):
    with open(arquivo, "w", encoding="utf-8") as arq:
        for p in palavras:
            arq.write(p + "\n")
def salvar_pontuacao(ranking_arquivo, nome, pontos):
    ranking = {}
    try:
        with open(ranking_arquivo, "r", encoding="utf-8") as arq:
            for linha in arq:
                n, p = linha.strip().split(" - ")
                ranking[n] = int(p)
    except:
        pass
    if nome in ranking:
        ranking[nome] += pontos
    else:    
        ranking[nome] = pontos
    with open(ranking_arquivo, "w", encoding="utf-8") as arq:
        for n, p in ranking.items():
            arq.write(f"{n} - {p}\n")

'''Menu do jogo'''

def adicionar_palavra(arquivo):
    palavra = input(amarelo+"Digite a palavra que deseja adicionar: "+reset).lower()
    palavras = ler_palavras(arquivo)
    palavras.append(palavra)
    salvar_palavras(arquivo, palavras)
    print(verde+"Sua palavra foi adicionada."+reset)
def listar_palavras(arquivo):
    palavras = ler_palavras(arquivo)
    if not palavras:
        print(vermelho+"Erro, Nenhuma palavra foi cadastrada."+reset)
        return
    for i, p in enumerate(palavras, start=1):
        print(i, "-", p)
def remover_palavra(arquivo):
    palavras = ler_palavras(arquivo)
    if not palavras:
        print(laranja+" A lista está vazia."+reset)
        return
    listar_palavras(arquivo)
    pos = int(input(amarelo+"Insira o id da palavra para remover: "+reset)) - 1
    if 0 <= pos < len(palavras):
        palavras.pop(pos)
        salvar_palavras(arquivo, palavras)
        print(verde+"Palavra removida com sucesso."+reset)
    else:
        print(vermelho+"id inválido."+reset)

''' Nivel de dificuldade com base na quantidade de letras'''

def nivel_dificuldade(palavra):
    tamanho = len(palavra.replace(" ", ""))
    if tamanho <= 4:
        return verde+"Fácil"+reset
    elif tamanho <= 8:
        return amarelo+"Médio"+reset
    elif tamanho <= 12:
        return laranja+"Difícil"+reset
    else:
        return vermelho+"Impossível"+reset

''' Sistema de dicas com perda de pontos '''

def usar_dica(secreta, mostrada):
    letras = [
        secreta[i] for i in range(len(secreta))
        if mostrada[i] == "_" and secreta[i] != " "]
    if not letras:
        return False
    letra = random.choice(letras)
    for i in range(len(secreta)):
        if secreta[i] == letra:
            mostrada[i] = letra
    print(f" Você usou uma dica. Letra revelada: '{letra}'")
    return True

'''Visualização do ranking'''

def mostrar_ranking(ranking_arquivo):
    ranking = {}
    try:
        with open(ranking_arquivo, "r", encoding="utf-8") as arq:
            for linha in arq:
                n, p = linha.strip().split(" - ")
                ranking[n] = int(p)
    except:
        print(vermelho+"Nenhum ranking encontrado."+reset)
        return
    if not ranking:
        print(laranja+"Nenhum player registrado."+reset)
        return
    ranking_ordenado = []
    for jogador in ranking:
        ranking_ordenado.append((jogador, ranking[jogador]))
    for i in range(len(ranking_ordenado)):
        for j in range(i + 1, len(ranking_ordenado)):
            if ranking_ordenado[j][1] > ranking_ordenado[i][1]:
                ranking_ordenado[i], ranking_ordenado[j] = ranking_ordenado[j], ranking_ordenado[i]
    print(azul+" RANKING DOS JOGADORES"+reset)
    for i, (nome, pontos) in enumerate(ranking_ordenado, start=1):
        print(amarelo+f"{i}. {nome} - {pontos} pontos")