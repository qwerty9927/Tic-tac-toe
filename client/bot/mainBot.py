from bot.mcts import MonteCarloTreeSearchNode, TicTacToe


class MainBot():
    @staticmethod
    def main(board, opposite):
        game = TicTacToe(board, opposite)
        mcts = MonteCarloTreeSearchNode(game)
        action = mcts.best_action()
        return tuple(int(element) for element in action)
