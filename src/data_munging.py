import unittest
import re
import sys

# http://codekata.com/kata/kata04-data-munging/


def max_temp_spread(name):
    the_day, max_spread = None, -1
    with open(name, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            if not line or re.match('^\s*Dy', line) \
               or re.match('^\s*mo', line):
                continue
            data = re.split('\s+', line)
            day = data[0]
            max_temp = int(data[1].rstrip('*'))
            min_temp = int(data[2].rstrip('*'))
            spread = max_temp - min_temp
            if spread > max_spread:
                max_spread = spread
                the_day = day
    return the_day


def min_for_against_goals_spread(name):
    the_team, min_diff = None, sys.maxsize
    with open(name, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            if not line or re.match('^Team', line) or re.match('^-', line):
                continue
            data = re.split('\s+', line)
            team = data[1]
            for_goals = int(data[6])
            against_goals = int(data[8])
            diff = abs(for_goals - against_goals)
            if diff < min_diff:
                min_diff = diff
                the_team = team
    return the_team


def data_munging(name, entry_pos, first_pos,
                 second_pos, skip_patterns=(), cmp=lambda a, b: a > b):
    best_entry, best_value = None, None
    with open(name, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            if not line:
                continue
            should_skip = False
            for p in skip_patterns:
                if re.match(p, line):
                    should_skip = True
                    break
            if should_skip:
                continue
            data = re.split('\s+', line)
            entry = data[entry_pos]
            first = int(data[first_pos].rstrip('*'))
            second = int(data[second_pos].rstrip('*'))
            delta = abs(first - second)
            if best_value is None or cmp(delta, best_value):
                best_value = delta
                best_entry = entry
    return best_entry


class DataMungingTest(unittest.TestCase):

    def test_max_temp_spread(self):
        self.assertEqual('9', max_temp_spread('weather.dat'))

    def test_min_for_against_goals_spread(self):
        self.assertEqual(
            'Aston_Villa', min_for_against_goals_spread('football.dat'))

    def test_data_munging_max_temp_spread(self):
        self.assertEqual('9', data_munging(
            'weather.dat', 0, 1, 2, skip_patterns=('^Dy', '^mo')))

    def test_data_munging_min_for_against_goals_spread(self):
        self.assertEqual('Aston_Villa', data_munging(
            'football.dat', 1, 6, 8,
            skip_patterns=('^Team', '^--'), cmp=lambda a, b: a < b))


if __name__ == '__main__':
    unittest.main()
