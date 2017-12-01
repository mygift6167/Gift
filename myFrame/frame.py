# -*- coding: utf-8 -*-
import numpy as np
import pieces
import os


class Dummy:
    pass


class Board:
    def __init__(self):
        self.layout = np.ndarray(shape=(10, 9), dtype=object)
        self.encode_layout = np.ndarray(shape=(10, 9), dtype=int)
        self.record, self.count_60 = [], 0
        self.black, self.red = Dummy(), Dummy()

        self.black.layout = self.layout       # 黑方视角
        self.red.layout = np.rot90(self.black.layout, k=2)      # 红方视角

        self.black.general = pieces.General((4, 0), 'B', self, 'black_general')
        self.black.advisor_L = pieces.Advisor((3, 0), 'B', self, 'black_advisor_L')
        self.black.advisor_R = pieces.Advisor((5, 0), 'B', self, 'black_advisor_R')
        self.black.elephant_L = pieces.Elephant((2, 0), 'B', self, 'black_elephant_L')
        self.black.elephant_R = pieces.Elephant((6, 0), 'B', self, 'black_elephant_R')
        self.black.horse_L = pieces.Horse((1, 0), 'B', self, 'black_horse_L')
        self.black.horse_R = pieces.Horse((7, 0), 'B', self, 'black_horse_R')
        self.black.chariot_L = pieces.Chariot((0, 0), 'B', self, 'black_chariot_L')
        self.black.chariot_R = pieces.Chariot((8, 0), 'B', self, 'black_chariot_R')
        self.black.cannon_L = pieces.Cannon((1, 2), 'B', self, 'black_cannon_L')
        self.black.cannon_R = pieces.Cannon((7, 2), 'B', self, 'black_cannon_R')
        self.black.soldier_0 = pieces.Soldier((0, 3), 'B', self, 'black_soldier_0')
        self.black.soldier_1 = pieces.Soldier((2, 3), 'B', self, 'black_soldier_1')
        self.black.soldier_2 = pieces.Soldier((4, 3), 'B', self, 'black_soldier_2')
        self.black.soldier_3 = pieces.Soldier((6, 3), 'B', self, 'black_soldier_3')
        self.black.soldier_4 = pieces.Soldier((8, 3), 'B', self, 'black_soldier_4')

        # 注意 红方的左右与 黑方（棋盘方向）是相反的
        self.red.general = pieces.General((4, 9), 'R', self, 'red_general')
        self.red.advisor_L = pieces.Advisor((5, 9), 'R', self, 'red_advisor_L')
        self.red.advisor_R = pieces.Advisor((3, 9), 'R', self, 'red_advisor_R')
        self.red.elephant_L = pieces.Elephant((6, 9), 'R', self, 'red_elephant_L')
        self.red.elephant_R = pieces.Elephant((2, 9), 'R', self, 'red_elephant_R')
        self.red.horse_L = pieces.Horse((7, 9), 'R', self, 'red_horse_L')
        self.red.horse_R = pieces.Horse((1, 9), 'R', self, 'red_horse_R')
        self.red.chariot_L = pieces.Chariot((8, 9), 'R', self, 'red_chariot_L')
        self.red.chariot_R = pieces.Chariot((0, 9), 'R', self, 'red_chariot_R')
        self.red.cannon_L = pieces.Cannon((7, 7), 'R', self, 'red_cannon_L')
        self.red.cannon_R = pieces.Cannon((1, 7), 'R', self, 'red_cannon_R')
        self.red.soldier_0 = pieces.Soldier((8, 6), 'R', self, 'red_soldier_0')
        self.red.soldier_1 = pieces.Soldier((6, 6), 'R', self, 'red_soldier_1')
        self.red.soldier_2 = pieces.Soldier((4, 6), 'R', self, 'red_soldier_2')
        self.red.soldier_3 = pieces.Soldier((2, 6), 'R', self, 'red_soldier_3')
        self.red.soldier_4 = pieces.Soldier((0, 6), 'R', self, 'red_soldier_4')

        self.pieces_dict = {'B': {'G': self.black.general,
                             'A': {'L': self.black.advisor_L, 'R': self.black.advisor_R},
                             'E': {'L': self.black.elephant_L, 'R': self.black.elephant_R},
                             'H': {'L': self.black.horse_L, 'R': self.black.horse_R},
                             'R': {'L': self.black.chariot_L, 'R': self.black.chariot_R},
                             'C': {'L': self.black.cannon_L, 'R': self.black.cannon_R},
                             'S': [self.black.soldier_0, self.black.soldier_1, self.black.soldier_2,
                                   self.black.soldier_3, self.black.soldier_4, ]},
                            'R': {'G': self.red.general,
                             'A': {'L': self.red.advisor_L, 'R': self.red.advisor_R},
                             'E': {'L': self.red.elephant_L, 'R': self.red.elephant_R},
                             'H': {'L': self.red.horse_L, 'R': self.red.horse_R},
                             'R': {'L': self.red.chariot_L, 'R': self.red.chariot_R},
                             'C': {'L': self.red.cannon_L, 'R': self.red.cannon_R},
                             'S': [self.red.soldier_0, self.red.soldier_1, self.red.soldier_2,
                                   self.red.soldier_3, self.red.soldier_4, ]}
                            }
        self.pieces_list = [self.black.general, self.black.advisor_L, self.black.advisor_R,
                            self.black.elephant_L, self.black.elephant_R, self.black.horse_L, self.black.horse_R,
                            self.black.chariot_L, self.black.chariot_R, self.black.cannon_L, self.black.cannon_R,
                            self.black.soldier_0, self.black.soldier_1, self.black.soldier_2,
                            self.black.soldier_3, self.black.soldier_4,
                            self.red.general, self.red.advisor_L, self.red.advisor_R,
                            self.red.elephant_L, self.red.elephant_R, self.red.horse_L, self.red.horse_R,
                            self.red.chariot_L, self.red.chariot_R, self.red.cannon_L, self.red.cannon_R,
                            self.red.soldier_0, self.red.soldier_1, self.red.soldier_2,
                            self.red.soldier_3, self.red.soldier_4]
        for piece in self.pieces_list:
            x, y = piece.location
            self.layout[y, x] = piece

    def reset(self):
        self.__init__()

    def training_move(self, action, color, return_capture_=False):  # GUI 文件调用时需要获得capture返回值
        if color != 'B' and color != 'R':
            raise UserWarning('''Error in training_move, got a wrong 'color' input''')
        r_dict = {'Draw': 0, 'B': 10, 'R': 10, 'capture': 1, 'block': -6}
        x, y = int(action / 90) % 9, int((action / 90)/9)
        x_, y_ = action % 90 % 9, int((action % 90)/9)
        done, winner, reward = False, None, 0
        error_num, capture = self.move((x_, y_), color=color, from_=(x, y))
        observation_ = self.encode_board(color)
        if error_num is None:
            winner = self.check_winner()
            if winner:
                if winner == 'Draw':
                    done, reward = True, r_dict[winner]
                elif winner == color and capture:
                # elif winner == color:
                    done, reward = True, r_dict[winner]
                else:
                    print(self.board_print(color))
                    with open('error.txt', 'a') as file:
                        file.write('\n\n{}     {}\n'.format(action, color))
                        file.write('\n{}\n'.format(self.board_print(color)))
                    raise UserWarning('Error in training_move, got {} and {} and {}!!!'.format(winner,
                                                                                               color, capture))
                return error_num, done, reward, observation_
            if capture:
                reward = r_dict['capture']
        else:
            reward = r_dict['block']
        if return_capture_ is False:
            return error_num, done, reward, observation_
        else:
            return error_num, done, reward, observation_, capture

    def move(self, destination, color, piece=None, from_=None):
        if color != 'B' and color != 'R':
            raise UserWarning('''Error in move, got a wrong 'color' input''')
        error_num = 0            # 1: 输入的起始坐标没有棋子； 2: 起始坐标指向对方棋子； 3: 目标坐标指向己方棋子；4:移动非法
        capture = False
        if piece or destination:
            loc = piece.location if piece else from_
            x, y = loc
            if not piece:
                piece = self.layout[y, x]
            if piece:
                if piece.color == color:
                    # 判断目标坐标是否有棋子：
                    destination_ = self.layout[destination[1], destination[0]]
                    if destination_:
                        if destination_.color == color:
                            error_num = 3
                            return error_num, capture
                        else:
                            capture = True
                    if not piece.blocking(destination):
                        self.count_60 += 1
                        if capture:
                            destination_.captured()
                            self.count_60 = 0
                        self.layout[destination[1], destination[0]], self.layout[y, x] = self.layout[y, x], None
                        piece.location = destination
                        error_num = None
                    else:
                        error_num = 4
                else:
                    error_num = 2
            else:
                error_num = 1
        return error_num, capture

    def find_piece(self, location, color='B'):
        if color != 'B' and color != 'R':
            raise UserWarning('''Error in find_piece, got a wrong 'color' input''')
        if color == 'B':
            piece = self.layout[location[1], location[0]]
            if piece:
                return piece
        elif color == 'R':
            piece = self.red.layout[location[1], location[0]]
            if piece:
                return piece

    @staticmethod
    def red_action(action):
        return 89*89 - action

    def check_winner(self):
        self.record.append(self.layout.copy())
        if len(self.record) > 6:
            self.record.pop(0)
            if np.array_equal(self.record[0], self.record[2]) and np.array_equal(self.record[2], self.record[4]):
                if np.array_equal(self.record[1], self.record[3]) and np.array_equal(self.record[3], self.record[5]):
                    return 'Draw'
        if self.count_60 >= 60:
            return 'Draw'
        if not self.black.general.survival:
            return 'R'
        elif not self.red.general.survival:
            return 'B'

    def encode_board(self, color='B'):
        if color != 'B' and color != 'R':
            raise UserWarning('''Error in encode_board, got a wrong 'color' input''')
        self.encode_layout.fill(0)
        competitor = 'R' if color == 'B' else 'B'
        for piece in self.pieces_list:
            if piece.survival:
                x, y = piece.location
                if piece.color == color:
                    self.encode_layout[y][x] = piece.index
                elif piece.color == competitor:
                    self.encode_layout[y][x] = -piece.index
        # return self.encode_layout.flatten().tolist()
        return self.encode_layout.flatten()

    def board_print(self, color='B'):
        if color != 'B' and color != 'R':
            raise UserWarning('''Error in board_print, got a wrong 'color' input''')
        print_data = self.layout[-1::-1, :] if color == 'B' else self.red.layout[-1::-1, :]
        print_str = ''

        # 注意行在前 列在后
        for y in print_data:
            print_str += '\n\t[  '
            for x in y:
                tab = '\t'
                if not x:
                    x, tab = ' 0 ', '\t'
                else:
                    x = x.symbol
                print_str += x + tab
            print_str += ' ]'
        return print_str


if __name__ == '__main__':
    board = Board()
    print(board.board_print())
    board.move((4,1),piece=board.black.general, color='B')
    board.move((4,2),piece=board.black.cannon_R, color='B')
    print(board.board_print())
    print(board.encode_board())
