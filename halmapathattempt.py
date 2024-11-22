import tkinter as tk
import sys

GRID_CELL_SIZE = 50
GAME_PIECE_PADDING = 5
MOVE_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (-1, -1), (1, -1)]

class GameManager:
    def __init__(self, board_size):
        self.board = {}
        self.board_size = board_size
        self.selected_piece = None
        for row in range(board_size):
            for col in range(board_size):
                self.board[(row, col)] = 'empty'
        
        half_board_size = board_size // 2
        for row in range(half_board_size):
            for col in range(half_board_size - row):
                self.board[(row, col)] = 'red'
                
        for row in range(board_size - 1, half_board_size - 1, - 1):
            for col in range(board_size - 1, (half_board_size - 1) + (board_size - 1 - row), - 1):
                self.board[(row, col)] ='green'
        self.board_display = GameBoard(self.board, self)
    
    def start_move(self, cell):
        self.selected_piece = cell
        possible_moves = MoveGenerator.get_moves(cell, self.board, self.board_size)
        self.board_display.show_moves(cell, possible_moves)
    
    def check_moves(self, cell):
        self.selected_piece = cell
        move_paths = MoveGenerator.get_moves(cell, self.board, self.board_size, return_paths=True)
        print(move_paths)
        self.board_display.show_move_paths(cell, move_paths)
        
    def execute_move(self, dest_cell):
        self.board[dest_cell] = self.board[self.selected_piece]
        self.board[self.selected_piece] = "empty"
        self.exit_move()
        self.board_display.update(self.board)
        
    def exit_move(self):
        self.board_display.exit_move_state()
        self.selected_piece = None
                
    def show_invalid_move_warning(self):
        message_label = tk.Label(tk_root, text="Invalid Move! Try Again", font=("Helvetica", 16))
        message_label.pack(pady=20)

class GameCell:
    def __init__(self, row, col, game_board, manager):
        self.pos = (row, col)
        self.board = game_board
        self.canvas = tk.Canvas(tk_root, width = GRID_CELL_SIZE, 
                                        height = GRID_CELL_SIZE, bg='burlywood1', 
                                                highlightbackground='black')
        self.state = "empty"
        self.canvas.grid(row=row, column=col)
        self.highlighted = False
        self.manager = manager
        
    def clear(self):
        self.canvas.delete("all")
        self.state = "empty"
        
    def set_red_state(self):
        self.canvas.create_oval(GAME_PIECE_PADDING, GAME_PIECE_PADDING, 
                        GRID_CELL_SIZE - GAME_PIECE_PADDING, GRID_CELL_SIZE - GAME_PIECE_PADDING,
                                    fill = "white")
        self.state = "red"
        self.canvas.bind('<Button-1>', lambda event: manager.start_move(self.pos))
        self.canvas.bind('<Button-3>', lambda event: manager.check_moves(self.pos))

    
    def set_green_state(self):
        self.canvas.create_oval(GAME_PIECE_PADDING, GAME_PIECE_PADDING, 
                        GRID_CELL_SIZE - GAME_PIECE_PADDING, GRID_CELL_SIZE - GAME_PIECE_PADDING,
                                    fill = "black")
        self.state = "green"
        self.canvas.bind('<Button-1>', lambda event: manager.start_move(self.pos))
        self.canvas.bind('<Button-3>', lambda event: manager.check_moves(self.pos))
        
    def highlight(self):
        if self.state == "empty":
            self.canvas.create_rectangle(0, 0, GRID_CELL_SIZE, GRID_CELL_SIZE, 
                                        outline="black", fill="burlywood4")
            self.canvas.bind('<Button-1>', lambda event: manager.execute_move(self.pos))
        elif self.state == "red":
            self.canvas.create_oval(GAME_PIECE_PADDING, GAME_PIECE_PADDING, 
                                    GRID_CELL_SIZE - GAME_PIECE_PADDING, GRID_CELL_SIZE - GAME_PIECE_PADDING,
                                        fill = "white", outline="red", width=3)
            self.canvas.bind('<Button-1>', lambda event: manager.exit_move())
        else:
            self.canvas.create_oval(GAME_PIECE_PADDING, GAME_PIECE_PADDING, 
                                    GRID_CELL_SIZE - GAME_PIECE_PADDING, GRID_CELL_SIZE - GAME_PIECE_PADDING,
                                        fill = "black", outline="green", width=3)
            self.canvas.bind('<Button-1>', lambda event: manager.exit_move())
        self.highlighted = True        
    
    def unbind_click(self):
        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<Button-3>')

