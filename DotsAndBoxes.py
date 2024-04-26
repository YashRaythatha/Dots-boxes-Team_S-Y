# This Game is developed by Saurabh and Yash
class DotsAndBoxes:
    def __init__(self):
        # these values will describe how to setup rows/cols (currently outdated with testing)
        # there are 5 rows of dots, each with 6 spaces
        self.rowSpaces = 3
        self.rowDots = 4
        # there are 6 columns of dots, each with 4 spaces
        self.colSpaces = 3
        self.colDots = 4

        # rows describe all of the horizontal lines, 0 is empty, 1 is line
        self.rows = []
        self.intializeRows()
        # cols describe all the vertical lines, 0 is empty, 1 is line
        self.cols = []
        self.initializeCols()
        # set of empty spaces, good for random move generation
        self.moves = set()
        self.initializeMoves()

        # True means AI will make the next move, False means Human will make the next move
        self.player = True

        # scores for first and second player
        self.P1Score = 0
        self.P2Score = 0

        # 2D array to aid in drawing
        self.boxes = []
        self.boxesOwners = []  # 2D array to track ownership of boxes
        self.initializeBoxes()

    def intializeRows(self):
        for i in range(self.rowDots):
            col = []
            for j in range(self.rowSpaces):
                col.append(0)
            self.rows.append(col)

    def initializeCols(self):
        for i in range(self.colDots):
            col = []
            for j in range(self.colSpaces):
                col.append(0)
            self.cols.append(col)

    def initializeMoves(self):
        """
        Fill the moves list with all available moves at the start of the game
        No return provided
        """
        # moves for the rows array
        for row in range(self.colDots):
            for col in range(self.colSpaces):
                # 0 indicates this is a horizontal line
                self.moves.add((1, row, col))

        # moves for the col array
        for row in range(self.rowDots):
            for col in range(self.rowSpaces):
                # 1 indicates this is a vertical line
                self.moves.add((0, row, col))

    def initializeBoxes(self):
        # Initialize boxes and box ownership array
        for i in range(self.colSpaces):
            row = []
            rowOwners = []
            for j in range(self.rowSpaces):
                row.append(0)
                rowOwners.append(0)
            self.boxes.append(row)
            self.boxesOwners.append(rowOwners)

    def addLine(self, direction, dotIndex, lineIndex):
        # TODO: add check at the start to make sure given moves are legal to avoid bugs
        # TODO; more rigorous error testing, seems good but I'm not 100% sure things are good
        """
        Add a line to the current board game, remove it from the set, and switch players
        direction: 0 for horizontal line, 1 for vertical line
        dotIndex: if horizontal, the row # the line will be in
        lineIndex: if horizontal, the actual gap the line would be drawn in
        Returns True if a valid move, false otherwise
        """

        if direction == 0:
            # make sure inputs are valid for horizontal pieces
            if dotIndex >= self.rowDots or lineIndex >= self.rowSpaces:
                # print("Invalid move, out of bounds")
                return False
            if self.rows[dotIndex][lineIndex] == 1:
                # print('A line already exists there, try again')
                return False
            self.rows[dotIndex][lineIndex] = 1
            self.moves.remove((0, dotIndex, lineIndex))
        else:
            # make sure moves are valid for vertical pieces
            if dotIndex >= self.colDots or lineIndex >= self.colSpaces:
                # print("Invalid move, out of bounds")
                return False
            if self.cols[dotIndex][lineIndex] == 1:
                # print("A line already exists there, try again")
                return False
            self.cols[dotIndex][lineIndex] = 1
            self.moves.remove((1, dotIndex, lineIndex))
        # after adding line, check if the player got a point and then see if the game is over
        goAgain = self.checkPoint(direction, dotIndex, lineIndex)

        # switch the player
        if not goAgain:
            self.player = not self.player

        return True

    def checkPoint(self, direction, dotIndex, lineIndex):
        """
        Checks if the given move creates a box
        direction: 0 for horizontal line, 1 for vertical line
        dotIndex: if horizontal, the row # the line will be in
        lineIndex: if horizontal, the actual gap the line would be drawn in
        No values returned
        """
        # this will be the value added to player score at the end
        pointEarned = 0
        if direction == 0:
            # check if there is a line above and then see if you can make a box
            if dotIndex > 0:
                if self.rows[dotIndex - 1][lineIndex] and self.cols[lineIndex][dotIndex-1] and self.cols[lineIndex + 1][dotIndex-1]:
                    pointEarned += 1
                    self.boxes[dotIndex - 1][lineIndex] = 1
                    self.boxesOwners[dotIndex -
                                     1][lineIndex] = 1 if self.player else 2
            # check if there is a line bellow and then see if you can make a box
            if dotIndex < self.rowDots - 1:
                if self.rows[dotIndex + 1][lineIndex] and self.cols[lineIndex][dotIndex] and self.cols[lineIndex+1][dotIndex]:
                    pointEarned += 1
                    self.boxes[dotIndex][lineIndex] = 1
                    self.boxesOwners[dotIndex][lineIndex] = 1 if self.player else 2
        else:
            if dotIndex > 0:
                # check if there is a line to the left and then see if you can make a box
                if self.cols[dotIndex - 1][lineIndex] and self.rows[lineIndex][dotIndex-1] and self.rows[lineIndex+1][dotIndex-1]:
                    pointEarned += 1
                    self.boxes[lineIndex][dotIndex - 1] = 1
                    self.boxesOwners[lineIndex][dotIndex -
                                                1] = 1 if self.player else 2

            # check if there is a line to the right and then see if you can make a box
            if dotIndex < self.colDots - 1:
                if self.cols[dotIndex + 1][lineIndex] and self.rows[lineIndex][dotIndex] and self.rows[lineIndex+1][dotIndex]:
                    pointEarned += 1
                    self.boxes[lineIndex][dotIndex] = 1
                    self.boxesOwners[lineIndex][dotIndex] = 1 if self.player else 2

        # add earned points to the correct player
        if self.player:
            self.P1Score += pointEarned
        else:
            self.P2Score += pointEarned

        # if player should go again, return true
        if pointEarned > 0:
            return True
        else:
            return False

    def checkEnd(self):
        """
        Checks to see if the game is over yet.
        Returns True if it is, false otherwise
        """
        if len(self.moves) == 0:
            return True
        else:
            return False

    def printBoard(self):
        """
        Prints the current board state to the console
        Returns nothing
        """
        # print arrays if desired
        # print("row and col")
        # print(self.rows)
        # print(self.cols)
        # show player scores and turn
        if self.player:
            print("Player turn: P1")
        else:
            print("Player turn: P2")
        print("P1 Score:", self.P1Score)
        print("P2 Score:", self.P2Score)
        print("board:")
        for col in range(self.rowDots):
            for row in range(self.colDots):
                # print dots across a row
                print('.', end="")
                if row < self.rowSpaces:
                    # print(row, col)
                    # add horizontal lines where needed
                    if self.rows[col][row] == 0:
                        print(' ', end="")
                    else:
                        print('-', end="")

            print()
            # print vertical lines where needed before next row
            if col < self.colSpaces:
                for row in range(self.colDots):
                    if self.cols[row][col] == 0:
                        print("  ", end="")
                    else:
                        print("| ", end="")
            print()
