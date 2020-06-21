"""
This section of code is the runner.
@file    run_this.py
@author  Haoyi Niu
@date    2020-06-21
"""

from Env import CircuitEnv
from DQN_Modified import DeepQNetwork

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def run():
    step = 0
    Rb_list = []
    Rc_list = []
    for episode in range(1000):
        # initial observation
        Rb, Rc = env.reset()
        observation =[Rb, Rc]

        while True:
            # RL choose action based on observation
            action = RL.choose_action(observation)

            # if (action == 2 and observation[0] <= 1) \
            #     or (action == 3 and observation[0] <= 10) \
            #     or (action == 6 and observation[1] <= 1)\
            #     or (action == 7 and observation[1] <= 10):
            print(action, observation)
            # break
            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            # swap observation
            observation = observation_
            Rb_list.append(observation_[0])
            Rc_list.append(observation_[1])

            # break while loop when end of this episode
            if done:
                break
            step += 1
        print(episode)
        #print(RL.cost_his)
    
    sns.set()
    plt.title("Rb/Rc changing with trianing steps")
    plt.plot(np.arange(len(Rb_list)),Rb_list,label="Rb",color="#F08080")
    plt.plot(np.arange(len(Rc_list)),Rc_list,label="Rc",color="#DB7093",linestyle="--")
    plt.ylabel('Resistance/kilohm')
    plt.xlabel('training steps')
    plt.legend()
    plt.show()
    # end of training
    print('train over')


if __name__ == "__main__":
    # maze game
    env = CircuitEnv()
    RL = DeepQNetwork(env.n_actions, env.n_features,
                    learning_rate=0.01,
                    reward_decay=0.9,
                    e_greedy=0.9,
                    replace_target_iter=200,
                    memory_size=2000,
                    output_graph=True
                    )
    run()
    RL.plot_cost()