#!/usr/bin/env python
# -*- coding: utf-8 -*-

# options.py: options defined for whill controller class
# Author: Ravi Joshi
# Date: 2018/10/01


class Power:
    Off = 0
    On = 1

    ''' check if the input value belongs to the class
    '''
    @classmethod
    def has_value(cls, value):
        attrs = vars(cls)
        return any(item == value for item in attrs.values())

    ''' make the class iterable
        this is used only for reporting invalid input
    '''
    class __metaclass__(type):
        def __iter__(cls):
            return iter(
                filter(
                    lambda k: not k[0].startswith('__'),
                    cls.__dict__.iteritems()
                )
            )


class CommandId:
    ProtocolSign = 0xAF
    SetPower = 0x02