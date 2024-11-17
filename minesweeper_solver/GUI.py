import tkinter as tk
from minesweeper import Minesweeper
import minesweeper

beginner = Minesweeper((4, 4), 9, 9, 10)
intermediate = Minesweeper((4, 4), 16, 16, 40)
expert = Minesweeper((4, 4), 16, 30, 99)
def custom() -> Minesweeper:
    print('Rows: ', end='')
    n = int(input())
    print('Columns: ', end='')
    m = int(input())
    print('Number of bombs: ', end='')
    k = int(input())
    starting_pos = (4, 4)
    return Minesweeper(starting_pos, n, m, k)


states, key, ending = minesweeper.play_game(expert, minesweeper.my_player)


class MinesweeperDisplayApp:
    def __init__(self, root, states, key, is_victory):
        self.root = root
        self.root.title("Minesweeper Display App")

        self.states = states
        self.key = key
        self.is_victory = is_victory  # "VICTORY" or "DEFEAT"
        self.current_index = 0

        self.rows = len(states[0])
        self.cols = len(states[0][0])

        # Create a grid of labels
        self.grid_labels = []
        for r in range(self.rows):
            row_labels = []
            for c in range(self.cols):
                label = tk.Label(root, text="", font=("Courier", 18), width=2, height=1, borderwidth=1, relief="solid")
                label.grid(row=r, column=c, padx=2, pady=2)
                row_labels.append(label)
            self.grid_labels.append(row_labels)

        # Frame for buttons
        button_frame = tk.Frame(root)
        button_frame.grid(row=self.rows, columnspan=self.cols, pady=10)

        # Navigation buttons
        self.prev_button = tk.Button(button_frame, text="Previous", command=self.previous_array, width=10)
        self.prev_button.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_array, width=10)
        self.next_button.grid(row=0, column=2, padx=5)

        # "Go to End" button
        self.end_button = tk.Button(button_frame, text="Go to End", command=self.go_to_end, width=10)
        self.end_button.grid(row=0, column=3, padx=5)

        # "Go to Start" button
        self.end_button = tk.Button(button_frame, text="Go to Start", command=self.go_to_start, width=10)
        self.end_button.grid(row=0, column=0, padx=5)

        # Display the first array
        self.update_grid()

    def update_grid(self):
        """Update the grid to show the symbols based on the current arrays."""
        state = self.states[self.current_index]
        is_last_state = self.current_index == len(self.states) - 1

        for r in range(self.rows):
            for c in range(self.cols):
                value = state[r][c]

                if is_last_state and value == 0:
                    # Treat 0 as 1 in the last state
                    if self.is_victory == "DEFEAT" and self.key[r, c] == 9:
                        symbol = "💣"  # Bomb for 9 in key
                    else:
                        symbol = str(self.key[r, c]) if self.key[r, c] != 0 else " "

                elif value == 0:
                    symbol = "■"
                elif value == 1:
                    symbol = str(self.key[r, c]) if self.key[r, c] != 0 else " "
                elif value == 2:
                    symbol = "⚑"
                elif value == 3:
                    symbol = "💣"
                else:
                    symbol = " "

                self.grid_labels[r][c].config(text=symbol)

        # Update button states based on the current index
        if is_last_state:
            self.next_button.config(state=tk.DISABLED, text=self.is_victory)
        else:
            self.next_button.config(state=tk.NORMAL, text="Next")

        self.prev_button.config(state=tk.NORMAL if self.current_index > 0 else tk.DISABLED)

    def next_array(self):
        """Move to the next array."""
        if self.current_index < len(self.states) - 1:
            self.current_index += 1
            self.update_grid()

    def previous_array(self):
        """Move to the previous array."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_grid()

    def go_to_end(self):
        """Instantly go to the last array."""
        self.current_index = len(self.states) - 1
        self.update_grid()

    def go_to_start(self):
        """Instantly go to the first array."""
        self.current_index = 0
        self.update_grid()


# Create the main window and run the app
root = tk.Tk()
app = MinesweeperDisplayApp(root, states, key, ending)
root.mainloop()
