# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys

from pexpect import EOF
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.board[row][col] == ".":
            return None
        else:
            return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int): 
        """-> (str, str)"""
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if self.row == 0 or self.[row - 1][col] == "":
            return None, self.board[row + 1][col]
        elif self.row == 9:
            return self.board[row - 1][col], None
        
        elif self.[row + 1][col] == "" and self.[row - 1][col] == "":
            return None, None
        pass

    def adjacent_horizontal_values(self, row: int, col: int):
        """ -> (str, str)"""
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        pass


    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        board = [["."] * 11 for _ in range(11)]
        line = sys.stdin.readline().split()
        while line != []:
            if line[0] == "ROW":
                for i in range(0, 10, 1):
                    board[i][10] = line[i+1]
            elif line[0] == "COLUMN":
                for i in range(0, 10, 1):
                    board[10][i] = line[i+1]
            elif line[0] == "HINT":
                board[int(line[1])][int(line[2])] = line[3]
            line = sys.stdin.readline().split()
        return board



class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    board = Board
    for row in board:
        for col in row:
            print(col, end=" ")
        print()
   
     def actions_initial(self, board: Board):
        """ Completa as primeiras ações possiveis """
        self.board = board
        for i in range(0, 10, 1):
            if board[10][i] == "0":
                for column in range(0, 10, 1):
                    if board[column][i] == ".":
                        board[column][i] = "W"
        return board

    
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
