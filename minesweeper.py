import itertools
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
        if(len(self.cells) == self.count):
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.cells and self.count == 0):
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if(cell in self.cells):
            self.cells.remove(cell)
            self.count-=1
            #------------------conclusions?

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if(cell in self.cells):
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

        # Set of all cells
        self.all_cells = set([p for p in itertools.product(range(self.height), repeat=2)])

    def find_neighbours(self, cell):
        #returns a set of surrounding cells        
        neighbour_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbour_cells.add((i,j))
        return neighbour_cells

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
        self.moves_made.add(cell)
        self.mark_safe(cell)
        neighbours = self.find_neighbours(cell) 
        new_sentense = Sentence((neighbours - self.mines - self.safes), count - len(self.mines & neighbours))
        if (new_sentense not in self.knowledge):
            self.knowledge.append(new_sentense)
            print(f"last added knowledge {sorted(self.knowledge[-1].cells)} and count = {self.knowledge[-1].count}, now has {len(self.knowledge)} knowledge")
        for s in self.knowledge:
            km = s.known_mines().copy()
            #print(f"km - {km}")
            ks = s.known_safes().copy()
            #print(f"ks - {ks}")
            for mine in km:
                self.mark_mine(mine) 
            for safe in ks:
                self.mark_safe(safe)
            if(not s.cells):
                self.knowledge.remove(s)
                print(f"removed an empty rule {s}, leaved {len(self.knowledge)}")
            for s_sub in self.knowledge:
                if (s_sub.cells and s!=s_sub and s_sub.cells.issubset(s.cells)):
                    print(f"adding {s.cells} - {s_sub.cells} count = {s.count} - {s_sub.count}")
                    new_sentense = Sentence(s.cells - s_sub.cells, s.count - s_sub.count)   
                    print(new_sentense)
                    if (new_sentense not in self.knowledge):
                        self.knowledge.append(new_sentense)
        print(f"mines {sorted(self.mines)}")

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        #print(self.safes - self.moves_made)
        print(sorted(self.mines))
        possible_safe_moves = self.safes - self.moves_made
        if not (possible_safe_moves):
            return None
        psm = (possible_safe_moves).pop()
        print(psm)
        return psm

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        '''all_cells = set()        
        for i in range(self.height):
            for j in range(self.width):
                all_cells.add((i,j))
        print(list(itertools.combinations(range(self.height), 2)))
        cells = [p for p in itertools.product(range(self.height), repeat=2)]
        print(f"product length {len(cells)}")
        print(f'all cells with {len(all_cells)} count {sorted(all_cells)}')'''

        possible_cells = (self.all_cells - self.mines - self.moves_made)
        p = random.choice(tuple(possible_cells)) if possible_cells else print('No more possible moves')
        #p = possible_cells.pop() if possible_cells else print('No more possible moves')
        print(f"randome move {p}")
        return p 
        #return possible_cells.pop() if possible_cells else print('No more possible moves')
 