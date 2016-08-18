'''
This file containts all kinds of mutators.

@author: Meifang Yang
@position: MyFuzzer/Mutators/mutators.py
@created: 2016-08-18 20:27
@version: 1(2016-08-18 20:27)
'''

import sys, os, time, array, random
from mutator import *

class SplicingMutator(Mutator):
    '''
    used to splic data.
    '''
    def __init__(self, debug = False):
        '''
        @debug: False/True, print debug information or not
        '''
        self.name = "SplicingMutator"
        self.debug = debug
        if self.debug == True:
            print '=== Initializing SplicingMutator ==='

    def mutate(self, raw_data, splicing_data):
        '''
        @raw_data: the raw data which need to be mutated.
        @splicing_data: the data will be spliced to raw data.
        '''
        try:            
            f_diff,l_diff = self._locate_diffs(raw_data, splicing_data)
            if f_diff < 0 or l_diff < 2 or l_diff == f_diff:
                print "SplicingMutator Error : f_diff < 0 or l_diff < 2 or l_diff == f_diff"
                return None
            split_at = random.randint(f_diff, l_diff)
            if self.debug == True:
                print 'split_at : %d' % (split_at)
            mutated_data = raw_data[0:split_at] + splicing_data[split_at:]
            if self.debug == True:
                print "mutated_data : %s" % mutated_data
            return mutated_data

        except Exception,e:
            print "SplicingMutator Error: error in _get_mutation_afl_splicing function , " , e
            return None


    def _locate_diffs(self, str1, str2):
        '''
        Helper function for self.mutate.
        '''
        minlen=min(len(str1),len(str2))
        f_loc=-1
        l_loc=-1
        for i in range(0,minlen):
            if str1[i]!=str2[i]:
                if f_loc == -1:
                    f_loc=i
                l_loc = i
        return f_loc, l_loc



if __name__ == "__main__":
    sm = SplicingMutator(debug = True)
    sm.mutate("1234", "134567")
    

