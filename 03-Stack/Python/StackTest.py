#
# Developed by 10Pines SRL
# License:
# This work is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View,
# California, 94041, USA.
#

import unittest


class Stack:
    STACK_EMPTY_DESCRIPTION = 'Stack is empty'
    def __init__(self):
        
        self.cantidadDeElementos = 0
        self.PilaVacia = StackVacio()
        self.PilaNoVacia = StackNoVacio()
        self.Subclases = [self.PilaVacia, self.PilaNoVacia]
    def elegirPila(self):
        for subclase in self.Subclases:
            if subclase.esUsada(self.cantidadDeElementos):
                return subclase
    def pop(self):
        pilaAusar = self.elegirPila()
        elemento = pilaAusar.pop()
        self.cantidadDeElementos = self.cantidadDeElementos-1
        return elemento
    def esUsada(self,cantidadDeElementos):
        self.shouldBeImplementedBySubclass()
    def top(self):
        pilaAusar = self.elegirPila()
        return pilaAusar.top()
        self.shouldBeImplementedBySubclass()
    def push(self,elemento):
        self.cantidadDeElementos = self.cantidadDeElementos +1
        return self.PilaNoVacia.push(elemento)
    def isEmpty(self):
        return self.cantidadDeElementos == 0

    def size(self):
        return self.cantidadDeElementos
    def shouldBeImplementedBySubclass(self):
        raise NotImplementedError('Should be implemented by the subclass')

class StackVacio(Stack):
    def __init__(self):
        pass
    def esUsada(self,cantidadDeElementos):
        return cantidadDeElementos == 0
    def pop(self):
        raise Mi_Error()
    def top(self):
        raise Mi_Error()

class StackNoVacio(Stack):
    def __init__(self):
        self.stack = []
    def esUsada(self,cantidadDeElementos):
        return cantidadDeElementos != 0
    def push(self, anObject):
        self.stack.append(anObject)

    def pop(self):
        return self.stack.pop()

    def top(self):
        return self.stack[len(self.stack)-1]

    def isEmpty(self):
        return self.elementos == []

    def size(self):
        return len(self.elementos)

class Mi_Error(Exception, Stack):
    
    def __init__(self):
        un_stack = Stack()
        self.message = un_stack.STACK_EMPTY_DESCRIPTION

class StackTest(unittest.TestCase):

    def testStackShouldBeEmptyWhenCreated(self):
        stack = Stack()

        self.assertTrue(stack.isEmpty())

    def testPushAddElementsToTheStack(self):
        stack = Stack()
        stack.push('something')

        self.assertFalse(stack.isEmpty())

    def testPopRemovesElementsFromTheStack(self):
        stack = Stack()
        stack.push("Something")
        stack.pop()

        self.assertTrue(stack.isEmpty())

    def testPopReturnsLastPushedObject(self):
        stack = Stack()
        pushedObject = "Something"
        stack.push(pushedObject)
        self.assertEquals(pushedObject, stack.pop())

    def testStackBehavesLIFO(self):
        firstPushed = "First"
        secondPushed = "Second"
        stack = Stack()
        stack.push(firstPushed)
        stack.push(secondPushed)

        self.assertEquals(secondPushed,stack.pop())
        self.assertEquals(firstPushed,stack.pop())
        self.assertTrue(stack.isEmpty())

    def testTopReturnsLastPushedObject(self):
        stack = Stack()
        pushedObject = "Something"

        stack.push(pushedObject)

        self.assertEquals(pushedObject, stack.top())

    def testTopDoesNotRemoveObjectFromStack(self):
        stack = Stack()
        pushedObject = "Something"

        stack.push(pushedObject)

        self.assertEquals( 1,stack.size())
        stack.top()
        self.assertEquals( 1,stack.size())

    def testCanNotPopWhenThereAreNoObjectsInTheStack(self):
        stack = Stack()

        try:
            stack.pop()
            self.fail()
        except Exception as stackIsEmpty:
            self.assertEquals(Stack.STACK_EMPTY_DESCRIPTION,stackIsEmpty.message)

    def testCanNotTopWhenThereAreNoObjectsInTheStack(self):
        stack = Stack()

        try:
            stack.top()
            self.fail()
        except Exception as stackIsEmpty:
            self.assertEquals(Stack.STACK_EMPTY_DESCRIPTION,stackIsEmpty.message)

if __name__ == "__main__":
    unittest.main()



