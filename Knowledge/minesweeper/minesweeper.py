import itertools as it
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If length of cells equals no. of mines, then each cell must be a mine
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) Add cell to known moves
        self.moves_made.add(cell)
        # 2) Add cell to known safe ones, and update knowledge accordingly
        self.mark_safe(cell)
        # 3) Need to find all adjacent cells to the current cell
        new_sentence_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue

                neighbouring_cell = (i, j)
                # Need to ensure this cell is not out of bounds
                if i < 0 or self.height <= i or j < 0 or self.width < j:
                    continue
                # If the neighbouring cell is known to be safe, skip
                if neighbouring_cell in self.safes:
                    continue
                # If the neighbouring cell is known to be a mine, skip
                if neighbouring_cell in self.mines:
                    count -= 1
                    continue
                # Add remaining cells into temp holder sentence
                new_sentence_cells.add(neighbouring_cell)

        # Now we can actually add a new sentence to our knowledge base
        self.knowledge.append(Sentence(new_sentence_cells, count))

        # 4) Based off this new knowledge, update any known cells that are safe as safe
        sentence_safes_all = set()
        sentence_mines_all = set()
        for sentence in self.knowledge:
            sentence_safes_all |= sentence.known_safes()
            sentence_mines_all |= sentence.known_mines()

        knowledge_change = True
        empty_sentence = Sentence(set(), 0)
        while knowledge_change:
            knowledge_change = False
            if sentence_safes_all:
                for safe in sentence_safes_all:
                    self.mark_safe(safe)
                knowledge_change = True
            if sentence_mines_all:
                for mine in sentence_mines_all:
                    self.mark_mine(mine)
                knowledge_change = True

            self.knowledge = [sentence for sentence in self.knowledge if sentence != empty_sentence]

            for [sentence1, sentence2] in it.permutations(self.knowledge, 2):
                new_inferred_sentence = None
                if sentence1.cells.issubset(sentence2.cells):
                    new_inferred_sentence = Sentence(
                        sentence2.cells - sentence1.cells,
                        sentence2.count - sentence1.count
                    )
                elif sentence2.cells.issubset(sentence1.cells):
                    new_inferred_sentence = Sentence(
                        sentence1.cells - sentence2.cells,
                        sentence1.count - sentence2.count
                    )

                if new_inferred_sentence and new_inferred_sentence.cells not in self.knowledge:
                    self.knowledge.append(new_inferred_sentence)
                    knowledge_change = True

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = list(self.safes - self.moves_made)
        if len(safe_moves) == 0:
            return None

        return random.choice(safe_moves)

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        