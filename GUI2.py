import random
import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Sudoku Board", font=("Arial", 18))
        self.label.pack()

        self.canvas = tk.Canvas(self.frame, width=450, height=450)
        self.canvas.pack()

        self.load_manual_button = tk.Button(self.frame, text="Load Data Manually", command=self.load_manual_data)
        self.load_manual_button.pack(side=tk.LEFT)

        self.load_random_button = tk.Button(self.frame, text="Load Random Data", command=self.load_random_data)
        self.load_random_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.frame, text="Clear Board", command=self.clear_board)
        self.clear_button.pack(side=tk.LEFT)

        self.submit_button = tk.Button(self.frame, text="Submit Data", command=self.submit_data)
        self.submit_button.pack(side=tk.LEFT)

        self.solve_button = tk.Button(self.frame, text="Solve Sudoku", command=self.solve_sudoku)
        self.solve_button.pack(side=tk.LEFT)

        self.create_board()

    def create_board(self):
        for i in range(9):
            for j in range(9):
                x1 = j * 50
                y1 = i * 50
                x2 = x1 + 50
                y2 = y1 + 50

                # Draw the grid lines with thicker lines for the 3x3 grid
                if i % 3 == 0:
                    self.canvas.create_line(x1, y1, x2, y1, width=2)  # Top horizontal line
                else:
                    self.canvas.create_line(x1, y1, x2, y1)  # Top horizontal line

                if j % 3 == 0:
                    self.canvas.create_line(x1, y1, x1, y2, width=2)  # Left vertical line
                else:
                    self.canvas.create_line(x1, y1, x1, y2)  # Left vertical line

                self.canvas.create_rectangle(x1, y1, x2, y2)
                if self.board[i][j] != 0:
                    self.canvas.create_text(x1 + 25, y1 + 25, text=self.board[i][j], font=("Arial", 16))


    def load_manual_data(self):
        # Open a new window to input manual data
        manual_window = tk.Toplevel(self.root)
        manual_window.title("Load Manual Data")

        entry_frame = tk.Frame(manual_window)
        entry_frame.pack(pady=10)

        entries = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(entry_frame, width=4, font=("Arial", 16))
                entry.grid(row=i, column=j)
                row.append(entry)
            entries.append(row)

        
        def submit_manual_data():
            has_value = False  # Flag to check if at least one number is entered

            for i in range(9):
                for j in range(9):
                    value = entries[i][j].get()
                    if value:
                        try:
                            num = int(value)
                            if num < 1 or num > 9:
                                raise ValueError
                            self.board[i][j] = num
                            has_value = True
                        except ValueError:
                            messagebox.showerror("Invalid Input", "Please enter valid numbers from 1 to 9.")
                            return

            if not has_value:
                messagebox.showerror("Invalid Input", "Please enter at least one valid number before submitting.")
                return

            # Fill the rest of the board with zeros
            for i in range(9):
                for j in range(9):
                    if not entries[i][j].get():
                        self.board[i][j] = 0

            manual_window.destroy()
            self.draw_numbers()
            

        submit_button = tk.Button(manual_window, text="Submit", command=submit_manual_data)
        submit_button.pack()

    def load_random_data(self):
        difficulty_window = tk.Toplevel(self.root)
        difficulty_window.title("Select Difficulty")

        def select_difficulty(difficulty):
            difficulty_window.destroy()
            self.board = self.generate_random_board(difficulty)
            self.draw_numbers()

        easy_button = tk.Button(difficulty_window, text="Easy", command=lambda: select_difficulty("easy"))
        easy_button.pack(side=tk.LEFT)

        medium_button = tk.Button(difficulty_window, text="Medium", command=lambda: select_difficulty("medium"))
        medium_button.pack(side=tk.LEFT)

        hard_button = tk.Button(difficulty_window, text="Hard", command=lambda: select_difficulty("hard"))
        hard_button.pack(side=tk.LEFT)

    def generate_random_board(self, difficulty):
        def is_valid(board, row, col, num):
            for i in range(9):
                if board[row][i] == num:
                    return False

            for j in range(9):
                if board[j][col] == num:
                    return False

            start_row = (row // 3) * 3
            start_col = (col // 3) * 3
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if board[i][j] == num:
                        return False

            return True

        def solve_sudoku(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        numbers = random.sample(range(1, 10), 9)
                        for num in numbers:
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if solve_sudoku(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        board = [[0] * 9 for _ in range(9)]
        solve_sudoku(board)

        # Adjust the number of filled cells based on the difficulty level
        if difficulty == "easy":
            num_to_remove = random.randint(35, 45)
        elif difficulty == "medium":
            num_to_remove = random.randint(46, 54)
        elif difficulty == "hard":
            num_to_remove = random.randint(55, 60)

        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for i in range(num_to_remove):
            row, col = cells[i]
            board[row][col] = 0

        return board

    def clear_board(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.draw_numbers()

    def submit_data(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    messagebox.showerror("Incomplete Board", "Please fill all cells before submitting.")
                    return

        messagebox.showinfo("Submission Successful", "Sudoku board submitted successfully!")

    def solve_sudoku(self):
        if not self.solve_sudoku_util():
            messagebox.showinfo("Not Solvable", "The given Sudoku board is not solvable.")
        else:
            self.draw_numbers()

    def solve_sudoku_util(self):
        def is_valid(row, col, num):
            for i in range(9):
                if self.board[row][i] == num:
                    return False

            for j in range(9):
                if self.board[j][col] == num:
                    return False

            start_row = (row // 3) * 3
            start_col = (col // 3) * 3
            for i in range(start_row, start_row + 3):
                for j in range(start_col, start_col + 3):
                    if self.board[i][j] == num:
                        return False

            return True

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(row, col, num):
                            self.board[row][col] = num
                            if self.solve_sudoku_util():
                                return True
                            self.board[row][col] = 0
                    return False
        return True

    def draw_numbers(self):
        self.canvas.delete("all")
        self.create_board()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    sudoku_gui = SudokuGUI()
    sudoku_gui.run()
