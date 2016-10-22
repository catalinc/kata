import unittest
import collections

# Solution to http://codekata.com/kata/kata06-anagrams/


def is_anagram(a, b):
    return len(a) == len(b) and sort(a) == sort(b)


def sort(s):
    return ''.join(sorted(s))


def find_anagrams(filename):
    d = collections.defaultdict(list)
    with open(filename) as input_file:
        for word in input_file:
            word = word.rstrip('\n')
            key = sort(word)
            d[key].append(word)
    return [a for a in d.values() if len(a) >= 2]


class Test(unittest.TestCase):

    def test_is_anagram(self):
        self.assertTrue(is_anagram('sunders', 'undress'))

    def test_find_anagrams(self):
        r = find_anagrams('wordlist.txt')
        self.assertEqual(20683, len(r))


if __name__ == '__main__':
    unittest.main()
