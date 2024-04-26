# This Game is developed by Saurabh and Yash
import DotsAndBoxes


"""
inputGame: a DotsAndBoxes game for the current state
myId: a unique number to represent this board state
parentId: the unique ID of the parent state
move: a tuple for the move that transitioned the parent state to this one
"""


class DBNode:
    def __init__(self, inputGame, myId, parentId, move):
        # the player will be found within inputGame
        self.board = inputGame
        self.id = myId
        self.parent = parentId
        self.newMove = move

        # children is a set of all the children IDs of this node
        self.children = set()

        # values used in the MCTS process
        self.visitCount = 1
        self.reward = 0

    def addChild(self, child):
        self.children.add(child)
