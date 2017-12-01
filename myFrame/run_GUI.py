# -*- coding: utf-8 -*-
from frame import Board
from GUI import GUIBoard
from model import DQN
import time
import threading


def run_model(board, RL):
    step = 0
    with open('record.txt', 'w') as file:
        for episode in range(1):
            time.time()
            color = 'B'
            observation = board.board.encode_board(color)

            invalid_count, invalid_step = 0, 0
            file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            while True:
                action = RL.choose_action(observation)
                r_action = board.board.red_action(action) if color == 'R' else action
                error_num, done, reward, observation_ = board.training_move(r_action, color)
                RL.store_transition(observation, action, reward, observation_)

                if error_num is None:
                    file.write('\nstep {}:       ( {} invalid actions generated )'.format(step, invalid_count))
                    file.write(board.board.board_print(color))
                    print(step)
                    invalid_step += invalid_count
                    invalid_count = 0
                    color = 'R' if color == 'B' else 'B'
                else:
                    invalid_count += 1

                if (step > 200) and (step % 5 == 0):
                    RL.learn()
                observation = board.board.encode_board(color)

                if done:
                    break
                step += 1
            print('game over, final step count is {}!!!!'.format(step))
            file.write('\n{}!! game over, final step count is {}, invalid step count is {}!!!!\n'.format(
                done, step, invalid_step))
            file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            file.write(time.strftime("Spend time: %H:%M:%S", time.gmtime(time.clock())))


if __name__ == '__main__':
    board = GUIBoard()
    # path = os.path.abspath('./model/''%Y-%m-%d/''model-%Y%m%d-%H%M')
    RL = DQN(n_actions=90*90, n_features=9*10, restore_DQN=False, restore_file=None)

    added_thread = threading.Thread(target=board.mainloop)
    added_thread.start()
    run_model(board, RL)
