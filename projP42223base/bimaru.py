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

    #DELETE
    def print_board(self):
        for row in range(11):
            for col in range(11):
                print(self.board[row][col], end=" ")
            print()
        print()


    def __init__(self):
        self.board = [["□"] * 11 for _ in range(11)]
        self.fleet = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0: 
            return None, self.get_value(row + 1, col)
        if row == 9: 
            return self.get_value(row - 1, col), None
        return self.get_value(row - 1, col), self.get_value(row + 1, col)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0: 
            return None, self.get_value(row, col + 1)
        if col == 9: 
            return self.get_value(row, col - 1), None
        return self.get_value(row, col - 1), self.get_value(row, col + 1)


    def copy_board(self, old_board):
        self.fleet = old_board.fleet[:]
        for row in range(11):
            for col in range(11):
                self.board[row][col] = old_board.board[row][col]
        
    
    def check_rows(self, row: int):
        """Verifica se o número de barcos numa linha está correto."""
        count = 0
        for col in range(10):
            if self.get_value(row, col) == "?":
                self.clear_boats_row(row)
            if self.get_value(row, col + 1) == "M":
                self.case_M(row, col + 1)
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
            if self.get_value(row, col) == "?":
                self.clear_boats_col(col)
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
            for col in range(10):
                if self.board[row][col] == "□":
                    self.board[row][col] = "?"
                    self.change_cases_filled(row, col)
                    self.clear_boats_row(row)
        elif mode == 2:
            """Preenche a linha com água."""
            for col in range(10):
                if self.board[row][col] == "□":
                    self.board[row][col] = "."
                elif self.get_value(row, col) == "?":
                    self.clear_boats_row(row)


    def fill_cols(self, col: int, mode: int):
        """Preenche a coluna com barcos."""
        if mode == 1:
            for row in range(10):
                if self.board[row][col] == "□":
                    self.board[row][col] = "?"
                    self.change_cases_filled(row, col)
                    self.clear_boats_col(col)
        elif mode == 2:
            """Preenche a coluna com água."""
            for row in range(10):
                if self.board[row][col] == "□":
                    self.board[row][col] = "."     
                elif self.get_value(row, col) == "?":
                    self.clear_boats_col(col)
        
    
    def change_cases_filled(self, row: int, col: int):
        """Diminui o número de posições que aind apodem ser preenchidas """
        row_10, col_10 = int(self.board[row][10]) - 1, int(self.board[10][col]) - 1
        self.board[row][10] = str(row_10)
        if row_10 == 0:
            self.fill_rows(row, 2)
        self.board[10][col] = str(col_10)
        if col_10 == 0: 
            self.fill_cols(col, 2)
    
    def calculate_boat_size(self, row: int, col: int) -> int:
        if self.get_value(row, col) in ["b", "B", "t", "T", "l", "L", "r", "R"]:
            return 2
        
        adjacent_top, adjacent_bottom = self.adjacent_vertical_values(row, col)
        adjacent_left, adjacent_right = self.adjacent_horizontal_values(row, col)

        if (adjacent_top in ["t", "T"] and adjacent_bottom in ["b", "B"]) or (adjacent_left in ["l", "L"] and adjacent_right in ["r", "R"]):
            return 3
        
        elif adjacent_top in ["m", "M"] or adjacent_bottom in ["m", "m"] or adjacent_left in ["m", "M"] or adjacent_right in ["m", "M"]:
            return 4
        
        return 0


    def remove_from_fleet(self, size: int):
        if size != 0:
            for i in range(len(self.fleet)):
                if (self.fleet[i] == size):
                    self.fleet.pop(i)
                    return

    def case_M(self, row: int, col: int):
        if self.adjacent_horizontal_values(row, col)[0] in ["W", ".", None] or self.adjacent_horizontal_values(row, col)[1] in ["W", ".", None]:
            if self.get_value(row - 1, col) == "□": 
                self.board[row - 1][col] = "?"
                self.change_cases_filled(row - 1, col)
                self.put_water_m(row - 1, col)
            
            if self.get_value(row + 1, col) == "□": 
                self.board[row + 1][col] = "?"
                self.change_cases_filled(row + 1, col)
                self.put_water_m(row + 1, col)

        elif self.adjacent_vertical_values(row, col)[0] in ["W", ".", None] or self.adjacent_vertical_values(row, col)[1] in ["W", ".", None]:
            if self.get_value(row, col + 1) == "□": 
                self.board[row][col + 1] = "?"
                self.change_cases_filled(row, col + 1)
                self.put_water_m(row, col + 1)
           
            if self.get_value(row, col - 1) == "□": 
                self.board[row][col - 1] = "?"
                self.change_cases_filled(row, col - 1)
                self.put_water_m(row, col - 1)

    def clear_case(self, row: int, col: int):
        if self.adjacent_vertical_values(row, col)[0] in [".", "W", None] and self.adjacent_vertical_values(row, col)[1] in [".", "W", None] and self.adjacent_horizontal_values(row, col)[0] in [".", "W", None] and self.adjacent_horizontal_values(row, col)[1] in [".", "W", None]:
            self.board[row][col] = "c"
            self.remove_from_fleet(1)
            return
        
        elif self.adjacent_vertical_values(row, col)[0] in [".", "W", None] and self.adjacent_vertical_values(row, col)[1] in ["b", "B", "m", "M", "?"]:
            self.board[row][col] = "t"
            self.put_water_t(row, col)
            self.remove_from_fleet(self.calculate_boat_size(row + 1, col))

        elif self.adjacent_vertical_values(row, col)[0] in ["t", "T", "m", "M", "?"] and self.adjacent_vertical_values(row, col)[1] in [".", "W", None]:
            self.board[row][col] = "b"
            self.put_water_b(row, col)
            self.remove_from_fleet(self.calculate_boat_size(row - 1, col))
                
        elif self.adjacent_horizontal_values(row, col)[0] in [".", "W", None] and self.adjacent_horizontal_values(row, col)[1] in ["r", "R", "m", "M", "?"]:
            self.board[row][col] = "l"
            self.put_water_l(row, col)
            self.remove_from_fleet(self.calculate_boat_size(row, col + 1))

        elif self.adjacent_horizontal_values(row, col)[0] in ["l", "L", "m", "M", "?"] and self.adjacent_horizontal_values(row, col)[1] in [".", "W", None]:
            self.board[row][col] = "r"
            self.put_water_r(row, col)
            self.remove_from_fleet(self.calculate_boat_size(row , col - 1))
        
        elif self.adjacent_vertical_values(row, col)[0] in ["t", "T", "m", "M", "?"] and self.adjacent_vertical_values(row, col)[1] in ["b", "B", "M", "?", "m"]:
            self.board[row][col] = "m"
            self.put_water_m(row, col)
            self.remove_from_fleet(self.calculate_boat_size(row , col))
        
        elif self.adjacent_horizontal_values(row, col)[0] in ["l", "L", "m", "M", "?"] and self.adjacent_horizontal_values(row, col)[1] in ["r", "R", "M", "?", "m"]:
            self.board[row][col] = "m"
            self.put_water_m(row, col)
            self.remove_from_fleet(self.calculate_boat_size(row , col))

        return


    def clear_boats_col(self, col: int):
        for row in range(10):
            if self.get_value(row, col) == "?":
                self.clear_case(row, col)
        return 


    def clear_boats_row(self, row: int):
        for col in range(10):
            if self.get_value(row, col) == "?":
                self.clear_case(row, col)
        return
    
    def put_boat(self, row: int, col: int, size: int, orientation):
        if size >= 2:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("putting boat: [(" + str(row) + ", " + str(col) + "), " + str(size) + ", " + orientation + "]")

        if size == 1:
            self.board[row][col] = "c"
            self.change_cases_filled(row, col)

        elif orientation == "H":
            if col != 0 and self.board[row][col - 1] == "□": self.board[row][col - 1] = "."
            for i in range(size):
                if self.get_value(row, col + i) == "□":
                    self.board[row][col + i] = "?"
                    self.change_cases_filled(row, col + i)
            if self.board[row][col + size] == "□": self.board[row][col + size] = "."

            self.clear_boats_row(row)

        elif orientation == "V":
            if row != 0 and self.board[row - 1][col] == "□": self.board[row - 1][col] = "."
            for i in range(size):
                if self.get_value(row + i, col) == "□":
                    self.board[row + i][col] = "?"
                    self.change_cases_filled(row + i, col)
            if self.board[row + size][col] == "□": self.board[row + size][col] = "."
            self.clear_boats_col(col)

        self.remove_from_fleet(size)

        if size >= 2:
            self.print_board()
            print(self.fleet)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~end")


    def make_stuff_happen(self):
        count = 0
        while count == 0:
            count = 1
            for row in range(10):
                mode = self.check_rows(row)
                if mode != 0:
                    count = 0
                    self.fill_rows(row, mode)
                    self.clear_boats_row(row)
            for col in range(10):
                mode = self.check_cols(col)
                if mode != 0:
                    count = 0
                    self.fill_cols(col, mode)    
                    self.clear_boats_col(col)

    def put_water_t(self, row, col):
        if row == 0:
            if 0 < col:
                if self.get_value(row, col - 1) == "□": self.board[row][col - 1] = "."
                if self.get_value(row + 1, col - 1) == "□": self.board[row + 1][col - 1] = "."
                
            if col < 9:
                if self.get_value(row, col + 1) == "□": self.board[row][col + 1] = "."
                if self.get_value(row + 1, col + 1) == "□": self.board[row + 1][col + 1] = "."

        if 0 < row < 9:
            if self.get_value(row - 1, col) == "□": self.board[row - 1][col] = "."
            if 0 < col:
                if self.get_value(row, col - 1) == "□": self.board[row][col - 1] = "."
                if self.get_value(row - 1, col - 1) == "□": self.board[row - 1][col - 1] = "."
                if self.get_value(row + 1, col - 1) == "□": self.board[row + 1][col - 1] = "."
                
            if col < 9:
                if self.get_value(row, col + 1) == "□": self.board[row][col + 1] = "."
                if self.get_value(row - 1, col + 1) == "□": self.board[row - 1][col + 1] = "."
                if self.get_value(row + 1, col + 1) == "□": self.board[row + 1][col + 1] = "."
    
    def put_water_b(self, row, col):
        if row == 9:
            if 0 < col:
                if self.get_value(row , col + 1) == "□": self.board[row][col + 1] = "."
                if self.get_value(row - 1, col + 1) == "□":self.board[row - 1][col + 1] = "."
                
            if col < 9:
                if self.get_value(row, col - 1) == "□": self.board[row][col - 1] = "."
                if self.get_value(row - 1, col - 1) == "□":self.board[row - 1][col - 1] = "."

        if 0 < row < 9:
            if self.get_value(row + 1, col) == "□": self.board[row + 1][col] = "."
            if 0 < col:
                if self.get_value(row, col - 1) == "□": self.board[row][col - 1] = "."
                if self.get_value(row + 1, col - 1) == "□": self.board[row + 1][col - 1] = "."
                if self.get_value(row - 1, col - 1) == "□": self.board[row - 1][col - 1] = "."
                
            if col < 9:
                if self.get_value(row, col + 1) == "□": self.board[row][col + 1] = "."
                if self.get_value(row + 1, col + 1) == "□": self.board[row + 1][col + 1] = "."
                if self.get_value(row - 1, col + 1) == "□": self.board[row - 1][col + 1] = "."

    def put_water_l(self, row, col):
        if col == 0:
            if 0 < row:
                if self.get_value(row - 1, col) == "□": self.board[row - 1][col] = "."
                if self.get_value(row - 1, col + 1) == "□": self.board[row - 1][col + 1] = "."

            if row < 9:
                if self.get_value(row + 1, col) == "□": self.board[row + 1][col] = "."
                if self.get_value(row + 1, col - 1) == "□": self.board[row + 1][col + 1] = "."

        if 0 < col < 9:
            if self.get_value(row, col - 1) == "□": self.board[row][col - 1] = "."
            if 0 < row:
                if self.get_value(row - 1, col) == "□": self.board[row - 1][col] = "."
                if self.get_value(row - 1, col - 1) == "□": self.board[row - 1][col - 1] = "."
                if self.get_value(row - 1, col + 1) == "□": self.board[row - 1][col + 1] = "."
                
            if row < 9:
                if self.get_value(row + 1, col) == "□": self.board[row + 1][col] = "."
                if self.get_value(row + 1, col - 1) == "□": self.board[row + 1][col - 1] = "."
                if self.get_value(row + 1, col + 1) == "□": self.board[row + 1][col + 1] = "."

    def put_water_r(self, row, col):
        if col == 9:
            if 0 < row:
                if self.get_value(row + 1, col) == "□": self.board[row + 1][col] = "."
                if self.get_value(row + 1, col - 1) == "□": self.board[row + 1][col - 1] = "."

            if row < 9:             
                if self.get_value(row - 1, col) == "□": self.board[row - 1][col] = "."
                if self.get_value(row - 1, col - 1) == "□": self.board[row - 1][col - 1] = "."

        if 0 < col < 9:
            if self.get_value(row, col + 1) == "□": self.board[row][col + 1] = "."
            if 0 < row:
                if self.get_value(row - 1, col) == "□": self.board[row - 1][col] = "."
                if self.get_value(row - 1, col - 1) == "□": self.board[row - 1][col - 1] = "."
                if self.get_value(row - 1, col + 1) == "□": self.board[row - 1][col + 1] = "."
                
            if row < 9:
                if self.get_value(row + 1, col) == "□": self.board[row + 1][col] = "."
                if self.get_value(row + 1, col - 1) == "□": self.board[row + 1][col - 1] = "."
                if self.get_value(row + 1, col + 1) == "□":self.board[row + 1][col + 1] = "."

    def put_water_m(self, row, col):
        if row != 0:
            if col != 0:
                if self.get_value(row - 1, col - 1) == "□": self.board[row - 1][col - 1] = "."
            if col != 9:
                if self.get_value(row - 1, col + 1) == "□": self.board[row - 1][col + 1] = "."
        if row != 9:
            if col != 0:
                if self.get_value(row + 1, col - 1) == "□": self.board[row + 1][col - 1] = "."
            if col != 9:
                if self.get_value(row + 1, col + 1) == "□": self.board[row + 1][col + 1] = "."
 
    def put_water_c(self, row, col):
        if col != 0:
            if self.get_value(row, col - 1) != "W": self.board[row][col - 1] = "."
        if col != 9:
            if self.get_value(row, col + 1) != "W": self.board[row][col + 1] = "."
        if row != 0:
            if self.get_value(row - 1, col) != "W": self.board[row - 1][col] = "."
            if col != 0:
                if self.get_value(row - 1, col - 1) != "W": self.board[row - 1][col - 1] = "."
            if col != 9:
                if self.get_value(row - 1, col + 1) != "W":self.board[row - 1][col + 1] = "."
        if row != 9:
            if self.get_value(row + 1, col) != "W": self.board[row + 1][col] = "."
            if col != 0:
                if self.get_value(row + 1, col - 1) != "W": self.board[row + 1][col - 1] = "."
            if col != 9:
                if self.get_value(row + 1, col + 1) != "W": self.board[row + 1][col + 1] = "." 


    def actions_initial(self):
        """ Completa as primeiras ações possiveis """

        for row in range(10):
            for col in range(10):
                value = self.get_value(row, col)
                
                """ T """
                if value == "T":
                    self.change_cases_filled(row, col)
                    self.board[row + 1][col] = "?"
                    self.change_cases_filled(row + 1, col)         
                    self.put_water_t(row, col)
                    self.put_water_m(row + 1, col)

                """ B """
                if value == "B":
                    self.change_cases_filled(row, col)
                    self.board[row - 1][col] = "?"
                    self.change_cases_filled(row - 1, col)
                    self.put_water_b(row, col)
                    self.put_water_m(row - 1, col)

                """ L """
                if value == "L":
                    self.change_cases_filled(row, col)
                    self.board[row][col +1] = "?"
                    self.change_cases_filled(row, col + 1)
                    self.put_water_l(row, col)
                    self.put_water_m(row, col + 1)


                """ R """
                if value == "R":
                    self.change_cases_filled(row, col)
                    self.board[row][col -1] = "?"
                    self.change_cases_filled(row, col - 1)
                    self.put_water_r(row, col)
                    self.put_water_m(row, col - 1)


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
        self.called = 0

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        boats = state.board.fleet
        if boats == []: return actions

        if boats[0] == 4:
            for row in range(11):
                for col in range(11):
                    value = state.board.get_value(row, col)
                    control = ""
                    if value in ["L", "l", "□", "?"] and state.board.adjacent_vertical_values(row, col)[0] in [".", "□", "W"] and state.board.adjacent_vertical_values(row, col)[1] in [".", "□", "W"]:
                        if col + 4 < 10 and state.board.get_value(row, col + 4) in [".", "□", "W"]:    
                            row_value = int(state.board.board[row][10])
                            if value == "L" or value == "l":
                                control += "l"
                            if value == "□" and int(state.board.board[10][col]) >=1: row_value -= 1
                            if state.board.board[row][col+1] in ["M", "m", "□", "?"] and state.board.adjacent_vertical_values(row, col+1)[0] in [".", "□", "W"] and state.board.adjacent_vertical_values(row, col+1)[1] in [".", "□", "W"]:
                                if value == "M" or value == "m":
                                    control += "m"
                                if state.board.board[row][col+1] == "□" and int(state.board.board[10][col+1]) >=1: row_value -= 1
                                if state.board.board[row][col+2] in ["M", "m", "□", "?"] and state.board.adjacent_vertical_values(row, col+2)[0] in [".", "□", "W"] and state.board.adjacent_vertical_values(row, col+2)[1] in [".", "□", "W"]:
                                    if value == "M" or value == "m":
                                        control += "m"
                                    if state.board.board[row][col+2] == "□" and int(state.board.board[10][col+2]) >=1: row_value -= 1
                                    if state.board.board[row][col+3] in ["□", "?", "R", "r"] and state.board.adjacent_vertical_values(row, col+3)[0] in [".", "□", "W"] and state.board.adjacent_vertical_values(row, col+3)[1] in [".", "□", "W"]:
                                        if value == "R" or value == "r" and int(state.board.board[10][col+2]) >=1:
                                            control += "r"
                                        if state.board.board[row][col+3] == "□" and int(state.board.board[10][col+3]) >=1: row_value -= 1
                                        if control == "lmmr": state.board.remove_from_fleet(4)
                                        if control != "lmmr" and row_value >= 0:
                                            actions.append([(row, col), 4, "H"]) 
                    
                    if value in ["T", "t", "□", "?"] and state.board.adjacent_horizontal_values(row, col) in [".", "□", "W"]:
                        if value == "T" or value == "t":
                            control += "t"
                        if row + 4 < 10 and state.board.get_value(row + 4, col) in [".", "□", "W"]:
                            col_value = int(state.board.board[10][col])
                            if value == "□" and int(state.board.board[row][10]) >=1: col_value -= 1
                            if state.board.board[row+1][col] in ["M", "m", "□", "?"] and state.board.adjacent_horizontal_values(row+1, col)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row+1, col)[1] in [".", "□", "W"]:
                                if state.board.board[row+1][col] == "M" or state.board.board[row+1][col] == "m":
                                    control += "m"
                                if state.board.board[row+1][col]== "□" and int(state.board.board[row +1][10]) >=1: col_value -= 1
                                if state.board.board[row+2][col] in ["M", "m", "□", "?"] and state.board.adjacent_horizontal_values(row+2, col)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row+2, col)[1] in [".", "□", "W"]:
                                    if state.board.board[row+2][col] == "M" or state.board.board[row+2][col] == "m":
                                        control += "m"
                                    if state.board.board[row+2][col] == "□" and int(state.board.board[row +2][10]) >=1: col_value -= 1
                                    if state.board.board[row+3][col] in ["B", "b", "□", "?"] and state.board.adjacent_horizontal_values(row+3, col)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row+3, col)[1] in [".", "□", "W"]:
                                        if state.board.board[row+3][col] == "B" or state.board.board[row+3][col] == "b":
                                            control += "b"
                                        if state.board.board[row+3][col]== "□" and int(state.board.board[row +3][10]) >=1: col_value -= 1
                                        if control == "tmmb": state.board.remove_from_fleet(4)
                                        if control != "tmmb" and col_value >= 0:
                                            actions.append([(row, col), 4, "V"]) 
            
        if boats == []: return actions
        
        if boats[0] == 3:
            for row in range(11):
                for col in range(11):
                    value = state.board.get_value(row, col)
                    control = ""
                    if value in ["L", "l", "□", "?"] and state.board.adjacent_vertical_values(row, col) in [".", "□", "W"]:
                        if col + 3 < 10 and state.board.get_value(row, col + 3) in [".", "□", "W"]:
                            row_value = int(state.board.board[row][10])
                            if value == "L" or value == "l":
                                control += "l"
                            if value == "□" and int(state.board.board[10][col]) >=1: row_value -= 1

                            if state.board.board[row][col+1] in ["M", "m", "□", "?"] and state.board.adjacent_vertical_values(row, col+1)[0] in [".", "□", "W"] and state.board.adjacent_vertical_values(row, col+1)[1] in [".", "□", "W"]:
                                if state.board.board[row][col+1] == "M" or state.board.board[row][col+1] == "m":
                                    control += "m"
                                if state.board.board[row][col+1] == "□" and int(state.board.board[10][col+1]) >=1: row_value -= 1

                                if state.board.board[row][col+2] in ["R", "r", "□", "?"] and state.board.adjacent_vertical_values(row, col+2)[0] in [".", "□", "W"] and state.board.adjacent_vertical_values(row, col+2)[1] in [".", "□", "W"]:
                                    if state.board.board[row][col+2] == "R" or state.board.board[row][col+2] == "r":
                                        control += "r"
                                    if state.board.board[row][col+2] == "□": row_value -= 1
                                    if control == "lmr": state.board.remove_from_fleet(3)
                                    if control != "lmr" and row_value >= 0: actions.append([(row, col), 3, "H"]) 

                    if value in ["T", "t", "□", "?"] and state.board.adjacent_horizontal_values(row, col)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row, col)[1] in [".", "□", "W"]:
                        if row + 3 < 10 and state.board.get_value(row + 3, col) in [".", "□", "W"]:
                            col_value = int(state.board.board[10][col])
                            if value == "T" or value == "t" and int(state.board.board[row][10]) >=1:
                                control += "t"
                            if value == "□" and int(state.board.board[row][10]) >=1: col_value -= 1

                            if state.board.board[row+1][col] in ["M", "m", "□", "?"] and state.board.adjacent_horizontal_values(row+1, col)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row+1, col)[1] in [".", "□", "W"]:
                                if state.board.board[row+1][col] == "M" or state.board.board[row+1][col] == "m":
                                    control += "m"
                                if state.board.board[row+1][col] == "□" and int(state.board.board[row+1][10]) >=1: col_value -= 1

                                if state.board.board[row+1][col] in ["B", "b", "□", "?"] and state.board.adjacent_horizontal_values(row+2, col)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row+2, col)[1] in [".", "□", "W"]:
                                    if state.board.board[row+1][col] == "B" or state.board.board[row+1][col] == "b":
                                            control += "b"
                                    if state.board.board[row+2][col] == "□" and int(state.board.board[row+2][10]) >=1: col_value -= 1
                                    if control == "tmb": state.board.remove_from_fleet(3)
                                    if control != "tmb" and col_value >= 0: actions.append([(row, col), 3, "V"])
            print(actions)

        if boats == []: return actions
        if boats[0] == 2:
            for row in range(11):
                for col in range(11):
                    value = state.board.get_value(row, col)
                    control = ""

                    if value in ["L", "l", "□", "?"] and state.board.adjacent_horizontal_values(row, col)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row, col)[1] in [".", "□", "W"]:
                        if col + 2 < 10 and state.board.get_value(row, col + 2) in [".", "□", "W"]:
                            row_value = int(state.board.board[row][10])
                            if value == "L" or value == "l":
                                control += "l"
                            if value == "□" and int(state.board.board[10][col]) >=1: row_value -= 1
                            
                            if state.board.board[row][col+1] in ["R", "r", "□", "?"] and state.board.adjacent_horizontal_values(row, col+1)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row, col+1)[1] in [".", "□", "W"]:
                                if state.board.board[row][col+1] == "R" or state.board.board[row][col+1] == "r":
                                    control += "r"
                                if state.board.board[row][col+1] == "□" and int(state.board.board[10][col+1]) >=1: row_value -= 1
                                if control == "lr": state.board.remove_from_fleet(2)
                                if control != "lr" and row_value >= 0: actions.append([(row, col), 2, "H"])
                    
                    if value in ["T", "t", "□", "?"] and state.board.adjacent_horizontal_values(row, col)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row, col)[1] in [".", "□", "W"]: 
                        if row + 2 < 10 and state.board.get_value(row + 2, col) in [".", "□", "W"]:
                            col_value = int(state.board.board[10][col])
                            if value == "T" or value == "t":
                                control += "t"
                            if value == "□" and int(state.board.board[row][10]) >=1: col_value -= 1

                            if state.board.board[row+1][col] in ["B", "b", "□", "?"] and state.board.adjacent_horizontal_values(row+1, col)[0] in [".", "□", "W"] and state.board.adjacent_horizontal_values(row+1, col)[1] in [".", "□", "W"]:
                                if state.board.board[row+1][col] == "B" or state.board.board[row+1][col] == "b":
                                    control += "b"
                                if state.board.board[row+1][col] == "□" and int(state.board.board[row+1][10]) >=1: col_value -= 1
                                if control == "tb": state.board.remove_from_fleet(2)
                                if control != "tb" and col_value >= 0: actions.append([(row, col), 2, "V"])
            
        if boats == []: return actions
        if boats[0] == 1:
            for row in range(11):
                for col in range(11):
                    value = state.board.get_value(row, col)
                    if value == "□" and int(state.board.board[10][col]) >=1 and int(state.board.board[row][10]) >=1: 
                        actions.append([(row, col), 1, "H"])
                    elif value == "?" and int(state.board.board[10][col]) >=1 and int(state.board.board[row][10]) >=1:
                        actions.append([(row, col), 1, "H"])
        
        return actions



        
    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        new_board = Board()
        new_board.copy_board(state.board)
        new_state = BimaruState(new_board)
        board = new_state.board

        board.put_boat(action[0][0], action[0][1], action[1], action[2])

        return new_state


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        if state.board.fleet != []: return False
        for row in range(10):
            if state.board.get_value(row, 10) != "0": 
                return False
            for col in range(10):
                if state.board.get_value(10, col) != "0": 
                    return False
                if state.board.get_value(row, col) in ["?", "□"]:
                    print(state.board.get_value(row, col))
                    return False
        return True
        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass



if __name__ == "__main__":
    board = Board.parse_instance()
    problem  = Bimaru(board)
    """for row in range(0, 11, 1):
        for col in range(0, 11, 1):
            print(board.board[row][col], end=" ")
        print()
    print(board.fleet)
    print("+------------------------------------------------+") """
    solution = depth_first_tree_search(problem)
    solution.state.board.print_board()



    """ board.actions_initial()
    problem = Bimaru(board)



 """
    """for row in range(0, 11, 1):
        for col in range(0, 11, 1):
            print(board.board[row][col], end=" ")
        print()"""

    

   
     

    
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
