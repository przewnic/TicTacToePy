""" Simple TicTacToe game. """

import sys
from PyQt5 import QtWidgets
from MainWindow import MainWindow


def main():
    """ Start the game."""
    app = QtWidgets.QApplication(sys.argv)
    MainWindow()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
