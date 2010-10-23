from Instruction import Instruction

import unittest
import Types
from Variable import Variable
from Instructions.Instruction import register
from ReferenceType import ReferenceType


class call(Instruction):

    def __init__(self, method):
        self.name = 'call'
        parts = method.split()
        if parts[0] == 'instance':
            self.instance = True
            parts.pop(0)
        else:
            self.instance = False
            
        self.method_type = Types.BuiltInTypes[parts[0]]
        self.method_namespace, self.method_name = parts[1].split('::')
        if self.method_name[0] == '.':
            self.method_name = self.method_name[1:]
        #self.method_name = method_name
        #self.method_type = method_type
        self.method_parameters = '' #method_parameters
        self.opcode = 0x28
        self.value = None

    def execute(self, vm):
        targetMethod = vm.find_method_by_signature(self.method_namespace, self.method_name, self.method_type, self.method_parameters)
        m = targetMethod.get_method()
        #fixme throw exception
        
        # push this pointer on to stack
        if self.instance:
            obj = vm.stack.pop()
            m.parameters.append(obj)
            
        vm.execute_method(m)

register('call', call)

class callTest(unittest.TestCase):

    def test_call_no_parameters_int(self):
        from VM import VM
        from MethodDefinition import MethodDefinition
        vm = VM()

        m = MethodDefinition()
        m.name = 'TestMethod()'
        m.namespace = 'A.B'
        m.returnType = Types.Int32
        m.parameters = []
        m.names = 'A.B'
        vm.methods.append(m)

        self.assertEqual(vm.currentMethod, None)

        c = call('int32 A.B::TestMethod()')
        c.execute(vm)

        self.assertEqual(vm.currentMethod.methodDefinition, m)
        self.assertEqual(vm.stack.get_number_of_frames(), 2)
        
    def test_call_constructor_strips_period(self):
        from VM import VM
        from MethodDefinition import MethodDefinition
        vm = VM()

        m = MethodDefinition()
        m.name = 'ctor()'
        m.namespace = 'A.B'
        m.returnType = Types.Int32
        m.parameters = []
        m.names = 'A.B'
        vm.methods.append(m)

        self.assertEqual(vm.currentMethod, None)

        c = call('int32 A.B::.ctor()')
        c.execute(vm)

        self.assertEqual(vm.currentMethod.methodDefinition, m)
        self.assertEqual(vm.stack.get_number_of_frames(), 2)
        
    def test_call_one_parameter_int(self):
        from VM import VM
        from MethodDefinition import MethodDefinition
        vm = VM()

        m = MethodDefinition()
        m.namespace = 'A.B'
        m.name = 'TestMethod()' # fixme - name shouldn't have brackets
        m.returnType = Types.Int32
        m.parameters = [Types.Int32]
        vm.methods.append(m)
        
        param = Variable()
        param.value = 123
        param.type = Types.Int32
        vm.stack.push(param)
        
        c = call('int32 A.B::TestMethod()')
        c.execute(vm)
        
        self.assertEqual(vm.currentMethod.methodDefinition, m)
        self.assertEqual(vm.stack.get_number_of_frames(), 2)
        self.assertEqual(vm.stack.pop(), param)
               
    def test_call_no_parameters_instance_puts_this_pointer_on_stack(self):
        from VM import VM
        from MethodDefinition import MethodDefinition
        vm = VM()

        m = MethodDefinition()
        m.name = 'TestMethod()'
        m.namespace = 'A.B'
        m.returnType = Types.Int32
        m.parameters = []
        m.names = 'A.B'
        m.attributes.append(MethodDefinition.AttributeTypes['instance'])
        vm.methods.append(m)

        r = ReferenceType()
        vm.stack.push(r)
        
        self.assertEqual(vm.currentMethod, None)

        c = call('instance int32 A.B::TestMethod()')
        c.execute(vm)

        self.assertEqual(vm.currentMethod.methodDefinition, m)
        self.assertEqual(vm.stack.get_number_of_frames(), 2)
        self.assertEqual(len(vm.current_method().parameters), 1)
        self.assertEqual(vm.current_method().parameters[0], r)