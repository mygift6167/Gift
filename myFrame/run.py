# -*- coding: utf-8 -*-
from frame import Board
from model import DQN
import os
import time


def run_model(board, RL):
    file_time = None
    for episode in range(3):
        step = 0
        board.reset()
        with open('record.txt', 'w') as file:
            time.clock()
            color = 'B'
            observation = board.encode_board(color)

            invalid_count, invalid_step = 0, 0  # 无效步数（距上次）， 无效步数（总）
            valid_step = 0
            time_start = time.localtime()
            file.write(time.strftime("%Y-%m-%d %H:%M:%S", time_start))
            while True:
                action = RL.choose_action(observation)
                # action = random.randint(0, 90*90-1)
                r_action = board.red_action(action) if color == 'R' else action
                error_num, done, reward, observation_ = board.training_move(r_action, color)
                RL.store_transition(observation, action, reward, observation_)

                if error_num is None:
                    file.write('\nstep {}/{}:   '.format(step, valid_step))
                    file.write('\n\t( {} invalid actions generated )   {}'.format(invalid_count, action))
                    file.write(board.board_print(color))
                    print(step, valid_step)
                    valid_step += 1
                    invalid_step += invalid_count
                    invalid_count = 0
                    color = 'R' if color == 'B' else 'B'
                else:
                    invalid_count += 1

                if (step > 32) and (step % 5 == 0):
                    RL.learn()
                observation = board.encode_board(color)

                if done:
                    RL.save_net()
                    break
                step += 1
            print('game over, final step count is {}!!!!'.format(step))
            print('\nfinal valid rate is {:.2f}\n'.format(invalid_step/step*100))
            file.write('\n{}!! game over, final step count is {}, invalid step count is {}!!!!\n'.format(
                                                                                    done, step, invalid_step))
            file.write('\nfinal valid rate is {:.2f}\n'.format(100-invalid_step/step*100))
            file_time = time.localtime()
            file.write(time.strftime("%Y-%m-%d %H:%M:%S", file_time))
            file.write(time.strftime("\t\tSpend time: %H:%M:%S", time.gmtime(time.clock())))
        if os.path.isfile('record.txt'):
            os.rename('record.txt', 'record - {}.txt'.format(time.strftime("%H%M%S", file_time)))


if __name__ == '__main__':
    board = Board()
    """path = os.path.abspath('./model/'+'%Y-%m-%d/'+'model-%Y%m%d-%H%M')"""
    path = os.path.abspath('./model/'+'2017-11-29/'+'model-20171129-1258')
    RL = DQN(n_actions=90*90, n_features=9*10, restore_DQN=True, restore_file=path)
    # RL = DQN(n_actions=90*90, n_features=9*10, restore_DQN=False, restore_file=None)
    run_model(board, RL)
    