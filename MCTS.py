# This Game is developed by Saurabh and Yash
import DotsAndBoxes
import DBNode
import random
import math
import copy

"""
Driver of the MCTS algorithm
tree: dictionary with IDs as keys and their respective nodes as the value
currentId: the next ID value to be used in children creation
rootId: ID of the root for this search
rollouts: number of rollouts to be performed
Returns the ID of the next move the AI will choose AND the value for currentId
"""


def MCTS(tree, currentId, rootId, rollouts):
    # generate random seed for simulations
    random.seed()

    # tests
    wlf = [0, 0, 0]

    # get the root of the tree and increment ID counter
    root = tree[rootId]

    # total moves to decide how to traverse the tree
    totalNodes = float(len(root.board.moves))

    # this is the node referenced when traversing the tree
    currentNode = root

    # this will keep track of how many rollouts have been completed
    numOfRollouts = 0
    while numOfRollouts < rollouts:
        # start currentNode at the root
        currentNode = tree[root.id]

        # traverse to the end of the tree based on UCT
        while len(currentNode.children) != 0:
            nextNodeId = randomSelect(tree, currentNode)
            currentNode = tree[nextNodeId]

        # first check if a node should have neighbours and if it does, then add them to children
        if not currentNode.board.checkEnd():
            # note that currentId is updated at the end
            currentId = expand(tree, currentNode, currentId)

        # if no children were found, then backpropogate this value
        if len(currentNode.children) == 0:
            # the value that will be back propogated
            reward = 0

            # this will be the reward at the end of the tree
            if currentNode.board.P1Score - currentNode.board.P2Score > 0:
                reward = 0.0
            else:
                reward = -1.0 * 1.8 ** currentNode.board.P2Score

            # back propogate the value up the tree
            backPropogation(tree, currentNode, reward, rootId)
        # if children were found then begin a rollout from a random position
        else:
            randChild = random.choice(tuple(currentNode.children))
            currentNode = tree[randChild]

            # perform a rollout on the child and collect the reward
            reward = rollout(currentNode, wlf)

            # back propogate the value up the tree
            backPropogation(tree, currentNode, reward, rootId)
        numOfRollouts += 1

    # find the best child of the root node and return the id
    bestNodeId = maxChild(tree, root)
    return bestNodeId, currentId


"""
Randomly selects a child during the selection phase
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
Returns random child Id
"""


def randomSelect(tree, currentNode):
    randomId = random.sample(currentNode.children, 1)
    return randomId[0]


"""
Expands the tree by adding all of the children of some node
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
currentId: the ID value that should be used to start assigning values to the children
Returns the new value for currentId
"""


def expand(tree, currentNode, currentId):
    tempNode = copy.deepcopy(currentNode)
    parentId = copy.deepcopy(currentNode.id)
    # create a child for each available node in the game's available moves
    for move in tempNode.board.moves:
        # create a game with the new move
        tempGame = copy.deepcopy(currentNode.board)
        (direction, dotInd, lineInd) = move
        tempGame.addLine(direction, dotInd, lineInd)

        # create this new state in the tree and add it as a child to the current node
        tree[currentId] = DBNode.DBNode(
            tempGame, currentId, parentId, move)
        tree[parentId].addChild(currentId)

        # increment the ID
        currentId += 1
    return currentId


"""
Will play out one full game of dots and boxes randomly
currentNode: the current piece being investigated
Returns a reward for the game
"""


def rollout(currentNode, wlf):
    # node that will be used for simulation
    tempNode = copy.deepcopy(currentNode)
    # will make values much worse if there is a mess up close to the start
    badMove = 1.0
    badSeen = False
    # if this is a losing branch, then make it known
    losingBranch = 0.0
    if currentNode.board.P1Score < currentNode.board.P2Score:
        losingBranch = 15.0 ** (currentNode.board.P2Score -
                                currentNode.board.P1Score)
    while tempNode.board.P1Score < 5 and tempNode.board.P2Score < 5:
        # select a random move available in the game
        play = random.choice(tuple(tempNode.board.moves))
        (direction, dotInd, lineInd) = play
        # this will return True if the game is done
        tempNode.board.addLine(direction, dotInd, lineInd)
        if currentNode.board.P2Score > currentNode.board.P2Score and not badSeen:
            badSeen = True
            badMove = -10000.0 / float(len(currentNode.board.moves) -
                                       len(tempNode.board.moves))

    if (tempNode.board.P1Score > tempNode.board.P2Score):
        return 3.0
    else:
        return -1.0 * len(tempNode.board.moves) + badMove - losingBranch


"""
Back propogates return from simulated game up the tree
tree: dictionary with IDs as keys and their respectives nodes as the values
currentNode: the ID of the current node
reward: the reward found from the rollout at currentNode
rootId: the ID of the root node in this simulation
No return
"""


def backPropogation(tree, currentNode, reward, rootId):
    # determine if AI is p1 or p2
    aiPlayer = tree[rootId].board.player
    # traverse back up the tree
    while currentNode.id != rootId:
        tree[currentNode.id].visitCount += 1
        tree[currentNode.id].reward += float(reward)

        # set the current node to the parent
        currentNode = tree[currentNode.parent]

    # update the root's visit and reward values too
    tree[rootId].visitCount += 1
    tree[rootId].reward += reward


"""
Finds the best move to play at the end of the simulation
tree: dictionary with IDs as keys and their respectives nodes as the values
root: the root node for this simulation
Returns the ID of the next most promising game state
"""


def maxChild(tree, currentNode):
    # values for the max win score and the node's ID
    maxValue = float('-inf')
    maxId = 0

    # print("total children:", len(currentNode.children))

    for child in currentNode.children:
        tempNode = tree[child]
        # best node has the greatest reward compared to visit count
        winValue = float(tempNode.reward) / float(tempNode.visitCount)
        # uncomment bellow lines to get diagnostics for each child of current node
        # print("Child", tree[child].newMove, "visits",
        #       tree[child].visitCount, "reward:", tree[child].reward, "win value:", winValue)

        if winValue > maxValue:
            maxValue = winValue
            maxId = child

    return maxId
