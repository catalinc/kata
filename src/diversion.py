import unittest

# Solution to http://codekata.com/kata/kata15-a-diversion/


def count_non_adjacent_ones(n):
    c = 0
    for i in range(2**n):
        if not has_adjacent_ones(i):
            c += 1
    return c


def has_adjacent_ones(n):
    p = 0
    while n:
        b = n & 1
        if p == 1 and b == 1:
            return True
        p = b
        n >>= 1
    return False


def count_non_adjacent_ones_with_fib(n):
    return nth_fib(n + 2)


def nth_fib(n):
    if n <= 2:
        return 1
    prev, last = 1, 1
    while n > 2:
        prev, last = last, last + prev
        n -= 1
    return last


class Test(unittest.TestCase):

    def test_has_adjacent_ones(self):
        for n in (3, 6, 7, 13, 14, 15):
            self.assertTrue(has_adjacent_ones(n), 'failed for %d' % n)

    def test_does_not_have_adjacent_ones(self):
        for n in (0, 2, 5, 8, 9, 10, 16):
            self.assertFalse(has_adjacent_ones(n), 'failed for %d' % n)

    def test_count_non_adjacent_ones(self):
        test_data = [(3, 5), (4, 8)]
        for n, count in test_data:
            self.assertEqual(count, count_non_adjacent_ones(n))


if __name__ == '__main__':
    unittest.main()
