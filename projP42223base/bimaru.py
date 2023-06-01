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
        self.board : Board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self):
        self.board = [["□"] * 11 for _ in range(11)]
        self.fleet = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if self.board[row][col] == "□":
            return None
        else:
            return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        pos_a = self.board[row - 1][col]
        pos_u = self.board[row + 1][col]
        if pos_a == "□" or row == 0: pos_a = None
        if pos_u == "□" or row == 9: pos_u = None
        return pos_a, pos_u
    

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        pos_l = self.board[row][col - 1]
        pos_r = self.board[row][col + 1]
        if pos_l == "□" or col == 0: pos_l = None
        if pos_r == "□" or col == 0: pos_r = None
        return pos_l, pos_r
        
    
    def check_rows(self, row: int):
        """Verifica se o número de barcos numa linha está correto."""
        count = 0
        for col in range(10): 
            if self.board[row][col] == "□":
                count += 1
        if count != 0:
            if count == int(self.board[row][10]):
                return 1 
            if (int(self.board[row][10]) == 0):
                return 2
            else: return 0
        else: return 0


    def check_cols(self, col: int) -> int:
        """Verifica se o número de barcos numa coluna está correto."""
        count = 0
        for row in range(10):
            if self.board[row][col] == "□":
                count += 1
        if count != 0:
            if count == int(self.board[10][col]):
                return 1 
            if int(self.board[10][col]) == 0:
                return 2
            else: return 0
        else: return 0

    def fill_rows(self, row: int, mode: int):
        if mode == 1:
            """Preenche a linha com barcos."""
            for col in range(0, 10, 1):
                if self.board[row][col] == "□":
                    self.board[row][col] = "?"
                    self.change_cases_filled(row, col)
        elif mode == 2:
            """Preenche a linha com água."""
            for col in range(0, 10, 1):
                if self.board[row][col] == "□":
                    self.board[row][col] = "."
        

    def fill_cols(self, col: int, mode: int):
        """Preenche a coluna com barcos."""
        if mode == 1:
            for row in range(10):
                if self.board[row][col] == "□":
                    self.board[row][col] = "?"
                    self.change_cases_filled(row, col)
        elif mode == 2:
            """Preenche a coluna com água."""
            for row in range(10):
                if self.board[row][col] == "□":
                    self.board[row][col] = "."     
        
    
    def change_cases_filled(self, row: int, col: int):
        """Diminui o número de posições que aind apodem ser preenchidas """
        self.board[row][10] = str(int(self.board[row][10]) - 1)
        self.board[10][col] = str(int(self.board[10][col]) - 1)
    
    def remove_from_fleet(self, size: int):
        for i in range(len(self.fleet)):
            if (self.fleet[i] == size):
                self.fleet.pop(i)
                return

    def clearing_boats(self):
        for row in range(10):
            for col in range(10):
                value = self.get_value(row, col)
                if value == "?":
                    """ c """
                    if self.adjacent_horizontal_values(row,col) == (".", ".") and self.adjacent_vertical_values(row,col) == (".", "."):
                        self.board[row][col] = "c"

                    """ t """
                    if row == 1 and self.adjacent_horizontal_values(row,col) == (".", "."):
                        self.board[row][col] = "t"




                if value == "M":
                    if self.adjacent_horizontal_values(row, col) in [(".", ".") , (".", None), (None, ".")]:
                        self.board[row-1][col] = "?"
                        self.change_cases_filled(row - 1, col)
                        self.board[row+1][col] = "?"
                        self.change_cases_filled(row + 1, col)

                    elif self.adjacent_vertical_values(row, col) in [(".", ".") , (".", None), (None, ".")]:
                        self.board[row][col-1] = "?"
                        self.change_cases_filled(row, col -1)
                        self.board[row][col+1] = "?"
                        self.change_cases_filled(row, col +1)   

    
    def make_stuff_happen(self):
        count = 0
        while count == 0:
            count = 1
            for row in range(10):
                mode = self.check_rows(row)
                if mode != 0:
                    count = 0
                    self.fill_rows(row, mode)
            for col in range(10):
                mode = self.check_cols(col)
                if mode != 0:
                    count = 0
                    self.fill_cols(col, mode)    

    def put_water_t(self, row, col):
        self.change_cases_filled(row, col)
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
    
    def put_water_b(self, row, col):
        self.change_cases_filled(row, col)
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

    def put_water_l(self, row, col):
        self.change_cases_filled(row, col)
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

    def put_water_r(self, row, col):
        self.change_cases_filled(row, col)
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

    def put_water_m(self, row, col):
        if col != 0:
            self.board[row - 1][col -1] = "."
            self.board[row - 1][col +1] = "."
        if col != 9:
            self.board[row + 1][col -1] = "."
            self.board[row + 1][col +1] = "."
    
    def put_water_c(self, row, col):
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


    def actions_initial(self):
        """ Completa as primeiras ações possiveis """

        for row in range(10):
            for col in range(10):
                value = self.get_value(row, col)
                
                """ T """
                if value == "T":
                    self.board[row + 1][col] = "?"
                    self.change_cases_filled(row + 1, col)         
                    self.put_water_t(row, col)

                """ B """
                if value == "B":
                    self.board[row - 1][col] = "?"
                    self.change_cases_filled(row - 1, col)
                    self.put_water_b(row, col)

                """ L """
                if value == "L":
                    self.board[row][col +1] = "?"
                    self.change_cases_filled(row, col + 1)
                    self.put_water_l(row, col)


                """ R """
                if value == "R":
                    self.board[row][col -1] = "?"
                    self.change_cases_filled(row, col - 1)
                    self.put_water_r(row, col)


                """ M """
                if value == "M":
                    self.change_cases_filled(row, col)
                    self.put_water_m(row, col)
                    

                """ C """
                if value == "C":
                    self.remove_from_fleet(1)
                    self.change_cases_filled(row, col)
                    self.put_water_c(row, col)
        
        self.make_stuff_happen()
            


        

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
        board.actions_initial()
        return board



