import os
import subprocess
import unittest


class TestPyflakesClean(unittest.TestCase):
    """ ensure that the tree is pyflakes clean """

    def test_pyflakes_clean(self):
        paths = [
            os.path.join(os.path.dirname(__file__), ".."),
            os.path.join(os.path.dirname(__file__), "..", "gdebi"),
            os.path.join(os.path.dirname(__file__), "..", "gdebi-gtk"),
            os.path.join(os.path.dirname(__file__), "..", "gdebi-kde"),
            ]                                    
        self.assertEqual(subprocess.call(["pyflakes",] +  paths), 0)
        self.assertEqual(subprocess.call(["pyflakes3",] +  paths), 0)


if __name__ == "__main__":
    unittest.main()
