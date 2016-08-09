"""

"""
import os
import string
import random

from twisted.internet import (
    reactor,
    defer,
    threads,
    protocol
)


__all__ = ["SocatLoopback"]


def temp_path(length):
    '''
    Get a random tmp path.
    '''
    chars = string.ascii_uppercase + string.digits
    rand_chars = lambda: random.SystemRandom().choice(chars)
    return '/tmp/' + ''.join(rand_chars() for _ in range(length))


class SocatLoopback(protocol.ProcessProtocol):

    '''
    Twisted wrapper for the unix socat utility.
    '''

    bin_path = "/usr/bin/socat"

    def __init__(self):
        self.stop_deferred = None
        self.start_deferred = None
        self.left_path = temp_path(6)
        self.right_path = temp_path(6)

    def outReceived(self, data):
        pass

    def errReceived(self, data):
        pass

    def connectionMade(self):
        if self.start_deferred is not None:
            # Not sure why this delay is needed. Without it, the reactor stops
            # unexpected
            reactor.callLater(0.01, self.start_deferred.callback, None)

    def processEnded(self, reason):
        if self.stop_deferred is not None:
            self.stop_deferred.callback(reason.value.exitCode)

    def start(self):
        '''
        Spawn socat process.
        '''
        self.start_deferred = defer.Deferred()
        reactor.spawnProcess(self,
                             self.bin_path,
                             [self.bin_path,
                              "pty,raw,echo=0,link={}".format(self.left_path),
                              "pty,raw,echo=0,link={}".format(self.right_path)],
                             env=os.environ,
                             path="/")
        return self.start_deferred

    def stop(self):
        '''
        Send SIG_TERM to the socat process.
        '''
        self.stop_deferred = defer.Deferred()
        self.transport.signalProcess('TERM')
        return self.stop_deferred

    def getLoopbackPair(self):
        '''
        Returns the paths for the socat endpoints.
        '''
        return (self.left_path, self.right_path)
