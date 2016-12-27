import unittest


class Game:

    def __init__(self):
        self.frames = []

    def roll(self, pins):
        last = self._last_frame()
        if last.is_complete():
            if len(self.frames) < 10:
                last = Frame()
                self.frames.append(last)
            else:
                if len(last.rolls) == 2 and last.pins() < 10:
                    raise ValueError('no more rolls allowed')
        last.roll(pins)

    def score(self):
        score = 0
        for i in range(0, len(self.frames)):
            frame = self.frames[i]
            score += frame.pins()
            if frame.is_spare() or frame.is_strike():
                if i < 9:
                    f_next = self.frames[i + 1]
                    score += f_next.rolls[0]
                    if frame.is_strike():
                        if len(f_next.rolls) >= 2:
                            score += f_next.rolls[1]
                        else:
                            f_next = self.frames[i + 2]
                            score += f_next.rolls[0]

        return score

    def _last_frame(self):
        if not self.frames:
            self.frames.append(Frame())
        return self.frames[-1]


class Frame:

    def __init__(self):
        self.rolls = []

    def roll(self, pins):
        self.rolls.append(pins)

    def is_complete(self):
        return self.is_strike() or len(self.rolls) == 2

    def is_strike(self):
        return len(self.rolls) == 1 and self.rolls[0] == 10

    def is_spare(self):
        return len(self.rolls) == 2 and self.pins() == 10

    def pins(self):
        return sum(self.rolls)


class TestBowlingGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_score_game_not_started(self):
        self.assertEqual(self.game.score(), 0)

    def test_roll_more_than_allowed(self):
        with self.assertRaises(ValueError) as context:
            for i in range(0, 11):
                self.game.roll(1)
                self.game.roll(1)
        self.assertTrue('no more rolls allowed' in str(context.exception))

    def test_score_regular_game(self):
        rolls = [1, 4,
                 4, 5,
                 6, 4,
                 5, 5,
                 10,
                 0, 1,
                 7, 3,
                 6, 4,
                 10,
                 2, 8, 6]
        for pins in rolls:
            self.game.roll(pins)
        self.assertEqual(133, self.game.score())

    def test_score_perfect_game(self):
        for _ in range(0, 9):
            self.game.roll(10)
        for _ in range(0, 3):
            self.game.roll(10)
        self.assertEqual(300, self.game.score())


if __name__ == '__main__':
    unittest.main()
