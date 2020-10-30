from itertools import cycle
from enum import Enum

lista_peoes = [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
peoes_iniciais = [4, 4, 4, 4]


class Cor(Enum):
    vermelho = 0
    verde = 1
    amarelo = 2
    azul = 3


def novo_jogo():  # cria tudo necessário para o começo de uma partida
    global vez, casas, lista_casas, retasfinais, bases, jogadores

    vez = -1
    lista_casas = list()
    retasfinais = list()

    for i in range(52):  # inicializa cada casa (menos as finais de cada cor)
        casa = dict()
        casa['numero'] = i
        casa['peoes'] = list()  # lista vazia de peões ocupando aquela casa
        if i == 0 or i == 13 or i == 26 or i == 39:
            casa['tipo'] = 'saida'
        elif i == 9 or i == 22 or i == 35 or i == 48:
            casa['tipo'] = 'abrigo'
        else:
            casa['tipo'] = 'comum'
        lista_casas.append(casa.copy())

    casas = cycle(lista_casas)  # fazendo lista circular de casas

    for item in lista_casas:
        print(item)

    jogadores = list()
    for i in range(4):
        retafinal = list()

        for i in range(6):
            casa.clear()
            casa['peoes'] = list()
            retafinal.append(casa.copy())

        retasfinais.append(retafinal.copy())

    for i in range(retasfinais.count(retafinal)):
        print(retasfinais[i], i, Cor(i).name)


def passar_a_vez():
    global vez, casas, lista_casas, retasfinais, bases, jogadores

    if vez >= 3:
        vez = 0
    else:
        vez += 1

    print('vez do', Cor(vez).name, vez, '!')


def posicionar_na_saida(peao):
    global vez, casas, lista_casas, retasfinais, bases, jogadores

    lista_casas[13 * peao]['peoes'].append(peao)
    # OBS: Os números das casas de saída são múltiplos de 13

    print('após inserção:')
    print(lista_casas[13 * peao])


def posicionar(num_casa, cor_peao):
    lista_casas[num_casa]['peoes'].append(cor_peao)


def movimentar(casa_origem, cor_peao, movimentos):
    global vez, casas, lista_casas, retasfinais, bases, jogadores

    if cor_peao in lista_casas[casa_origem]['peoes']:
        lista_casas[casa_origem]['peoes'].remove(cor_peao)
    else:
        print('ERRO, não existe peão da cor especificada na casa especificada!')
        return

    casas_percorridas = 0

    while movimentos > 0:

        # REGRA DO 6: No caso de tirar 6 no dado, salvar a ultima posição e a cor do peão movimentado
            # Caso saia 6 pela terceira vez, pegar esse peão e trazê-lo de volta a casa inicial

        # TODO: verificar se peão precisa ir para a reta final
        # TODO: se sim, chamar função de posicionamento na reta final, passando os movimentos restantes como parâmetro

        if casa_origem == 51:
            casa_origem = 0
        else:
            casa_origem += 1

        # TODO: chamar verificação de barreiras aqui
        # TODO: se houver barreira, posicionar na casa anterior e dar break

        movimentos -= 1
        casas_percorridas += 1

        # TODO: somar o número de casas percorridas ao score do jogador da cor do peão, para definir colocações ao final da partida

    posicionar(casa_origem, cor_peao)


def abrigo(posicao, peao):
    if len(lista_casas[posicao]['peoes']) < 2:
        lista_casas[posicao]['peoes'].append(peao)
    else:
        print("Abrigo so para 2 pecas diferentes")
        exit(0)


def voltar_ao_inicio(peao):
    if peoes_iniciais[peao] == 4:
        print("Casas cheias")
    else:
        peoes_iniciais[peao] = peoes_iniciais[peao] + 1


def retirar_do_inicio(peao):
    if peoes_iniciais[peao] == 0:
        print("Casas estão vazias")
    else:
        peoes_iniciais[peao] = peoes_iniciais[peao] - 1


def captura(peao, posicao):
    global vez, casas, lista_casas, retasfinais, bases, jogadores

    if len(lista_casas[posicao]['peoes']) == 0:
        print("Vazia")
        return
    else:
        b = lista_casas[posicao]['peoes'].pop(0)
        print(b)
        # lista_casas['peoes'].clear()
        lista_casas[posicao]['peoes'].append(peao)
        voltar_ao_inicio(b)
        exit(0)


# ---------------------------TESTES--------------------------------------------

novo_jogo()

posicionar_na_saida(0)
posicionar_na_saida(2)

for i in range(10):
    passar_a_vez()

movimentar(0, 0, 5)

posicionar(10, 3)

movimentar(10, 3, 2)

movimentar(20, lista_peoes[0][1], 5)

for item in lista_casas:
    print(item)
