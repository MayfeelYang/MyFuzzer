#-*- coding = utf-8 -*-

'''
Mutator base classes and some interfaces.

@author: Meifang Yang
@position: MyFuzzer/Mutators/mutator.py
cd @created: 2016-08-17 09:12
@version: 1(2016-08-17 09:12)
'''

import os

class Mutator(object):
    '''
    Mutator is a base class of all kinds of mutators.
    '''

    def __init__(self):
        self.name = "Mutator"

class MutatorCompleted(Exception):
    '''
    At end of available mutations.
    '''
    pass

class MutatorError(Exception):
    '''
    Bad stuff just occured!
    '''
    def __init__(self, info):
        print info
    pass


#end
