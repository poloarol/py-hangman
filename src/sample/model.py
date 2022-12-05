""" model.py """

import string
from typing import Dict, List, Any

import numpy as np
import six
from keras import layers, models, optimizers

letters: List[str] = list(string.ascii_lowercase)
letters_dict: Dict[str, int] = {letter: i for i, letter in enumerate(letters)}
letters_dict["-"] = 27


def set_seed(seed: int = 42) -> None:
    """set tensorflow seed"""
    tf.set_random_seed(seed)


def pad_sequences(
    sequences: str , maxlen: Any = None, dtype: int ="int32",\
        padding: str = "pre", truncating: str = "pre", value: float = 0.0
):
    """
    Pads sequences to the same length.
    This function transforms a list of
    `num_samples` sequences (lists of integers)
    into a 2D Numpy array of shape `(num_samples, num_timesteps)`.
    `num_timesteps` is either the `maxlen` argument if provided,
    or the length of the longest sequence otherwise.
    Sequences that are shorter than `num_timesteps`
    are padded with `value` at the end.
    Sequences longer than `num_timesteps` are truncated
    so that they fit the desired length.
    The position where padding or truncation happens is determined by
    the arguments `padding` and `truncating`, respectively.
    Pre-padding is the default.
    # Arguments
        sequences: List of lists, where each element is a sequence.
        maxlen: Int, maximum length of all sequences.
        dtype: Type of the output sequences.
            To pad sequences with variable length strings, you can use `object`.
        padding: String, 'pre' or 'post':
            pad either before or after each sequence.
        truncating: String, 'pre' or 'post':
            remove values from sequences larger than
            `maxlen`, either at the beginning or at the end of the sequences.
        value: Float or String, padding value.
    # Returns
        x: Numpy array with shape `(len(sequences), maxlen)`
    # Raises
        ValueError: In case of invalid values for `truncating` or `padding`,
            or in case of invalid shape for a `sequences` entry.
    """

    if not hasattr(sequences, "__len__"):
        raise ValueError("`sequences` must be iterable.")
    num_samples = len(sequences)

    lengths = []
    for sequence in sequences:
        lengths.append(len(sequence))

    if maxlen is None:
        maxlen = np.max(lengths)

    # take the sample shape from the first non empty sequence
    # checking for consistency in the main loop below.
    sample_shape = tuple()
    for sequence in sequences:
        if len(sequence) > 0:
            sample_shape = np.asarray(sequence).shape[1:]
            break

    is_dtype_str = np.issubdtype(dtype, np.str_) or np.issubdtype(dtype, np.unicode_)
    if isinstance(value, six.string_types) and dtype != object and not is_dtype_str:
        raise ValueError(
            f"`dtype` {dtype} is not compatible with `value`'s\
        type: {type(value)}. You should set `dtype=object` for variable length strings."
        )

    x_var = np.full((num_samples, maxlen) + sample_shape, value, dtype=dtype)
    for idx, sequence in enumerate(sequences):
        if not sequence:
            continue  # empty list/array was found
        if truncating == "pre":
            trunc = sequence[-maxlen:]
        elif truncating == "post":
            trunc = sequence[:maxlen]
        else:
            raise ValueError("Truncating type {trucating} not understood")

        # check `trunc` has expected shape
        trunc = np.asarray(trunc, dtype=dtype)
        if trunc.shape[1:] != sample_shape:
            raise ValueError(
                f"Shape of sample {trunc.shape[1:]}\
                of sequence at position {idx}\
                is different from expected shape {sample_shape}"
            )

        if padding == "post":
            x_var[idx, : len(trunc)] = trunc
        elif padding == "pre":
            x_var[idx, -len(trunc) :] = trunc
        else:
            raise ValueError(f"Padding type {padding} not understood")
    return x_var


class WordNet:
    """
    Defines a bidirectional LSTM network.
    The network consists of two input that,
    reads the current state and a one-hot
    encoded matrix of guessed letters.
    """

    def __init__(self, max_word_size: int = 8) -> None:
        self.max_word_size: int = max_word_size

    def __post_init__(self) -> None:
        state_embedding = self.get_state_embedding()
        guessed_embedding = self.get_guessed_embedding()
        x_input = layers.Concatenate()(
            [state_embedding.output, guessed_embedding.output]
        )
        x_input = layers.Dense(100, activation="tanh")(x_input)
        x_input = layers.Dense(26, activation="softmax")(x_input)
        self.full_model = layers.Model(
            [state_embedding.input, guessed_embedding.input], x_input, name="fullmodel"
        )
        self.compile()

    def get_state_embedding(self) -> models.Model:
        """
        Generates the current games state embedding
        """
        input_layer = layers.Input(shape=(self.max_word_size,))
        x_input = layers.Embedding(30, 100, mask_zero=True)(input_layer)
        x_input = layers.Bidirectional(
            layers.LSTM(100, dropout=0.2, return_sequences=True)
        )(x_input)
        x_input = layers.Bidirectional(
            layers.LSTM(100, dropout=0.2, return_sequences=True)
        )(x_input)
        x_input = layers.GlobalAveragePooling1D()(x_input)
        x_input = layers.Dense(100, activation="tanh")(x_input)
        return models.Model(input_layer, x_input, name="StateEmbedding")

    def get_guessed_embedding(self) -> models.Model:
        """
        Generates one-hot encoded matrix of guessed letters
        """
        input_layer = layers.Input(shape=(self.max_word_size,))
        x_input = layers.Dense(60, activation="tanh")(input_layer)
        x_input = layers.Dense(60, activation="tanh")(x_input)
        return models.Model(input_layer, x_input, name="GuessedEmbedding")

    def __call__(self, state, guessed):
        return self.full_model.predict([state, guessed]).flatten()

    def fit(self, *args, **kwargs) -> None:
        """fit tensorflow model"""
        return self.full_model.fit(*args, **kwargs)

    def train_on_batch(self, *args, **kwargs):
        """train tensorflow model"""
        return self.full_model.train_on_batch(*args, **kwargs)

    def summary(self):
        """Provide summary to tensorflow model"""
        self.full_model.summary()

    def save(self, *args, **kwargs) -> None:
        """Save tensorflow model"""
        self.full_model.save(*args, **kwargs)

    def load_weights(self, *args, **kwargs) -> None:
        """Load weights of tensorflow model"""
        self.full_model.load_weights(*args, **kwargs)
        self.compile()

    def compile(self, optimizer=None) -> None:
        """Compile tensorflow model"""
        if optimizer is not None:
            self.full_model.compile(
                loss="categorical_crossentropy", optimizer=optimizer
            )
        else:
            self.full_model.compile(
                loss="categorical_crossentropy",
                optimizer=optimizers.Adam(1e-3, clipnorm=1),
            )


