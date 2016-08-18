'''
This file containts all kinds of mutators.

@author: Meifang Yang
@position: MyFuzzer/Mutators/mutators.py
@created: 2016-08-17 09:28
@version: 1(2016-08-17 09:28)
'''

import sys, os, time, array, random
from mutator import *

class FlipMutator(Mutator):
    '''
    Sequential or random flip some bits or bytes.
    '''

    def __init__(self, debug = False):
        '''
        @debug: False/True, print debug information or not
        '''
        self.name = "FlipMutator"
        self.debug = debug
        self.flip_array = [1, 2, 4, 8, 16, 32]
        if self.debug == True:
            print '=== Initializing FlipMutator ==='


    def mutate(self, raw_data, mode = 'random', flip_count = 1, pos = 0, percent = 0.2):
        '''
        @raw_data: the data which need to be mutated.
        @mode: sequential/random.
        @flip_count: only in the sequential mode can be set to a certain number in [1, 2, 4, 8, 16, 32]
        @pos:only in th sequential mode can be set
        @percent: only in the random mode can be set to a certain number in range(0, 1), e.g. percent = 0.5.
        '''
        self.mode = mode
        mutated_data = ''
        if mode == 'sequential':
            if flip_count not in self.flip_array:
                raise MutatorError(self.name + ": flip_count error!")
            if pos < len(raw_data) * 8 and (len(raw_data) * 8 - pos) <= flip_count:
                raise MutatorError(self.name + ": pos error!")
            #sequential mutation
            mutated_data = raw_data
            if flip_count<8:
                for i in range(0,flip_count):
                    mutated_data = self._bit_flip(array.array('B', mutated_data), pos)
                    pos += 1
            else:
                for i in range(0,flip_count >> 3):
                    if(pos >= len(raw_data) * 8):
                        break
                    mutated_data = self._byte_flip(array.array('B', mutated_data), pos >> 3)
                    pos += 8
            if self.debug == True:
                print "====================="
                print "mode : %s" % self.mode
                print "mutated_data : %s" % mutated_data
            return mutated_data

        elif mode == 'random':
            if percent > 1 or percent <= 0:
                raise MutatorError(self.name + ": percent error!")
            #random mutation
            total_bits = len(raw_data) * 8
            change_num = int(total_bits * percent)
            mutated_data = raw_data
            for i in range(0, change_num):
                pos = random.Random().randint(0, total_bits - 1)
                #print pos
                mutated_data = self._bit_flip(array.array('B', mutated_data), 0)       
            if self.debug == True:
                print "====================="
                print "mode : %s" % self.mode
                print "mutated_data : %s" % mutated_data
            return mutated_data
                    
        else:
            raise MutatorError(self.name + " Error: Wrong Mode!")
            return None


    def _FLIP_BIT(self, _ar, _b):
        '''
        the helper function of bit_flip.
        @_ar: the array of the testcase
        @_b: the bit position in the testcase.
        '''
        _ar[_b >> 3] ^= 128 >> (_b & 7)
        return _ar


    def _bit_flip(self, buf, pos):
        '''
        _bit-flip like the bit-flip in AFL.
        @buf: the array of the testcase
        @pos: the bit position in the testcase.
        '''
        arr = self._FLIP_BIT(buf, pos)
        #print arr
        return arr.tostring()


    def _byte_flip(self, buf, pos):
        '''
        _byte-flip like the byte-flip in AFL.
        @buf:the array of the testcase
        @pos:the byte position in the testcase.

        '''
        buf[pos] ^= 0xFF
        #print buf
        return buf.tostring()

       


if __name__ == "__main__":
    f = open("test.sample", "rb")
    data = f.read()
    fm = FlipMutator(debug = True)
    fm.mutate(raw_data = data, mode = "sequential", flip_count = 1)
    fm = FlipMutator(debug = True)
    fm.mutate(raw_data = data, mode = "sequential", flip_count = 1, pos = 13)
    fm = FlipMutator(debug = True)
    fm.mutate(raw_data = data, mode = "sequential", flip_count = 2)
    fm = FlipMutator(debug = True)
    fm.mutate(raw_data = data, mode = "sequential", flip_count = 4)
    fm = FlipMutator(debug = True)
    fm.mutate(raw_data = data, mode = "sequential", flip_count = 8)
    fm = FlipMutator(debug = True)
    fm.mutate(raw_data = data, mode = "sequential", flip_count = 16)
    fm = FlipMutator(debug = True)
    fm.mutate(raw_data = data, mode = "sequential", flip_count = 32)
    '''
    wrong test case
    fm = FlipMutator(debug = True)
    fm.mutate(raw_data = data, mode = "sequential", flip_count = 64)
    '''
    fm = FlipMutator(debug = True)
    fm.mutate(raw_data = data, mode = "random", percent = 0.1)
