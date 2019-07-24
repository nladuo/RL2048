from RL_brain import DuelingDQN
from env.game import Game
from collections import deque
import numpy as np


def train_2048():
    step = 0
    scores = deque(maxlen=4000)
    for episode in range(20000000):
        observation = env.reset()  # initial observation

        while True:
            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            RL.store_transition(observation, action, reward, observation_)

            if (step > 500) and (step % 10 == 0):
                RL.learn()

            if step % 1000 == 0:
                print("step", step, "reward:", reward, "action:", action)

            # swap observation
            observation = observation_

            step += 1
            # break while loop when end of this episode
            if done:
                break
        scores.append(env.score)

        if episode % 5 == 0:
            print("#" * 80)
            print(episode, ",", int(step / 10), ",score:", env.score, ",e:", RL.epsilon)
            print("avg-score: {}".format(np.mean(list(scores)[-1500:])))

        if episode % 100 == 0:
            print(observation)
            train_step, lr = RL.get_lr()
            print("train_step:", train_step, ",Learning Rate:", lr)
            env.show()

if __name__ == "__main__":
    env = Game()
    RL = DuelingDQN(env.n_actions,
                    env.n_features,
                    start_learning_rate=1e-3,
                    reward_decay=0.95,
                    e_greedy=0.99,
                    start_epsilon=0.5,
                    e_greedy_increment=1e-5)
    train_2048()
