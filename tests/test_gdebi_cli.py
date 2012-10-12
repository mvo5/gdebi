#!/usr/bin/python

import unittest

from mock import Mock

from GDebi.GDebiCli import GDebiCli


class GDebiCliTestCase(unittest.TestCase):

    def test_simple(self):
        mock_options = Mock()
        mock_options.rootdir = None
        mock_options.apt_opts = []
        app = GDebiCli(options=mock_options)


if __name__ == "__main__":
    unittest.main()
