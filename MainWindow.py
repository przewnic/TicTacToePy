""" Simple TicTacToe game. """

from PyQt5 import QtWidgets
from PyQt5 import uic
from random import randint


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        """  Initialize Window and game's logic. """
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('main.ui', self)
        self.setWindowTitle("TicTacToe")
        self.buttons = [self.x1, self.x2, self.x3,
                        self.x4, self.x5, self.x6,
                        self.x7, self.x8, self.x9]
        self.clear_buttons()
        self.restart.clicked.connect(self.on_restart)
        self.mode.stateChanged.connect(self.on_mode)
        self.player_1 = "X"
        self.player_2 = "O"
        self.fields = [
                    None, None, None,
                    None, None, None,
                    None, None, None]
        self.x1.clicked.connect(lambda: self.on_button(0))
        self.x2.clicked.connect(lambda: self.on_button(1))
        self.x3.clicked.connect(lambda: self.on_button(2))
        self.x4.clicked.connect(lambda: self.on_button(3))
        self.x5.clicked.connect(lambda: self.on_button(4))
        self.x6.clicked.connect(lambda: self.on_button(5))
        self.x7.clicked.connect(lambda: self.on_button(6))
        self.x8.clicked.connect(lambda: self.on_button(7))
        self.x9.clicked.connect(lambda: self.on_button(8))
        self.turn = True
        self.stop_game = False  # Set to True when one player wins
        self.on_mode()  # Two player if checked
        self.show()

    def on_mode(self):
        """
            Choosing between single player and two player mode.
            If checked - two player mode
            If not checked - one player mode
        """
        self.chosen_mode = self.mode.isChecked()

    def clear_buttons(self):
        """ Sets button labels to ''. """
        for button in self.buttons:
            button.setText("")
            button.setStyleSheet('background-color: none')

    def clear_fields(self):
        """ Sets fileds to None. """
        for i, _ in enumerate(self.fields):
            self.fields[i] = None

    def on_restart(self):
        """ Clears fields and labels. """
        self.turn = True
        self.clear_buttons()
        self.clear_fields()
        self.winner.setText("Winner: ")
        self.stop_game = False

    def set_winner(self, i, j, k):
        """" Setting winer. """
        if i == -1:
            winner = "Draw"
            for button in self.buttons:
                button.setStyleSheet('background-color: lightblue')
        else:
            winner = self.fields[i]
            for index in (i, j, k):
                self.buttons[index].setStyleSheet('background-color: green')
        self.winner.setText("Winner: " + winner)
        self.stop_game = True

    def on_button(self, i):
        """ Handler of clicking on a game button. """
        # Game ended
        if self.stop_game:
            return
        # Cliked the same button again
        if self.fields[i]:
            return
        # Set button label depending on turn
        if self.turn:
            self.set_field(i, self.player_1)
        else:
            self.set_field(i, self.player_2)

        self.turn = not self.turn
        win, index = self.check_win(self.fields)
        if win:
            self.set_winner(*index)
            return
        if not self.chosen_mode:
            self.best_move()

    def set_field(self, index, player):
        """ Sets value in game logic list and sets button label. """
        self.fields[index] = player
        self.buttons[index].setText(player)

    def random_move(self):
        """ Random oponent - chooses random empty field to put the mark on. """
        if not all(self.fields):
            empty_fields = [i for i, f in enumerate(self.fields) if f is None]
            empty_index = randint(0, len(empty_fields)-1)
            field_index = empty_fields[empty_index]
            self.set_field(field_index, self.player_2)
            win, index = self.check_win(self.fields)
            if win:
                self.set_winner(*index)
            self.turn = not self.turn

    def best_move(self):
        if not all(self.fields):
            _best = None
            _best_value = 10
            for move, _ in enumerate(self.fields):
                if _ is not None:
                    continue
                board = self.fields
                board[move] = self.player_2
                counted_value = self.minmax(board, 0, True)
                board[move] = None
                if counted_value < _best_value:
                    _best = move
                    _best_value = counted_value
                if counted_value == 0:
                    _best = move
                    break

            self.set_field(_best, self.player_2)
            win, index = self.check_win(self.fields)
            if win:
                self.set_winner(*index)
            self.turn = not self.turn

    def minmax(self, board, depth, max_player):
        win, index = self.check_win(board)
        if win:
            if index[0] == -1:
                return 0
            elif board[index[0]] == self.player_1:
                return 1
            else:
                return -1

        if max_player:
            best_value = -10
            for move, _ in enumerate(board):
                if _ is not None:
                    continue
                board[move] = self.player_1
                value = self.minmax(board, depth+1, False)
                best_value = max(best_value, value)
                board[move] = None
        else:
            best_value = 10
            for move, _ in enumerate(board):
                if _ is not None:
                    continue
                board[move] = self.player_2
                value = self.minmax(board, depth+1, True)
                best_value = min(best_value, value)
                board[move] = None
        return value

    def check_win(self, board):
        """ Check if any player won the game. """
        for i in range(3):
            k = i*3
            # Check horizontal lines
            if all(board[k:k+3]):
                if board[k] == board[k+1] == board[k+2]:
                    return True, (k, k+1, k+2)
            # Check vertical lines
            if all([board[i], board[i+3], board[i+6]]):
                if board[i] == board[i+3] == board[i+6]:
                    return True, (i, i+3, i+6)
        # Check diagonals
        if all([board[0], board[4], board[8]]):
            if board[0] == board[4] == board[8]:
                return True, (0, 4, 8)
        if all([board[2], board[4], board[6]]):
            if board[2] == board[4] == board[6]:
                return True, (2, 4, 6)
        # Check if draw
        if all(board):
            return True, (-1, -1, -1)
        return False, ()
