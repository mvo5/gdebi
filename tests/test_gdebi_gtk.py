#!/usr/bin/python

import os
import unittest

from GDebi.GDebiGtk import GDebiGtk

class GDebiGtkTestCase(unittest.TestCase):

    def test_simple(self):
        datadir = os.path.join(os.path.dirname(__file__), "..", "data")
        app = GDebiGtk(datadir=datadir, options=None)


if __name__ == "__main__":
    unittest.main()
