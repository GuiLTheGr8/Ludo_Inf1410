from enum import Enum
import random

class Cor(Enum):
    vermelho = 0
    verde = 1
    amarelo = 2
    azul = 3


global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais


def novo_jogo():  # cria tudo necessário para o começo de uma partida
    global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais

    lista_peoes = [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]
    peoes_iniciais = [4, 4, 4, 4]

    pontuacao_jogadores = [0, 0, 0, 0]

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

    for item in lista_casas:
        print(item)

    for i in range(4):
        retafinal = list()

        for _ in range(6):
            casa = dict()
            casa['peoes'] = list()
            retafinal.append(casa.copy())

        retasfinais.append(retafinal.copy())

        print(retasfinais[i], i, Cor(i).name)


def passar_a_vez():
    global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais

    if vez >= 3:
        vez = 0
    else:
        vez += 1

    print('vez do', Cor(vez).name, vez, '!')


def posicionar_na_saida(peao):
    global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais

    lista_casas[13 * peao]['peoes'].append(peao)
    # OBS: Os números das casas de saída são múltiplos de 13

    print('após inserção:')
    print(lista_casas[13 * peao])


def posicionar(num_casa, cor_peao):
    global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais

    peao_na_casa = int()

    if len(lista_casas[num_casa]['peoes']) > 0:
        peao_na_casa = lista_casas[num_casa]['peoes'][0]

    if peao_na_casa and peao_na_casa != cor_peao and lista_casas[num_casa]['tipo'] != 'abrigo':
        captura(peao_na_casa, num_casa)

    lista_casas[num_casa]['peoes'].append(cor_peao)

def movimentar(casa_origem, cor_peao, movimentos):
    global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais

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

        # TODO: somar o número de casas percorridas ao score do jogador da cor do peão
        # para definir colocações ao final da partida

    posicionar(casa_origem, cor_peao)


def abrigo(posicao, peao):
    global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais

    if len(lista_casas[posicao]['peoes']) < 2:
        lista_casas[posicao]['peoes'].append(peao)
    else:
        print("Abrigo so para 2 pecas diferentes")
        exit(0)


def voltar_ao_inicio(peao):
    global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais

    if peoes_iniciais[peao] == 4:
        print("Casas cheias")
    else:
        peoes_iniciais[peao] = peoes_iniciais[peao] + 1


def retirar_do_inicio(peao):
    global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais

    if peoes_iniciais[peao] == 0:
        print("Casas estão vazias")
    else:
        peoes_iniciais[peao] = peoes_iniciais[peao] - 1


def captura(peao, posicao):
    global vez, lista_casas, retasfinais, bases, pontuacao_jogadores, lista_peoes, peoes_iniciais

    if len(lista_casas[posicao]['peoes']) == 0:
        print("Vazia")
        return
    else:
        b = lista_casas[posicao]['peoes'].pop(0)
        print('Capturou:', b)
        voltar_ao_inicio(b)
        return


def rolardados():
    global rolar, resul1, resul2, result3, TURN, rolagens, indice, ultimo

    rolar = rolar + 1  # vendo inicio da rolagem, e o turno do jogadador da vez
    if rolar == 1:
        result1 = random.randint(1, 6)  # sortear numero de 1 a 6
        print("Resultado da Primeira Rolagem", result1)  # mostrar numero sorteado
        rolagens.append(result1)  # o valor sorteado entra na lista de rolagens
        # movimentar(casa_origem, cor_peao, result1) #chamar a função de movimento recebendo o número sorteado, casa inicial e cor do peao
        if result1 != 6:  # se numero sorteado for diferente de 6
            rolar = 0  # variavel de rolagem é limpa
            vez = False  # vez é passado para o próximo jogador
        rolar = rolar + 1
    # se result1 for 6, rolar dado novamente
    if rolar == 2:
        if result1 == 6:
            result2 = random.randint(1, 6)  # sortear numero de 1 a 6
            print("Resultado da Segunda Rolagem", result2)  # mostrar numero sorteado
            rolagens.append(result2)  # o valor sorteado entra na lista de rolagens
            # movimentar(casa_origem, cor_peao, result2) #chamar a função de movimento recebendo o número sorteado, casa inicial e cor do peao
            if result2 != 6:  # se numero sorteado for diferente de 6
                rolar = 0  # variavel de rolagem é limpa
                vez = False  # vez é passado para o próximo jogador
            rolar = rolar + 1
    # se result2 for 6, rolar dado novamente
    if rolar == 3:
        if result2 == 6:
            result3 = random.randint(1, 6)  # sortear numero de 1 a 6
            print("Resultado da Terceira Rolagem", result3)  # mostrar numero sorteado
            rolagens.append(result3)  # o valor sorteado entra na lista de rolagens
            if result3 != 6:  # se numero sorteado for diferente de 6
                # movimentar(casa_origem, cor_peao, result3) #chamar a função de movimento recebendo o número sorteado, casa inicial e cor do peao
                rolar = 0  # variavel de rolagem é limpa
                vez = False  # vez é passado para o próximo jogador
            if result3 == 6:
                indice = len(
                    lista_peoes) - 1  # acessa o tamanho da lista e -1 para obter o indice do ultimo elemento da lista
                ultimo = lista[indice]  # acessa o ultimo item da lista
                print("Último Peão Moviemntado", ultimo)
                # 15 nesse exemplo que criei
                if ultimo in retafinal():  # se o ultimo peao movimentado estiver na lista de reta final(nada acontece)
                    rolar = 0  # variavel de rolagem é limpa
                    vez = False  # passa a vez
                # caso contrario
                posicionar_no_inicio(lista, vez, inicial)
                # chama funcao movimento que move ultimo peao pra casa inicial
                # inicia peoes recebe peoesclicacos[ultimo](???)
                # casainicial.append(peoesclicados[ultimo])#não acho que seja assim

# ---------------------------TESTES--------------------------------------------

novo_jogo()

posicionar_na_saida(0)
posicionar_na_saida(2)

for i in range(10):
    passar_a_vez()

movimentar(0, 0, 5)

posicionar(10, 3)

movimentar(10, 3, 2)

movimentar(5, 0, 7)

movimentar(20, lista_peoes[0][1], 5)

for item in lista_casas:
    print(item)
