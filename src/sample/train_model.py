""" train_model.py """

import os
import random
from typing import List

import tqdm
from keras import optimizers

from model import NetworkAgent, WordNet
from hangman import Hangman
from utils import get_train_test_set

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def train() -> None:
    """
    To train the model, we need it to interact with the environment,
    to do so, we need trial before game over is set higher than the
    actual game parameter so episodes are longer.
    """

    save_episode: int = 5000
    view_episode: int = 500
    update_episode: int = 5
    average_correct_guesses: int = 0
    wins: int = 0
    num_trials: int = 20000
    progress_bar = tqdm.tqdm(range(num_trials))

    train_set, test_set = get_train_test_set()
    copy_train_set: List[str] = train_set[:]


    # longuest_word_size: int = max(max(list(map(len, train_set))), max(list(map(len, test_set))))
    longuest_word_size: int = 26
    print(f"The longuest word has length: {longuest_word_size}")

    word_network = WordNet(max_word_size=longuest_word_size)
    agent_network = NetworkAgent(max_word_size=longuest_word_size, model=word_network, policy="stochastic")

    word_network.summary()

    for episode_set in progress_bar:
        for _ in range(update_episode):
            word: str = random.choice(copy_train_set)
            copy_train_set.remove(word)
            environment: Hangman = Hangman(word=word)
            game_completed: bool = False
            num_of_correct_guesses: int = 0

            while not game_completed:
                game_state: str = environment.get_board()
                current_guess: str = agent_network.select_action(state = game_state)
                game_state, reward, game_completed, answer =\
                    environment.step(letter = current_guess)

                if reward > 0:
                    num_of_correct_guesses = num_of_correct_guesses + 1

                if reward == environment.win_reward:
                    wins = wins + 1

                agent_network.finalize_episode(answer=answer.get("ans", ""))
                average_correct_guesses = num_of_correct_guesses + len(word)

                print(current_guess, answer["ans"])

        loss: float = agent_network.train_model()
        progress_bar.set_description(f"Loss : {loss :.3f}")

        if (episode_set +1) % view_episode == 0 :
            views = (episode_set + 1, average_correct_guesses / (update_episode*view_episode),\
                view_episode * update_episode, wins / (update_episode*view_episode))

            print(f'Episode {views[0]} -------- Average Correct Count : {views[1]:.3f}     Last {views[2]} winrate : {views[3]:.3f}')

            if loss is not None :
                print('Loss :', loss)
                print()
                average_correct_guesses = 0
                wins = 0

        if (episode_set +1) % save_episode == 0 :
            agent_network.model.save('policy.h5', include_optimizer=False)

if __name__ == "__main__":
    train()
