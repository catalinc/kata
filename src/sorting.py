import unittest
import string

# Solution to http://codekata.com/kata/kata11-sorting-it-out/


class Countsort(object):

    def __init__(self, max_val):
        self.freq = [0 for _ in xrange(max_val)]

    def add(self, n):
        self.freq[n] += 1

    @property
    def sorted(self):
        L = []
        for i in xrange(len(self.freq)):
            v = self.freq[i]
            if v > 0:
                while v > 0:
                    L.append(i)
                    v -= 1
        return L


class Rack(object):

    def __init__(self):
        self._balls = Countsort(60)

    def add(self, n):
        self._balls.add(n)

    @property
    def balls(self):
        return self._balls.sorted


class CharacterSorter(object):

    def __init__(self):
        self._letters = Countsort(26)

    def update(self, text):
        for c in text.lower():
            if c in string.ascii_lowercase:
                i = ord(c) - ord('a')
                self._letters.add(i)

    @property
    def letters(self):
        L = []
        for i in self._letters.sorted:
            c = chr(i + ord('a'))
            L.append(c)
        return ''.join(L)


class Test(unittest.TestCase):

    def test_rack_add(self):
        rack = Rack()
        self.assertEqual([], rack.balls)
        rack.add(20)
        self.assertEqual([20], rack.balls)
        rack.add(10)
        self.assertEqual([10, 20], rack.balls)
        rack.add(30)
        self.assertEqual([10, 20, 30], rack.balls)

    def test_character_sort(self):
        sorter = CharacterSorter()
        sorter.update(
            'When not studying nuclear physics, Bambi likes to play beach volleyball.')
        self.assertEqual(
            'aaaaabbbbcccdeeeeeghhhiiiiklllllllmnnnnooopprsssstttuuvwyyyy', sorter.letters)
if __name__ == '__main__':
    unittest.main()
