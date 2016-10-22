import unittest
import re


# Code kata from http://osherove.com/tdd-kata-1/

def add(numbers):
    if not numbers:
        return 0
    sep = ',|\n'
    if numbers.startswith('//'):
        nl_pos = numbers.index('\n')
        sep = [_escape(s) for s in re.split('[\[\]]', numbers[2:nl_pos]) if s]
        sep = '|'.join(sep)
        numbers = numbers[nl_pos + 1:]
    r = 0
    matches = re.split(sep, numbers)
    for m in matches:
        n = int(m)
        if n <= 1000:
            r += int(m)
    return r


def _escape(s):
    for c in '*^$+':
        s = s.replace(c, '\\' + c)
    return s


class Test(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(0, add(""))

    def test_comma_delimiter(self):
        self.assertEqual(6, add("1,2,3"))

    def test_comma_and_newline_delimiters(self):
        self.assertEqual(6, add("1,2\n3"))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.assertEqual(6, add("1,2\n"))

    def test_custom_one_char_delimiter(self):
        self.assertEqual(6, add("//;\n1;2;3"))

    def test_ignore_numbers_bigger_than_1000(self):
        self.assertEqual(4, add("1,1001,3"))

    def test_delimiter_longer_than_one_char(self):
        self.assertEqual(6, add("//[***]\n1***2***3"))

    def test_two_one_char_delimiters(self):
        self.assertEqual(9, add("//[,][%]\n2,3%4"))

    def test_multiple_one_char_and_longer_than_one_char_delimiters(self):
        self.assertEqual(28, add("//[,][%][**][##][$$][++]\n1%2,3**4#5$$6++7"))


if __name__ == '__main__':
    unittest.main()
