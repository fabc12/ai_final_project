from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from game_engine import GameEngine
import numpy as np


class Frame(QWidget):
    is_computer_turn = False
    is_first_move = True
    is_ended = False
    engine = None
    buttons = [[None for _ in range(3)] for _ in range(3)]
    game_label = None

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 700)
        self.setWindowTitle('Tic Toc Toe')
        self.center()

        layout = QGridLayout()

        # start_btn = QPushButton(self)
        # start_btn.setText("start")
        # start_btn.setGeometry(140, 100, 100, 50)
        #
        # reset_btn = QPushButton(self)
        # reset_btn.setText("reset")
        # reset_btn.setGeometry(260, 100, 100, 50)

        icon = QIcon()
        icon.addPixmap(QPixmap('normal.png'), )
        icon.addPixmap(QPixmap('disabled.png'), QIcon.Disabled)
        icon.addPixmap(QPixmap('clicking.png'), QIcon.Active)

        for i in range(3):
            for j in range(3):
                button = self.buttons[i][j] = QPushButton()
                button.setFixedSize(50, 50)
                button.setIcon(QIcon('square.png'))
                button.setIconSize(QSize(50, 50))
                button.clicked.connect(lambda _, c=i, g=j: self.button_click(c, g))
                layout.addWidget(button, i, j)
                layout.setSpacing(0)

        layout.setContentsMargins(100, 200, 100, 200)
        self.setLayout(layout)
        label = self.game_label = QLabel(self)
        label.setGeometry(200, 550, 100, 100)
        label.setStyleSheet('''' font-size: 24px; ''')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def button_click(self, x: int, y: int):
        if not self.is_ended:
            if not self.is_computer_turn:
                self.sender().setIcon(QIcon('circle.png'))
                self.is_computer_turn = not self.is_computer_turn
                if self.is_first_move:
                    self.engine = GameEngine(x, y)
                    self.is_first_move = False
                self.engine.make_human_move(x, y)
                board_value = self.engine.calculate_value(self.engine.game_board)
                if board_value != -2:
                    self.end_game(board_value)
                next_x, next_y = self.engine.next_move()
                self.engine.make_computer_move(next_x, next_y)
                self.buttons[next_x][next_y].setIcon(QIcon('cross.png'))
                board_value = self.engine.calculate_value(self.engine.game_board)
                if board_value != -2:
                    self.end_game(board_value)
                self.is_computer_turn = False

    def end_game(self, value):
        if value == 1:
            self.game_label.setText('Computer won')
        elif value == -1:
            self.game_label.setText('you won')
        elif value == 0:
            self.game_label.setText("It's draw")
        self.is_ended = True


def main():
    app = QApplication(sys.argv)
    ex = Frame()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
