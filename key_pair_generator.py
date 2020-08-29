import random
import config


def get_shift_pairs():
    random.seed(config.random_seed)
    alpha_chars = list(filter(lambda x: str.isalpha(x), config.chars))
    shift_pairs = []

    for char in config.chars:
        shift_pairs.append((char, config.shift))
        shift_pairs.append((config.shift, char))

    for char in alpha_chars:
        shift_pairs.append((char.upper(), ''))

    return shift_pairs


def get_all_possible_char_pairs(chars):
    all_char_pairs = []

    # generate all possible key pairs
    for first_char in chars:
        for second_char in chars:
            if (first_char, second_char) not in all_char_pairs:
                all_char_pairs.append((first_char, second_char))

    return all_char_pairs


# print(get_char_pairs())
# print(get_shift_pairs())