class Bimaru(Problem):
    def __init__(self, board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        boats = state.board.fleet
        if boats[0] == 4:
            for row in range(11):
                for col in range(11):
                    value = state.board.get_value(row, col)
                    if value in ["L", "l", None, "?"]:
                        if state.board.board[row][col+1] in ["M", "m", "□", "?"]:
                            if state.board.board[row][col+2] in ["M", "m", "□", "?"]:
                                if state.board.board[row][col+3] in ["□", "?", "R", "r"]:
                                    actions.append([(row, col), 4, "H"]) 
                    
                    if value in ["T", "t", None, "?"]:
                        #print(row, col, value)
                        if state.board.board[row+1][col] in ["M", "m", "□", "?"]:
                            if state.board.board[row+2][col] in ["M", "m", "□", "?"]:
                                if state.board.board[row+3][col] in ["B", "b", "□", "?"]:
                                    actions.append([(row, col), 4, "V"])
        
        if boats[0] == 3:
            for row in range(11):
                for col in range(11):
                    value = state.board.get_value(row, col)
                    control = ""
                    if value in ["L", "l", None, "?"]:
                        if value == "L" or value == "l":
                            control += "l"
                        if state.board.board[row][col+1] in ["M", "m", "□", "?"]:
                            if value == "M" or value == "m":
                                control += "m"
                            if state.board.board[row][col+2] in ["R", "r", "□", "?"]:
                                    if value == "R" or value == "r":
                                        control += "r"
                                    if control != "lmr": actions.append([(row, col), 3, "H"]) 
                    
                    if value in ["T", "t", None, "?"]:
                        if value == "T" or value == "t":
                            control += "t"
                        if state.board.board[row+1][col] in ["M", "m", "□", "?"]:
                            if value == "M" or value == "m":
                                control += "m"
                            if state.board.board[row+1][col] in ["B", "b", "□", "?"]:
                                if value == "B" or value == "b":
                                        control += "b"
                                actions.append([(row, col), 3, "V"])
             
        if boats[0] == 2:
            for row in range(11):
                for col in range(11):
                    value = state.board.get_value(row, col)
                    control = ""
                    if value in ["L", "l", None, "?"]:
                        if value == "L" or value == "l":
                            control += "l"
                        if state.board.board[row][col+1] in ["R", "r", "□", "?"]:
                            if value == "R" or value == "r":
                                control += "r"
                            if control != "lr": actions.append([(row, col), 2, "H"])
                    
                    if value in ["T", "t", None, "?"]:
                        if value == "T" or value == "t":
                            control += "t"
                        if state.board.board[row+1][col] in ["B", "b", "□", "?"]:
                            if value == "B" or value == "b":
                                control += "b"
                            if control != "tb": actions.append([(row, col), 2, "V"])
        
        if boats[0] == 1:
            for row in range(11):
                for col in range(11):
                    value = state.board.get_value(row, col)
                    if value in [None, "?"]:
                        actions.append([(row, col), 1, "H"])
                    
        return actions

        
    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        pos = action[1]
        size = action[2]
        orient = action[3]

        if size == 4:
            state.remove_from_fleet(4)
            if orient == "H":
                for i in range(4):
                    if i == 0 and state.board[pos[0]][pos[1]] == "□":
                        state.board[pos[0]][pos[1]] = "l"
                        state.board.change_cases_filled(pos[0], pos[1])
                        state.board.put_water_l(pos[0], pos[1])
                    elif i == 1 and state.board[pos[0]][pos[1]+i] == "□":
                        state.board[pos[0]][pos[1]+i] = "m"
                        state.board.change_cases_filled(pos[0], pos[1]+i)
                        state.board.put_water_m(pos[0], pos[1]+i)
                    elif i == 2 and state.board[pos[0]][pos[1]+i] == "□":
                        state.board[pos[0]][pos[1]+i] = "m"
                        state.board.change_cases_filled(pos[0], pos[1]+i)
                        state.board.put_water_m(pos[0], pos[1]+i)
                    elif i == 3 and state.board[pos[0]][pos[1]+i] == "□":
                        state.board[pos[0]][pos[1]+i] = "r"
                        state.board.change_cases_filled(pos[0], pos[1]+i)
                        state.board.put_water_r(pos[0], pos[1]+i)
                    

            else:
                for i in range(4):
                    if i == 0 and state.board[pos[0]][pos[1]] == "□":
                        state.board[pos[0]][pos[1]] = "t"
                        state.board.change_cases_filled(pos[0], pos[1])
                        state.board.put_water_t(pos[0], pos[1])
                    if i == 1 and state.board[pos[0]+i][pos[1]] == "□":
                        state.board[pos[0]+i][pos[1]] = "m"
                        state.board.change_cases_filled(pos[0]+i, pos[1])
                        state.board.put_water_m(pos[0]+i, pos[1])
                    if i == 2 and state.board[pos[0]+i][pos[1]] == "□":
                        state.board[pos[0]+i][pos[1]] = "m"
                        state.board.change_cases_filled(pos[0]+i, pos[1])
                        state.board.put_water_m(pos[0]+i, pos[1])
                    if i == 3 and state.board[pos[0]+i][pos[1]] == "□":
                        state.board[pos[0]+i][pos[1]] = "b"
                        state.board.change_cases_filled(pos[0]+i, pos[1])
                        state.board.put_water_b(pos[0]+i, pos[1])

        elif size == 3:
            state.remove_from_fleet(3)
            if orient == "H":
                for i in range(3):
                    if i == 0 and state.board[pos[0]][pos[1]] == "□":
                        state.board[pos[0]][pos[1]] = "l"
                        state.board.change_cases_filled(pos[0], pos[1])
                        state.board.put_water_l(pos[0], pos[1])
                    elif i == 1 and state.board[pos[0]][pos[1]+i] == "□":
                        state.board[pos[0]][pos[1]+i] = "m"
                        state.board.change_cases_filled(pos[0], pos[1]+i)
                        state.board.put_water_m(pos[0], pos[1]+i)
                    elif i == 2 and state.board[pos[0]][pos[1]+i] == "□":
                        state.board[pos[0]][pos[1]+i] = "r"
                        state.board.change_cases_filled(pos[0], pos[1]+i)
                        state.board.put_water_r(pos[0], pos[1]+i)
            else:
                for i in range(3):
                    if i == 0 and state.board[pos[0]][pos[1]] == "□":
                        state.board[pos[0]][pos[1]] = "t"
                        state.board.change_cases_filled(pos[0], pos[1])
                        state.board.put_water_t(pos[0], pos[1])
                    if i == 1 and state.board[pos[0]+i][pos[1]] == "□":
                        state.board[pos[0]+i][pos[1]] = "m"
                        state.board.change_cases_filled(pos[0]+i, pos[1])
                        state.board.put_water_m(pos[0]+i, pos[1])
                    if i == 2 and state.board[pos[0]+i][pos[1]] == "□":
                        state.board[pos[0]+i][pos[1]] = "b"
                        state.board.change_cases_filled(pos[0]+i, pos[1])
                        state.board.put_water_b(pos[0]+i, pos[1])
        
        elif size == 2:
            state.remove_from_fleet(2)
            if orient == "H":
                for i in range(2):
                    if i == 0 and state.board[pos[0]][pos[1]] == "□":
                        state.board[pos[0]][pos[1]] = "l"
                        state.board.change_cases_filled(pos[0], pos[1])
                        state.board.put_water_l(pos[0], pos[1])
                    elif i == 1 and state.board[pos[0]][pos[1]+i] == "□":
                        state.board[pos[0]][pos[1]+i] = "r"
                        state.board.change_cases_filled(pos[0], pos[1]+i)
                        state.board.put_water_r(pos[0], pos[1]+i)
            else:
                for i in range(2):
                    if i == 0 and state.board[pos[0]][pos[1]] == "□":
                        state.board[pos[0]][pos[1]] = "t"
                        state.board.change_cases_filled(pos[0], pos[1])
                        state.board.put_water_t(pos[0], pos[1])
                    if i == 1 and state.board[pos[0]+i][pos[1]] == "□":
                        state.board[pos[0]+i][pos[1]] = "b"
                        state.board.change_cases_filled(pos[0]+i, pos[1])
                        state.board.put_water_b(pos[0]+i, pos[1])

        elif size == 1:
                state.remove_from_fleet(1)
                state.board[pos[0]][pos[1]] = "c"
                state.board.change_cases_filled(pos[0], pos[1])
                state.board.put_water_c(pos[0], pos[1])   
            
        return state


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if state.board.fleet != []: return False
        for count in range(10):
            if state.board[count][10] != 0 or state.board[10][count] != 0:
                return False
        return True
        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass



if __name__ == "__main__":
    board = Board.parse_instance()
    problem  = Bimaru(board)
    s0 = BimaruState(board)

    print(problem.actions(s0))
    




    """ board.actions_initial()
    problem = Bimaru(board)
    depth_first_tree_search(problem)



 """
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
