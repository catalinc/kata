import unittest
import collections
import sys


class Dictionary(object):

    def __init__(self, filename):
        self.words = collections.defaultdict(list)
        with open(filename) as infile:
            for line in infile:
                w = line.rstrip()
                self.words[len(w)].append(w)

    def distance(self, s, t):
        c = 0
        for i in range(len(s)):
            if s[i] != t[i]:
                c += 1
        return c

    def word_chain(self, s, t):
        ws = set(self.words[len(s)])
        ws.discard(s)
        ws.discard(t)
        chain = [s]
        while ws:
            last = chain[-1]
            best_next = None
            best_score = sys.maxint
            for w in ws:
                if self.distance(last, w) == 1:
                    score = self.distance(w, t)
                    if score < best_score:
                        best_score = score
                        best_next = w
            if not best_next:
                return []
            chain.append(best_next)
            ws.discard(best_next)
            if self.distance(best_next, t) == 1:
                chain.append(t)
                return chain


class Test(unittest.TestCase):

    def setUp(self):
        self.d = Dictionary("wordlist.txt")

    def test_distance(self):
        self.assertEqual(0, self.d.distance('lead', 'lead'))
        self.assertEqual(1, self.d.distance('lead', 'load'))
        self.assertEqual(3, self.d.distance('lead', 'gold'))

    def test_chain_found(self):
        self.assertEqual(['cat', 'cot', 'dot', 'dog'],
                         self.d.word_chain('cat', 'dog'))
        self.assertEqual(['lead', 'load', 'goad', 'gold'],
                         self.d.word_chain('lead', 'gold'))
        self.assertEqual(['ruby', 'rube', 'robe', 'rode', 'code'],
                         self.d.word_chain('ruby', 'code'))

    def test_chain_not_found(self):
        self.assertFalse(self.d.word_chain(
            'hhhhhhhhhhhhhhhh', 'hhhhhhhhhhhhhhxx'))


if __name__ == '__main__':
    unittest.main()