class GameBoard:
    def __init__(self, board, manager):
        self.display_board = {}
        self.manager = manager
                
        for cell, state in board.items():
            row, col = cell
            self.display_board[cell] = GameCell(row, col, self, self.manager)
            if state == 'red':
                self.display_board[cell].set_red_state()
            elif state == 'green':
                self.display_board[cell].set_green_state()
    
    def exit_move_state(self):
        for cell in self.display_board.values():
            state = cell.state
            if cell.highlighted:
                cell.highlighted = False
                cell.clear()
            if state == "red":
                cell.set_red_state()
            elif state == "green":
                cell.set_green_state()
    
    def show_moves(self, piece, moves):
        for cell, canvas in self.display_board.items():
            if cell in moves or cell == piece:
                canvas.highlight()
            else:
                canvas.unbind_click()
    
    def show_move_paths(self, piece, paths):
        self.display_board[piece].highlight()
        for path in paths:
            for index in range(len(path) - 1):
                curr_cell = path[index]
                next_cell = path[index + 1]

                x1 = self.display_board[curr_cell].canvas.winfo_rootx()
                y1 = self.display_board[curr_cell].canvas.winfo_rootx()
                x2 = self.display_board[next_cell].canvas.winfo_rootx()
                y2 = self.display_board[next_cell].canvas.winfo_rootx()
                self.display_board[curr_cell].canvas.create_line(
                    x1, y1, x2, y2, arrow=tk.LAST, 
                    fill="green", width=2
                )
        
    def update(self, new_board):
        for cell, canvas in self.display_board.items():
            if new_board[cell] == "empty":
                canvas.clear()
            elif new_board[cell] == "red":
                canvas.set_red_state()
            else:
                canvas.set_green_state()
            
class MoveGenerator:
    def get_moves(cell, game_board, board_size, return_paths=False):
        move_stack = [[cell, []]]
        valid_moves = []
        final_paths = []
        
        while move_stack:
            curr_cell, path = move_stack.pop()
            row, col = curr_cell
            new_path = path + [curr_cell]
        
            for row_change, col_change in MOVE_DIRS:
                move = (row + row_change, col + col_change)
                if MoveGenerator.valid_cell(move[0], move[1], board_size) and move not in new_path:
                    if game_board[move] == "red" or game_board[move] == "green":
                        jump_move = (move[0] + row_change, move[1] + col_change)
                        if MoveGenerator.valid_cell(jump_move[0], jump_move[1], board_size) and game_board[jump_move] == "empty" and jump_move not in new_path:
                            valid_moves.append(jump_move)
                            final_paths.append(new_path + [jump_move])
                            if MoveGenerator.check_for_surrounding_piece(jump_move, game_board, board_size):
                                move_stack.append([(jump_move[0], jump_move[1]), new_path])
                    elif curr_cell == cell:
                        valid_moves.append(move)
                        final_paths.append(new_path + [move])
        
        if return_paths:
            return final_paths
        return valid_moves

    def check_for_surrounding_piece(cell, board, board_size):
        row, col = cell
        for row_change, col_change in MOVE_DIRS:
            adj_cell = (row + row_change, col + col_change)
            if MoveGenerator.valid_cell(adj_cell[0], adj_cell[1], board_size) and \
            (board[(adj_cell)] == "red" or board[adj_cell] == "green"):
                return True
        return False
        
    def valid_cell(row, col, board_size):
        return row < board_size and row > -1 and col < board_size and col > -1


tk_root = tk.Tk()
tk_root.title("Game Board with Canvas Cells")
manager = GameManager(8)  # Define rows, columns, and cell size
tk_root.mainloop()
