""" train_model.py """

import os
import tqdm

from typing import List
from model import Network_Agent, WordNet
# from utils import 

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def train(words: List[str]) -> None:
    """
    To train the model, we need it to interact with the environment,
    to do so, we need trial before game over is set higher than the
    actual game parameter so episodes are longer.
    """

    longuest_word_size: int = max(list(map(len, words)))
    print(f"The longuest word has length: {longuest_word_size}")

    word_network = WordNet(max_word_size=longuest_word_size)
    agent_network = Network_Agent(max_word_size=longuest_word_size, model=word_network)

    agent_network.summary()