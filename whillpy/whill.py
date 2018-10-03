#!/usr/bin/env python
# -*- coding: utf-8 -*-

# whill.py: whill controller class
# Author: Ravi Joshi
# Date: 2018/10/01

# import modules
from __future__ import print_function
import sys
import serial
import time
from .options import power, Joystick, CommandId


def log(message, level=sys.stderr):
    ''' function for backward compatibility of print statement
    '''
    print(message, file=level)


class connect:
    def __init__(self, port):
        ''' Whill control class
            input: serial port name
        '''
        self.connection = None
        try:
            # following UART configurations are taken from the communication specifications manual
            self.connection = serial.Serial(port=port, baudrate=38400, parity=None, bytesize=8, stopbits=2)
        except serial.SerialException as e:
            log('[ERROR] %s' % e)
        self.previous_time = None
        self.successive_power_wait = 5.0  # sec. wait in order to execute next command

    def set_power(self, option):
        ''' turn on or off the power of WHILL
            input: power option
            returns: number of bytes written to the interface
        '''
        if not power._has_value(option):
            # print out the valid values
            power_options = ['power.%s' % op[0]
                             for op in power if not op[0].startswith('_')]
            power_options = ', '.join(power_options)
            log('[ERROR] invalid input. valid values are %s' % power_options)
            return -1

        # wait for sometime if we have already sent power command previously
        current_time = time.time()
        entry_condition = self.previous_time is None or (
            current_time - self.previous_time) > self.successive_power_wait

        if entry_condition is False:
            log('[ERROR] wait for %d seconds to execute command' %
                self.successive_power_wait)
            return -1

        self.previous_time = current_time
        set_power_command = [CommandId.SetPower, option]
        return self._send_command(set_power_command)

    def move(self, straight, turn):
        ''' move WHILL as per given straight and turn parameters
            input: straight = Joystick value in front/back direction (-100 ~ +100)
                   turn = Joystick value in left/right direction (-100 ~ +100)
            returns: number of bytes written to the interface
        '''
        if not Joystick.Min <= straight <= Joystick.Max:
            log('[ERROR] invalid straight input. valid values are (%d ~ %d)' % (
                Joystick.Min, Joystick.Max))
            return -1

        if not Joystick.Min <= turn <= Joystick.Max:
            log('[ERROR] invalid turn input. valid values are (%d ~ %d)' % (
                Joystick.Min, Joystick.Max))
            return -1

        set_joystick_command = [
            CommandId.SetJoystick, Joystick.EnableHostControl, straight, turn]
        return self._send_command(set_joystick_command)

    def _get_checksum(self, command):
        ''' checksum is the value of XOR of following values:
                protocol sign
                data lenght
                control command
            returns: checksum and data length
        '''
        # data length incluse 1 byte for checksum. hence we need to add 1
        data_len = len(command) + 1
        checksum = 0
        for idx, value in enumerate(command):
            # negative values are stored as 2's compliment
            if value < 0:
                # in order to calculate 2's compliment, we need to covert
                # the number into binary, flip the bits and then add 1 into it
                # alternativly we can simply add 2^8 to the number
                # (remeber that we are dealing with 8 bit numbers)
                command[idx] = 2**8 + value
            checksum ^= command[idx]  # XOR
        checksum ^= CommandId.ProtocolSign ^ data_len
        return checksum, data_len

    def _attach_metadata(self, command):
        ''' control command has following format
            Protocol sign | Data length | Control command | Checksum
              (1 byte)    |  (1 byte)   | variable length | (1 byte)
            returns: composed command
        '''
        checksum, data_len = self._get_checksum(command)
        return [CommandId.ProtocolSign, data_len] + command + [checksum]

    def _send_command(self, command):
        ''' attach metadata to the command and then
            convert the command into bytes, finally send itself.
            returns: number of bytes written to the interface
        '''
        command = self._attach_metadata(command)
        command = bytearray(command)
        return self.connection.write(command)

    def __del__(self):
        ''' cleanup the serial connection object
        '''
        if self.connection:
            self.connection.close()
