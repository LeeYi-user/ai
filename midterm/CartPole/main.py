import gymnasium as gym
import time
import random
import numpy as np
import tensorflow as tf
from threading import Thread
from collections import deque

EPISODES = 1000
BATCH_SIZE = 32

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.terminate = False
        self.memory = deque(maxlen = 2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Dense(24, input_dim = self.state_size, activation = "relu"),
            tf.keras.layers.Dense(24, activation = "relu"),
            tf.keras.layers.Dense(self.action_size, activation = "linear")
        ])

        model.compile(optimizer = tf.keras.optimizers.Adam(learning_rate = self.learning_rate), loss = "mean_squared_error")
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        else:
            act_values = self.model.predict(state, verbose = 0)
            return np.argmax(act_values[0])

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        if len(self.memory) < BATCH_SIZE:
            return

        minibatch = random.sample(self.memory, BATCH_SIZE)
        current_states = np.array([transition[0][0] for transition in minibatch]) / 255
        current_qs_list = self.model.predict(current_states, verbose = 0)
        new_current_states = np.array([transition[3][0] for transition in minibatch]) / 255
        future_qs_list = self.model.predict(new_current_states, verbose = 0)
        states, targets_f = [], []

        for index, (state, action, reward, next_state, done) in enumerate(minibatch):
            target = reward

            if not done:
                target = reward + self.gamma * np.amax(future_qs_list[index])

            target_f = current_qs_list[index]
            target_f[action] = target
            states.append(state[0])
            targets_f.append(target_f)

        self.model.fit(np.array(states), np.array(targets_f), epochs = 1, verbose = 0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train_in_loop(self):
        while True:
            if self.terminate:
                return

            self.train()
            time.sleep(0.01)

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

if __name__ == "__main__":
    env = gym.make("CartPole-v1") # , render_mode = "human")
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)

    try:
        agent.load("./save/cartpole-dqn.weights.h5")
    except:
        pass

    trainer_thread = Thread(target = agent.train_in_loop, daemon = True)

    trainer_thread.start()

    for episode in range(1, EPISODES + 1):
        timestep = 0
        state, _ = env.reset()
        state = np.reshape(state, [1, state_size])
        done = False

        while not done:
            timestep += 1

            # env.render()
            action = agent.act(state)

            next_state, reward, terminated, truncated, _ = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            reward = reward if not done else -10
            done = terminated or truncated

            agent.memorize(state, action, reward, next_state, done)
            state = next_state

        print(f"episode = { episode }: timestep = { timestep }")

        if episode % 10 == 0:
            agent.save("./save/cartpole-dqn.weights.h5")

    agent.terminate = True
    trainer_thread.join()
    env.close()
