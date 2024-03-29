from typing import Callable
import argparse
import random


class SuccessiveWins:
    def __init__(self, dad_win_prob, champ_win_prob):
        """

        :param dad_win_prob: probability of Elmer's Dad winning a match
        :param champ_win_prob: probability of the champion winning a match
        """
        self._dad_win_prob = dad_win_prob
        self._champ_win_prob = champ_win_prob

    def _three_games_win_probability(self):
        return random.random(), random.random(), random.random()

    def wins_cfc_series(self) -> bool:
        """
        The outcome of playing the champion-father-champion series
        """
        g1, g2, g3 = self._three_games_win_probability()

        return (g1 > self._champ_win_prob and g2 > self._dad_win_prob) or \
               (g2 > self._dad_win_prob and g3 > self._champ_win_prob)

    def wins_fcf_series(self) -> bool:
        """
        The outcome of playing the father-champion-father series
        """
        g1, g2, g3 = self._three_games_win_probability()

        return (g1 > self._dad_win_prob and g2 > self._champ_win_prob) or \
               (g2 > self._champ_win_prob and g3 > self._dad_win_prob)


def win_simulations(trials: int, win_series: Callable) -> float:
    """

    :param trials: number of trials
    :param win_series: the series to win
    :return: win probabilty
    """
    wins = 0
    for _ in range(trials):
        if win_series():
            wins += 1

    return wins/trials

def is_valid_probabity(prob):
    return 0.0 <= prob < 1.0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--champ_wins", help="the probability of the champ winning a match", type=float, default=0.67)
    parser.add_argument("-d", "--dad_wins", help="the probability of Elmer Dad's winning a match", type=float, default=0.5)
    parser.add_argument("-t", "--trials", help="the number of trials for the simulation", type=int, default=10000)
    args = parser.parse_args()

    if not is_valid_probabity(args.champ_wins):
        raise ValueError("champ_wins probability is not in the range of [0.0, 1.0).")

    if not is_valid_probabity(args.dad_wins):
        raise ValueError("champ_wins probability is not in the range of [0.0, 1.0).")

    if args.trials < 1:
        raise ValueError("trials must be > 0.")


    elmer = SuccessiveWins(args.dad_wins, args.champ_wins)
    wins_fcf = win_simulations(args.trials, elmer.wins_fcf_series)
    wins_cfc = win_simulations(args.trials, elmer.wins_cfc_series)
    print(f"Elmer's probability of winning the father-champ-father series ({args.trials} trials): {wins_fcf}")
    print(f"Elmer's probability of winning the champ-father-champ series ({args.trials} trials): {wins_cfc}")
