'''Imports principais'''

import random
from funcoes import *

'''Cores'''
verde = "\033[92m"
vermelho = "\033[91m"
amarelo = "\033[93m"
azul = "\033[94m"
reset = "\033[0m"
cinza = "\033[90m"
ciano = "\033[96m"
laranja = "\033[38;5;208m"

'''Verificação da biblioteca de sons'''

USAR_SOM = False
try:
    import pygame
    pygame.init()
    pygame.mixer.init()
    som_acerto = pygame.mixer.Sound("audio/acerto_da_letra.wav")
    som_erro = pygame.mixer.Sound("audio/erro.mp3")
    som_vitoria = pygame.mixer.Sound("audio/booyah-free-fire.mp3")
    som_gameover = pygame.mixer.Sound("audio/faustao-errou-game-over.mp3")
    pygame.mixer.music.load("audio/musica_de_fundo.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    USAR_SOM = True
except:
    print(amarelo + "Biblioteca pygame não encontrada, instale-a para uma melhor experiência." + reset)

'''Caminho de arquivos'''

ARQUIVO = "forca/palavras.txt"
RANKING = "forca/ranking.txt"

'''Boneco interface no próprio terminal'''

boneco = [
    """
    
    
    
    
    """,
    """
      O
    
    
    """,
    """
      O
      |
    
    """,
    """
      O
     /|
    
    """,
    """
      O
     /|\\
    
    """,
    """
      O
     /|\\
     /
    """,
    """
      O
     /|\\
     / \\
    """
]
'''base do jogo'''

def jogar_forca():
    palavras = ler_palavras(ARQUIVO)
    if not palavras:
        print(vermelho+"Não existe palavras cadastradas."+reset)
        return
    nome = input(azul+"Insira o seu nome: "+reset)
    secreta = random.choice(palavras)
    mostrada = []
    for c in secreta:
        if c != " ":
            mostrada.append("_")        
        else:
            mostrada.append("")
    tentativas = 6
    usadas = []
    pontos = 0
    dicas = 2
    print(azul+"Dificuldade:"+reset, nivel_dificuldade(secreta))
    while tentativas > 0 and "_" in mostrada:
        print(vermelho+boneco[6 - tentativas]+reset)
        print("\nPalavra:", " ".join(mostrada))
        print(vermelho+"Tentativas:"+reset, tentativas)
        print(amarelo+"Letras usadas:"+reset, usadas)
        print(amarelo+"Dicas restantes:"+reset, dicas)
        print(azul+"Digite uma letra ou '!' para o uso de dicas (-15 pontos)"+reset)
        entrada = input(">>").lower()
        if entrada == "!":
            if dicas > 0:
                usar_dica(secreta, mostrada)
                dicas -= 1
                pontos -= 15
                print(vermelho+"Você perdeu 15 pontos por usar uma dica."+reset)
            else:
                print(vermelho+"Sem dicas restantes."+reset)
            continue
        if len(entrada) != 1 or not entrada.isalpha():
            print(vermelho+"Entrada inválida."+reset)
            continue
        if entrada in usadas:
            print(amarelo+"Letra já usada."+reset)
            continue
        usadas.append(entrada)
        achou = False
        for i in range(len(secreta)):
            if secreta[i] == entrada:
                mostrada[i] = entrada
                achou = True
                pontos += 10
        if achou:
            print(verde+"Acertou!"+reset)
            if USAR_SOM:
                som_acerto.play()
        else:
            tentativas -= 1
            print(vermelho+"Errou!"+reset)
            if USAR_SOM:
                som_erro.play()
    if "_" not in mostrada:
        print(verde+"Parabéns, você acertou a palavra!"+reset)
        print(azul+"Pontuação:"+reset, pontos)
        if USAR_SOM:
            som_vitoria.play()
    else:
        print(vermelho+"Você errou a palavra! Mais sorte da próxima:"+reset, secreta)
        print(azul+"Pontuação:"+reset, pontos)
        if USAR_SOM:
            som_gameover.play()
    salvar_pontuacao(RANKING, nome, pontos)

'''Menu de interação'''

def menu():
    while True:
        print(azul+"\n JOGO DA FORCA"+reset)
        print(verde+"1 - Jogar"+reset)
        print(ciano+"2 - Adicionar palavra"+reset)
        print(amarelo+"3 - Lista de palavras"+reset)
        print(vermelho+"4 - Remover palavra"+reset)
        print(verde+"5 - Ver ranking"+reset)
        print(cinza+"0 - Sair"+reset)
        op = input(amarelo+"Escolha uma opção: "+reset)
        if op == "1":
            jogar_forca()
        elif op == "2":
            adicionar_palavra(ARQUIVO)
        elif op == "3":
            listar_palavras(ARQUIVO)
        elif op == "4":
            remover_palavra(ARQUIVO)
        elif op == "5":
            mostrar_ranking(RANKING)
        elif op == "0":
            if USAR_SOM:
                pygame.mixer.music.stop()
            print(cinza+"Você saiu do jogo."+reset)
            break
        else:
            print(vermelho+"Opção inválida."+reset)
menu()