# ldstr.py
# The CIL ldstr instruction
# Copyright 2010 Marty Dill - see LICENSE for details

from Instruction import Instruction

import unittest
from Instructions.Instruction import register


class ldstr(Instruction):

    def __init__(self, arguments):
        self.name = 'ldstr'
        self.opcode = 72
        self.value = arguments

    def execute(self, vm):
        stack = vm.stack
        stack.push(self.value)

register('ldstr', ldstr)

class ldstrTest(unittest.TestCase):
        
    def testExecute(self):
        from VM import VM
        vm = VM()
        x = ldstr('Hello world')
        x.execute(vm)

        self.assertEqual(vm.stack.count(), 1)
        self.assertEqual(vm.stack.pop(), 'Hello world')

