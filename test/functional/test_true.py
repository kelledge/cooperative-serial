"""
A simple test suite to ensure that nose is configured properly
"""
from test.utilities import SocatLoopback

from twisted.trial import unittest
from twisted.internet import defer

class TestTrue(unittest.TestCase):

    @defer.inlineCallbacks
    def setUp(self):
        self.loopback = SocatLoopback()
        yield self.loopback.start()

    @defer.inlineCallbacks
    def tearDown(self):
        yield self.loopback.stop()

    def test_assert_true(self):
        """
        Make sure nose is setup to run this.
        """
        self.assertTrue(False)
