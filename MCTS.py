import random
import copy
import DBNode
from DBNode import DBNode
import math


def MCTS(tree, currentId, rootId, rollouts):

    random.seed()  # Initialize random number generator
    numOfRollouts = 0

    while numOfRollouts < rollouts:
        currentNode = tree[rootId]
        # Traverse the tree from the root to a leaf node
        while currentNode.children:
            currentNode = tree[ucbSelect(tree, currentNode)]

        # Expand the tree if the game hasn't ended
        if not currentNode.board.checkEnd():
            currentId = expand(tree, currentNode, currentId)

        # Perform a rollout from the current node and backpropagate the result
        if currentNode.children:
            childNode = tree[random.choice(list(currentNode.children))]
            reward = rollout(childNode)
        else:
            reward = evaluateEndGame(currentNode)

        backPropagation(tree, currentNode, reward, rootId)
        numOfRollouts += 1

    return maxChild(tree, tree[rootId]), currentId


def ucbSelect(tree, currentNode):
    """ Selects a child node using the Upper Confidence Bound (UCB) formula. """
    best_value = float('-inf')
    best_node_id = None
    total_visits = sum(
        tree[child_id].visitCount for child_id in currentNode.children)
    C = math.sqrt(2)  # Exploration parameter

    for child_id in currentNode.children:
        child = tree[child_id]
        if child.visitCount == 0:
            return child_id  # Always explore unvisited nodes first

        # Calculate the UCB1 value
        exploit = child.reward / child.visitCount
        explore = C * math.sqrt(math.log(total_visits) / child.visitCount)
        ucb_value = exploit + explore

        if ucb_value > best_value:
            best_value = ucb_value
            best_node_id = child_id

    return best_node_id


def expand(tree, currentNode, currentId):
    """ Expands the tree by adding all possible moves from the current node. """
    for move in currentNode.board.moves:
        new_board = copy.deepcopy(currentNode.board)
        new_board.addLine(*move)
        newNode = DBNode(new_board, currentId, currentNode.id, move)
        tree[currentId] = newNode
        currentNode.addChild(currentId)
        currentId += 1
    return currentId


def rollout(node):
    """ Simulates a random play to the end of the game from the node. """
    tempNode = copy.deepcopy(node)
    while not tempNode.board.checkEnd():
        move = random.choice(list(tempNode.board.moves))
        tempNode.board.addLine(*move)
    return evaluateEndGame(tempNode)


def evaluateEndGame(node):
    """ Evaluates the game outcome from the node's perspective. """
    if node.board.P1Score > node.board.P2Score:
        return 1
    else:
        return -1


def backPropagation(tree, node, reward, rootId):
    """ Propagates the simulation results back up the tree. """
    while node.id != rootId:
        node.visitCount += 1
        node.reward += reward
        node = tree[node.parent]


def maxChild(tree, rootNode):
    """ Returns the ID of the child with the highest win ratio. """
    best_value = float('-inf')
    best_id = None
    for child_id in rootNode.children:
        child = tree[child_id]
        win_ratio = child.reward / child.visitCount
        if win_ratio > best_value:
            best_value = win_ratio
            best_id = child_id
    return best_id
