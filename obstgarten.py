import time
from random import choice
from tqdm import tqdm  # pip install tqdm


class Obstgarten:
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    BLUE = "blue"
    CROW = "crow"
    BASKET = "basket"

    def __init__(self, blue: int = 4, red: int = 4, yellow: int = 4, green: int = 4, crow: int = 5):
        self.fruits = {self.BLUE: blue, self.RED: red, self.YELLOW: yellow, self.GREEN: green}
        self.crow = crow

    def game_lost(self):
        return self.crow == 0

    def game_won(self):
        return self.fruits[self.BLUE] == self.fruits[self.RED] == self.fruits[self.YELLOW] == self.fruits[self.GREEN] == 0

    def game_ended(self):
        return self.game_lost() or self.game_won()

    def roll_the_dice(self):
        dice = (self.CROW, self.BASKET, *tuple(key for (key, value) in self.fruits.items() if value > 0))
        return choice(dice)

    def handle_basket_smart(self):
        _max = max(self.fruits, key=self.fruits.get)
        self.fruits[_max] -= 1

    def handle_basket_random(self):
        dice = tuple(key for (key, value) in self.fruits.items() if value > 0)
        random = choice(dice)
        self.fruits[random] -= 1

    def handle_basket_bad(self):
        fitered = {key: value for key, value in self.fruits.items() if value > 0}
        _min = min(fitered, key=fitered.get)
        self.fruits[_min] -= 1

    def play(self):
        while not self.game_ended():
            dice_result = self.roll_the_dice()
            if dice_result == self.CROW:
                self.crow -= 1
            elif dice_result == self.BASKET:
                self.handle_basket_smart()
            else:
                self.fruits[dice_result] -= 1
        return not self.game_lost()


def timeit(func):
    def timeit_wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        duration = end - start
        print(f"Time: {duration:3.1f} s")

    return timeit_wrapper


def print_tries(func):
    def print_wrapper(tries, *args, **kwargs):
        won, lost = func(tries, *args, **kwargs)
        print(f"You won {won:,} games.")
        print(f"You lost {lost:,} games.")
        percentage = won / tries * 100
        print(f"You won {percentage:3.1f} % of the games.")

    return print_wrapper


@timeit
@print_tries
def run_with_progressbar(tries: int, blue: int = 4, red: int = 4, yellow: int = 4, green: int = 4, crow: int = 5):
    won = 0
    lost = 0
    for _ in tqdm(range(tries), desc="Processing", mininterval=0.25, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}"):
        won_this_game = Obstgarten(blue, red, yellow, green, crow).play()
        if won_this_game:
            won += 1
        else:
            lost += 1
    return won, lost


if __name__ == "__main__":
    TRIES = 200 * 1000

    # params small variant
    # BLUE: int = 4
    # RED: int = 4
    # YELLOW: int = 4
    # GREEN: int = 4
    # CROW: int = 5

    # params big variant
    BLUE: int = 10
    RED: int = 10
    YELLOW: int = 10
    GREEN: int = 10
    CROW: int = 9

    run_with_progressbar(TRIES, BLUE, RED, YELLOW, GREEN, CROW)
