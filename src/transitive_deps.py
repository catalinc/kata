import unittest
import collections


class Dependencies(object):

    def __init__(self):
        self.graph = collections.defaultdict(set)

    def add_direct(self, clazz, others):
        for c in others:
            self.graph[clazz].add(c)

    def dependencies_for(self, clazz):
        visited = set()
        to_visit = set(self.graph[clazz])
        while to_visit:
            dep = to_visit.pop()
            if not dep in visited:
                visited.add(dep)
                for c in self.graph[dep]:
                    if not (c in visited or c == clazz):
                        to_visit.add(c)
        deps = list(visited)
        deps.sort()
        return deps


class Test(unittest.TestCase):

    def test_basic(self):
        dep = Dependencies()
        dep.add_direct('A', ['B', 'C'])
        dep.add_direct('B', ['C', 'E'])
        dep.add_direct('C', ['G'])
        dep.add_direct('D', ['A', 'F'])
        dep.add_direct('E', ['F'])
        dep.add_direct('F', ['H'])

        self.assertEqual(['B', 'C', 'E', 'F', 'G', 'H'],
                         dep.dependencies_for('A'))
        self.assertEqual(['C', 'E', 'F', 'G', 'H'],
                         dep.dependencies_for('B'))
        self.assertEqual(['G'], dep.dependencies_for('C'))
        self.assertEqual(['A', 'B', 'C', 'E', 'F', 'G', 'H'],
                         dep.dependencies_for('D'))
        self.assertEqual(['F', 'H'],
                         dep.dependencies_for('E'))
        self.assertEqual(['H'],
                         dep.dependencies_for('F'))

    def test_circular(self):
        dep = Dependencies()
        dep.add_direct('A', 'B')
        dep.add_direct('B', 'C')
        dep.add_direct('C', 'A')

        self.assertEqual(['B', 'C'], dep.dependencies_for('A'))
        self.assertEqual(['A', 'C'], dep.dependencies_for('B'))
        self.assertEqual(['A', 'B'], dep.dependencies_for('C'))

if __name__ == '__main__':
    unittest.main()
