import unittest
import time


def timeit(fn):
    def timed(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        print('%s %2.4f s' % (fn.__name__, end - start))
        return result
    return timed


class WordDictionary(object):

    def __init__(self, filename):
        self._dictionary = set()
        with open(filename) as input_file:
            for line in input_file:
                line = line.rstrip('\n').lower()
                self._dictionary.add(line)

    def is_two_words(self, s):
        for i in xrange(1, len(s)):
            if self.is_word(s[0:i]) and self.is_word(s[i:]):
                return True

    def is_word(self, s):
        return s in self._dictionary

    def find_all_from_two_words(self, size=6):
        L = [w for w in self._dictionary if len(w) < size]
        L.sort(cmp=lambda a, b: len(a) - len(b))
        r = set()
        for i in xrange(0, len(L)):
            p = L[i]
            for j in xrange(i, len(L)):
                s = L[j]
                n = len(p) + len(s)
                if n < size:
                    continue
                if n > size:
                    break
                w1 = p + s
                if self.is_word(w1):
                    r.add(w1)
                w2 = s + p
                if self.is_word(w2):
                    r.add(w2)
        return r

    def find_all_from_two_words_fast(self, size=6):
        L = [w for w in self._dictionary
             if len(w) == size and self.is_two_words(w)]
        return L


class Test(unittest.TestCase):

    wd = WordDictionary('wordlist.txt')

    def test_is_word(self):
        words = ('water', 'album', 'sun')
        for w in words:
            self.assertTrue(self.wd.is_word(w), 'failed for %s' % w)

    def test_is_not_word(self):
        not_words = ('trilulilu', 'bossap', 'hopas')
        for w in not_words:
            self.assertFalse(self.wd.is_word(w), 'failed for %s' % w)

    def test_is_two_words(self):
        two_words = ('albums', 'barely', 'befoul',
                     'convex', 'hereby', 'gelatin', "hobo's")
        for w in two_words:
            self.assertTrue(self.wd.is_two_words(w), 'failed for %s' % w)

    @timeit
    def test_find_all_from_two_words(self):
        ws = self.wd.find_all_from_two_words(6)
        self.assertEqual(22450, len(ws))

    @timeit
    def test_find_all_from_two_words_fast(self):
        ws = self.wd.find_all_from_two_words_fast(6)
        self.assertEqual(22450, len(ws))


if __name__ == '__main__':
    unittest.main()
