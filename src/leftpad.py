import unittest


def leftpad(s, length, ch=' '):
    if s is None:
        raise ValueError('s is None')
    if length < 0:
        raise ValueError('length is negative')
    n = length - len(s)
    i = 0
    pad = []
    while i < n:
        pad.append(ch)
        i += 1
    return s + ''.join(pad)


class LeftPadTest(unittest.TestCase):
    def test_leftpad_none(self):
        with self.assertRaises(ValueError):
            leftpad(None, 1)

    def test_leftpad_negative_length(self):
        with self.assertRaises(ValueError):
            leftpad('abc', -1)

    def test_leftpad_empty_string(self):
        self.assertEqual(' ' * 4, leftpad('', 4))

    def test_leftpad_non_empty_string(self):
        self.assertEqual('abc    ', leftpad('abc', 7))

    def test_leftpad_len_smaller_than_string_len(self):
        self.assertEqual('abcd', leftpad('abcd', 2))


if __name__ == '__main__':
    unittest.main()
