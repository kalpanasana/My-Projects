import tkinter as tk
from tkinter import messagebox

# Initialize main window
root = tk.Tk()
root.title("Tic Tac Toe")

# Game state
current_player = "X"
board = [""] * 9

# Button click handler
def handle_click(index):
    global current_player

    if buttons[index]["text"] == "":
        buttons[index]["text"] = current_player
        board[index] = current_player

        if check_winner():
            messagebox.showinfo("Game Over", f"🎉 Player {current_player} wins!")
            reset_board()
        elif "" not in board:
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_board()
        else:
            current_player = "O" if current_player == "X" else "X"

def check_winner():
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for pattern in win_patterns:
        a, b, c = pattern
        if board[a] == board[b] == board[c] != "":
            return True
    return False

def reset_board():
    global current_player, board
    for button in buttons:
        button["text"] = ""
    board = [""] * 9
    current_player = "X"

# Create buttons
buttons = []
for i in range(9):
    button = tk.Button(root, text="", font=("Arial", 24), width=5, height=2, command=lambda i=i: handle_click(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

# Run the app
root.mainloop()