class Agent:
    """
    Agent is embedded with a model and policy.
    Agent can use stochastic policy:
        choose action randomly from computed probability
    or greedy:
        choose the most probable action out of unused actions.

    Agent is trained off-policy, after a set
    amount of episode (in my case I trained with 3 episodes),
    and after each episode during training must be finalized
    with finalize_episode method to compute the correct course
    of actions.
    train_model method will collect accumulated episodes and
    perform one iteration of gradient descent with the collected
    episode data.

    Tried both with stochastic and greedy.
    Greedy policy converges better.
    """

    def __init__(
        self, model: models.Model, policy: str = "greedy", is_training: bool = True
    ) -> None:
        """ init method """
        if policy not in ["greedy", "stochastic"]:
            raise ValueError("Policy must be either stochastic or greedy")

        self.policy: str = policy
        self.model: models.Model = model
        self.is_training: bool = is_training
        self.guessed: List[str] = []

    @staticmethod
    def guessed_mat(guessed):
        """ generate guess matrix """
        mat = np.empty([1, 26])

        for i, letter in enumerate(letters):
            mat[0, i] = 1 if letter in guessed else 0

        return mat

    def get_guessed_mat(self):
        """ return guessed matrix """
        return self.guessed_mat(self.guessed)

    def reset_guessed(self) -> None:
        """ reset guessed matrix """
        self.guessed = []

    @property
    def policy(self):
        """ return policy implemented """
        return self.policy

    @policy.setter
    def set_policy(self, new_policy: str) -> str:
        """ set policy to implement """
        self.policy = new_policy

    def select_action(self, state):
        """ actions """
        probs = self.get_probs(state)
        if self.policy == "greedy":
            i = 1
            sorted_probs = probs.argsort()
            while letters[sorted_probs[-i]] in self.guessed:
                i += 1
            idx_act = sorted_probs[-i]
        elif self.policy == "stochastic":
            idx_act = np.random.choice(np.arange(probs.shape[0]), p=probs)
        guess = letters[idx_act]
        if guess not in self.guessed:
            self.guessed.append(guess)
        return guess

    def get_probs(self, state):
        """ return probability """
        raise NotImplementedError()

    def eval(self):
        """ evaluate model """
        self.is_training = False
        self.set_policy("greedy")

    def train(self):
        """ train model """
        self.is_training = True


class Network_Agent(Agent):
    """ Network Agent for Hangman game"""

    def __init__(
        self,
        max_word_size: int,
        model: models.Model,
        policy: str = "greedy",
        is_training: bool = True,
    ) -> None:
        super().__init__(model, policy, is_training)
        self.max_word_size: int = max_word_size
        self.state_history: List[str] = []
        self.episodic_memory: List[str] = []

    def get_probs(self, state) -> float:
        """returns the probability of given state"""

        state = self.preprocess_input(state)
        probs = self.model(*state)
        probs /= probs.sum()

        return probs

    def finalize_episode(self, answer) -> None:
        """ guess words """
        input_one, input_two = zip(*self.episodic_memory)
        input_one = np.vstack(list(input_one)).astype(
            float
        )  # stack the game state matrix
        input_two = np.vstack(list(input_two)).astype(
            float
        )  # stack the one hot-encoded guessed

        obj = 1.0 - input_two  # compute the unused letters one-hot encoded
        len_ep = len(self.episodic_memory)  # length of episode

        correct_mask = np.array(
            [[1 if letter in answer else 0 for letter in letters]]
        )  # get mask from correct answer
        correct_mask = np.repeat(correct_mask, len_ep, axis=0).astype(float)
        obj = correct_mask * obj
        # the correct action is choosing the
        # letters that are both unused AND exist in the word
        obj /= obj.sum(axis=1).reshape(-1, 1)  # normalize so it sums to one

        self.state_history.append((input_one, input_two, obj))
        self.episodic_memory = []
        self.reset_guessed()

    def preprocess_input(self, state):
        """ Process input """
        new_input = []

        for letter in state:
            new_input.append(letters_dict[letter])

        state = pad_sequences([new_input], maxlen=self.max_word_size)

        if self.is_training:
            self.episodic_memory.append((state, self.get_guessed_mat()))
        return state, self.get_guessed_mat()


if __name__ == "__main__":
    pass