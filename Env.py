"""
This script is the environment part of this Reinforcement learning example.
The RL is in RL_brain.py.
@file    Env.py
@author  Haoyi Niu
@date    2020-06-21
"""
import numpy as np
import time
import random

# basic circuit parameters as hard constraints
Vcc = 5   # 
Ubeq = 0.75  # 
Uces = 1  # 
beta = 100
Rs = 1
Rbe = 0.1 # 100 Ohm
RL = 10   # 10k Ohm

class CircuitEnv:
    def __init__(self):
        self.action_space = ['Rb+1k', 'Rb+10k', 'Rb-1k', 'Rb-10k',
                            'Rc+1k', 'Rc+10k', 'Rc-1k', 'Rc-10k']
        self.n_actions = len(self.action_space)           # every action for both Rb1 and Rc
        self.n_features = 2                               # pair(Rb1,Rc)
        self.Rb = random.randint(11,50)
        self.Rc = random.randint(11,50)

    # initiate or reinitialize resistance parameters
    def reset(self):
        self.Rb = random.randint(11,50)
        self.Rc = random.randint(11,50)
        # return observation
        return self.Rb, self.Rc

    def getUceq(self, action):
        if action == 0:     # Rb+1k
            self.Rb += 1
        elif action == 1:   # Rb+10k
            self.Rb += 10
        elif action == 2:   # Rb-1k
            self.Rb -= 1
        elif action == 3:   # Rb-10k
            self.Rb -=10
        elif action == 4:   # Rc+1k
            self.Rc += 1
        elif action == 5:   # Rc+10k
            self.Rc += 10
        elif action == 6:   # Rc-1k
            self.Rc -= 1
        elif action == 7:   # Rc-10k
            self.Rc -=10
        Ibq = (Vcc-Ubeq)/self.Rb - Ubeq/Rs
        return Vcc-beta*self.Rc*Ibq

    def getAu(self, action):
        RL_ = self.Rc * RL /(self.Rc + RL)
        return beta * RL_ / Rs

    def step(self, action):
        Uceq = self.getUceq(action)
        Au = self.getAu(action)
        done = False
        if Uceq > Uces:
            reward = 50 - abs(Au - 100)
            if Au > 90 and Au <110:
                done = True
        else:
            reward = -100
        s_ = [self.Rb, self.Rc]
        #print(done)
        return s_, reward, done

        # self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        # next_coords = self.canvas.coords(self.rect)  # next state

        # reward function
        # if next_coords == self.canvas.coords(self.oval):
        #     reward = 1
        #     done = True
        # elif next_coords in [self.canvas.coords(self.hell1)]:
        #     reward = -1
        #     done = True
        # else:
        #     reward = 0
        #     done = False
        # s_ = (np.array(next_coords[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(MAZE_H*UNIT)