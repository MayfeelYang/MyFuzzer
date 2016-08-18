'''
This file containts all kinds of mutators.

@author: Meifang Yang
@position: MyFuzzer/Mutators/mutators.py
@created: 2016-08-18 09:28
@version: 1(2016-08-18 09:28)
'''

import sys, os, time, array, random
from mutator import *
ARITH_MAX = 35

class ArithmeticMutator(Mutator):
    '''
    Sequential or random flip some bits or bytes.
    '''

    def __init__(self, debug = False):
        '''
        @debug: True/False, print debug information or not
        '''
        self.name = "ArithmeticMutator"
        self.debug = debug
        self.arithmetic_array = [1, 2, 4]
        if self.debug == True:
            print '=== Initializing ArithmeticMutator ==='


    def mutate(self, raw_data, pos, arith_value = 1, arith_steps = 1, BigEndian = False):
        '''
        @raw_data: the data which need to be mutated.
        @pos: mutation starts at this pos(byte)
        @arith_value: the operator is used for inc/dec 
        @arith_steps: 1byte(8-bits)/2bytes(16-bits)/4bytes(32-bits)
        @BigEndian: only arith_steps = 2 or 4, this parameter is availiable, True - BigEndian mode, False - LittleEndian mode
        '''
        if len(raw_data) - pos <= 0 :
            raise MutatorError("ArithmeticMutator ERROR: Wrong pos!")
            return None
        if len(raw_data) - pos < arith_steps:
            raise MutatorError("ArithmeticMutator ERROR: Wrong arith_steps!")
            return None
        mutated_data = self._arithmetic_inc_dec(raw_data, pos, arith_value, arith_steps, BigEndian)
        if self.debug == True:
            print "arith_steps : %s" % arith_steps
            print "mutated_data : %s" % mutated_data
        return mutated_data
        

    def _arithmetic_inc_dec(self, buf_str, pos, arith_value, arith_steps = 1, BigEndian = False):
        '''
        a helper function of mutate
        @buf_str: a part of raw_data in String Format
        @pos: mutation starts at the pos(byte)
        @arith_value: the operator is used for inc/dec
        @arith_steps: 1byte(8-bits)/2bytes(16-bits)/4bytes(32-bits)
        '''
        changed = None
        try:
            buf_str_first = buf_str[0 : pos]
            buf_str_last = buf_str[pos : ]
            print "buf_str_last : %s" % buf_str_last
            if arith_steps == 1:
                buf_last = array.array('b', buf_str_last)
                buf_last[0] += arith_value
                changed = buf_last.tostring()
                print buf_last
                print changed
            elif arith_steps == 2:
                buf_str_last_1 = buf_str_last[0 : 2]
                buf_str_last_2 = buf_str_last[2 : ]
                if BigEndian == True:
                    tmp = array.array('h', buf_str_last_1[ : : -1])
                    try:
                        tmp[0] += arith_value
                        changed = tmp.tostring()[ : : -1] + buf_str_last_2
                    except Exception, e:
                        print "ArithmeticMutator Error : arith_value is too big!"
                        return None
                else:
                    buf_last = array.array('h', buf_str_last_1)
                    print buf_last
                    buf_last[0] += arith_value
                    changed = buf_last.tostring() + buf_str_last_2
                    print changed

            else:
                buf_str_last_1 = buf_str_last[0 : 4]
                buf_str_last_2 = buf_str_last[4 : ]
                if BigEndian == True:
                    tmp = array.array('i', buf_str_last_1[ : : -1])
                    try:
                        tmp[0] += arith_value
                        changed = tmp.tostring()[ : : -1] + buf_str_last_2
                    except Exception, e:
                        print "ArithmeticMutator Error : arith_value is too big!"
                        return None
                else:
                    buf_last = array.array('i', buf_str_last_1)
                    print buf_last
                    buf_last[0] += arith_value
                    changed = buf_last.tostring() + buf_str_last_2
                    print changed
            return buf_str_first + changed
        except Exception,e:
            print "ArithmeticMutator Error: _arithmetic_inc_dec , " , e


if __name__ == "__main__":
    print "======================"
    am = ArithmeticMutator(debug = True)
    am.mutate("12341234", 0, arith_value = 30, arith_steps = 1, BigEndian = False)
    print "======================"
    am = ArithmeticMutator(debug = True)
    am.mutate("12341234", 0, arith_value = 30, arith_steps = 2, BigEndian = False)
    print "======================"
    am = ArithmeticMutator(debug = True)
    am.mutate("12341234", 0, arith_value = 30, arith_steps = 4, BigEndian = False)
    print "======================"
    am = ArithmeticMutator(debug = True)
    am.mutate("12341234", 0, arith_value = 30, arith_steps = 2, BigEndian = True)
    print "======================"
    am = ArithmeticMutator(debug = True)
    am.mutate("12341234", 3, arith_value = 30, arith_steps = 1, BigEndian = False)
    print "======================"
    am = ArithmeticMutator(debug = True)
    am.mutate("12341234", 4, arith_value = 30, arith_steps = 4, BigEndian = False)

