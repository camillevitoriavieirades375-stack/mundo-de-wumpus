import random
from typing import Set, Tuple, Dict, List, Any

class AmbienteWumpus:
    # Etapa 1 - Gerador Aleatorio de Ambientes do Mundo de Wumpus
    def __init__(self, dimensao: int = 4, qtd_pocos: int = 3, qtd_wumpus: int = 1, qtd_ouro = 1):
        if dimensao < 3:
            raise ValueError ("A dimensao da grade deve ser n >= 3")

        self.dimensao = dimensao
        self.inicio_agente = (0,0)

        self.qtd_pocos = qtd_pocos
        self.qtd_wumpus = qtd_wumpus
        self.qtd_ouro = qtd_ouro

        # Cordenadas de cordenadas p busca eficiente {(linha, coluna)}
        self.pocos: Set[Tuple[int, int]] = set()
        self.wumpus: Set[Tuple[int, int]] =set()
        self.ouro: Set[Tuple[int, int]] = set()

        # Dicionario mapeando cada celula para o seu conjunto de percepcoes
        self.percepcoes: Dict[Tuple[int, int], Set[str]] = {
            (lin, col): set() for lin in range(dimensao) for col in range(dimensao)
        }

        self._gerar_mundo()

    def _obter_vizinhos(self, lin: int, col: int) -> List[Tuple[int, int]]:
        """Retorna as casas vizinhas ortogonais validas (Cima, Baixo, Esquerda, Direita)."""
        vizinhos = []
        deslocamentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d_lin, d_col in deslocamentos:
            nova_lin, nova_col = lin + d_lin, col + d_col
            if 0 <= nova_lin < self.dimensao and 0 <= nova_col < self.dimensao:
                vizinhos.append((nova_lin, nova_col))
        return vizinhos

    def _gerar_mundo(self) -> None:
        """Gera entidades e calcula percepcoes seguindo as regras do Slide 22."""
        # 1. Casas candidatas a receber elementos (exceto a casa inicial (0, 0))
        casas_disponiveis = [
            (lin, col) 
            for lin in range(self.dimensao) 
            for col in range(self.dimensao) 
            if (lin, col) != self.inicio_agente
        ]
        random.shuffle(casas_disponiveis)

        # 2. Sorteio dos Pocos
        self.qtd_pocos = min(self.qtd_pocos, len(casas_disponiveis))
        self.pocos = set(casas_disponiveis[:self.qtd_pocos])

        # 3. Casas permitidas para Wumpus e Ouro (sem pocos e sem (0, 0))
        casas_sem_pocos = [casa for casa in casas_disponiveis if casa not in self.pocos]

        # Sorteio do Wumpus
        if self.qtd_wumpus > 0 and casas_sem_pocos:
            qtd = min(self.qtd_wumpus, len(casas_sem_pocos))
            self.wumpus = set(random.sample(casas_sem_pocos, qtd))

        # Sorteio do Ouro
        if self.qtd_ouro > 0 and casas_sem_pocos:
            qtd = min(self.qtd_ouro, len(casas_sem_pocos))
            self.ouro = set(random.sample(casas_sem_pocos, qtd))

        # 4. Calculo das Percepcoes
        for p_lin, p_col in self.pocos:
            for v_lin, v_col in self._obter_vizinhos(p_lin, p_col):
                self.percepcoes[(v_lin, v_col)].add("brisa")

        for w_lin, w_col in self.wumpus:
            for v_lin, v_col in self._obter_vizinhos(w_lin, w_col):
                self.percepcoes[(v_lin, v_col)].add("fedor")

        for o_lin, o_col in self.ouro:
            self.percepcoes[(o_lin, o_col)].add("brilho")

    # --- METODOS DE CONSULTA (INTERFACE PARA OS AGENTES DAS ETAPAS 2, 3 E 4) ---

    def obter_percepcoes(self, lin: int, col: int) -> Set[str]:
        """Retorna o conjunto de percepcoes sentidas na coordenada informada."""
        return self.percepcoes.get((lin, col), set()).copy()

    def tem_poco(self, lin: int, col: int) -> bool:
        """Verifica se ha poco na celula."""
        return (lin, col) in self.pocos

    def tem_wumpus(self, lin: int, col: int) -> bool:
        """Verifica se ha Wumpus vivo na celula."""
        return (lin, col) in self.wumpus

    def tem_ouro(self, lin: int, col: int) -> bool:
        """Verifica se ha ouro na celula."""
        return (lin, col) in self.ouro

    def para_dicionario(self) -> Dict[str, Any]:
        """Exporta os dados diretamente para os agentes e rotinas de teste."""
        return {
            "dimensao": self.dimensao,
            "inicio_agente": list(self.inicio_agente),
            "pocos": [list(p) for p in self.pocos],
            "wumpus": [list(w) for w in self.wumpus],
            "ouro": [list(o) for o in self.ouro],
            "percepcoes": {
                f"{lin},{col}": list(percs)
                for (lin, col), percs in self.percepcoes.items()
                if percs
            }
        }

    def exibir_tabuleiro(self) -> None:
        """Imprime a grade no terminal (linha 0 na parte inferior)."""
        print(f"\n--- Mundo de Wumpus ({self.dimensao}x{self.dimensao}) ---")
        for lin in range(self.dimensao - 1, -1, -1):
            linha_str = []
            for col in range(self.dimensao):
                conteudo = []
                if (lin, col) == self.inicio_agente:
                    conteudo.append("A")
                if (lin, col) in self.pocos:
                    conteudo.append("P")
                if (lin, col) in self.wumpus:
                    conteudo.append("W")
                if (lin, col) in self.ouro:
                    conteudo.append("O")

                percs = "".join([p[0].upper() for p in sorted(self.percepcoes[(lin, col)])])
                marcador = ",".join(conteudo)
                rotulo = f"[{marcador}|{percs}]" if marcador or percs else "[   ]"
                linha_str.append(f"{rotulo:^10}")
            print(f"{lin} | " + " ".join(linha_str))
        
        print("    " + "-" * (11 * self.dimensao))
        print("      " + " ".join([f"{col:^10}" for col in range(self.dimensao)]))
        print("Legenda: A=Agente, P=Poco, W=Wumpus, O=Ouro | B=Brisa, F=Fedor, R=bRilho\n")
