import math
import random

class TreeNode():
    def __init__(self, board, parent):
        self.board = board
        if self.board.is_win() or self.board.is_draw():
            self.is_terminal = True
        else:
            self.is_terminal = False
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = {}

class MCTS():
    def search(self, initial_state):
        '''
        Create root node from where search begins
        For 1000 times do selection-expansion-simulation-backpropagation
        Select best child option after iteration
        return the best child
        '''

        self.root = TreeNode(initial_state, None)
        for _ in range(1000):
            node = self.select_node(self.root)
            score = self.rollout(node.board)                                         #type:ignore
            self.backpropagate(node, score)
        # pick up the best move in the current position
        try:
            return self.get_best_child(self.root, 0)
        
        except:
            pass

    def select_node(self, node):
        '''
        if the node is fully expanded
            return the best_child node with best ucb1 value
        else 
            add children to that node and return that new children
        '''
        while not node.is_terminal :                                                #type:ignore  
            if node.is_fully_expanded:                                              #type:ignore
                node = self.get_best_child(node, 2)
            else:
                return self.expand(node)
        return node


    def expand(self, node):
        '''
        Get list of possible states of the board
        if a possible state is not present in child node, add it and return it for selection
        Everytime check if a node is fully expanded and update the flag
        '''
        states = node.board.generate_states()
        for board in states:
            if str(board.position) not in node.children:
                new_node = TreeNode(board,node)
                node.children[str(board.position)] = new_node

                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                return new_node
        
    # simulate random game untill end of that game
    def rollout(self, board):
        '''
        keep iterating while the board state is not of win
        make a random choice among the possible board state and update the board
        random choice will raise expection if its argument is empty i.e. draw condition
        '''
        while not board.is_win():
            try:
                board = random.choice(board.generate_states())
            except:
                return 0 #draw condition
        if board.player_2 == 'x':
            return 1
        return -1

    # backpropagate score and no. of visits to root node
    def backpropagate(self, node, score):
        '''
        keep updating the no of visits and score untill, we reach root node
        '''
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent

    # select best node basing on UCB1 formula
    def get_best_child(self, node, exploration_constant):
        '''
        loop over each board state and calc ucb1 formula
        based on ucb1 formula get best children node
        if multiple then make random choice to choose one
        '''
        best_score = float('-inf')
        best_nodes = []
        current_player = 0 
        
        # loop over child nodes
        for child_node in node.children.values():

            if child_node.board.player_2 == 'x': current_player = 1
            elif child_node.board.player_2 == 'o': current_player = -1
            
            # get move score using UCT formula
            move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))                                        

            # better move has been found
            if move_score > best_score:
                best_score = move_score
                best_nodes = [child_node]
            
            # found as good move as already available
            elif move_score == best_score:
                best_nodes.append(child_node)
            
        # return one of the best moves randomly
        return random.choice(best_nodes)
