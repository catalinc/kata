import unittest
import re
import collections
import random
import sys

# Solution to http://codekata.com/kata/kata14-tom-swift-under-the-milkwood/


class Trigrams(object):

    def __init__(self):
        self.trigrams = collections.defaultdict(list)

    def add_from_file(self, filename):
        with open(filename) as infile:
            buffer = []
            word_regex = re.compile('[a-z\'.]+', re.IGNORECASE)
            for line in infile:
                for word in word_regex.findall(line):
                    buffer.append(word)
                    if len(buffer) == 3:
                        first, second, third = buffer
                        self.trigrams[first + ' ' + second].append(third)
                        buffer.pop(0)

    def generate(self, count):
        words = random.sample(self.trigrams.keys(), 1)[0].split(' ')
        while len(words) < count:
            k = words[-2] + ' ' + words[-1]
            v = self.trigrams.get(k)
            if not v:
                break
            w = random.sample(v, 1)[0]
            words.append(w)
        return ' '.join(words)


class Test(unittest.TestCase):

    def test_generate_from_file(self):
        t = Trigrams()
        t.add_from_file('Hello.java')
        text = t.generate(1000)
        self.assertTrue(text.split(' ') >= 3)


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        filename = sys.argv[1]
        count = int(sys.argv[2])
        t = Trigrams()
        t.add_from_file(filename)
        text = t.generate(count)
        print(text)
    else:
        print('usage: %s <filename> <word_count>' % sys.argv[0])
