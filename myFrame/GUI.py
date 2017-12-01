# -*- coding: utf-8 -*-
import os
import tkinter as tk
from frame import Board
from PIL import Image, ImageTk


class GUIBoard(tk.Tk):
    def __init__(self, control=False):
        super().__init__()
        self.board = Board()
        self.geometry('640x652')
        self.chosen_flag = False

        self.canvas = tk.Canvas(self, height=652, width=640)
        self.canvas.place(x=0, y=0, anchor='nw')
        self.board_image = ImageTk.PhotoImage(Image.open(os.getcwd() + '/image/ChessBoard640.jpg'))
        # anchor: “n”, “s”, “w”, “e”, “nw”, “sw”, “se”, “ne”, “center”(默认）
        image = self.canvas.create_image(0, 0, anchor='nw', image=self.board_image)

        chosen_image1_ = tk.PhotoImage(file=os.getcwd() + '/image/ChosenBlack.png')
        chosen_image2_ = tk.PhotoImage(file=os.getcwd() + '/image/ChosenRed.png')
        self.chosen_images = {'B': chosen_image1_, 'R': chosen_image2_}
        self.chosen_image1, self.chosen_image2 = None, None
        self.record_image1, self.record_image2 = None, None             # 记录棋子之前位置，训练时使用
        self.chess_images_, self.chosen_piece = [], None

        # 建此字典，以将棋子图片批量定义为 实例属性
        images = {'B': ['0', 'BlackGeneral', 'BlackAdvisor', 'BlackElephant', 'BlackHorse', 'BlackChariot',
                        'BlackCannon', 'BlackSoldier'],
                  'R': ['0', 'RedGeneral', 'RedAdvisor', 'RedElephant', 'RedHorse', 'RedChariot',
                        'RedCannon', 'RedSoldier']}
        for piece in self.board.pieces_list:
            loc_ = self.get_location(piece.location)
            self.chess_images_.append(tk.PhotoImage(
                                            file=os.getcwd() + '/image/' + images[piece.color][piece.index] + '.png'))
            temp_ = self.canvas.create_image(loc_[0], loc_[1],image=self.chess_images_[-1])
            setattr(self, piece.name, temp_)

        # 建此字典，以将方便以后访问 棋子图片
        self.chess_dict = {'B': [self.black_general, self.black_advisor_L, self.black_advisor_R,
                                 self.black_elephant_L, self.black_elephant_R, self.black_horse_L, self.black_horse_R,
                                 self.black_chariot_L, self.black_chariot_R, self.black_cannon_L, self.black_cannon_R,
                                 self.black_soldier_0, self.black_soldier_1, self.black_soldier_2,
                                 self.black_soldier_3, self.black_soldier_4],
                           'R': [self.red_general, self.red_advisor_L, self.red_advisor_R,
                                 self.red_elephant_L, self.red_elephant_R, self.red_horse_L, self.red_horse_R,
                                 self.red_chariot_L, self.red_chariot_R, self.red_cannon_L, self.red_cannon_R,
                                 self.red_soldier_0, self.red_soldier_1, self.red_soldier_2,
                                 self.red_soldier_3, self.red_soldier_4]}
        if control:
            self.bind("<Button-1>", self.clicked)

    @staticmethod
    def get_location(location):
        x, y = location
        result = (round(66 + 63.25*x), round(614 - 64*y))
        return result

    @staticmethod
    def get_board_location(location):
        x, y = location
        result = (round((x - 66)/63.25), round((614 - y)/64))
        return result

    def clicked(self, event=None, train_location=None):
        def delete_(image):
            if image:
                self.canvas.delete(image)

        x, y = event.x, event.y if train_location is None else train_location
        if self.chosen_piece:
            if self.move_piece((x, y)):
                self.chosen_flag = False
                delete_(self.chosen_image1)
                delete_(self.chosen_image2)
                self.chosen_piece, self.chosen_image1, self.chosen_image2 = None, None, None
                return
        for piece in self.board.pieces_list:
            if not piece.survival:
                continue
            x_, y_ = self.get_location(piece.location)
            if abs(x - x_) <= 20 and abs(y - y_) <= 20:
                print(piece.name)
                if self.chosen_flag:
                    self.chosen_flag = False
                    if self.chosen_image1 or self.chosen_image2:
                        delete_(self.chosen_image1)
                        delete_(self.chosen_image2)
                        self.chosen_piece, self.chosen_image1, self.chosen_image2 = None, None, None
                else:
                    self.chosen_flag = True
                    if self.chosen_image1 is None and self.chosen_image2 is None:
                        self.chosen_piece = piece
                        if piece.color == 'B':
                                self.chosen_image1 = self.canvas.create_image(x_, y_, image=self.chosen_images['B'])
                        elif piece.color == 'R':
                                self.chosen_image2 = self.canvas.create_image(x_, y_, image=self.chosen_images['R'])

    def move_piece(self, loc):
        if self.chosen_piece:
            x, y = loc
            for x_ in [int(66 + 63.25*i) for i in range(9)]:
                for y_ in [int(614 - 64*i) for i in range(10)]:
                    if abs(x - x_) <= 20 and abs(y - y_) <= 20:
                        # print('x_ is {}, y_ is {}'.format(x_, y_))
                        location = self.get_board_location((x_, y_))
                        # print('location is {}'.format(location))
                        x__, y__ = self.get_location(self.chosen_piece.location)
                        error_num, capture = self.board.move(location, self.chosen_piece.color, self.chosen_piece)
                        if error_num is None:
                            if capture:
                                for piece in self.board.pieces_list:
                                    if piece.location == location and piece.survival is False:
                                        self.canvas.delete(getattr(self, piece.name))
                            self.canvas.move(getattr(self, self.chosen_piece.name), int(x_ - x__), int(y_ - y__))
                            return True

    def training_move(self, action, color):
        def delete_(image):
            if image:
                self.canvas.delete(image)

        x, y = (int(action / 90) % 9, int((action / 90)/9))
        x_, y_ = (action % 90 % 9, int((action % 90)/9))
        error_num, done, reward, observation_, capture = self.board.training_move(action, color, return_capture_=True)
        if error_num is None:
            for P in self.board.pieces_list:
                if P.location == (x_, y_) and P.survival is True:
                    x, y = self.get_location((x, y))
                    if capture:
                        for piece in self.board.pieces_list:
                            if piece.location == (x_, y_) and piece.survival is False:
                                self.canvas.delete(getattr(self, piece.name))
                    x_, y_ = self.get_location((x_, y_))
                    self.canvas.move(getattr(self, P.name), int(x_ - x), int(y_ - y))
                    if color == 'B':
                            delete_(self.record_image1)
                            delete_(self.chosen_image1)
                            self.record_image1 = self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10,
                                                                              outline='blue')
                            self.chosen_image1 = self.canvas.create_image(x_, y_, image=self.chosen_images['B'])
                    elif color == 'R':
                            delete_(self.record_image2)
                            delete_(self.chosen_image2)
                            self.record_image2 = self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10,
                                                                              outline='red')
                            self.chosen_image2 = self.canvas.create_image(x_, y_, image=self.chosen_images['R'])
        return error_num, done, reward, observation_


if __name__ == '__main__':
    board = GUIBoard(control=True)
    board.mainloop()
