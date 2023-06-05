# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 83:
# 103011 André Oliveira
# 103120 Beatriz Mendes

import sys

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

    
    def print_board(self):
        """ Função que imprime uma board de acordo com formato descrito no enunciado. """
        for row in range(10):
            for col in range(10):
                print(self.board[row][col], end='')
            print()
        pass


    def __init__(self):
        """ Uma Board é inicializada como uma matriz 11x11, e com uma lista que corresponde à frota de um jogo Bimaru. """
        self.board = [["□"] * 11 for _ in range(11)]
        self.fleet = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


    def get_value(self, row, col):
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def adjacent_vertical_values(self, row, col):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row - 1 >= 9 or row + 1 <= 0:
            return None, None
        if row <= 0: 
            return None, self.get_value(row + 1, col)
        if row >= 9: 
            return self.get_value(row - 1, col), None
        return self.get_value(row - 1, col), self.get_value(row + 1, col)

    def adjacent_horizontal_values(self, row, col):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col - 1 >= 9 or col + 1 <= 0:
            return None, None
        if col <= 0: 
            return None, self.get_value(row, col + 1)
        if col >= 9: 
            return self.get_value(row, col - 1), None
        return self.get_value(row, col - 1), self.get_value(row, col + 1)


    def copy_board(self, old_board):
        """ Cria uma cópia da Board 'old_board'"""
        self.fleet = old_board.fleet[:]
        for row in range(11):
            for col in range(11):
                self.board[row][col] = old_board.board[row][col]
        
    
    def check_rows(self, row):
        """Verifica se o número de barcos numa linha está correto."""
        count = 0
        for col in range(10):
            value = self.get_value(row, col)
            if value == "?":
                self.clear_case(row, col)
            elif value == "□":
                count += 1
            if self.get_value(row, col + 1) == "M":
                self.case_M(row, col + 1)
        if count != 0:
            if count == int(self.board[row][10]):
                return 1 
            if (int(self.board[row][10]) == 0):
                return 2
        return 0


    def check_cols(self, col):
        """Verifica se o número de barcos numa coluna está correto."""
        count = 0
        for row in range(10):
            value = self.get_value(row, col)
            if value == "?":
                self.clear_boats_col(col)
            elif value == "□":
                count += 1
            if self.get_value(row + 1, col) == "M":
                self.case_M(row + 1, col)
        if count != 0:
            if count == int(self.board[10][col]):
                return 1 
            if int(self.board[10][col]) == 0:
                return 2
        return 0

    def fill_rows(self, row, mode):
        if mode == 1:
            """Preenche a linha com barcos."""
            for col in range(10):
                if self.get_value(row, col) == "□":
                    self.board[row][col] = "?"
                    self.change_cases_filled(row, col)
                    self.clear_boats_row(row)
        elif mode == 2:
            """Preenche a linha com água."""
            for col in range(10):
                if self.get_value(row, col) == "□":
                    self.board[row][col] = "."
                elif self.get_value(row, col) == "?":
                    self.clear_boats_row(row)


    def fill_cols(self, col, mode):
        """Preenche a coluna com barcos."""
        if mode == 1:
            for row in range(10):
                if self.board[row][col] == "□":
                    self.board[row][col] = "?"
                    self.change_cases_filled(row, col)
                    self.clear_boats_row(row)
        elif mode == 2:
            """Preenche a coluna com água."""
            for row in range(10):
                if self.board[row][col] == "□":
                    self.board[row][col] = "."     
                elif self.get_value(row, col) == "?":
                    self.clear_boats_col(col)
        
    
    def change_cases_filled(self, row, col):
        """Diminui o número de posições que ainda podem ser preenchidas """
        row_10, col_10 = int(self.board[row][10]) - 1, int(self.board[10][col]) - 1
        self.board[row][10] = str(row_10)
        if row_10 == 0:
            self.fill_rows(row, 2)
        self.board[10][col] = str(col_10)
        if col_10 == 0: 
            self.fill_cols(col, 2)
    
    def calculate_boat_size(self, row, col):
        """Calcula o tamanho do barco que engloba a posição (row, col)."""
        if self.get_value(row, col) in ["b", "B", "t", "T", "l", "L", "r", "R"]:
            return 2
        
        adjacent_top, adjacent_bottom = self.adjacent_vertical_values(row, col)
        adjacent_left, adjacent_right = self.adjacent_horizontal_values(row, col)

        if (adjacent_top in ["t", "T"] and adjacent_bottom in ["b", "B"]) or (adjacent_left in ["l", "L"] and adjacent_right in ["r", "R"]):
            return 3
        
        elif adjacent_top in ["m", "M"] or adjacent_bottom in ["m", "M"] or adjacent_left in ["m", "M"] or adjacent_right in ["m", "M"]:
            return 4
        
        return 0


    def remove_from_fleet(self, size):
        """Remove o barco de tamanho 'size' da frota."""
        if size in self.fleet:
            for i in range(len(self.fleet)):
                if (self.fleet[i] == size):
                    self.fleet.pop(i)
                    return

    def case_M(self, row, col):
        """ Atualiza o tabuleiro quando uma posição é marcada como 'M'. """
        if self.adjacent_horizontal_values(row, col + 2)[1] in ["m", "M", "r", "R", "?"] or self.adjacent_horizontal_values(row, col - 2)[0] in ["m", "M", "l", "L", "?"]:
            if self.board[row][col + 1] == "□": self.board[row][col + 1] = "."
            if self.board[row][col - 1] == "□": self.board[row][col - 1] = "."
        
        elif self.adjacent_vertical_values(row + 2, col)[1] in ["m", "M", "b", "B", "?"] or self.adjacent_vertical_values(row - 2, col)[0] in ["m", "M", "t", "T", "?"]:
            if self.board[row + 1][col] == "□": self.board[row + 1][col] = "."
            if self.board[row - 1][col] == "□": self.board[row - 1][col] = "."


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
        
        self.remove_from_fleet(self.calculate_boat_size(row, col))


    def clear_case(self, row, col):
        """ Limpa a posição (row, col) do tabuleiro. """
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
            if self.calculate_boat_size(row , col) == 4: self.remove_from_fleet(4)

        
        elif self.adjacent_horizontal_values(row, col)[0] in ["l", "L", "m", "M", "?"] and self.adjacent_horizontal_values(row, col)[1] in ["r", "R", "M", "?", "m"]:
            self.board[row][col] = "m"
            self.put_water_m(row, col)
            if self.calculate_boat_size(row , col) == 4: self.remove_from_fleet(4)

        return

    #Funções auxiliares para o clear_case
    def clear_boats_col(self, col):
        """ Limpa a coluna col do tabuleiro."""
        for row in range(10):
            if self.get_value(row, col) == "?":
                self.clear_case(row, col)
        return 

    def clear_boats_row(self, row):
        """ Limpa a linha row do tabuleiro."""
        for col in range(10):
            if self.get_value(row, col) == "?":
                self.clear_case(row, col)
        return
    
    #Funções que colocam água nas posições adjacentes
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
            if self.get_value(row, col - 1) == "□": self.board[row][col - 1] = "."
        if col != 9:
            if self.get_value(row, col + 1) == "□": self.board[row][col + 1] = "."
        if row != 0:
            if self.get_value(row - 1, col) == "□": self.board[row - 1][col] = "."
            if col != 0:
                if self.get_value(row - 1, col - 1) == "□": self.board[row - 1][col - 1] = "."
            if col != 9:
                if self.get_value(row - 1, col + 1) == "□":self.board[row - 1][col + 1] = "."
        if row != 9:
            if self.get_value(row + 1, col) == "□": self.board[row + 1][col] = "."
            if col != 0:
                if self.get_value(row + 1, col - 1) == "□": self.board[row + 1][col - 1] = "."
            if col != 9:
                if self.get_value(row + 1, col + 1) == "□": self.board[row + 1][col + 1] = "." 


    def make_stuff_happen(self):
        """ Função que faz loop enquanto são feitas alterações ao projeto. """
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


    def actions_initial(self):
        """ Completa as primeiras ações possiveis, de modo a que o tabuleiro esteja o mais simplificado possível antes de iniciar a bfs. """
    
        for row in range(10):
            for col in range(10):
                value = self.get_value(row, col)
                
                """ T """
                if value == "T":
                    self.change_cases_filled(row, col)
                    if self.get_value(row + 1, col) == "□": 
                        self.board[row + 1][col] = "?"
                        self.change_cases_filled(row + 1, col)         
                    self.put_water_t(row, col)
                    self.put_water_m(row + 1, col)

                """ B """
                if value == "B":
                    self.change_cases_filled(row, col)
                    if self.get_value(row - 1, col) == "□": 
                        self.board[row - 1][col] = "?"
                        self.change_cases_filled(row - 1, col)
                    self.put_water_b(row, col)
                    self.put_water_m(row - 1, col)

                """ L """
                if value == "L":
                    self.change_cases_filled(row, col)
                    if self.get_value(row, col + 1) == "□": 
                        self.board[row][col + 1] = "?"
                        self.change_cases_filled(row, col + 1)
                    self.put_water_l(row, col)
                    self.put_water_m(row, col + 1)


                """ R """
                if value == "R":
                    self.change_cases_filled(row, col)
                    if self.get_value(row, col - 1) == "□": 
                        self.board[row][col - 1] = "?"
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

    #FUNÇÕES USADAS NA DFS
    def put_boat(self, row, col, size, orientation):
        """ Coloca um barco de tamanho size no tabuleiro. O barco começa na posição (row, col) e tem orientação 'orientation'."""

        if size == 1:
            """ Coloca um barco de tamanho 1 no tabuleiro. """
            self.board[row][col] = "c"
            self.change_cases_filled(row, col)
            self.remove_from_fleet(size)

        elif orientation == "H":
            """ Coloca um barco horizontal de tamanho 'size' no tabuleiro. """
            if col != 0 and self.board[row][col - 1] == "□": self.board[row][col - 1] = "."
            for i in range(size):
                if self.get_value(row, col + i) == "□":
                    self.board[row][col + i] = "?"
                    self.change_cases_filled(row, col + i)
            if self.board[row][col + size] == "□": self.board[row][col + size] = "."
            self.clear_boats_row(row)

        elif orientation == "V":
            """ Coloca um barco vertical de tamanho 'size' no tabuleiro. """
            if row != 0 and self.board[row - 1][col] == "□": self.board[row - 1][col] = "."
            for i in range(size):
                if self.get_value(row + i, col) == "□":
                    self.board[row + i][col] = "?"
                    self.change_cases_filled(row + i, col)
            if self.board[row + size][col] == "□": self.board[row + size][col] = "."
            self.clear_boats_col(col)
        

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board. """
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
        check = 0
        boat_aux = ""
        actions = []
        boats = state.board.fleet
        if boats == []: return actions


        boat_size = boats[0]
        
        for row in range(10):
            for col in range(10):
                value = state.board.get_value(row, col)
                if boat_size > 1:
                    """H"""
                    if (col + boat_size - 1 < 10 and value in ["L", "l", "□", "?"] and 
                        state.board.adjacent_vertical_values(row, col)[0] in [".", "□", "W", None] and
                        state.board.adjacent_vertical_values(row, col)[1] in [".", "□", "W", None]):
                        boat_aux += value
                        if (state.board.adjacent_horizontal_values(row, col + boat_size - 1)[1] in [".", "□", "W", None] and 
                            state.board.adjacent_horizontal_values(row, col)[0] in [".", "□", "W", None]):
                            for i in range(1, boat_size - 1, 1):
                                aux = state.board.get_value(row, col + i)
                                boat_aux += aux
                                if  aux not in ["□", "?", "m", "M"]: check = 1
                            aux = state.board.get_value(row, col + boat_size - 1)
                            boat_aux += aux
                            if aux not in ["□", "?", "r", "R"] or int(state.board.board[row][10]) - boat_aux.count("□") < 0: 
                                check = 1
                            if check == 0 and boat_aux.count("?") + boat_aux.count("□") != 0: 
                                actions.append([(row, col), boat_size, "H"])
                    check, boat_aux = 0, ""

                    """V"""
                    if (row + boat_size - 1 < 10 and value in ["T", "t", "□", "?"] and 
                        state.board.adjacent_horizontal_values(row, col)[0] in [".", "□", "W", None] and 
                        state.board.adjacent_horizontal_values(row, col)[1] in [".", "□", "W", None]):
                        boat_aux += value
                        if (state.board.adjacent_vertical_values(row + boat_size - 1, col)[1] in [".", "□", "W", None] and 
                            state.board.adjacent_vertical_values(row, col)[0] in [".", "□", "W", None]):
                            for i in range(1, boat_size - 1, 1):
                                aux = state.board.get_value(row + i, col)
                                boat_aux += aux
                                if aux not in ["m", "M", "?", "□"]: check = 1
                            aux = state.board.get_value(row + boat_size - 1, col)
                            boat_aux += aux
                            if aux not in ["□", "b", "B", "?"] or int(state.board.board[10][col]) - boat_aux.count("□") < 0: 
                                check = 1
                            if check == 0 and boat_aux.count("?") + boat_aux.count("□") != 0: 
                                actions.append([(row, col), boat_size, "V"])
                    check, boat_aux = 0, ""
                
                elif boat_size == 1:
                    if value == "?":
                        state.board.clear_case(row, col)
                    elif value == "□": 
                        if (state.board.adjacent_vertical_values(row, col)[0] in [".", "□", "W", None] and 
                            state.board.adjacent_vertical_values(row, col)[1] in [".", "□", "W", None] and 
                            state.board.adjacent_horizontal_values(row, col)[0] in [".", "□", "W", None] and 
                            state.board.adjacent_horizontal_values(row, col)[1] in [".", "□", "W", None]):
                                actions.append([(row, col), boat_size, "C"])
    
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
                    return False
        return True
        

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass



if __name__ == "__main__":
    board = Board.parse_instance()
    problem  = Bimaru(board)
    solution = depth_first_tree_search(problem)
    solution.state.board.print_board()
    pass
