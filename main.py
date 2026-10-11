
from game import Minesweeper


def select_difficulty():
    while True:
        print("\nSelect difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        choice = input("Enter difficulty (Easy/Medium/Hard): ").strip().lower()

        difficulty_options = {
            "1": "easy",
            "2": "medium",
            "3": "hard",
            "easy": "easy",
            "medium": "medium",
            "hard": "hard",
        }

        if choice in difficulty_options:
            return difficulty_options[choice]

        print("Invalid difficulty. Please choose Easy, Medium, or Hard.")


def main():
    difficulty = select_difficulty()
    game = Minesweeper(difficulty)
    game.run()


if __name__ == "__main__":
    main()
