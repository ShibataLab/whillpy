#!/usr/bin/env python
# -*- coding: utf-8 -*-

# whill.py: whill controller class
# Author: Ravi Joshi
# Date: 2018/10/01

# import modules
import serial
import time
from options import Power, CommandId


class Whill:
    def __init__(self, port):
        ''' Whill control class
            input: serial port name
        '''
        self.connection = None
        try:
            self.connection = serial.Serial(port=port, baudrate=38400)
        except serial.SerialException as e:
            print '[ERROR] %s' % e
        self.previous_time = None
        self.successive_power_wait = 5.0  # sec. wait in order to execute next command

    def set_power(self, power):
        ''' turn on or off the power of WHILL
            input: power option
            returns: number of bytes written to the interface
        '''
        if not Power.has_value(power):
            # print out the valid values
            power_options = ['Power.%s' % option[0] for option in Power]
            power_options = ', '.join(power_options)
            print '[ERROR] invalid input. valid values are %s' % power_options
            return -1

        # wait for sometime if we have already sent power command previously
        current_time = time.time()
        entry_condition = self.previous_time is None or (
            current_time - self.previous_time) > self.successive_power_wait

        if entry_condition is False:
            print '[ERROR] wait for %d seconds to execute command' % self.successive_power_wait
            return -1

        self.previous_time = current_time
        set_power_command = [CommandId.SetPower, power]
        return self._send_command(set_power_command)

    def _get_checksum(self, command):
        ''' checksum is the value of XOR of following values:
                protocol sign
                data lenght
                control command
            returns the checksum and data length
        '''
        # data length incluse 1 byte for checksum. hence we need to add 1
        data_len = len(command) + 1
        checksum = 0
        for value in command:
            checksum ^= value  # XOR
        checksum ^= CommandId.ProtocolSign ^ data_len
        return checksum, data_len

    def _attach_metadata(self, command):
        ''' control command has following format
            Protocol sign | Data length | Control command | Checksum
              (1 byte)    |  (1 byte)   | variable length | (1 byte)
            returns the composed command
        '''
        checksum, data_len = self._get_checksum(command)
        return [CommandId.ProtocolSign, data_len] + command + [checksum]

    def _send_command(self, command):
        ''' attach metadata to the command and then
            convert the command into bytes, finally send itself.
            returns the number of bytes written to the interface
        '''
        command = self._attach_metadata(command)
        command = bytearray(command)
        return self.connection.write(command)

    def __del__(self):
        ''' cleanup the serial connection object
        '''
        if self.connection:
            self.connection.close()
