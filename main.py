import random
from funcoes import *

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
    print("Biblioteca pygame não encontrada, instale-a para uma melhor experiência.")

ARQUIVO = "forca/palavras.txt"
RANKING = "forca/ranking.txt"

def jogar_forca():
    palavras = ler_palavras(ARQUIVO)
    if not palavras:
        print("Não existe palavras cadastradas.")
        return
    nome = input("Insira o seu nome: ")
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
    print("Dificuldade:", nivel_dificuldade(secreta))
    while tentativas > 0 and "_" in mostrada:
        print("\nPalavra:", " ".join(mostrada))
        print("Tentativas:", tentativas)
        print("Letras usadas:", usadas)
        print("Dicas restantes:", dicas)
        print("Digite uma letra ou '!' para o uso de dicas (-15 pontos)")
        entrada = input(">>").lower()
        if entrada == "!":
            if dicas > 0:
                usar_dica(secreta, mostrada)
                dicas -= 1
                pontos -= 15
                print("Você perdeu 15 pontos por usar uma dica.")
            else:
                print("Sem dicas restantes.")
            continue
        if len(entrada) != 1 or not entrada.isalpha():
            print("Entrada inválida.")
            continue
        if entrada in usadas:
            print("Letra já usada.")
            continue
        usadas.append(entrada)
        achou = False
        for i in range(len(secreta)):
            if secreta[i] == entrada:
                mostrada[i] = entrada
                achou = True
                pontos += 10
        if achou:
            print("Acertou!")
            if USAR_SOM:
                som_acerto.play()
        else:
            tentativas -= 1
            print("Errou!")
            if USAR_SOM:
                som_erro.play()
    if "_" not in mostrada:
        print("Parabéns, você acertou a palavra!")
        print("Pontuação:", pontos)
        if USAR_SOM:
            som_vitoria.play()
    else:
        print("Você errou a palavra! Mais sorte da próxima:", secreta)
        print("Pontuação:", pontos)
        if USAR_SOM:
            som_gameover.play()
    salvar_pontuacao(RANKING, nome, pontos)

def menu():
    while True:
        print("\nJOGO DA FORCA")
        print("1 - Jogar")
        print("2 - Adicionar palavra")
        print("3 - Lista de palavras")
        print("4 - Remover palavra")
        print("5 - Ver ranking")
        print("0 - Sair")
        op = input("Escolha uma opção: ")
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
            print("Você saiu do jogo.")
            break
        else:
            print("Opção inválida.")

menu()
