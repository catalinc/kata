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
                if len(last.rolls) == 3 or not (last.is_spare() or last.is_strike()):
                    raise ValueError('no more rolls allowed')
        last.roll(pins)

    def score(self):
        score = 0
        for i in range(0, len(self.frames)):
            f = self.frames[i]
            score += f.pins()
            if f.is_spare() or f.is_strike():
                if i == 9:
                    score += f.rolls[2]
                else:
                    f_next = self.frames[i + 1]
                    score += f_next.rolls[0]
                    if f.is_strike():
                        score += f_next.rolls[1]
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
        return len(self.rolls) in (2, 3)

    def is_strike(self):
        return self.rolls[0] == 10 or self.rolls[1] == 10

    def is_spare(self):
        return not self.is_strike() and self.pins() == 10

    def pins(self):
        return self.rolls[0] + self.rolls[1]


class TestBowlingGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_score_game_not_started(self):
        self.assertEqual(self.game.score(), 0)

    def test_roll_more_than_allowed(self):
        with self.assertRaises(ValueError) as context:
            for i in xrange(0, 11):
                self.game.roll(1)
                self.game.roll(1)
        self.assertTrue('no more rolls allowed' in context.exception)

    def test_score_regular_game(self):
        rolls = [1, 4,
                 4, 5,
                 6, 4,
                 5, 5,
                 10, 0,
                 0, 1,
                 7, 3,
                 6, 4,
                 10, 0,
                 2, 8, 6]
        for r in rolls:
            self.game.roll(r)
        self.assertEqual(133, self.game.score())

    def test_score_perfect_game(self):
        for _ in range(0, 9):
            self.game.roll(10)
            self.game.roll(0)
        for _ in range(0, 3):
            self.game.roll(10)
        self.assertTrue(300, self.game.score())

if __name__ == '__main__':
    unittest.main()
