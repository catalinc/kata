import unittest
import math
import hashlib
import bitarray
import mmh3
import fnvhash

# Solution to http://codekata.com/kata/kata05-bloom-filters/


class BloomFilter(object):

    def __init__(self, n=1000000, p=.01):
        """BloomFilter implementation based on:
        https://en.wikipedia.org/wiki/Bloom_filter

        Keyword arguments:
        n -- expected number of elements to add
        p -- false positive probability
        """
        self.m = int(math.ceil(-1 * ((n * math.log(p)) / (math.log(2)**2))))
        self.k = int(math.ceil((self.m / n) * math.log(2)))
        self.bits = bitarray.bitarray(self.m)
        self.bits.setall(False)

    def add(self, s):
        added = False
        for i in self._hashes(s):
            if not self.bits[i]:
                added = True
                self.bits[i] = True
        return added

    def test(self, s):
        for i in self._hashes(s):
            if not self.bits[i]:
                return False
        return True

    def _hashes(self, s):
        for i in xrange(1, self.k + 1):
            yield (fnvhash.fnv1a_32(s) + i * mmh3.hash(s)) % self.m


class SpellChecker(object):

    def __init__(self, filename):
        with open(filename) as dictionary:
            self.bloom_filter = BloomFilter()
            for word in dictionary:
                word = word.rstrip('\n')
                self.bloom_filter.add(word)

    def check(self, word):
        return self.bloom_filter.test(word)


class BloomFilterTest(unittest.TestCase):

    def test_add(self):
        bf = BloomFilter()
        self.assertTrue(bf.add('abc'))
        self.assertFalse(bf.add('abc'))
        self.assertTrue(bf.add('def'))

    def test_contains(self):
        bf = BloomFilter()
        bf.add('abc')
        bf.add('def')
        self.assertTrue(bf.test('abc'))
        self.assertTrue(bf.test('def'))
        self.assertFalse(bf.test('ab'))
        self.assertFalse(bf.test('abcd'))


class SpellCheckerTest(unittest.TestCase):

    def test_spellcheck(self):
        checker = SpellChecker('/usr/share/dict/words')
        self.assertTrue(checker.check('water'))
        self.assertFalse(checker.check('woya'))


if __name__ == '__main__':
    unittest.main()
