# TRABALHO DE INTELIGENCIA ARTIFICIAL
# RESOLVER O PROBLEMA DOS CANIBAIS E MISSIONÁRIOS
# MÉTODO USADO: BUSCA CEGA --
# -- Estratégia de busca sem informação
# -- Usa-se apenas a informação disponível na definição do problema

class Estado:

    # Representa um estado dentro de uma árvore de estados do problema
    # Um estado contém:
    # A quantidade de MISSIONÁRIOS A ESQUERDA do rio = missionarios_esq
    # MISSIONÁRIOS A DIREITA do rio = missionarios_dir
    # a quantidade de CANIBAIS A ESQUERDA do rio = canibais_esq
    # CANIBAIS A DIREITA do rio = canibais_dir
    # o LADO DO RIO = lado_rio
    # seu PAI = pai e seus FILHO = filhos

    # Um estado pode ser VÁLIDO OU NÃO

    def __init__(self, missionarios_esq, missionarios_dir, canibais_esq, canibais_dir, lado_rio):

        # inicializador do estado com suas informações

        self.missionarios_esq = missionarios_esq
        self.missionarios_dir = missionarios_dir
        self.canibais_esq = canibais_esq
        self.canibais_dir = canibais_dir
        self.lado_rio = lado_rio
        self.pai = None
        self.filhos = []

    def __str__(self):

        # faz a representação do estado
        # responsável por imprimir seus dados na tela com as informações

        return '\n\nMissionarios: {}\t ~~~~~~ Missionarios: {}\nCanibais: {}\t ~~~~~~ Canibais: {}'.format(
            self.missionarios_esq, self.missionarios_dir, self.canibais_esq, self.canibais_dir
        )

    def estado_valido(self):

        # verifica se o estado é valido
        # nao pode haver mais CANIBAIS do que MISSIONÁRIOS em nenhum dos lados

        # a quantidade de pessoas nao pode ser negativa
        if ((self.missionarios_esq < 0) or (self.missionarios_dir < 0)
                or (self.canibais_esq < 0) or (self.canibais_dir < 0)):
            return False

        # se nao tiver MISSIONARIOS no lado, nao precisa verificar
        return ((self.missionarios_esq == 0 or self.missionarios_esq >= self.canibais_esq) and
                (self.missionarios_dir == 0 or self.missionarios_dir >= self.canibais_dir))

    def estado_final(self):

        # verifica se o estado é uma SOLUÇÃO para o problema
        # Um estado é um estado final se todos os missionários e canibais atravessaram o rio
        # não pode haver ninguém na ESQUERDA e todos devem estar na DIREITA

        resultado_esq = self.missionarios_esq == self.canibais_esq == 0
        resultado_dir = self.missionarios_dir == self.canibais_dir == 3
        return resultado_esq and resultado_dir

    def gerar_filhos(self):

        # Gera todos os possíveis filhos de um estado, se for VÁLIDO E NÃO FOR FINAL

        # Encontra o NOVO LADO DO RIO

        novo_lado_rio = 'dir' if self.lado_rio == 'esq' else 'esq'

        # Gera a lista de possíveis movimentos

        movimentos = [
            {'missionarios': 2, 'canibais': 0},
            {'missionarios': 1, 'canibais': 0},
            {'missionarios': 1, 'canibais': 1},
            {'missionarios': 0, 'canibais': 1},
            {'missionarios': 0, 'canibais': 2},
        ]

        # Gera todos os possíveis estados e armazena apenas os válidos na lista de filhos
        # do estado atual

        for movimento in movimentos:
            if self.lado_rio == 'esq':

                # Se o barco estiver a esquerda do rio, os missionários e canibais saem da
                # margem esquerda do rio e vão para a direita
                missionarios_esq = self.missionarios_esq - movimento['missionarios']
                missionarios_dir = self.missionarios_dir + movimento['missionarios']
                canibais_esq = self.canibais_esq - movimento['canibais']
                canibais_dir = self.canibais_dir + movimento['canibais']

            else:

                # Caso contrário, os missionários e canibais saem da margem direita do rio
                # e vão para a esquerda
                missionarios_dir = self.missionarios_dir - movimento['missionarios']
                missionarios_esq = self.missionarios_esq + movimento['missionarios']
                canibais_dir = self.canibais_dir - movimento['canibais']
                canibais_esq = self.canibais_esq + movimento['canibais']

            # Cria o estado do filho e caso este seja válido, o adiciona à lista de filhos do pai
            filho = Estado(missionarios_esq, missionarios_dir, canibais_esq, canibais_dir, novo_lado_rio)
            filho.pai = self

            if filho.estado_valido():
                self.filhos.append(filho)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Missionarios_Canibais:

    # FUNÇÃO RESPONSAVEL POR RESOLVER O PROBLEMA
    # VAI GERAR A POSSIVEL ÁRVORE DE ESTADOS

    def __init__(self):

        # Inicializa uma instância do problema com uma raiz pré-definida e ainda sem solução

        # Insere a raiz na fila de execução, que será utilizada para fazer uma busca em largura:
        # começa com os 3 MISSIONARIOS e os 3 CANIBAIS no LADO ESQUERDO

        self.fila_execucao = [Estado(3, 0, 3, 0, 'esq')]
        self.solucao = None


    def gerar_solucao(self):

        # buscar a solução da ÁRVORE DE ESTADOS --> algoritmo de busca cega
        # Utiliza uma fila em sua execução

        estados = 0     # contagem de estados feita quando alcança o estado final
        for elemento in self.fila_execucao:

            if elemento.estado_final():
                # Se a solução foi encontrada, o caminho que compõe a solução é gerado realizando
                # o caminho de volta até a raiz da árvore de estados e então encerra a busca

                self.solucao = [elemento]
                while elemento.pai:
                    self.solucao.insert(0, elemento.pai)
                    elemento = elemento.pai
                    estados = estados + 1
                break

            # Caso o elemento não seja a solução, gera seus filhos e os adiciona na fila de execução
            elemento.gerar_filhos()
            estados = estados + 1
            self.fila_execucao.extend(elemento.filhos)

        print("\n\n\tNúmero de estados: ", estados)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def main():
    # Instancia o problema e gera sua solução

    import time

    inicio = time.time()
    problema = Missionarios_Canibais()
    problema.gerar_solucao()

    # Exibe a solução em tela, separando cada passo
    cont = 0

    for estado in problema.solucao:
        print(estado)
        cont = cont + 1
        print(34 * '-')

    fim = time.time()
    print("\n\nIterações: ", cont)
    print("\nTempo de execução: ", fim - inicio)


if __name__ == '__main__':
    main()
