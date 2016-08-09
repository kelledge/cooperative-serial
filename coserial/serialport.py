from twisted.internet import abstract, fdesc

import serial
from collections import namedtuple
from serial import PARITY_NONE, PARITY_EVEN, PARITY_ODD
from serial import STOPBITS_ONE, STOPBITS_TWO
from serial import FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS

class SerialPortParameters(namedtuple('SerialPortParameters', ['baudrate',
                                                               'bytesize',
                                                               'parity',
                                                               'stopbits',
                                                               'xonxoff',
                                                               'rtscts'])):
    """
    Namedtuple for storing serial port parameters
    """

class SerialPort(abstract.FileDescriptor):
    """
    A select()able serial device, acting as a transport.
    """

    connected = 1

    def __init__(self, protocol, deviceNameOrPortNumber, reactor,
                 default_parameters):
        abstract.FileDescriptor.__init__(self, reactor)
        self._serial = serial.Serial(
            deviceNameOrPortNumber, baudrate=baudrate, bytesize=bytesize,
            parity=parity, stopbits=stopbits, timeout=timeout,
            xonxoff=xonxoff, rtscts=rtscts)
        self.reactor = reactor
        self.flushInput()
        self.flushOutput()
        self.protocol = protocol
        self.protocol.makeConnection(self)
        self.startReading()

    def fileno(self):
        return self._serial.fd

    def writeSomeData(self, data):
        """
        Write some data to the serial device.
        """
        return fdesc.writeToFD(self.fileno(), data)

    def doRead(self):
        """
        Some data's readable from serial device.
        """
        return fdesc.readFromFD(self.fileno(), self.protocol.dataReceived)

    def connectionLost(self, reason):
        """
        Called when the serial port disconnects.

        Will call C{connectionLost} on the protocol that is handling the
        serial data.
        """
        abstract.FileDescriptor.connectionLost(self, reason)
        self._serial.close()
        self.protocol.connectionLost(reason)

    def flushInput(self):
        self._serial.flushInput()

    def flushOutput(self):
        self._serial.flushOutput()

    def applySerialPortParameters(parameters):
        """
        Apply a given SerialPortParameters object for SerialPort
        """
        self._serial.setBaudrate(parameters.baudrate)
        self._serial.setByteSize(parameters.bytesize)
        self._serial.setParity(parameters.parity)
        self._serial.setStopbits(parameters.stopbits)
        self._serial.setXonXoff(parameters.xonxoff)
        self._serial.setRtsCts(parameters.rtscts)
