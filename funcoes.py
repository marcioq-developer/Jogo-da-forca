import random

def ler_palavras(arquivo):
    try:
        with open(arquivo,"r",encoding="utf-8") as arq:
            return arq.read().splitlines()
    except:
        return []

def salvar_palavras(arquivo,palavras):
    with open(arquivo,"w",encoding="utf-8") as arq:
        for p in palavras:
            arq.write(p+"\n")

def salvar_pontuacao(ranking_arquivo,nome,pontos):
    ranking={}
    try:
        with open(ranking_arquivo,"r",encoding="utf-8") as arq:
            for linha in arq:
                n,p=linha.strip().split(" - ")
                ranking[n]=int(p)
    except:
        pass
    if nome in ranking:
        ranking[nome]+=pontos
    else:
        ranking[nome]=pontos
    with open(ranking_arquivo,"w",encoding="utf-8") as arq:
        for n,p in ranking.items():
            arq.write(f"{n} - {p}\n")

def adicionar_palavra(arquivo):
    palavra=input("Digite a palavra que deseja adicionar: ").lower()
    palavras=ler_palavras(arquivo)
    palavras.append(palavra)
    salvar_palavras(arquivo,palavras)
    print("Sua palavra foi adicionada.")

def listar_palavras(arquivo):
    palavras=ler_palavras(arquivo)
    if not palavras:
        print("Erro, nenhuma palavra foi cadastrada.")
        return
    for i,p in enumerate(palavras,start=1):
        print(i,"-",p)

def remover_palavra(arquivo):
    palavras=ler_palavras(arquivo)
    if not palavras:
        print("A lista está vazia.")
        return
    listar_palavras(arquivo)
    pos=int(input("Insira o id da palavra para remover: "))-1
    if 0<=pos<len(palavras):
        palavras.pop(pos)
        salvar_palavras(arquivo,palavras)
        print("Palavra removida com sucesso.")
    else:
        print("Id inválido.")

def nivel_dificuldade(palavra):
    tamanho=len(palavra.replace(" ",""))
    if tamanho<=4:
        return "Fácil"
    elif tamanho<=8:
        return "Médio"
    elif tamanho<=12:
        return "Difícil"
    else:
        return "Impossível"

def usar_dica(secreta,mostrada):
    letras=[secreta[i] for i in range(len(secreta)) if mostrada[i]=="_" and secreta[i]!=" "]
    if not letras:
        return False
    letra=random.choice(letras)
    for i in range(len(secreta)):
        if secreta[i]==letra:
            mostrada[i]=letra
    print(f"Você usou uma dica. Letra revelada: '{letra}'")
    return True

def mostrar_ranking(ranking_arquivo):
    ranking={}
    try:
        with open(ranking_arquivo,"r",encoding="utf-8") as arq:
            for linha in arq:
                n,p=linha.strip().split(" - ")
                ranking[n]=int(p)
    except:
        print("Nenhum ranking encontrado.")
        return
    if not ranking:
        print("Nenhum player registrado.")
        return
    ranking_ordenado=[]
    for jogador in ranking:
        ranking_ordenado.append((jogador,ranking[jogador]))
    for i in range(len(ranking_ordenado)):
        for j in range(i+1,len(ranking_ordenado)):
            if ranking_ordenado[j][1]>ranking_ordenado[i][1]:
                ranking_ordenado[i],ranking_ordenado[j]=ranking_ordenado[j],ranking_ordenado[i]
    print("RANKING DOS JOGADORES")
    for i,(nome,pontos) in enumerate(ranking_ordenado,start=1):
        print(f"{i}. {nome} - {pontos} pontos")
