# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 83:
# 103011 André Oliveira
# 103120 Beatriz Mendes

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

    def __init__(self):
        self.board = [["□"] * 11 for _ in range(11)]


    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.board[row][col] == "□":
            return None
        else:
            return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if self.row == 0 or self.board[row - 1][col] == "":
            return None, self.board[row + 1][col]
        elif self.row == 9 or self.board[row + 1][col] == "":
            return self.board[row - 1][col], None
        elif self.board[row + 1][col] == "" and self.board[row - 1][col] == "":
            return None, None
        else:
            return self.board[row - 1][col], self.board[row + 1][col]

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if self.col == 0 or self.board[row][col - 1] == "":
            return None, self.board[row + 1][col]
        elif self.col == 9 or self.board[row][col + 1] == "":
            return self.board[row][col - 1], None
        elif self.board[row][col - 1] == "" and self.board[row][col + 1] == "":
            return None, None
        else:
            return self.board[row][col - 1], self.board[row][col + 1]

    
    def check_rows(self, row: int):
        """Verifica se o número de barcos numa linha está correto."""
        """ print(type(board[row][10]))
        """
        count = 0
        for col in range(10): 
            if self.board[row][col] == "□":
                count += 1
        if count == int(self.board[row][10]): return 1
        if int(self.board[row][10]) == 0:
            return 2
        else: return 0


    def check_cols(self, col: int) -> bool:
        """Verifica se o número de barcos numa coluna está correto."""
        count = 0
        for row in range(10):
            if self.board[row][col] == "□":
                count += 1
        if count == int(self.board[10][col]): return 1
        if int(self.board[10][col]) == 0:
            return 2
        else: return 0

    def fill_rows(self, row: int, mode: int):
        if mode == 1:
            """Preenche a linha com barcos."""
            for col in range(0, 10, 1):
                if self.board[row][col] == "□":
                    self.board[row][col] = "?"
        elif mode == 2:
            """Preenche a linha com água."""
            for col in range(0, 10, 1):
                if self.board[row][col] == "□":
                    self.board[row][col] = "."
        


    def fill_cols(self, col: int, mode: int):
        """Preenche a coluna com barcos."""
        if mode == 1:
            for row in range(0, 10, 1):
                if self.board[row][col] == "□":
                    self.board[row][col] = "?"
        elif mode == 2:
            """Preenche a coluna com água."""
            for row in range(0, 10, 1):
                if self.board[row][col] == "□":
                    self.board[row][col] = "."     
        
    

    def actions_initial(self):
        """ Completa as primeiras ações possiveis """
        for row in range(0, 10, 1):
            for col in range(0, 10, 1):
                
                """ T """
                if self.board[row][col] == "T":
                    self.board[row + 1][col] = "m"
                    if row == 0:
                        if 0 < col:
                            self.board[row][col -1] = "."
                            self.board[row +1][col -1] = "."
                            self.board[row +2][col -1] = "."
                            
                        if col < 9:
                            self.board[row][col +1] = "."
                            self.board[row +1][col +1] = "."
                            self.board[row +2][col +1] = "."

                    if 0 < row < 9:
                        self.board[row -1][col] = "."
                        if 0 < col:
                            self.board[row -1][col -1] = "."
                            self.board[row][col -1] = "."
                            self.board[row +1][col -1] = "."
                            if row != 8: self.board[row +2][col -1] = "."
                            
                        if col < 9:
                            self.board[row -1][col +1] = "."
                            self.board[row][col +1] = "."
                            self.board[row +1][col +1] = "."
                            if row != 8: self.board[row +2][col +1] = "."
                  
                """ B """
                if self.board[row][col] == "B":
                    self.board[row - 1][col] = "m"
                    if row == 9:
                        if 0 < col:
                            self.board[row][col +1] = "."
                            self.board[row -1][col +1] = "."
                            self.board[row -2][col +1] = "."
                            
                        if col < 9:
                            self.board[row][col -1] = "."
                            self.board[row -1][col -1] = "."
                            self.board[row -2][col -1] = "."

                    if 0 < row < 9:
                        self.board[row +1][col] = "."
                        if 0 < col:
                            if row != 1: self.board[row -2][col -1] = "."
                            self.board[row -1][col -1] = "."
                            self.board[row][col -1] = "."
                            self.board[row +1][col -1] = "."
                            
                        if col < 9:
                            if row != 1: self.board[row -2][col +1] = "."
                            self.board[row -1][col +1] = "."
                            self.board[row][col +1] = "."
                            self.board[row +1][col +1] = "."

                """ L """
                if self.board[row][col] == "L":
                    self.board[row][col +1] = "m"
                    if col == 0:
                        if 0 < row:
                            self.board[row -1][col -1] = "."
                            self.board[row -1][col] = "."
                            self.board[row -1][col +1] = "."
                            self.board[row -1][col +2] = "."

                        if row < 9:
                            self.board[row +1][col -1] = "."
                            self.board[row +1][col] = "."
                            self.board[row +1][col +1] = "."
                            self.board[row +1][col +2] = "."

                    if 0 < col < 9:
                        self.board[row][col -1] = "."
                        if 0 < row:
                            self.board[row -1][col -1] = "."
                            self.board[row -1][col] = "."
                            self.board[row -1][col +1] = "."
                            if col != 8: self.board[row -1][col +2] = "."
                            
                        if row < 9:
                            self.board[row +1][col -1] = "."
                            self.board[row +1][col] = "."
                            self.board[row +1][col +1] = "."
                            if col != 8: self.board[row +1][col +2] = "."

                """ R """
                if self.board[row][col] == "R":
                    self.board[row][col -1] = "m"
                    if col == 9:
                        if 0 < row:
                            self.board[row -1][col -2] = "."
                            self.board[row -1][col -1] = "."
                            self.board[row -1][col] = "."
                            self.board[row -1][col +1] = "."

                        if row < 9:             
                            self.board[row +1][col -2] = "."
                            self.board[row +1][col -1] = "."
                            self.board[row +1][col] = "."
                            self.board[row +1][col +1] = "."

                    if 0 < col < 9:
                        self.board[row][col +1] = "."
                        if 0 < row:
                            if col != 1: self.board[row -1][col -2] = "."
                            self.board[row -1][col -1] = "."
                            self.board[row -1][col] = "."
                            self.board[row -1][col +1] = "."
                            
                        if row < 9:
                            if col != 1: self.board[row +1][col -2] = "."
                            self.board[row +1][col -1] = "."
                            self.board[row +1][col] = "."
                            self.board[row +1][col +1] = "."

                """ M """
                if self.board[row][col] == "M":
                    if col != 0:
                        self.board[row - 1][col -1] = "."
                        self.board[row - 1][col +1] = "."
                    if col != 9:
                        self.board[row + 1][col -1] = "."
                        self.board[row + 1][col +1] = "."
                    

                """ C """
                if self.board[row][col] == "C":
                    self.board[row][col -1] = "."
                    self.board[row][col +1] = "."
                    if row != 0:
                        self.board[row - 1][col - 1] = "."
                        self.board[row - 1][col] = "."
                        self.board[row - 1][col + 1] = "."
                    if row != 9:
                        self.board[row +1][col -1] = "."
                        self.board[row +1][col] = "."
                        self.board[row +1][col +1] = "." 

        for row in range(10):
            mode = self.check_rows(row)
            if mode != 0:
                self.fill_rows(row, mode)     
        for col in range(10):
            mode = self.check_cols(col)
            if mode != 0:
                self.fill_cols(col, mode)
        


        

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        board = Board()
        line = sys.stdin.readline().split()
        while line != []:
            if line[0] == "ROW":
                for i in range (10):
                    board.board[i][10] = line[i+1]
                board.board[i+1][10] = int(line[i+1])
            elif line[0] == "COLUMN":
                for i in range (10):
                    board.board[10][i] = line[i+1]
                board.board[10][i+1] = int(line[i+1])
            elif line[0] == "HINT":
                board.board[int(line[1])][int(line[2])] = line[3]
            line = sys.stdin.readline().split()
        return board



class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        

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
    board: Board = Board.parse_instance()
    board.actions_initial()



    for row in range(0, 11, 1):
        for col in range(0, 11, 1):
            print(board.board[row][col], end=" ")
        print()


    """ state.actions()
    state.result() """
    

   
     

    
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
