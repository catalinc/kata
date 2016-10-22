import unittest
import collections

# Solution to http://codekata.com/kata/kata09-back-to-the-checkout/


class Checkout(object):

    def __init__(self, rules):
        self.rules = rules
        self.total = 0
        self.counter = collections.Counter()

    def scan(self, item):
        for r in self.rules:
            if r.match(item):
                self.counter.update(item)
                r.apply(self)
                break


class Rule(object):

    def __init__(self, item, price, special_price=()):
        self.item = item
        self.price = price
        self.special_price = special_price

    def match(self, item):
        return self.item == item

    def apply(self, checkout):
        checkout.total += self.price
        if self.special_price:
            bundle_count, bundle_price = self.special_price
            count = checkout.counter[self.item]
            if count > 0 and count % bundle_count == 0:
                checkout.total -= bundle_count * self.price
                checkout.total += bundle_price


class TestCheckout(unittest.TestCase):

    RULES = (Rule('A', 50, (3, 130)),
             Rule('B', 30, (2, 45)),
             Rule('C', 20),
             Rule('D', 15))

    def price(self, goods):
        co = Checkout(self.RULES)
        for g in goods:
            co.scan(g)
        return co.total

    def test_totals(self):
        self.assertEqual(0, self.price(""))
        self.assertEqual(50, self.price("A"))
        self.assertEqual(80, self.price("AB"))
        self.assertEqual(115, self.price("CDBA"))

        self.assertEqual(100, self.price("AA"))
        self.assertEqual(130, self.price("AAA"))
        self.assertEqual(180, self.price("AAAA"))
        self.assertEqual(230, self.price("AAAAA"))
        self.assertEqual(260, self.price("AAAAAA"))

        self.assertEqual(160, self.price("AAAB"))
        self.assertEqual(175, self.price("AAABB"))
        self.assertEqual(190, self.price("AAABBD"))
        self.assertEqual(190, self.price("DABABA"))

    def test_incremental(self):
        co = Checkout(self.RULES)
        self.assertEqual(0, co.total)
        co.scan("A")
        self.assertEqual(50, co.total)
        co.scan("B")
        self.assertEqual(80, co.total)
        co.scan("A")
        self.assertEqual(130, co.total)
        co.scan("A")
        self.assertEqual(160, co.total)
        co.scan("B")
        self.assertEqual(175, co.total)


if __name__ == '__main__':
    unittest.main()
