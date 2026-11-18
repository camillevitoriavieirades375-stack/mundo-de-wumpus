import random

class AgenteReativoV1:
    def __init__(self):
        self.tem_flecha = True

    def escolher_acao(self, percepcoes):
        movimentos = ['mov(N)', 'mov(S)', 'mov(L)', 'mov(O)']
        disparos = ['atirar(N)', 'atirar(S)', 'atirar(L)', 'atirar(O)']

        if 'br' in percepcoes:
            acoes_possiveis = ['pegar']
        elif 'f' in percepcoes:
            acoes_possiveis = list(movimentos)
            if self.tem_flecha:
                acoes_possiveis.extend(disparos)
        else:
            acoes_possiveis = list(movimentos)
            if not percepcoes:
                acoes_possiveis.append('fim')

        acao_escolhida = random.choice(acoes_possiveis)

        if acao_escolhida.startswith('atirar'):
            self.tem_flecha = False

        return acao_escolhida
