import unittest

# Solution to http://codekata.com/kata/kata13-counting-code-lines/


def count_code_lines(filename):
    with open(filename) as source_file:
        code = source_file.read()
        code = strip_comments(code)
        count = 0
        for line in code.split('\n'):
            line = line.strip()
            if line:
                count += 1
        return count


def strip_comments(code):
    start = code.find('/*')
    while start >= 0:
        end = code.find('*/', start)
        if end < 0:
            break
        code = code[0:start] + code[end + 2:]
        start = code.find('/*')
    start = code.find('//')
    while start >= 0:
        end = code.find('\n', start)
        if end < 0:
            break
        code = code[0:start] + code[end:]
        start = code.find('//')
    return code


class Test(unittest.TestCase):

    def test_count_code_lines_dave_java(self):
        self.assertEqual(3, count_code_lines('Dave.java'))

    def test_count_code_lines_hello_java(self):
        self.assertEqual(5, count_code_lines('Hello.java'))

if __name__ == '__main__':
    unittest.main()
