# -*- coding: utf-8 -*-


class Piece:
    __Symbol = ''

    def __init__(self, location, color, board, name):
        if color != 'B' and color != 'R':
            raise UserWarning('''Error in Piece.__init__, got a wrong 'color' input''')
        self.location = location
        self.color = color
        self.symbol = color + self.__Symbol
        self.survival = True
        self.board = board
        self.name = name

    def blocking(self, destination):
        return False

    @staticmethod
    def in_board(loc):
        x, y = loc
        if 0 <= x <= 8 and 0 <= y <= 9:
            return True

    def captured(self):
        self.survival = False
        # return self.board.pieces_list.remove(self)


class General(Piece):
    __Symbol = '_G'

    def __init__(self, location, color, board, name):
        super().__init__(location, color, board, name)
        self.symbol = color + self.__Symbol
        self.index = 1

    def blocking(self, destination):
        x_, y_ = destination
        x, y = self.location
        if self.in_board(destination):
            if 3 <= x_ <= 5 and (y_ <= 2 or y_ >= 7):
                if (abs(x_-x) == 1 and abs(y_-y) == 0) or (abs(x_-x) == 0 and abs(y_-y) == 1):
                    find_loc = (x, 9) if self.color == 'B' else (x, 0)
                    find_piece = self.board.find_piece(find_loc)                # 判断是否会使 帅与将在同一直线上直接对面
                    if find_piece:
                        if find_piece.index == 1 and find_piece.color != self.color:
                            find_piece = [self.board.find_piece((x, y__)) for y__ in range(1, 9)]
                            if not any(find_piece):
                                return True
                    return False
        return True


class Advisor(Piece):
    __Symbol = '_A'

    def __init__(self, location, color, board, name):
        super().__init__(location, color, board, name)
        self.symbol = color + self.__Symbol
        self.index = 2

    def blocking(self, destination):
        x_, y_ = destination
        x, y = self.location
        if self.in_board(destination):
            if 3 <= x_ <= 5 and (y_ <= 2 or y_ >= 7):
                if abs(x_-x) == 1 and abs(y_-y) == 1:
                    return False
        return True


class Elephant(Piece):
    __Symbol = '_E'

    def __init__(self, location, color, board, name):
        super().__init__(location, color, board, name)
        self.symbol = color + self.__Symbol
        self.index = 3

    def blocking(self, destination):
        x_, y_ = destination
        x, y = self.location
        if self.in_board(destination):
            if (y_ <= 4 and self.color == 'B') or (y_ >=5 and self.color == 'R'):
                if abs(x_-x) == 2 and abs(y_-y) == 2:
                    loc = int((x_+x)/2), int((y_+y)/2)
                    if not self.board.find_piece(loc):
                        return False
        return True


class Horse(Piece):
    __Symbol = '_H'

    def __init__(self, location, color, board, name):
        super().__init__(location, color, board, name)
        self.symbol = color + self.__Symbol
        self.index = 4

    def blocking(self, destination):
        x_, y_ = destination
        x, y = self.location
        if self.in_board(destination):
            if abs(x_ - x) == 2 and abs(y_ - y) == 1:
                loc = int((x_+x)/2), y
                if not self.board.find_piece(loc):
                    return False
            elif abs(x_ - x) == 1 and abs(y_ - y) == 2:
                loc = x, int((y_+y)/2)
                if not self.board.find_piece(loc):
                    return False
        return True


class Chariot(Piece):
    __Symbol = '_R'

    def __init__(self, location, color, board, name):
        super().__init__(location, color, board, name)
        self.symbol = color + self.__Symbol
        self.index = 5

    def blocking(self, destination):
        x_, y_ = destination
        x, y = self.location
        if self.in_board(destination):
            if x_ == x:
                if abs(y_-y) == 1:
                    return False
                for loc_y in range(min(y, y_) + 1, max(y, y_)):
                    if self.board.find_piece((x, loc_y)):
                        return True
                return False
            elif y_ == y:
                if abs(x_-x) == 1:
                    return False
                for loc_x in range(min(x, x_) + 1, max(x, x_)):
                    if self.board.find_piece((loc_x, y)):
                        return True
                return False
        return True


class Cannon(Piece):
    __Symbol = '_C'

    def __init__(self, location, color, board, name):
        super().__init__(location, color, board, name)
        self.symbol = color + self.__Symbol
        self.index = 6

    def blocking(self, destination):
        x_, y_ = destination
        x, y = self.location
        count = 0
        if self.in_board(destination):
            find_piece = self.board.find_piece(destination)
            if x_ == x:
                cons, v1, v2 = x, y, y_
                L = lambda a: (x, a)
            elif y_ == y:
                cons, v1, v2 = y, x, x_
                L = lambda a: (a, y)
            else:
                return True
            if find_piece and find_piece.color != self.color:       # 目标坐标有对方棋子，按吃子规则移动
                if abs(v1 - v2) == 1:
                    return True
                for loc_ in range(min(v1, v2) + 1, max(v1, v2)):
                    if self.board.find_piece(L(loc_)):
                        count += 1
                if count == 1:
                    return False
            else:                                       # 目标坐标无对方棋子（此处忽略目标坐标是己方棋子的情况，在 Board 中考虑）
                if abs(v1 - v2) == 1:
                    return False
                for loc_ in range(min(v1, v2) + 1, max(v1, v2)):
                    if self.board.find_piece(L(loc_)):
                        return True
                return False
            # if x_ == x:
            #     if abs(y_-y) == 1:
            #         return True
            #     for loc_y in range(min(y, y_) + 1, max(y, y_)):
            #         if self.board.find_piece((x, loc_y)):
            #             count += 1
            #     if count == 1:
            #         return False
            #     return False
            # elif y_ == y:
            #     if abs(x_-x) == 1:
            #         return True
            #     for loc_x in range(min(x, x_) + 1, max(x, x_)):
            #         if self.board.find_piece((loc_x, y)):
            #             count += 1
            #     if count == 1:
            #         return False
        return True


class Soldier(Piece):
    __Symbol = '_S'

    def __init__(self, location, color, board, name):
        super().__init__(location, color, board, name)
        self.symbol = color + self.__Symbol
        self.index = 7

    def blocking(self, destination):
        x_, y_ = destination
        x, y = self.location
        if self.in_board(destination):
            if x_ == x:
                if self.color == 'B' and y_-y == 1:
                    return False
                elif self.color == 'R' and y_-y == -1:
                    return False
            elif y_ == y:
                if (y >= 5 and self.color == 'B') or (y <= 4 and self.color == 'R'):
                    if abs(x_-x) == 1:
                        return False
        return True