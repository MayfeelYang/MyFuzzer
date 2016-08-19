'''
This file containts all kinds of mutators.

@author: Meifang Yang
@position: MyFuzzer/Mutators/mutators.py
@created: 2016-08-19 09:07
@version: 1(2016-08-19 09:07)
'''

import array
import random
from mutator import *
from arithmeticMutator import *
ARITH_MAX = 35

class RandomMutator(Mutator):
    '''
    Do some random mutation.
    '''

    def __init__(self, debug = False):
        '''
        @debug: True/False, print debug information or not
        '''
        self.name = "RandomMutator"
        self.debug = debug
        if self.debug == True:
            print '=== Initializing RandomMutator ==='

    def mutate(self, raw_data, mode, steps = 1, special_data = ""):
        if self.debug == True:
            print "================"
        '''
        @raw_data: the data which need to be mutated.
        @mode: different kinds of mutation
        @steps: 1byte(8-bits)/2bytes(16-bits)/4bytes(32-bits)
        @special_data: interesting_val or extra_data
        '''
        if mode == 1:
            '''
            flip a single bit somewhere.
            parameters: raw_data, mode
            '''
            pos = random.Random().randint(0, len(raw_data) * 8 - 1)
            buf = array.array('B', raw_data)
            buf[pos >> 3] ^= 128 >> (pos & 7)
            mutated_data = buf.tostring()
            return mutated_data

        elif mode == 2:
            '''
            Set byte to interesting value.
            parameters: raw_data, mode, special_data(interesting_val), steps(1/2/4bytes)
            '''
            mutated_data = self._set_interesting_val(raw_data, special_data, steps)
            return mutated_data

        elif mode == 3:
            '''
            Randomly subtract/add from some bytes.
            parameters: raw_data, steps(1/2/4bytes)
            '''
            am = ArithmeticMutator()
            big_endian =  random.Random().randint(0, 1)
            value = random.Random().randint(-ARITH_MAX, ARITH_MAX)
            pos = 0
            pos = random.Random().randint(0, len(raw_data) - steps)
            mutated_data = am.mutate(raw_data = raw_data, pos = 0, arith_value = value, arith_steps = steps, BigEndian = False)
            return mutated_data

        elif mode == 4:
            '''
            Set a random byte to a random value.
            parameters: raw_data
            '''
            buf = array.array('B', raw_data)
            pos = random.Random().randint(0, len(raw_data) - 1)
            buf[pos] ^= random.Random().randint(0, 255)
            mutated_data = buf.tostring()
            return mutated_data

        elif mode == 5:
            '''
            Delete bytes.
            parameters: raw_data, steps(byte, del_len, don't delete too much)
            '''
            if steps > len(raw_data):
                if self.debug == True:
                    print "RandomMutator Error: wrong steps!"
                return None
            buf = array.array('B', raw_data)
            pos = random.Random().randint(0, len(raw_data) - steps)
            for i in range(0, steps):
                del buf[pos]
            mutated_data = buf.tostring()
            return mutated_data

        elif mode == 6:
            '''
            Clone bytes(75%) or insert a block of constant bytes(25%)
            parameters: raw_data, steps(byte, clone_len)
            '''
            if steps > len(raw_data):
                if self.debug == True:
                    print "RandomMutator Error: wrong steps!"
                return None
            buf = array.array('B', raw_data)
            pos_from = random.Random().randint(0, len(raw_data) - steps)
            pos_to = random.Random().randint(0, len(raw_data))
            buf_head = buf[0 : pos_to]
            if random.Random().randint(0, 3) != 0:       #75%
                buf_mid = buf[pos_from : pos_from + steps]
            else:                                        #25%
                buf_mid = array.array('B', chr(random.Random().randint(0, 255)) * steps)
            buf_tail = buf[pos_to : ]
            mutated_data = (buf_head + buf_mid + buf_tail).tostring()
            return mutated_data

        elif mode == 7:
            '''
            Overwrite bytes with a randomly selected chunk (75%) or fixed ytes (25%).
            parameters: raw_data, steps(byte, copy_len)
            '''
            if steps > len(raw_data):
                if self.debug == True:
                    print "RandomMutator Error: wrong steps!"
                return None
            buf = array.array('B', raw_data)
            pos_from = random.Random().randint(0, len(raw_data) - steps)
            pos_to = random.Random().randint(0, len(raw_data) - steps)
            buf_copy = buf[pos_from : pos_from + steps]
            if random.Random().randint(0, 3) != 0:       #75%
                for i in range(0, steps):
                    buf[pos_to + i] = buf_copy[i]
            else:                                        #25%
                tmp = random.Random().randint(0, 255)
                for i in range(0, steps):
                    buf[pos_to + i] = tmp
            mutated_data = buf.tostring()
            return mutated_data

        elif mode == 8:
            '''
            Repeat some bytes of raw_data.
            parameters: raw_data, steps(byte, repeat_len)
            '''
            if steps > len(raw_data):
                if self.debug == True:
                    print "RandomMutator Error: wrong steps!"
                return None
            #repeat_time_list = [1, 2, 4, 8, 16, 32, 64, 128, 512, 1024, 2048, 4096, 32767, 0xFFFF]
            repeat_time_list = [1, 2, 4, 8]
            buf = array.array('B', raw_data)
            pos = random.Random().randint(0, len(raw_data) - steps)
            buf_repeat = buf[pos : pos + steps]
            repeat_time = repeat_time_list[random.Random().randint(0, len(repeat_time_list) - 1)]
            mutated_data = (buf[0 : pos] + buf_repeat * repeat_time + buf[pos + steps : ]).tostring()
            return mutated_data

        elif mode == 9:
            '''
            Overwrite bytes with an extra.
            parameters: raw_data, special_data(extra_data)
            '''
            if len(special_data) > len(raw_data):
                if self.debug == True:
                    print "RandomMutator Error: wrong special_data!"
                return None
            buf = array.array('B', raw_data)
            extra_array = array.array('B', special_data)
            pos = random.Random().randint(0, len(raw_data) - len(special_data))
            for i in range(0, len(special_data)):
                buf[pos + i] = extra_array[i]
            mutated_data = buf.tostring()
            return mutated_data

        elif mode == 10:
            '''
            Insert an extra
            parameters: raw_data, special_data(extra_data)
            '''
            buf = raw_data
            pos = random.Random().randint(0, len(raw_data))
            mutated_data = buf[0 : pos] + special_data + buf[pos : ]
            return mutated_data


    def _set_interesting_val(self, raw_data, interesting_val, steps):
        try:
            if steps not in [1, 2, 4]:
                return None
            buf = array.array('B', raw_data)
            mutated_data = None
            pos = random.Random().randint(0, len(raw_data) - steps)
            big_endian = random.Random().randint(0, 1)
            if steps == len(interesting_val):
                interesting_array = array.array('B', interesting_val)
                if big_endian == 0:
                    for i in range(0, steps):
                        buf[pos + i] = interesting_array[i]
                else:
                    for i in range(0, steps):
                        buf[pos + i] = interesting_array[steps - 1 - i]

                mutated_data = buf.tostring()
                return mutated_data
            else:
                if self.debug == True:
                    print "RandomMutator Error: wrong special_data!"
                return None
        except  Exception, e:
            print "RandomMutator Error: _set_interesting_val function , " , e


if __name__ == "__main__":
    rm = RandomMutator(True)
    print rm.mutate(raw_data = "12341234", mode = 1)

    print rm.mutate(raw_data = "12341234", mode = 2, steps = 1, special_data = '*')
    print rm.mutate(raw_data = "12341234", mode = 2, steps = 2, special_data = '%$')
    print rm.mutate(raw_data = "12341234", mode = 2, steps = 4, special_data = '%$#@')

    print rm.mutate(raw_data = "12341234", mode = 3, steps = 1)
    print rm.mutate(raw_data = "12341234", mode = 3, steps = 2)
    print rm.mutate(raw_data = "12341234", mode = 3, steps = 4)

    print rm.mutate(raw_data = "12341234", mode = 4)

    print rm.mutate(raw_data = "12341234", mode = 5, steps = 3)

    print rm.mutate(raw_data = "12341234", mode = 6, steps = 2)

    print rm.mutate(raw_data = "12341234", mode = 7, steps = 4)

    print rm.mutate(raw_data = "12341234", mode = 8, steps = 5)

    print rm.mutate(raw_data = "12341234", mode = 9, special_data = '%$')

    print rm.mutate(raw_data = "12341234", mode = 10, special_data = '***%$')







