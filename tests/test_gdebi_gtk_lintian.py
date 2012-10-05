#!/usr/bin/python

import os
import time
import unittest

from gi.repository import GObject
from mock import patch

from GDebi.GDebi import GDebi
from GDebi.GDebiCommon import GDebiCommon

EXPECTED_LINTIAN_OUTPUT = """Lintian exited with status: 1
N: Using profile ubuntu/main.
N: Setting up lab in /tmp/temp-lintian-lab-rRN1v73UQF ...
N: ----
N: Processing binary package error-package (version 1.0, arch all) ...
E: error-package: file-in-etc-not-marked-as-conffile etc/foo
E: error-package: control-file-has-bad-owner postinst egon/egon != root/root
E: error-package: no-copyright-file
E: error-package: package-has-no-description
E: error-package: no-maintainer-field
W: error-package: no-section-field
W: error-package: no-priority-field
E: error-package: wrong-file-owner-uid-or-gid etc/ 1000/1000
E: error-package: wrong-file-owner-uid-or-gid etc/foo 1000/1000
W: error-package: maintainer-script-ignores-errors postinst
"""


def do_events():
    context = GObject.main_context_default()
    while context.pending():
        context.iteration()


class GDebiGtkTestCase(unittest.TestCase):

    def setUp(self):
        self.testsdir = os.path.dirname(__file__)
        self.datadir = os.path.join(self.testsdir, "..", "data")
        self.options = None
        

    @patch.object(GDebiCommon, "openCache")
    def test_lintian(self, mock_open_cache):
        gdebi = GDebi(self.datadir, self.options)
        gdebi._run_lintian(
            os.path.join(self.testsdir, "error-package_1.0_all.deb"))
        # wait for the output
        buf = gdebi.textview_lintian_output.get_buffer()
        for i in range(10):
            time.sleep(0.2)
            do_events()
            start = buf.get_start_iter()
            end = buf.get_end_iter()
            if buf.get_text(start, end, False) != "Running lintian...":
                break
        # each change to the buffer makes the iters invalid
        start = buf.get_start_iter()
        end = buf.get_end_iter()
        buf = gdebi.textview_lintian_output.get_buffer()
        lintian_output = buf.get_text(start, end, False)
        self.assertEqual(lintian_output.strip(), EXPECTED_LINTIAN_OUTPUT)


if __name__ == "__main__":
    unittest.main()
