
from board import Board


DIFFICULTIES = {
    "easy": {"rows": 6, "cols": 6, "mines": 6},
    "medium": {"rows": 9, "cols": 9, "mines": 15},
    "hard": {"rows": 12, "cols": 12, "mines": 30},
}


class Minesweeper:
    def __init__(self, difficulty="easy"):
        difficulty = difficulty.strip().lower()

        if difficulty not in DIFFICULTIES:
            raise ValueError("Invalid difficulty. Choose Easy, Medium, or Hard.")

        self.difficulty = difficulty
        config = DIFFICULTIES[difficulty]
        self.board = Board(**config)

    def display(self, reveal_mines=False):
        b = self.board

        print("\n   " + " ".join(f"{c + 1:2}" for c in range(b.cols)))

        for r in range(b.rows):
            cells = []

            for c in range(b.cols):
                pos = (r, c)

                if reveal_mines and pos in b.mines:
                    ch = "*"
                elif pos in b.flags:
                    ch = "F"
                elif pos not in b.revealed:
                    ch = "#"
                elif pos in b.mines:
                    ch = "*"
                else:
                    ch = str(b.adjacent_mines(r, c))

                cells.append(f"{ch:2}")

            print(f"{r + 1:2} " + " ".join(cells))

    def run(self):
        b = self.board

        print(f"\nMinesweeper - {self.difficulty.title()}")
        print(f"Board: {b.rows} x {b.cols} | Mines: {b.mine_total}")
        print("Commands: r row col | f row col | q")

        while True:
            self.display()
            raw = input("> ").strip().lower()

            if raw == "q":
                print("Game ended.")
                return

            parts = raw.split()

            if len(parts) != 3 or parts[0] not in {"r", "f"}:
                print("Invalid command. Use r row col, f row col, or q.")
                continue

            try:
                r, c = int(parts[1]) - 1, int(parts[2]) - 1
            except ValueError:
                print("Invalid coordinates. Row and column must be numbers.")
                continue

            if not b.in_bounds(r, c):
                print("Outside the board. Choose a valid row and column.")
                continue

            pos = (r, c)

            if parts[0] == "f":
                was_flagged = pos in b.flags

                if not b.toggle_flag(pos):
                    print("Cannot flag a revealed cell.")
                elif was_flagged:
                    print(f"Flag removed from ({r + 1}, {c + 1}).")
                else:
                    print(f"Flag placed at ({r + 1}, {c + 1}).")

                continue

            # Reveal action: handle repeated reveals and flagged cells.
            if pos in b.revealed:
                print(f"Cell ({r + 1}, {c + 1}) is already revealed.")
                continue

            if pos in b.flags:
                print(
                    f"Cell ({r + 1}, {c + 1}) is flagged. "
                    "Remove the flag before revealing it."
                )
                continue

            # Count cells before and after the complete reveal operation.
            # Flood fill is internal to Board.reveal(), so feedback is
            # printed only once for the player's command.
            previously_revealed = len(b.revealed)
            hit_mine = b.reveal(pos)
            newly_revealed = len(b.revealed) - previously_revealed

            if hit_mine:
                print(f"Reveal action: {newly_revealed} cell(s) revealed.")
                self.display(reveal_mines=True)
                print("BOOM! You hit a mine.")
                return

            if newly_revealed == 1:
                adjacent = b.adjacent_mines(r, c)
                print(
                    f"Revealed ({r + 1}, {c + 1}). "
                    f"{adjacent} adjacent mine(s)."
                )
            elif newly_revealed > 1:
                print(
                    f"Reveal action complete: {newly_revealed} cells revealed, "
                    "including automatically expanded cells."
                )
            else:
                print("No new cells were revealed.")

            if b.won():
                self.display()
                print("You cleared the board!")
                return
