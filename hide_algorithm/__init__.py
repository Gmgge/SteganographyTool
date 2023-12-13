from hide_algorithm.LSB import LSB


class UnsupportedAlgorithm(Exception):
    pass


algorithm_map = {
    "LSB": LSB()
}


def init_hide_opt(hide_algorithm, hide_algorithm_map=algorithm_map):
    hide_opt = hide_algorithm_map.get(hide_algorithm, None)
    if hide_opt is None:
        raise UnsupportedAlgorithm
    return hide_opt
