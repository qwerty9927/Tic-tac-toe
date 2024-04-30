import numpy as np
import time
from collections import defaultdict


class TicTacToe:
    def __init__(self, board, player):
        self.board_size = 3
        self.win_length = 3
        self.board = board
        self.current_player = player  # Player 1 starts
        self.winner = None
        self.current_action = None

    def get_legal_actions(self):
        return list(zip(*np.where(self.board == 0)))

    def switch_player(self):
        return 3 - self.current_player

    def is_game_over(self):
        return self.winner is not None or np.all(self.board != 0)

    def move(self, action, board):
        new_state = TicTacToe(board, self.switch_player())
        new_state.board[action] = new_state.current_player
        new_state.winner = new_state.check_winner()
        new_state.current_action = action
        return new_state

    def check_winner(self):
        board = self.board

        # Check rows
        for row in board:
            if len(set(row)) == 1 and row[0] != 0:
                return row[0]

        # Check columns
        for col in range(self.board_size):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != 0:
                return board[0][col]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
            return board[0][2]

        # If no winner yet
        return None

    def game_result(self, root):
        if self.winner is not None:
            return 1 if self.winner == root.state.current_player else -1
        return 0


class MonteCarloTreeSearchNode:
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def best_action(self):
        playout = 0
        count = 0
        time0 = time.time()
        while time.time() - time0 <= 2:
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
            playout += 1
            count += 1
        print("Playout: ", playout)
        result = self.best_child(np.sqrt(2))
        return result.parent_action

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child(np.sqrt(2))
        return current_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.move(action, self.state.board.copy())
        child_node = MonteCarloTreeSearchNode(
            next_state, parent=self, parent_action=action)
        self.children.append(child_node)
        return child_node

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def best_child(self, c_param=1.41):
        choices_weights = [(c.q() / c.n()) + c_param *
                           np.sqrt((np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout(self):
        rollout_state = TicTacToe(
            self.state.board.copy(), self.state.current_player)
        while not rollout_state.is_game_over():
            possible_moves = rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            rollout_state = rollout_state.move(
                action, rollout_state.board.copy())
        return rollout_state.game_result(self)

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(-result)
